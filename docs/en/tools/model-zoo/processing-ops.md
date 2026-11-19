---
title: Preprocessing and postprocessing
description: Reference for every built in DX-ModelZoo preprocessing and postprocessing operation and the pipeline classes that run them.
---

# Preprocessing and postprocessing

This page lists every built in preprocessing and postprocessing operation you can use as a `type` in a model YAML, and the pipeline classes that run them.

## Before you start

* You know the [YAML configuration](yaml-config.md) keys.

## PreprocessingPipeline

Module: `dx_modelzoo.preprocessing`. Runs the YAML `preprocessing` steps in order on a BGR `np.ndarray`.

```python
class PreprocessingPipeline(Compose):   # torchvision.transforms.Compose subclass
    def __init__(self, steps_config: list[dict] | dict[str, list[dict]], npu_mode: bool = False)
    def __call__(self, img: np.ndarray) -> np.ndarray
```

| Parameter | Meaning |
|---|---|
| `steps_config` | Step config dicts (`{"type": ..., **params}`), the YAML `preprocessing` block. A dict keyed by input name for multi input models. |
| `npu_mode` | `True` skips the types in `NPU_SKIP_DEFAULT` |

`steps` holds the built operation objects. Pass config dicts, not operation objects.

```python
import cv2
from dx_modelzoo.preprocessing import PreprocessingPipeline

pipeline = PreprocessingPipeline(steps_config=[
    {"type": "resize", "size": [256, 256]},
    {"type": "centercrop", "height": 224, "width": 224},
])
out = pipeline(cv2.imread("test.jpg"))
```

The pipeline subclasses `torchvision.transforms.Compose` so DX-COM can read the preprocessing during compilation.

## Preprocessing types

| Type | Parameters | What it does | Skipped on NPU with `uint8` input |
|---|---|---|---|
| `resize` | `size`, `mode`, `interpolation` and pad options | Resize | no |
| `centercrop` | `height`, `width` | Center crop | no |
| `convertcolor` | `form` | Color conversion | no |
| `div` | `x` | Divide by `x` | yes |
| `mul` | `x` | Multiply by `x` | yes |
| `add` | `x` | Add `x` | yes |
| `subtract` | `x` | Subtract `x` | yes |
| `normalize` | `mean`, `std` | `(img - mean) / std` per channel | yes |
| `transpose` | `axis` | Permute axes, for example `[2, 0, 1]` for HWC to CHW | yes |
| `expanddim` | `axis` | Insert an axis, for example `0` for the batch | yes |
| `totensor` | none | HWC `uint8` in `[0, 255]` to CHW `float32` in `[0, 1]` (same as `div` 255 plus `transpose`) | no |
| `bgr_to_y_channel` | none | BGR to Y (luminance) channel, for super resolution | replaced by `bgr_to_y_channel_uint8` |
| `bgr_to_y_channel_uint8` | none | BGR to Y channel with `uint8` output | no |

### `resize`

```yaml
- type: resize
  mode: torchvision
  size: [256, 256]
  interpolation: BILINEAR
```

| Parameter | Meaning | Default |
|---|---|---|
| `size` | `[H, W]`, or one int for a square. You can give `height` and `width` instead. | required |
| `mode` | `default`, `torchvision`, `pad` or `pycls` | `default` |
| `interpolation` | `BILINEAR`, `LINEAR`, `NEAREST` or `BICUBIC` | depends on `mode` |
| `align_side`, `scale_method`, `pad_location`, `pad_value` | Fine tuning for `pad` mode (letterbox) | from `mode` |

| Mode | Backend | Behavior |
|---|---|---|
| `default` | OpenCV | Plain resize to the target size |
| `torchvision` | PIL | Same as `torchvision.transforms.Resize` (short side) |
| `pad` | OpenCV | Keep the aspect ratio and pad (letterbox) |
| `pycls` | OpenCV | pycls style resize (short side) |

Any other `mode` raises `ValueError: Invalid mode: ...`. There is no `opencv` or `letterbox` mode.

### `convertcolor`

