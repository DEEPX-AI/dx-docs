---
title: DxVnpuDec
description: Reference for the dxvnpudec element, which decodes H.264 and H.265 on the DX-H1 V-NPU.
---

# DxVnpuDec

`dxvnpudec` decodes H.264 and H.265 byte streams on the DX-H1 V-NPU hardware decoder and outputs NV12 frames in host memory at the coded resolution.

## Before you start

* A DX-H1 device and the DX-H1 V-NPU SDK.
* DX-Stream built with `./build.sh --dxvnpu`. The element is in the separate `libgstdxstream-vnpu.so` plugin.

## Example

```bash
gst-launch-1.0 filesrc location=input.h264 ! h264parse ! \
  dxvnpudec ! videoconvert ! autovideosink
```

On a specific device:

```bash
gst-launch-1.0 filesrc location=input.mp4 ! parsebin ! \
  dxvnpudec device-id=0 ! videoconvert ! fakesink
```

## Behavior

* The rank is set when the plugin loads. With a V-NPU device present it is `GST_RANK_PRIMARY + 1`, so `decodebin` picks `dxvnpudec` over software decoders such as `avdec_h264`. Without a device the rank is `GST_RANK_NONE` and `decodebin` never picks it.
* Output is always NV12. Use `dxconvert` or `dxscale` afterwards.

## Pads

| Pad | Caps |
|---|---|
| sink | `video/x-h264, stream-format=byte-stream, alignment=au`; `video/x-h265, stream-format=byte-stream, alignment=au` |
| src | `video/x-raw, format=NV12` |

## Properties

| Name | Type | Default | Range | Description |
|---|---|---|---|---|
| `device-id` | int | `-1` | -1 to 127 | V-NPU device index. `-1` selects one automatically. |

## Next steps

* [DxVnpuEnc](dxvnpuenc.md)
* [DxInfer backends](dxinfer.md#behavior)
