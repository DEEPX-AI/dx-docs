---
title: DxScale
description: Reference for the dxscale element, which scales video frames with the best available hardware backend.
---

# DxScale

`dxscale` scales video frames to `width` by `height`. It keeps the pixel format (NV12, I420, RGB or BGR) and uses the best available transform backend (see [Elements](index.md#hardware-backends-for-transforms)).

## Example

```bash
gst-launch-1.0 urisourcebin uri=file://$PWD/dx_stream/samples/videos/boat.mp4 ! decodebin ! videoconvert ! \
  video/x-raw,format=I420 ! \
  dxscale width=640 height=480 ! \
  videoconvert ! autovideosink
```

## Behavior

* With `width=0` and `height=0` (default) frames pass through unchanged.
* Set both values. If only one is set, the element does not fail but silently passes frames through.
* No color conversion; use [DxConvert](dxconvert.md) for that.
* Do not place it after `dxinputselector`: it needs stable caps. Scale each stream before `dxinputselector` or each output after `dxoutputselector`.

## Pads

| Pad | Caps |
|---|---|
| sink | `video/x-raw, format={ NV12, I420, RGB, BGR }` |
| src | `video/x-raw, format={ NV12, I420, RGB, BGR }` |

## Properties

| Name | Type | Default | Range | Description |
|---|---|---|---|---|
| `width` | uint | `0` | 0 to 8192 | Output width. `0` means pass through. |
| `height` | uint | `0` | 0 to 8192 | Output height. `0` means pass through. |

## Next steps

* [DxConvert](dxconvert.md)
* [Multi stream pipelines](../pipelines.md#multi-stream)
