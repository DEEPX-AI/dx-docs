---
title: PPU for YOLO models
description: Use the NPU Post Processing Unit to filter YOLO detections on the NPU, pick the right PPU type and find the node names.
---

# PPU for YOLO models

This page lets you move part of the YOLO detection post processing (confidence filtering and class prediction) onto the NPU Post Processing Unit (PPU), so the host CPU does less work.

## Before you start

* A YOLO family detection model that compiles without PPU.
* [Netron](https://netron.app) or a short Python script to read node names from your ONNX file.

## When to use the PPU

| Use it | Do not use it |
|---|---|
| YOLO family and similar detection models | Classification models (ResNet, MobileNet): they need no filtering |
| Edge devices with little CPU headroom | Segmentation models (DeepLab, U-Net): pixel level masks do not fit the PPU |
| Real time applications that need high FPS | Custom detection heads that do not match the YOLO output layout |

!!! warning "NMS still runs on the host CPU"
    The PPU does confidence filtering and class prediction (ArgMax) only. Run NMS (non maximum suppression) on the host CPU on the filtered outputs. There are no `iou_thres` or `max_det` keys.

!!! warning "Do not combine with pre_optimize"
    `ppu` and `pre_optimize` both rewrite detection post processing. DX-COM 2.5.0 does not reject a config with both: it compiles with `ppu` and drops `pre_optimize`, or fails later with an unrelated error. The only sign is the console line `falling back to legacy: ValueError: config 'pre_optimize' and 'ppu' are mutually exclusive`.

## Pick the type

| `type` | Python `PPUTypes` | Architecture | Models | Effect |
|---|---|---|---|---|
| 0 | `YOLO_BASE` | Anchor based | YOLOv3, YOLOv4, YOLOv5, YOLOv7 | Filtering and class prediction on the PPU |
| 1 | `YOLO_ANCHORFREE` | Anchor free | YOLOX, YOLOv8, YOLOv9, YOLOv10, YOLOv11, YOLOv12 | Filtering and class prediction on the PPU |
| 2 | `YOLOV8` | DFL based, CPU TopK | YOLOv8, YOLOv9, YOLOv11, YOLOv12 | Deprecated since 2.4.0. Does not use the PPU hardware. Use [Pre Optimize API](pre-optimize.md) instead. |

A wrong type can give wrong detections without an error. YOLO26 is not a PPU model: its NMS free output already contains filtered detections. For faster CPU post processing of YOLO26, use `pre_optimize` with `yolo_no_dfl_postprocess`.

## Type 0: anchor based

```json
{
  "ppu": {
    "type": 0,
    "conf_thres": 0.25,
    "activation": "Sigmoid",
    "num_classes": 80,
    "layer": {
      "Conv_245": {"num_anchors": 3},
      "Conv_294": {"num_anchors": 3},
      "Conv_343": {"num_anchors": 3}
    }
  }
}
```

| Field | Description |
|---|---|
| `type` | `0` |
| `conf_thres` | Confidence threshold, fixed at compile time. |
| `activation` | Normally `"Sigmoid"`. |
| `num_classes` | Number of detection classes. |
| `layer` | Dict from detection head Conv node name to `{"num_anchors": N}`. |

## Type 1: anchor free

YOLOX uses `bbox`, `obj_conf` and `cls_conf` for each scale:

```json
{
  "ppu": {
    "type": 1,
    "conf_thres": 0.25,
    "num_classes": 80,
    "layer": [
      {"bbox": "output_bbox_1", "obj_conf": "output_obj_1", "cls_conf": "output_cls_1"},
      {"bbox": "output_bbox_2", "obj_conf": "output_obj_2", "cls_conf": "output_cls_2"},
      {"bbox": "output_bbox_3", "obj_conf": "output_obj_3", "cls_conf": "output_cls_3"}
    ]
  }
}
```

YOLOv8 to YOLOv12 use one entry with `bbox` and `cls_conf`, which covers every scale:

```json
{
  "ppu": {
    "type": 1,
    "conf_thres": 0.25,
    "num_classes": 80,
    "layer": [
      {"bbox": "Mul_441", "cls_conf": "Sigmoid_442"}
    ]
  }
}
```

| Field | Description |
|---|---|
| `type` | `1` |
| `conf_thres` | Confidence threshold, fixed at compile time. |
| `num_classes` | Number of detection classes. |
| `layer` | List of head mappings: `bbox` (box output), `obj_conf` (object confidence, YOLOX only), `cls_conf` (class confidence). |

## Type 2: deprecated

!!! warning "Deprecated since DX-COM 2.4.0"
    Type 2 still compiles but prints a deprecation warning, and we will remove it in a future release. Use [Pre Optimize API](pre-optimize.md), which does the same TopK first optimization and also supports segmentation, pose, YOLO26 and RTMDet. See [Migrate from PPU type 2](pre-optimize.md#migrate-from-ppu-type-2).

Type 2 does not use the PPU hardware. TopK and all decoding run on the host CPU, but TopK first cuts the number of candidates that the later DFL decoding and filtering must handle.

```json
{
  "ppu": {
    "type": 2,
    "topk": 512,
    "num_classes": 80,
    "layer": [
      {"bbox": "bbox_head_p3", "cls_conf": "cls_head_p3"},
      {"bbox": "bbox_head_p4", "cls_conf": "cls_head_p4"},
      {"bbox": "bbox_head_p5", "cls_conf": "cls_head_p5"}
    ]
  }
}
```

| Field | Description |
|---|---|
| `type` | `2` |
| `topk` | Candidates kept before decoding. Without it DX-COM uses an internal default. 512 is a good start. |
| `num_classes` | Number of detection classes. |
| `layer` | One entry per detection scale: final `bbox` head node and final `cls_conf` head node of the same scale. |

## Find the node names

Use ONNX operator node names (the boxes in Netron), not tensor names. Open the model in [Netron](https://netron.app):

| Type | What to find |
|---|---|
| 0 (YOLOv3 to v7) | Trace back from the outputs to the detection head Conv layers. Their output shape is `[1, num_anchors*(5+num_classes), H, W]`. In YOLOv7 they are named like `/model.105/m.0/Conv`, `/model.105/m.1/Conv`, `/model.105/m.2/Conv`. |
| 1 (YOLOX) | For each of the 3 scales, the `bbox`, `obj_conf` and `cls_conf` Conv nodes: 9 Conv layers in total. |
| 1 (YOLOv8 and later) | Trace back from the final `Concat`. `bbox` is usually a `Mul` or `Add`, `cls_conf` usually a `Sigmoid`. |
| 2 | For each of the 3 scales, the final Conv nodes of the decoupled `bbox` and `cls_conf` head branches. |

## Compile with the PPU

=== "CLI"
    Add the `ppu` block to a complete config (see [Config file reference](config-reference.md#complete-working-example)) and compile:

    ```bash
    dxcom -m yolov8.onnx -c yolov8_config.json -o output/yolov8
    ```

=== "Python"
    Pass a `PPUConfig` and use a config without a `ppu` block (or a `dataloader`):

    ```python
    import dx_com
    from dx_com import PPUConfig, PPUTypes

    ppu_config = (
        PPUConfig()
        .set_type(PPUTypes.YOLO_ANCHORFREE)
        .set_num_classes(80)
        .set_conf_thres(0.25)
    )
    ppu_config.add_layer(bbox="Mul_441", cls_conf="Sigmoid_442")

    dx_com.compile(
        model="yolov8.onnx",
        output_dir="output/yolov8",
        config="yolov8_base_config.json",
        ppu_config=ppu_config,
    )
    ```

See [PPUConfig](python-api.md#ppuconfig) for every method.

## Next steps

* [Pre Optimize API](pre-optimize.md)
* [Use cases](use-cases.md#yolo-with-the-ppu)
* [Config file reference](config-reference.md#ppu)
