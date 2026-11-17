---
title: DxOsd
description: Reference for the dxosd element, which draws inference results on the video frame.
---

# DxOsd

`dxosd` draws the results in the metadata onto the frame: boxes, class labels and confidence, colors by track ID or class, segmentation maps, depth maps, oriented boxes, poses and face landmarks. It has no properties of its own.

## Example

```bash
gst-launch-1.0 urisourcebin uri=file://$PWD/dx_stream/samples/videos/boat.mp4 ! decodebin ! queue max-size-buffers=1 ! \
  dxpreprocess config-file-path=dx_stream/configs/YoloV5S_PPU/preprocess_config.json ! queue max-size-buffers=1 ! \
  dxinfer config-file-path=dx_stream/configs/YoloV5S_PPU/inference_config.json ! queue max-size-buffers=1 ! \
  dxpostprocess config-file-path=dx_stream/configs/YoloV5S_PPU/postprocess_config.json ! queue max-size-buffers=1 ! \
  dxosd ! queue max-size-buffers=1 ! videoconvert ! fpsdisplaysink sync=false
```

## Behavior

* Draws in place. Accepts RGB, BGR, NV12 and I420; the output format is the input format.
* Keeps `DXFrameMeta` on the output buffer, so later elements (for example `dxmsgconv`) still see the results.
* In the multi stream domain it stores the video info of each stream and draws each buffer with the right size and format.
* A buffer without `DXFrameMeta` passes through unchanged.

## Pads

| Pad | Caps |
|---|---|
| sink | `video/x-raw, format={ RGB, BGR, NV12, I420 }, width=[1, 16384], height=[1, 16384]`; `application/x-dxvideoraw` |
| src | same as sink |

## Properties

Only the standard GStreamer `name` property (default `dxosd0`).

## Next steps

* [DxMsgConv](dxmsgconv.md)
* [Pipelines](../pipelines.md)
