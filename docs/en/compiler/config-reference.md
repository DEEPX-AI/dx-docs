---
title: Config file reference
description: Every key of the DX-COM JSON config file, every preprocessing operation, and complete working examples.
---

# Config file reference

This page lets you write the JSON config file that tells DX-COM the model input, how to calibrate, and how to preprocess the calibration images.

## Before you start

* Know the input name and shape of your ONNX model. See [Find the input name](onnx-models.md#check-the-exported-model).
* Know the preprocessing your model was trained with (image size, RGB or BGR, scale, mean and std).

## Complete working example

This config compiles an ImageNet classifier with input `input` of shape `[1, 3, 224, 224]` (for example MobileNetV2 or ResNet50 exported from PyTorch). Copy it and change the input name, the path and the preprocessing to match your model.

```json
{
  "inputs": {
    "input": [1, 3, 224, 224]
  },
  "calibration_method": "ema",
  "calibration_num": 100,
  "default_loader": {
    "dataset_path": "/data/calibration_dataset",
    "file_extensions": ["jpeg", "jpg", "png", "JPEG"],
    "preprocessings": [
      {"resize": {"mode": "torchvision", "size": 256, "interpolation": "BILINEAR"}},
      {"centercrop": {"width": 224, "height": 224}},
      {"convertColor": {"form": "BGR2RGB"}},
      {"div": {"x": 255}},
      {"normalize": {"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}},
      {"transpose": {"axis": [2, 0, 1]}},
      {"expandDim": {"axis": 0}}
    ]
  }
}
```

```bash
dxcom -m model.onnx -c config.json -o output/
```

For an Ultralytics YOLO model with input `images` of shape `[1, 3, 640, 640]` (RGB in 0 to 1, no mean and std):

```json
{
  "inputs": {
    "images": [1, 3, 640, 640]
  },
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
  }
}
```

## All keys

| Key | Required | Default | Description |
|---|---|---|---|
| `inputs` | Yes | | Model input name and shape, `{"name": [1, C, H, W]}`. |
| `default_loader` | Yes | | Calibration dataset location, file types and preprocessing chain. |
| `calibration_method` | No | `"ema"` | `"ema"`, `"minmax"` or `"iqr"`. |
| `calibration_num` | No | `100` | Number of calibration samples. |
| `enhanced_scheme` | No | none | Manual DXQ scheme (DXQ-P0 to DXQ-P5) for better accuracy. DX-COM 2.1.0 and later. |
| `qmaster` | No | none | Q-Master (QAT) training settings. The block turns Q-Master on. DX-COM 2.4.0 and later. |
| `ppu` | No | none | NPU post processing for YOLO detection models. Do not combine with `pre_optimize`. |
| `pre_optimize` | No | none | ONNX level post processing rewrite for YOLO and RTMDet. Do not combine with `ppu`. DX-COM 2.4.0 and later. |
| `quantization_device` | No | | Deprecated in 2.5.0 and ignored. Remove it. |

## inputs

```json
{
  "inputs": {
    "input.1": [1, 3, 512, 512]
  }
}
```

* The key must match the ONNX input name exactly.
* The shape must match the ONNX input shape exactly. All values are positive integers.
* The batch size (first value) must be 1.
* Only one input is supported in a JSON config. For multi input models, use the [Python API](python-api.md#calibrate-with-a-dataloader) with a `DataLoader`.

## calibration_method

Sets how DX-COM picks the value range of each activation during INT8 quantization.

| Value | Description |
|---|---|
| `"ema"` | Exponential moving average of activation values. Default, recommended for most models. |
| `"minmax"` | Minimum and maximum activation values. |
| `"iqr"` | Interquartile range (25th to 75th percentile). More robust to outliers than `minmax`, useful when calibration data has extreme values. |

Values are lowercase. `"EMA"` is rejected.

## calibration_num

Number of calibration samples. A positive integer, default `100`. A higher number can estimate activation ranges better but takes longer. Try values such as 1, 5, 10, 100 and 1000 and keep the one that gives the best accuracy for your model.

If the dataset has fewer images than `calibration_num`, DX-COM uses all of them and prints no warning.

## default_loader

```json
{
  "default_loader": {
    "dataset_path": "/data/calibration_dataset",
    "file_extensions": ["jpeg", "jpg", "png", "JPEG"],
    "preprocessings": [
      {"resize": {"width": 224, "height": 224}},
      {"convertColor": {"form": "BGR2RGB"}},
      {"div": {"x": 255}},
      {"normalize": {"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}},
      {"transpose": {"axis": [2, 0, 1]}},
      {"expandDim": {"axis": 0}}
    ]
  }
}
```

| Field | Required | Description |
|---|---|---|
| `dataset_path` | Yes | Folder with calibration images. Subfolders are searched too. A relative path is resolved from the current working directory, not from the config file. Prefer an absolute path. |
| `file_extensions` | Yes | List of extensions without the dot. Matched case sensitively, so list `"JPG"` as well as `"jpg"` when both exist. |
| `preprocessings` | Yes | List of operations, applied in order. One operation per list item. |

### How the default loader reads images

`default_loader` reads each image with OpenCV as **BGR, HWC, uint8 (0 to 255)**. It applies only the operations you list. It never rescales, converts color or transposes on its own. The end of the chain must be exactly the model input shape:

| Model input in `inputs` | End the chain with |
|---|---|
| NCHW `[1, C, H, W]` (most PyTorch and all Ultralytics YOLO exports) | `{"transpose": {"axis": [2, 0, 1]}}` and then `{"expandDim": {"axis": 0}}` |
| NHWC `[1, H, W, C]` | `{"expandDim": {"axis": 0}}` |

If you forget the transpose, calibration fails before compiling:

```text
DataLoaderError: Invalid JSON Configuration for input 'input': The config specifies (1, 224, 224, 3),
but model requires (1, 3, 224, 224). Please check the preprocessing configuration.
```

The shape in this message is the shape after your preprocessing chain, not the `inputs` value.

For a model trained on RGB input in 0 to 1, put `convertColor` `BGR2RGB` and `div` 255 before `normalize`. `normalize` alone does not rescale 0 to 255 values, and the compile still succeeds with wrongly scaled calibration data.

## Preprocessing operations

| Operation | Example | Notes |
|---|---|---|
| `resize` | `{"resize": {"width": 224, "height": 224}}` | See [resize](#resize). |
| `centercrop` | `{"centercrop": {"width": 224, "height": 224}}` | Crops the central region. |
| `convertColor` | `{"convertColor": {"form": "BGR2RGB"}}` | See [convertColor](#convertcolor). |
| `div` | `{"div": {"x": 255}}` | Divides by `x` (scalar or per channel list). Can move to the NPU. |
| `mul` | `{"mul": {"x": 255}}` | Multiplies by `x`. |
| `add` | `{"add": {"x": 128}}` | Adds `x`. |
| `subtract` | `{"subtract": {"x": 127}}` | Subtracts `x`. Can move to the NPU. |
| `normalize` | `{"normalize": {"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}}` | Computes `(x - mean) / std`. Can move to the NPU. |
| `transpose` | `{"transpose": {"axis": [2, 0, 1]}}` | Reorders axes. `[2, 0, 1]` turns HWC into CHW. After `expandDim`, use `[0, 3, 1, 2]` instead. |
| `expandDim` | `{"expandDim": {"axis": 0}}` | Adds an axis, normally the batch axis at 0. |

Less common operations (`resize2`, `resize3`, `resize_tv`, `centercrop2`, `squeeze`, `slice`, `dtype`, `pil_2_cv`) are listed in [JSON operations and their DataLoader equivalents](python-api.md#json-operations-and-their-dataloader-equivalents).

### resize

```json
{"resize": {"mode": "default", "width": 320, "height": 320, "interpolation": "LINEAR"}}
```

| `mode` | Library | `interpolation` values |
|---|---|---|
| `default` | OpenCV | `LINEAR`, `NEAREST`, `CUBIC`, `AREA`, `LANCZOS4` |
| `torchvision` | PIL | `BILINEAR`, `NEAREST`, `BICUBIC`, `LANCZOS` |

Use the uppercase names from the row of the selected `mode`. Names from the other row (for example `BILINEAR` with `default`) and lowercase names are rejected.

You can give the target size as `size` instead of `width` and `height`. With `torchvision`, `size` resizes the shorter side, like `transforms.Resize(256)`:

```json
{"resize": {"mode": "torchvision", "size": 256, "interpolation": "BILINEAR"}}
```

### convertColor

```json
{"convertColor": {"form": "BGR2RGB"}}
```

`form` values: `RGB2BGR`, `BGR2RGB`, `RGB2GRAY`, `BGR2GRAY`, `RGB2YCrCb`, `BGR2YCrCb`, `RGB2YUV`, `BGR2YUV`, `RGB2HSV`, `BGR2HSV`, `RGB2LAB`, `BGR2LAB`.

* `form` is case sensitive.
* The `*2GRAY` forms output `(H, W, 1)`, so a 1 channel NCHW model still needs `transpose` `[2, 0, 1]`.
* `convertColor` never moves into the NPU graph. It is listed under `Skipped nodes` in `compiler.log`. Your inference code must apply the same conversion.

### Preprocessing that moves to the NPU

To lower host CPU load, DX-COM can put some preprocessing operations (`div`, `subtract`, `normalize` and layout changes) into the NPU graph. It depends on the input data type and the model, so it is not guaranteed.

After compiling, look for this line in `compiler.log` (written with `--gen_log`):

```text
[INFO] - Added nodes: Div(x=255) -> Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
```

| Status in the log | What to do in your inference code |
|---|---|
| Operation listed under `Added nodes` | Remove it. The NPU does it. |
| Operation not listed | Keep it. Your host code must do it. |

```python
# Preprocessing NOT moved to the NPU:
img = img / 255.0
normalized = (img - mean) / std
output = model.run(normalized)

# Preprocessing moved to the NPU (log shows "Added nodes"):
output = model.run(img)
```

If you keep an operation that moved to the NPU, it runs twice and accuracy drops without an error.

## enhanced_scheme

Manual DXQ scheme for better accuracy. See [DXQ schemes](quantization.md#dxq-schemes) for when to use each one.

| Scheme | Form |
|---|---|
| DXQ-P0 | `{"DXQ-P0": {"alpha": 0.5}}` |
| DXQ-P1 | `{"DXQ-P1": true}` |
| DXQ-P2 | `{"DXQ-P2": {"alpha": 0.1, "beta": 1.0, "cosim_num": 2}}` |
| DXQ-P3 | `{"DXQ-P3": {"num_samples": 1024}}` (`num_samples` optional, 1024 recommended) |
| DXQ-P4 | `{"DXQ-P4": {"num_samples": 1024}}` (`num_samples` optional, 1024 recommended) |
| DXQ-P5 | `{"DXQ-P5": {"num_samples": 1024}}` (`num_samples` optional, 1024 recommended) |

```json
{
  "enhanced_scheme": {
    "DXQ-P3": {"num_samples": 1024}
  }
}
```

Do not combine with `--use_q_pro` or with `qmaster`. Not supported for multi input models.

## qmaster

Training settings for Q-Master (quantization aware training). The presence of the block switches the compile from PTQ to Q-Master. Every key is optional.

```json
{
  "qmaster": {"batch_size": 16, "train_limit": 2000, "val_limit": 200, "epochs": 10}
}
```

All keys are listed in [Q-Master parameter reference](q-master.md#parameter-reference).

## ppu

Turns on the NPU Post Processing Unit for YOLO detection models. `type` 0 is anchor based, 1 is anchor free, 2 is deprecated.

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

| Field | Type | Used by | Description |
|---|---|---|---|
| `type` | int | all | `0` anchor based, `1` anchor free, `2` DFL based CPU TopK (deprecated). |
| `conf_thres` | float | 0, 1 | Confidence threshold, fixed at compile time. |
| `num_classes` | int | all | Number of detection classes. |
| `activation` | str | 0 | Activation, normally `"Sigmoid"`. |
| `layer` | dict (type 0) or list (type 1, 2) | all | Detection head node names. |
| `topk` | int | 2 | Candidates kept before decoding. |

There are no `iou_thres` or `max_det` keys: NMS always runs on the host CPU. See [PPU for YOLO models](ppu.md) for each type and how to find the node names.

## pre_optimize

A list of `{pass_name: config}` items. DX-COM applies the passes to the ONNX model before compiling.

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
        "topk": 300
      }
    }
  ]
}
```

The tensor names are examples: look them up in your own model. See [Pre Optimize API](pre-optimize.md) for every pass and key.

!!! warning "ppu and pre_optimize together"
    DX-COM 2.5.0 does not reject a config with both. It compiles with `ppu` and drops `pre_optimize`, or fails later with an unrelated error. The only sign is the console line `falling back to legacy: ValueError: config 'pre_optimize' and 'ppu' are mutually exclusive`. Use only one.

## quantization_device (deprecated)

Ignored since DX-COM 2.5.0, with the message `UserWarning: quantization_device (JSON config) is deprecated and ignored`. Remove it from your configs. Choose the device with `--use_gpu` (Python: `use_gpu`) and pick a GPU with `CUDA_VISIBLE_DEVICES`.

## Next steps

* [Compile a model](compile-a-model.md)
* [Quantization](quantization.md)
* [Use cases](use-cases.md)
