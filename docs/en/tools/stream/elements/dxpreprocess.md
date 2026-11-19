---
title: DxPreprocess
description: Reference for the dxpreprocess element, which turns frames or object regions into input tensors for dxinfer.
---

# DxPreprocess

`dxpreprocess` turns a raw video frame, or each detected object in it, into an input tensor for [DxInfer](dxinfer.md). It stores the tensor under the ID in `preprocess-id`; the `dxinfer` with the same `preprocess-id` uses it. Several `dxpreprocess` elements can run in one pipeline, for example for secondary models.

## Example

Run from the repository root after `./setup.sh`:

```bash
gst-launch-1.0 urisourcebin uri=file://$PWD/dx_stream/samples/videos/boat.mp4 ! decodebin ! queue ! \
  dxpreprocess preprocess-id=1 resize-width=640 resize-height=640 keep-ratio=true pad-value=114 ! queue ! \
  dxinfer preprocess-id=1 inference-id=1 model-path=$PWD/dx_stream/samples/models/yolo26-n_640x640.dxnn ! queue ! \
  fakesink
```

## Behavior

* **Primary mode** (default): preprocesses the whole frame, or the `roi` area of it.
* **Secondary mode** (`secondary-mode=true`): preprocesses each object from upstream detection. Only objects fully inside `roi`, of class `target-class-id` (or all classes with `-1`) and at least `min-object-width` by `min-object-height` are used.
* **Resize**: to `resize-width` by `resize-height`. With `keep-ratio=true` the aspect ratio is kept and the rest is padded with `pad-value` (same value for R, G and B).
* **Color**: `color-format` sets the tensor color order, `0` RGB or `1` BGR. This is independent of the input caps: an NV12 video can produce a BGR tensor.
* **Interval**: `interval=N` skips N frames (or objects) between two preprocessed ones.
* **QoS**: when the sink has `sync=true`, late buffers are dropped to stay real time.
* **Shared buffers**: when a buffer is shared (for example after `tee`), the element copies it before writing.
* **Hardware**: color conversion and resize use the best transform backend (see [Elements](index.md#hardware-backends-for-transforms)).
* **Multi stream**: in the domain, size and stream ID come from `DXFrameMeta`; outside, size comes from caps and `stream_id` is `0`.

### Custom preprocess function

Set `library-file-path` and `function-name` to call your own function. The function writes into a tensor buffer that DX-Stream allocates from `resize-width` and `resize-height`; do not free or reallocate it. `object_meta` is `nullptr` in primary mode.

```cpp
extern "C" bool PreProcess(GstBuffer *buf,
                           DXFrameMeta *frame_meta,
                           DXObjectMeta *object_meta,
                           void *output);
```

See [Write an application](../write-an-application.md#custom-preprocess-library) for building it and for the error rules.

## Pads

| Pad | Caps |
|---|---|
| sink | `video/x-raw, format={ RGB, I420, NV12 }`; `application/x-dxvideoraw` |
| src | `video/x-raw, format={ RGB, I420, NV12 }`; `application/x-dxvideoraw` |

BGR input is not accepted. Convert it with `dxconvert` or `videoconvert` first.

## Properties

| Name | Type | Default | Range | Description |
|---|---|---|---|---|
| `config-file-path` | string | none | | JSON file with any of the properties below. |
| `preprocess-id` | uint | `0` | 0 to 10000 | ID of the produced tensor. Must match `dxinfer preprocess-id`. |
| `resize-width` | uint | `0` | 0 to 10000 | Tensor width. |
| `resize-height` | uint | `0` | 0 to 10000 | Tensor height. |
| `keep-ratio` | bool | `true` | | Keep the aspect ratio and pad. |
| `pad-value` | uint | `0` | 0 to 255 | Padding value for R, G and B. |
| `color-format` | uint | `0` | 0 to 1 | Tensor color order: `0` RGB, `1` BGR. |
| `secondary-mode` | bool | `false` | | Preprocess each object instead of the frame. |
| `target-class-id` | int | `-1` | -1 to 10000 | Secondary mode: only this class. `-1` means all. |
| `min-object-width` | uint | `0` | 0 to 10000 | Secondary mode: minimum object width. |
| `min-object-height` | uint | `0` | 0 to 10000 | Secondary mode: minimum object height. |
| `roi` | string | `"-1,-1,-1,-1"` | | Region `x1,y1,x2,y2`. `-1` values mean the full frame. |
| `interval` | uint | `0` | 0 to 10000 | Frames or objects to skip between two preprocessed ones. |
| `transpose` | bool | `false` | | Transpose the axes of the output tensor. |
| `library-file-path` | string | none | | Custom preprocess library (`.so`). |
| `function-name` | string | none | | Function to call in that library. |

JSON example (`dx_stream/configs/YoloV5S_PPU/preprocess_config.json`):

```json
{
    "preprocess_id": 1,
    "resize_width": 640,
    "resize_height": 640,
    "keep_ratio": true,
    "pad_value": 114,
    "interval": 0
}
```

## Next steps

* [DxInfer](dxinfer.md)
* [Secondary inference pipeline](../pipelines.md#secondary-inference)
