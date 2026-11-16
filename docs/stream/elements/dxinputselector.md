---
title: DxInputSelector
description: Reference for the dxinputselector element, which merges several video streams into one chain ordered by PTS.
---

# DxInputSelector

`dxinputselector` merges N input streams into one output so they can share one inference chain. It always forwards the buffer with the smallest PTS. It is the entry of the [multi stream domain](multi-stream-domain.md): its output caps are `application/x-dxvideoraw`.

## Example

Two files through one detector, run from the repository root. `dxoutputselector` splits them again:

```bash
V=$PWD/dx_stream/samples/videos
gst-launch-1.0 \
  urisourcebin uri=file://$V/boat.mp4 ! decodebin ! queue ! in.sink_0 \
  urisourcebin uri=file://$V/blackbox-city-road.mp4 ! decodebin ! queue ! in.sink_1 \
  dxinputselector name=in ! \
  dxpreprocess config-file-path=dx_stream/configs/YoloV5S_PPU/preprocess_config.json ! queue ! \
  dxinfer config-file-path=dx_stream/configs/YoloV5S_PPU/inference_config.json ! queue ! \
  dxpostprocess config-file-path=dx_stream/configs/YoloV5S_PPU/postprocess_config.json ! queue ! \
  dxosd ! dxoutputselector name=out \
  out.src_0 ! queue ! videoconvert ! autovideosink \
  out.src_1 ! queue ! videoconvert ! autovideosink
```

The pipeline keeps running after both files end (see [DxOutputSelector](dxoutputselector.md#behavior)). Stop it with Ctrl+C.

## Behavior

* Buffers without a valid PTS are dropped.
* A buffer without `DXFrameMeta` gets one, with `_stream_id` set to the sink pad number.
* After every sink has its first sticky events, the element sends one domain `STREAM_START`, `CAPS` (`application/x-dxvideoraw`) and `SEGMENT`. Each input's own events are wrapped and passed along.
* `EOS` on one input is wrapped as a per stream `EOS`. The global `EOS` goes out only when all inputs reached `EOS`.
* Wrapped upstream `QoS` and `RECONFIGURE` events from `dxoutputselector` go back to the matching input.
* With two streams at the same frame rate, the merged order can drift by up to half the buffers: a buffer may arrive a few positions earlier or later than a strict interleave. This is normal for PTS based selection.

!!! warning "Elements that cannot follow DxInputSelector"
    `videoconvert`, `videoscale`, `compositor`, `dxscale`, `dxconvert` and `dxgather` do not work inside the domain. See the [placement rules](multi-stream-domain.md#placement-rules).

## Pads

| Pad | Presence | Caps |
|---|---|---|
| `sink_%u` | request | `video/x-raw` |
| `src` | always | `application/x-dxvideoraw` |

## Properties

| Name | Type | Default | Range | Description |
|---|---|---|---|---|
| `max-queue-size` | uint | `2` | 1 to max uint | Buffers per stream assumed when reporting latency (latency = `max-queue-size` times the frame duration). It does not limit any queue. |

!!! note
    `gst-inspect-1.0 dxinputselector` shows a default of 10 for `max-queue-size`, but the element starts with 2 unless you set it.

## Next steps

* [DxOutputSelector](dxoutputselector.md)
* [Multi stream pipelines](../pipelines.md#multi-stream)
