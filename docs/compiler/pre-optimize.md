---
title: Pre Optimize API
description: Rewrite YOLO and RTMDet post processing with dx_com.pre_optimize() so the host CPU works on TopK candidates only.
---

# Pre Optimize API

This page lets you speed up CPU post processing of YOLO and RTMDet models with `dx_com.pre_optimize()`, an ONNX level rewrite that runs before compiling.

## Before you start

* DX-COM 2.4.0 or later. The pass names and keys on this page are for DX-COM 2.5.0.
* A YOLO model exported with [Ultralytics](https://github.com/ultralytics/ultralytics), or an RTMDet model exported with [MMDetection](https://github.com/open-mmlab/mmdetection), with a static input size.
* A config file for the model. See [Config file reference](config-reference.md).

## When to use it

The detection head runs Sigmoid, Softmax, DFL decoding, dist2bbox and NMS pre filtering on the host CPU after NPU inference. Over the full anchor grid (for example 8400 candidates at 640×640) this CPU work can dominate latency and leave the NPU idle, mostly on weak CPUs such as ARM cores.

`pre_optimize()` reorders the graph:

1. TopK selection runs first and keeps `K` candidates (default 300, 512 for RTMDet).
1. The expensive operations run only on those `K` candidates.

CPU cost then grows with `K` instead of the anchor count. It replaces the deprecated [PPU type 2](ppu.md#type-2-deprecated).

!!! warning "Do not combine with ppu"
    `pre_optimize` and `ppu` cannot be used in one config. DX-COM 2.5.0 does not reject a config with both: it compiles with `ppu` and drops `pre_optimize`, or fails later with an unrelated error. The only sign is the console line `falling back to legacy: ValueError: config 'pre_optimize' and 'ppu' are mutually exclusive`.

## Passes

| Pass | Models | Tasks | Output |
|---|---|---|---|
| `yolo_dfl_postprocess` | YOLOv8, v9, v11, v12, v13 | detection, segmentation, pose | `[1, 4+C (+mask or +keypoints), K]`: boxes as `xywh` (center x, center y, width, height), then one score per class |
| `yolo_no_dfl_postprocess` | YOLO26 (NMS free) | detection, segmentation, pose | `[1, K, 6 (+mask or +keypoints)]`: boxes as `xyxy` (top left, bottom right), then one score and `class_id` |
| `rtmdet_postprocess` | RTMDet S, M, L, X | detection | NMS tensors. Only the pre NMS part is rebuilt; the original NMS and everything after it stay. |

For segmentation, the mask prototype output stays unchanged. Note that `yolo_dfl_postprocess` puts channels on axis 1 and `K` on axis 2, while `yolo_no_dfl_postprocess` puts `K` on axis 1.

!!! note "Changed in 2.5.0"
    * Passes were renamed: `yolo_postprocess` is now `yolo_dfl_postprocess`, and `yolo26_postprocess` is now `yolo_no_dfl_postprocess`. The old names raise an error with a migration hint.
    * YOLO passes need a `task` key (`base`, `seg` or `pose`).
    * `input_height` and `input_width` were removed. DX-COM reads the input size from the model. Passing them raises `ValueError`.
    * New: pose for both YOLO passes, segmentation for YOLO26, and the `rtmdet_postprocess` pass.

## API reference

```python
dx_com.pre_optimize(
    model: onnx.ModelProto,
    passes: dict[str, dict],
) -> onnx.ModelProto
```

| Parameter | Type | Description |
|---|---|---|
| `model` | `onnx.ModelProto` | The full model from `onnx.load()`. DX-COM uses the network input to work out the stride of each scale. |
| `passes` | `dict[str, dict]` | Pass name to pass config. Passes run in the given order. |

Returns an optimized `onnx.ModelProto`. Pass it to `dx_com.compile(model=...)`, or save it with `onnx.save()`.

Raises:

* `KeyError`: unknown pass name (old names give a migration hint), or a required key is missing.
* `ValueError`: a tensor name in `layers` cannot be found, or `task` validation fails (missing or unknown `task`, or per layer keys that are required or forbidden for that `task`).

### YOLO pass keys

`yolo_dfl_postprocess` and `yolo_no_dfl_postprocess` take:

| Key | Type | Required | Description |
|---|---|---|---|
| `task` | `str` | Yes | `base` (detection), `seg` (segmentation) or `pose` (keypoints). |
| `layers` | `list[dict]` | Yes | One entry per detection scale, mapping roles to Conv head output tensor names. Order by stride: 8, 16, 32 (80×80, 40×40, 20×20 at 640×640). The key is `layers` (plural); the old PPU block used `layer`. |
| `num_classes` | `int` | Yes for `yolo_dfl_postprocess`; optional (default 80) for `yolo_no_dfl_postprocess` | Number of classes. |
| `topk` | `int` | No (default 300) | Candidates kept after TopK. |

Roles in each `layers` entry:

| Role | Description |
|---|---|
| `bbox` | Output of the box regression head Conv: distances from each anchor point to the four box sides, as 16 bin distributions (`yolo_dfl_postprocess`) or direct values (`yolo_no_dfl_postprocess`). Example: `/model.22/cv2.0/cv2.0.2/Conv_output_0` (YOLOv8n-seg). |
| `cls_conf` | Output of the classification head Conv: one logit per class, before Sigmoid. Example: `/model.22/cv3.0/cv3.0.2/Conv_output_0`. |
| `mask_coeff` | Output of the mask coefficient head Conv: 32 coefficients per instance. Example: `/model.22/cv4.0/cv4.0.2/Conv_output_0` (YOLOv8n-seg). |
| `kpt` | Output of the keypoint head Conv, with `num_keypoints × values_per_keypoint` channels. Example: `/model.22/cv4.0/cv4.0.2/Conv_output_0` (YOLOv8n-pose, 17 × 3 = 51 channels). |
| `kpt_shape` | Keypoint layout `[num_keypoints, values_per_keypoint]`. `values_per_keypoint` is 3 (x, y, visibility), or 2 (x, y) without visibility. Ultralytics stores it in the ONNX metadata as `kpt_shape`. Example: `[17, 3]` (COCO). |

| `task` | Required roles per layer | Forbidden roles |
|---|---|---|
| `base` | `bbox`, `cls_conf` | `mask_coeff`, `kpt` |
| `seg` | `bbox`, `cls_conf`, `mask_coeff` | `kpt` |
| `pose` | `bbox`, `cls_conf`, `kpt`, `kpt_shape` | `mask_coeff` |

Validation runs before any graph change and the error message starts with the pass name. For `pose`, `kpt_shape` must be the same on every scale, and `num_keypoints × values_per_keypoint` must equal the keypoint Conv channel count.

### RTMDet pass keys

`rtmdet_postprocess` is detection only and has no `task` key.

| Key | Type | Required | Description |
|---|---|---|---|
| `cls_layers` | `list[str]` | Yes | Classification Conv head output tensor names, one per scale. |
| `reg_layers` | `list[str]` | Yes | Regression Conv head output tensor names, one per scale. |
| `use_exp` | `bool` | Yes | `True` if the regression branch applies `Exp` (for example RTMDet-M), else `False`. |
| `nms_boxes_tensor` | `str` | Yes | Boxes tensor that feeds the original NMS. |
| `nms_scores_tensor` | `str` | Yes | Full per class score tensor `[1, M, C]` (after Sigmoid) that feeds NMS. M is the number kept by the model's own first `TopK`, for example 5000. |
| `nms_score_tensor` | `str` | Yes | TopK score values tensor (TopK output). |
| `num_classes` | `int` | No (from `cls_layers`) | Number of classes. |
| `topk` | `int` | No (default 512) | Candidates kept after TopK. |

## Use it

You can run the passes from Python, or put them in the config file. Both give the same result.

!!! warning "Use your own tensor names"
    The names below come from real exports, but names such as `onnx::Concat_328` change with the exporter version, export options and opset. Look them up in your own file with the [script](#find-the-head-tensor-names).

### Python

```python
import onnx
import dx_com

model = onnx.load("yolov8n.onnx")
optimized = dx_com.pre_optimize(model, passes={
    "yolo_dfl_postprocess": {
        "task": "base",
        "layers": [
            {"bbox": "onnx::Concat_328", "cls_conf": "onnx::Concat_335"},
            {"bbox": "onnx::Concat_343", "cls_conf": "onnx::Concat_350"},
            {"bbox": "onnx::Concat_358", "cls_conf": "onnx::Concat_365"},
        ],
        "num_classes": 80,
        "topk": 300,
    },
})
# Output: [1, 84, 300]  (4 bbox xywh + 80 class scores, K = 300)

dx_com.compile(model=optimized, config="yolov8n.json", output_dir="./out")
```

### Config file

Add a `pre_optimize` list of single key `{pass_name: config}` items. `dx_com.compile()` applies them to the ONNX model before compiling.

```json
{
  "inputs": {"images": [1, 3, 640, 640]},
  "calibration_method": "ema",
  "calibration_num": 100,
  "default_loader": {
    "dataset_path": "/data/calibration_dataset",
    "file_extensions": ["jpeg", "jpg", "png"],
    "preprocessings": [
      {"resize": {"width": 640, "height": 640}},
      {"convertColor": {"form": "BGR2RGB"}},
      {"div": {"x": 255}},
      {"transpose": {"axis": [2, 0, 1]}},
      {"expandDim": {"axis": 0}}
    ]
  },
  "pre_optimize": [
    {
      "yolo_dfl_postprocess": {
        "task": "base",
        "layers": [
          {"bbox": "onnx::Concat_328", "cls_conf": "onnx::Concat_335"},
          {"bbox": "onnx::Concat_343", "cls_conf": "onnx::Concat_350"},
          {"bbox": "onnx::Concat_358", "cls_conf": "onnx::Concat_365"}
        ],
        "num_classes": 80,
        "topk": 300
      }
    }
  ]
}
```

```python
import dx_com

dx_com.compile(model="yolov8n.onnx", config="config.json", output_dir="./out")
```

The output is `<stem>.dxnn`, named after the source file as in a normal compile. No extra ONNX file is written.

### Pass configs for each model

Put any of these into `passes={...}` in Python, or as one item of the `pre_optimize` list in JSON (with JSON `true` and `false`).

YOLOv8n segmentation, output `[1, 116, 300]` (4 bbox + 80 classes + 32 mask coefficients) plus the unchanged prototype `[1, 32, 160, 160]`:

```python
{"yolo_dfl_postprocess": {
    "task": "seg",
    "layers": [
        {"bbox": "/model.22/cv2.0/cv2.0.2/Conv_output_0",
         "cls_conf": "/model.22/cv3.0/cv3.0.2/Conv_output_0",
         "mask_coeff": "/model.22/cv4.0/cv4.0.2/Conv_output_0"},
        {"bbox": "/model.22/cv2.1/cv2.1.2/Conv_output_0",
         "cls_conf": "/model.22/cv3.1/cv3.1.2/Conv_output_0",
         "mask_coeff": "/model.22/cv4.1/cv4.1.2/Conv_output_0"},
        {"bbox": "/model.22/cv2.2/cv2.2.2/Conv_output_0",
         "cls_conf": "/model.22/cv3.2/cv3.2.2/Conv_output_0",
         "mask_coeff": "/model.22/cv4.2/cv4.2.2/Conv_output_0"},
    ],
    "num_classes": 80,
    "topk": 300,
}}
```

YOLOv8n pose, output `[1, 56, 300]` (4 bbox + 1 class + 17×3 keypoints):

```python
{"yolo_dfl_postprocess": {
    "task": "pose",
    "layers": [
        {"bbox": "/model.22/cv2.0/cv2.0.2/Conv_output_0",
         "cls_conf": "/model.22/cv3.0/cv3.0.2/Conv_output_0",
         "kpt": "/model.22/cv4.0/cv4.0.2/Conv_output_0", "kpt_shape": [17, 3]},
        {"bbox": "/model.22/cv2.1/cv2.1.2/Conv_output_0",
         "cls_conf": "/model.22/cv3.1/cv3.1.2/Conv_output_0",
         "kpt": "/model.22/cv4.1/cv4.1.2/Conv_output_0", "kpt_shape": [17, 3]},
        {"bbox": "/model.22/cv2.2/cv2.2.2/Conv_output_0",
         "cls_conf": "/model.22/cv3.2/cv3.2.2/Conv_output_0",
         "kpt": "/model.22/cv4.2/cv4.2.2/Conv_output_0", "kpt_shape": [17, 3]},
    ],
    "num_classes": 1,
    "topk": 300,
}}
```

YOLO26n detection, output `[1, 300, 6]` (bbox xyxy + score + class_id):

```python
{"yolo_no_dfl_postprocess": {
    "task": "base",
    "layers": [
        {"bbox": "/model.23/one2one_cv2.0/one2one_cv2.0.2/Conv_output_0",
         "cls_conf": "/model.23/one2one_cv3.0/one2one_cv3.0.2/Conv_output_0"},
        {"bbox": "/model.23/one2one_cv2.1/one2one_cv2.1.2/Conv_output_0",
         "cls_conf": "/model.23/one2one_cv3.1/one2one_cv3.1.2/Conv_output_0"},
        {"bbox": "/model.23/one2one_cv2.2/one2one_cv2.2.2/Conv_output_0",
         "cls_conf": "/model.23/one2one_cv3.2/one2one_cv3.2.2/Conv_output_0"},
    ],
    "num_classes": 80,  # optional for this pass, default 80
    "topk": 300,
}}
```

YOLO26n segmentation, output `[1, 300, 38]` (bbox xyxy + score + class_id + 32 mask coefficients) plus the unchanged prototype `[1, 32, 160, 160]`:

```python
{"yolo_no_dfl_postprocess": {
    "task": "seg",
    "layers": [
        {"bbox": "/model.23/one2one_cv2.0/one2one_cv2.0.2/Conv_output_0",
         "cls_conf": "/model.23/one2one_cv3.0/one2one_cv3.0.2/Conv_output_0",
         "mask_coeff": "/model.23/one2one_cv4.0/one2one_cv4.0.2/Conv_output_0"},
        {"bbox": "/model.23/one2one_cv2.1/one2one_cv2.1.2/Conv_output_0",
         "cls_conf": "/model.23/one2one_cv3.1/one2one_cv3.1.2/Conv_output_0",
         "mask_coeff": "/model.23/one2one_cv4.1/one2one_cv4.1.2/Conv_output_0"},
        {"bbox": "/model.23/one2one_cv2.2/one2one_cv2.2.2/Conv_output_0",
         "cls_conf": "/model.23/one2one_cv3.2/one2one_cv3.2.2/Conv_output_0",
         "mask_coeff": "/model.23/one2one_cv4.2/one2one_cv4.2.2/Conv_output_0"},
    ],
    "num_classes": 80,
    "topk": 300,
}}
```

YOLO26n pose, output `[1, 300, 57]` (bbox xyxy + score + class_id + 17×3 keypoints):

```python
{"yolo_no_dfl_postprocess": {
    "task": "pose",
    "layers": [
        {"bbox": "/model.23/one2one_cv2.0/one2one_cv2.0.2/Conv_output_0",
         "cls_conf": "/model.23/one2one_cv3.0/one2one_cv3.0.2/Conv_output_0",
         "kpt": "/model.23/one2one_cv4_kpts.0/Conv_output_0", "kpt_shape": [17, 3]},
        {"bbox": "/model.23/one2one_cv2.1/one2one_cv2.1.2/Conv_output_0",
         "cls_conf": "/model.23/one2one_cv3.1/one2one_cv3.1.2/Conv_output_0",
         "kpt": "/model.23/one2one_cv4_kpts.1/Conv_output_0", "kpt_shape": [17, 3]},
        {"bbox": "/model.23/one2one_cv2.2/one2one_cv2.2.2/Conv_output_0",
         "cls_conf": "/model.23/one2one_cv3.2/one2one_cv3.2.2/Conv_output_0",
         "kpt": "/model.23/one2one_cv4_kpts.2/Conv_output_0", "kpt_shape": [17, 3]},
    ],
    "num_classes": 1,
    "topk": 300,
}}
```

RTMDet-S detection (RTMDet-M differs only in `"use_exp": True`):

```python
{"rtmdet_postprocess": {
    "cls_layers": [
        "/bbox_head/rtm_cls.0/Conv_output_0",
        "/bbox_head/rtm_cls.1/Conv_output_0",
        "/bbox_head/rtm_cls.2/Conv_output_0",
    ],
    "reg_layers": [
        "/bbox_head/rtm_reg.0/Conv_output_0",
        "/bbox_head/rtm_reg.1/Conv_output_0",
        "/bbox_head/rtm_reg.2/Conv_output_0",
    ],
    "use_exp": False,
    "nms_boxes_tensor": "/Gather_6_output_0",
    "nms_scores_tensor": "/Gather_7_output_0",
    "nms_score_tensor": "/TopK_output_0",
    "topk": 512,
}}
```

## Find the head tensor names

Each `layers` entry maps a role to the output tensor name of the last Conv of that head branch: the raw head output before any Sigmoid, DFL or box decoding. Always look the names up in your own model.

A head Conv meets all of these:

1. It is the last Conv of its branch. No activation (Sigmoid, SiLU, Mul) follows it. Its output feeds only `Concat`, `Reshape` or `Transpose`.
1. Its output is 4D, `[1, C, H/s, W/s]`, with stride `s` of 8, 16 or 32.
1. Its channel count `C` matches a role: `bbox` 64 (4 sides × 16 DFL bins) for `yolo_dfl_postprocess` or 4 for `yolo_no_dfl_postprocess`; `cls_conf` `num_classes`; `mask_coeff` 32; `kpt` `num_keypoints × values_per_keypoint` (for example 51).

Two Convs look similar but are not heads: the DFL Conv (1 channel, after a Softmax), and the segmentation prototype Conv (32 channels at stride 4, for example 160×160). For YOLO26, use the `one2one_*` branches (the NMS free head), not the `one2many` training branches. Without `kpt_shape` metadata, read it from the `Reshape` after the `Concat` of the three `kpt` outputs: its target shape is `[1, num_keypoints, values_per_keypoint, -1]`, for example `[1, 17, 3, -1]`.

### Script for YOLO

This script prints a ready to use `pre_optimize` block. For Ultralytics exports it reads `task`, the class count and `kpt_shape` from the ONNX metadata, so you normally set only `MODEL` and `PASS`.

```python
import ast
import json
from collections import defaultdict

import onnx
from onnx import shape_inference

# ---- set these for your model ----
MODEL = "model.onnx"
PASS = "yolo_dfl_postprocess"  # YOLOv8/v9/v11/v12/v13; "yolo_no_dfl_postprocess" for YOLO26
# None = read from the Ultralytics ONNX metadata
TASK = None                    # "base" | "seg" | "pose"
NUM_CLASSES = None             # 80 = COCO, 1 = single class (e.g. person pose)
KPT_SHAPE = None               # pose: [num_keypoints, values_per_keypoint], e.g. [17, 3]
MASK_CH = 32                   # seg: mask coefficient channels
# ----------------------------------

model = shape_inference.infer_shapes(onnx.load(MODEL))
g = model.graph
meta = {p.key: p.value for p in model.metadata_props}


def from_meta(key):
    assert key in meta, f"'{key}' is not in the ONNX metadata: set it manually above"
    return meta[key] if key == "task" else ast.literal_eval(meta[key])


if TASK is None:
    TASK = {"detect": "base", "segment": "seg", "pose": "pose"}.get(from_meta("task"))
    assert TASK, f"unsupported task '{meta['task']}'"
if NUM_CLASSES is None:
    NUM_CLASSES = len(from_meta("names"))
if TASK == "pose" and KPT_SHAPE is None:
    KPT_SHAPE = list(from_meta("kpt_shape"))

shape = {v.name: [d.dim_value for d in v.type.tensor_type.shape.dim]
         for v in list(g.input) + list(g.value_info) + list(g.output)}
consumers = defaultdict(set)
for n in g.node:
    for i in n.input:
        consumers[i].add(n.op_type)

# Channel count of each head Conv, per task
roles = {"bbox": 64 if PASS == "yolo_dfl_postprocess" else 4, "cls_conf": NUM_CLASSES}
if TASK == "seg":
    roles["mask_coeff"] = MASK_CH
elif TASK == "pose":
    roles["kpt"] = KPT_SHAPE[0] * KPT_SHAPE[1]
assert len(set(roles.values())) == len(roles), f"channel collision {roles}: pick heads in Netron"

# Head Conv = 4D output on an FPN scale (stride 8/16/32) with no activation after it
in_h = shape[g.input[0].name][2]
assert in_h, "input H is dynamic: re-export the model with a fixed input size"
heads = defaultdict(lambda: defaultdict(list))  # stride -> channels -> [tensor names]
for n in g.node:
    out = n.output[0]
    d = shape.get(out)
    if n.op_type != "Conv" or not d or len(d) != 4 or not d[2] or in_h % d[2]:
        continue
    stride, ops = in_h // d[2], consumers[out]
    if stride in (8, 16, 32) and ops <= {"Concat", "Reshape", "Transpose"}:
        heads[stride][d[1]].append(out)
assert heads, "no head Conv found: check PASS and the model input"

layers = []
for stride in sorted(heads):  # layers must be in stride order (8, 16, 32)
    layer = {}
    for role, ch in roles.items():
        names = heads[stride].get(ch, [])
        assert len(names) == 1, f"stride {stride}: expected 1 {role} Conv ({ch}ch), got {names}"
        layer[role] = names[0]
    if TASK == "pose":
        layer["kpt_shape"] = KPT_SHAPE
    layers.append(layer)

cfg = {"task": TASK, "layers": layers, "num_classes": NUM_CLASSES}
print(json.dumps({"pre_optimize": [{PASS: cfg}]}, indent=2))
# Python API: dx_com.pre_optimize(onnx.load(MODEL), passes={PASS: cfg})
```

When the model has no Ultralytics metadata (for example after another tool re-exported it), set the values yourself:

| Model and task | `PASS` | `TASK` | `NUM_CLASSES` | `KPT_SHAPE` | Roles per layer |
|---|---|---|---|---|---|
| YOLOv8 or v11, detection | `yolo_dfl_postprocess` | `base` | 80 | | `bbox` 64ch, `cls_conf` 80ch |
| YOLOv8 or v11, segmentation | `yolo_dfl_postprocess` | `seg` | 80 | | `bbox` 64ch, `cls_conf` 80ch, `mask_coeff` 32ch |
| YOLOv8 or v11, pose | `yolo_dfl_postprocess` | `pose` | 1 | `[17, 3]` | `bbox` 64ch, `cls_conf` 1ch, `kpt` 51ch, `kpt_shape` |
| YOLO26, detection | `yolo_no_dfl_postprocess` | `base` | 80 | | `bbox` 4ch, `cls_conf` 80ch |
| YOLO26, segmentation | `yolo_no_dfl_postprocess` | `seg` | 80 | | `bbox` 4ch, `cls_conf` 80ch, `mask_coeff` 32ch |
| YOLO26, pose | `yolo_no_dfl_postprocess` | `pose` | 1 | `[17, 3]` | `bbox` 4ch, `cls_conf` 1ch, `kpt` 51ch, `kpt_shape` |

For the YOLOv8n detection model above, the script prints:

```json
{
  "pre_optimize": [
    {
      "yolo_dfl_postprocess": {
        "task": "base",
        "layers": [
          {"bbox": "onnx::Concat_328", "cls_conf": "onnx::Concat_335"},
          {"bbox": "onnx::Concat_343", "cls_conf": "onnx::Concat_350"},
          {"bbox": "onnx::Concat_358", "cls_conf": "onnx::Concat_365"}
        ],
        "num_classes": 80
      }
    }
  ]
}
```

Paste it into the config as is, or pass `cfg` to `dx_com.pre_optimize()`. `topk` is not printed: add it to change the default of 300. If the script stops with an `AssertionError`, the message says which value to check, usually `NUM_CLASSES` (no `cls_conf` Conv found) or `PASS` (no `bbox` Conv found).

### Find them in Netron

1. Netron shows tensor shapes only when the model stores them. Save a copy with shapes first:

    ```python
    import onnx
    from onnx import shape_inference

    onnx.save(shape_inference.infer_shapes(onnx.load("model.onnx")), "model_shapes.onnx")
    ```

1. Open `model_shapes.onnx` in [Netron](https://netron.app) and scroll to the end of the graph, where the head branches merge into the output.
1. For each scale, follow the parallel branches up from the `Concat` that joins them. The first `Conv` on each branch is a head Conv. No Sigmoid or SiLU follows it.
1. Click the Conv. The side panel shows its output name (copy it into `layers`) and its shape `[1, C, H, W]`. `C` gives the role, `H` gives the scale.

### Script for RTMDet

This script finds all six required keys for an MMDetection RTMDet export with NMS in the graph:

```python
import json
from collections import defaultdict

import onnx
from onnx import shape_inference

MODEL = "rtmdet.onnx"

model = shape_inference.infer_shapes(onnx.load(MODEL))
g = model.graph
shape = {v.name: [d.dim_value for d in v.type.tensor_type.shape.dim]
         for v in list(g.input) + list(g.value_info) + list(g.output)}
producer = {o: n for n in g.node for o in n.output}
consumers = defaultdict(list)
for n in g.node:
    for i in n.input:
        consumers[i].append(n.op_type)

in_h = shape[g.input[0].name][2]
assert in_h, "input H is dynamic: re-export the model with a fixed input size"
cls_layers, reg_layers = [], []
for n in g.node:
    out = n.output[0]
    d = shape.get(out)
    if n.op_type != "Conv" or not d or len(d) != 4 or not d[2]:
        continue
    if "rtm_cls" in out:
        cls_layers.append((in_h // d[2], out))
    elif "rtm_reg" in out:
        reg_layers.append((in_h // d[2], out))
assert cls_layers and len(cls_layers) == len(reg_layers), f"cls={cls_layers} reg={reg_layers}"

nms = [n for n in g.node if n.op_type == "NonMaxSuppression"]
assert nms, "no NonMaxSuppression in the graph: export the model with NMS"
scores_t = producer[nms[0].input[1]]
assert scores_t.op_type == "Transpose", f"unexpected NMS score producer: {scores_t.op_type}"
topk = next(n for n in g.node if n.op_type == "TopK")  # the first TopK, over all anchors

cfg = {
    "cls_layers": [o for _, o in sorted(cls_layers)],  # stride 8, 16, 32
    "reg_layers": [o for _, o in sorted(reg_layers)],
    "use_exp": "Exp" in consumers[reg_layers[0][1]],  # Exp (not Mul) after rtm_reg
    "nms_boxes_tensor": nms[0].input[0],
    "nms_scores_tensor": scores_t.input[0],
    "nms_score_tensor": topk.output[0],
}
print(json.dumps({"pre_optimize": [{"rtmdet_postprocess": cfg}]}, indent=2))
```

For RTMDet-S it prints the same values as the RTMDet-S example above.

## Performance

Throughput on DX-M1 with an ARM Cortex-A53 host CPU:

| Pass | Model | Task | Before (FPS) | After (FPS) | Speed up |
|---|---|---|---:|---:|---:|
| `yolo_dfl_postprocess` | YOLOv8n | det | 89.53 | 355.73 | 4.0× |
| `yolo_dfl_postprocess` | YOLOv8n | seg | 63.81 | 209.69 | 3.3× |
| `yolo_dfl_postprocess` | YOLOv8n | pose | 268.98 | 400.59 | 1.5× |
| `yolo_no_dfl_postprocess` | YOLO26n | det | 184.89 | 315.73 | 1.7× |
| `yolo_no_dfl_postprocess` | YOLO26n | seg | 130.82 | 195.05 | 1.5× |
| `yolo_no_dfl_postprocess` | YOLO26n | pose | 242.77 | 304.38 | 1.3× |
| `rtmdet_postprocess` | RTMDet-S (score_threshold 0.3) | det | 156.56 | 290.16 | 1.9× |

Measured with DX-RT:

```bash
DXRT_DYNAMIC_CPU_THREAD=ON dxrun -m <model_path> -l 1000 --use-ort
```

## Migrate from PPU type 2

Replace the `ppu` block with a `pre_optimize` block. Before (deprecated):

```json
{
  "ppu": {
    "type": 2,
    "topk": 512,
    "num_classes": 80,
    "layer": [
      {"bbox": "onnx::Concat_328", "cls_conf": "onnx::Concat_335"},
      {"bbox": "onnx::Concat_343", "cls_conf": "onnx::Concat_350"},
      {"bbox": "onnx::Concat_358", "cls_conf": "onnx::Concat_365"}
    ]
  }
}
```

After:

```json
{
  "pre_optimize": [
    {
      "yolo_dfl_postprocess": {
        "task": "base",
        "layers": [
          {"bbox": "onnx::Concat_328", "cls_conf": "onnx::Concat_335"},
          {"bbox": "onnx::Concat_343", "cls_conf": "onnx::Concat_350"},
          {"bbox": "onnx::Concat_358", "cls_conf": "onnx::Concat_365"}
        ],
        "num_classes": 80,
        "topk": 512
      }
    }
  ]
}
```

You can reuse a PPU `layer` entry as a `layers` entry only when both refer to the same ONNX file and each name is a raw head Conv output. After a new export the names can change: look them up again with the [script](#script-for-yolo).

| | PPU type 2 | `pre_optimize` |
|---|---|---|
| Where to configure | JSON config | Python API or JSON `pre_optimize` block |
| Segmentation | No | Yes |
| Pose | No | Yes |
| YOLO26 | No | Yes (`yolo_no_dfl_postprocess`) |
| RTMDet | No | Yes (`rtmdet_postprocess`) |

## Next steps

* [Use cases](use-cases.md#yolo-post-processing-on-a-weak-cpu)
* [PPU for YOLO models](ppu.md)
* [Run the model with DX-RT](../runtime/index.md)
