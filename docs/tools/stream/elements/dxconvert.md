---
title: DxConvert
description: Reference for the dxconvert element, which converts frames between NV12, I420, RGB and BGR.
---

# DxConvert

`dxconvert` converts frames between NV12, I420, RGB and BGR (all 16 combinations). The output format comes from caps negotiation; the element has no properties. It uses the best available transform backend, and combinations no hardware backend supports run on libyuv.

## Example

NV12 to RGB:

```bash
gst-launch-1.0 urisourcebin uri=file://$PWD/dx_stream/samples/videos/boat.mp4 ! decodebin ! videoconvert ! \
  video/x-raw,format=NV12 ! \
  dxconvert ! video/x-raw,format=RGB ! \
  videoconvert ! autovideosink
```

Convert to RGB before inference (`dxpreprocess` accepts RGB, I420 and NV12, not BGR):

```bash
gst-launch-1.0 urisourcebin uri=file://$PWD/dx_stream/samples/videos/boat.mp4 ! decodebin ! videoconvert ! \
  video/x-raw,format=I420 ! \
  dxconvert ! video/x-raw,format=RGB ! \
  dxpreprocess preprocess-id=1 resize-width=640 resize-height=640 ! \
  dxinfer preprocess-id=1 inference-id=1 model-path=$PWD/dx_stream/samples/models/yolo26-n_640x640.dxnn ! \
  fakesink
```

To give the model a BGR tensor, set `color-format=1` on `dxpreprocess`; the input caps do not matter for that.

## Behavior

* Same input and output format: frames pass through unchanged.
* No scaling; input and output size are equal. Use [DxScale](dxscale.md) to scale.
* Do not place it after `dxinputselector`; convert each stream before it or each output after `dxoutputselector`.

## Pads

| Pad | Caps |
|---|---|
| sink | `video/x-raw, format={ NV12, I420, RGB, BGR }` |
| src | `video/x-raw, format={ NV12, I420, RGB, BGR }` |

## Properties

None besides the standard `name`.

## Next steps

* [DxScale](dxscale.md)
* [DxPreprocess](dxpreprocess.md)