`form` is one of `BGR2RGB`, `RGB2BGR`, `BGR2GRAY`, `RGB2GRAY`, `GRAY2BGR`, `GRAY2RGB`.

### NPU skip

```python
NPU_SKIP_DEFAULT = {"div", "normalize", "transpose", "expanddim", "mul", "add", "subtract"}
```

For NPU profiles these types are skipped when the compiled model takes `uint8` input. Set `appendix.npu_skip_arithmetic: false` in the YAML to keep them. Custom types are never skipped. See [Architecture](architecture.md#npu-preprocessing-skip).

## PostprocessingPipeline

Module: `dx_modelzoo.postprocessing`. Runs the YAML `postprocessing` steps in order. The output of one step is the input of the next.

```python
class PostprocessingPipeline:
    def __init__(self, steps_config: list[dict])
    def __call__(self, outputs, **kwargs)
```

Pass config dicts in `steps_config`. Passing operation objects raises `AttributeError: 'TopK' object has no attribute 'get'`. An unknown type raises `ValueError` with the list of available types.

The pipeline forwards these keywords to every step:

| Keyword | Given by | Meaning |
|---|---|---|
| `runtime_target` | all evaluators | `"onnx"` or `"npu"` |
| `origin_hw` | detection style evaluators | `(H, W)` of the original image |
| `input_hw` | detection style evaluators | `(H, W)` of the model input |

## Postprocessing types

These types are registered in the shared `postprocessing` package:

| Type | Parameters | Input | Output |
|---|---|---|---|
| `identity` | none | anything | the same object |
| `topk` | `k` (default `[1, 5]`), `skip_background` (default `false`) | class scores | top k class indices, best first |
| `nms` | `conf_thres` (`0.001`), `iou_thres` (`0.7`), `max_output_boxes` (`300`), `pad_resize` (`true`) | `{"boxes": [N, 4] xyxy, "scores": [N], "class_ids": [N]}` from a decode step | `[M, 6]` array: x1, y1, x2, y2, score, class id |
| `segmentation_argmax` | `layout` (`nchw` or `nhwc`, default `nchw`), `target_size` (`[H, W]`, optional nearest resize) | logits `(1, C, H, W)` | class map `(H, W)` |
| `rtdetr_decode` | `pad_location` (default `edge`) | RT-DETR `[detections, count]` output | decoded detections |

Many models use their own decode type from the `custom_ops.py` in their model folder, for example `rtmpose_simcc_decode` (RTMPose), `superpoint_decode` (SuperPoint), `mediapipe_pose_decode` (MediaPipe Pose) and `blazeface_decode` (BlazeFace).

Typical steps per task:

| Task | Postprocessing |
|---|---|
| Image classification | `topk` |
| Object detection | model decode step, then `nms` |
| Semantic segmentation | `segmentation_argmax` |
| Instance segmentation, face detection, pose | model decode step |
| Super resolution, depth estimation | `identity` |

```yaml
postprocessing:
  - type: yolov8_decode      # model specific decode from custom_ops.py
  - type: nms
    conf_thres: 0.001
    iou_thres: 0.7
```

## Write a custom postprocessing step

```python
from dx_modelzoo.postprocessing import POSTPROCESSING_REGISTRY
from dx_modelzoo.postprocessing.coord_scaler import unpad_and_scale


@POSTPROCESSING_REGISTRY.register("my_box_postprocess")
class MyBoxPostprocess:
    def __call__(self, outputs, origin_hw=None, input_hw=None, **kwargs):
        boxes = outputs[0]  # [M, 6] in model input space
        if origin_hw is not None and input_hw is not None:
            boxes[:, :4] = unpad_and_scale(boxes[:, :4], input_hw, origin_hw)
        return boxes
```

!!! warning "Always accept **kwargs"
    A step defined as `__call__(self, outputs)` fails with `TypeError: __call__() got an unexpected keyword argument 'runtime_target'`.

Code that runs once at start (for example building CLIP text embeddings) belongs in a helper file, not in a postprocessing step.

## Next steps

* [Custom models and datasets](custom-models.md)
* [YAML configuration](yaml-config.md)
* [Python API](python-api.md)
