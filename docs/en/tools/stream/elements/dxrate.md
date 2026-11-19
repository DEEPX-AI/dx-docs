---
title: DxRate
description: Reference for the dxrate element, which sets the output frame rate by dropping or duplicating frames.
---

# DxRate

`dxrate` sets the frame rate of a stream to the value in `framerate`, by dropping or duplicating frames. It always writes new, evenly spaced timestamps, also when the input already has the target rate.

## Example

Limit detection output to 15 frames per second and let `dxinfer` skip frames that would be dropped:

```bash
gst-launch-1.0 urisourcebin uri=file://$PWD/dx_stream/samples/videos/boat.mp4 ! decodebin ! queue ! \
  dxpreprocess config-file-path=dx_stream/configs/YoloV5S_PPU/preprocess_config.json ! queue ! \
  dxinfer config-file-path=dx_stream/configs/YoloV5S_PPU/inference_config.json ! queue ! \
  dxrate framerate=15 throttle=true ! queue ! \
  dxpostprocess config-file-path=dx_stream/configs/YoloV5S_PPU/postprocess_config.json ! queue ! \
  dxosd ! videoconvert ! fpsdisplaysink sync=false
```

## Behavior

* Output timestamps start at the first input buffer's timestamp and follow the target rate.
* A buffer with an invalid timestamp reuses the last known timestamp; if there is none, it is dropped with a warning.
* Reverse playback (negative rate) is not supported and gives an error.
* With `throttle=true`, a Throttle QoS event goes upstream when frames are dropped. `dxinfer` reacts to it by skipping frames, so put `dxrate` downstream of `dxinfer`.
* Adds one frame duration (1 / `framerate`) to `LATENCY`.
* In the multi stream domain each stream has its own rate state.
* `framerate` changes the number of frames per second, not the playback speed.

!!! warning "framerate is required"
    The default `framerate=0` is invalid: the element posts an error when it starts. Always set it.

## Pads

| Pad | Caps |
|---|---|
| sink | `video/x-raw`; `application/x-dxvideoraw` |
| src | `video/x-raw`; `application/x-dxvideoraw` |

## Properties

| Name | Type | Default | Range | Description |
|---|---|---|---|---|
| `framerate` | uint | `0` | 0 to 10000 | Target frames per second. Must be set. |
| `throttle` | bool | `false` | | Send Throttle QoS events upstream when frames are dropped. |

## Next steps

* [DxInfer](dxinfer.md)
* [Pipelines](../pipelines.md)
