---
title: DxVnpuEnc
description: Reference for the dxvnpuenc element, which encodes NV12 frames to H.264 or H.265 on the DX-H1 V-NPU.
---

# DxVnpuEnc

`dxvnpuenc` encodes NV12 frames to H.264 or H.265 on the DX-H1 V-NPU hardware encoder.

## Before you start

* A DX-H1 device and the DX-H1 V-NPU SDK.
* DX-Stream built with `./build.sh --dxvnpu`.

## Example

Encode a file to H.264 (`videoconvert` makes sure the input is NV12):

```bash
gst-launch-1.0 filesrc location=input.mp4 ! decodebin ! videoconvert ! \
  video/x-raw,format=NV12 ! \
  dxvnpuenc codec=h264 bitrate=8000 ! \
  h264parse ! mp4mux ! filesink location=output.mp4
```

Transcode H.265 to H.264 on the V-NPU:

```bash
gst-launch-1.0 filesrc location=input.h265 ! h265parse ! \
  dxvnpudec ! dxvnpuenc codec=h264 bitrate=4096 ! \
  h264parse ! filesink location=output.h264
```

## Behavior

* Accepts NV12 only. Convert other formats with `dxconvert` first.
* With a V-NPU device present the rank is `GST_RANK_PRIMARY + 1`, so `encodebin` picks it over software encoders such as `x264enc`. Without a device the rank is `GST_RANK_NONE`.
* When `encodebin` picks it, you cannot set `codec` or `bitrate`; it uses H.264 at 4096 kbps. Add `dxvnpuenc` to the pipeline yourself for other settings.

## Pads

| Pad | Caps |
|---|---|
| sink | `video/x-raw, format=NV12` |
| src | `video/x-h264, stream-format=byte-stream, alignment=au`; `video/x-h265, stream-format=byte-stream, alignment=au` |

## Properties

| Name | Type | Default | Range | Description |
|---|---|---|---|---|
| `codec` | enum | `h264` | `h264`, `h265` | Output codec. |
| `bitrate` | uint | `4096` | 1 to 100000 | Target bitrate in kbps. |
| `device-id` | int | `-1` | -1 to 127 | V-NPU device index. `-1` selects one automatically. |

## Next steps

* [DxVnpuDec](dxvnpudec.md)
* [DxConvert](dxconvert.md)
