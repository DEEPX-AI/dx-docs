---
title: DxOutputSelector
description: Reference for the dxoutputselector element, which splits the merged multi stream chain back into separate streams.
---

# DxOutputSelector

`dxoutputselector` routes each buffer of the merged chain to the output pad whose index equals the buffer's `DXFrameMeta._stream_id`. It is the exit of the [multi stream domain](multi-stream-domain.md): its outputs are normal `video/x-raw` streams.

## Example

See the example on [DxInputSelector](dxinputselector.md#example). Every output pad needs its own `queue`:

```text
dxoutputselector name=out \
  out.src_0 ! queue ! videoconvert ! autovideosink \
  out.src_1 ! queue ! videoconvert ! autovideosink
```

## Behavior

* A buffer whose `stream_id` has no matching `src` pad is dropped with a warning. A buffer without `DXFrameMeta` is dropped without a warning.
* Domain events (`STREAM_START`, `CAPS` of the domain, `SEGMENT`, the final global `EOS`) stop here. Each output gets its own stream's events unwrapped instead.
* `FLUSH_START`, `FLUSH_STOP` and unwrapped `TAG` and `GAP` go to every output. A raw `RECONFIGURE` on the sink pad is ignored.
* `QoS` and `RECONFIGURE` arriving on an output are wrapped with the stream ID and sent upstream, so only that stream's source slows down. Other upstream events (`SEEK`, `NAVIGATION`) pass as they are.

!!! warning "No global EOS downstream"
    The global `EOS` is not forwarded. A `gst-launch-1.0` pipeline through `dxoutputselector` does not exit at the end of the files; stop it with Ctrl+C. In an application, end the pipeline on the per stream `EOS` of each output, on a timeout, or on another sink's `EOS`.

!!! warning "Queues are required"
    Without a `queue` on each `src` pad the pipeline can hang.

## Pads

| Pad | Presence | Caps |
|---|---|---|
| `sink` | always | `application/x-dxvideoraw` |
| `src_%u` | request | `video/x-raw` |

## Properties

Only the standard `name` property (default `dxoutputselector0`).

## Next steps

* [DxInputSelector](dxinputselector.md)
* [Multi stream pipelines](../pipelines.md#multi-stream)
