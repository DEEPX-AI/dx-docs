---
title: DxGather
description: Reference for the dxgather element, which merges tee branches of one source back into one stream.
---

# DxGather

`dxgather` joins branches that come from the same source, usually split with `tee` to run two secondary models in parallel, back into one stream with all results merged.

## Example

The [secondary inference pipeline](../pipelines.md#secondary-inference) uses it like this (shortened):

```text
... ! dxtracker ! tee name=t \
  t. ! queue ! dxpreprocess preprocess-id=2 ... ! dxinfer ... ! dxpostprocess ... ! queue ! gather.sink_0 \
  t. ! queue ! dxpreprocess preprocess-id=3 ... ! dxinfer ... ! dxpostprocess ... ! queue ! gather.sink_1 \
  dxgather name=gather ! queue ! dxosd ! videoconvert ! fpsdisplaysink sync=false
```

## Behavior

* Merges buffers only when their PTS match. The newest PTS among the sink pads is the reference; buffers with an older PTS are dropped with a warning.
* Assumes all branches carry the same picture. It keeps one buffer and drops the others.
* Merges `DXObjectMeta` from all branches, matched by `_meta_id`: empty fields are filled from other branches and objects that exist only in another branch are added.
* Frame level data (segmentation map, depth map, user metadata) and object user metadata are not merged; the kept buffer's values stay.
* Buffers from another source (different `_stream_id`) are dropped with a warning. Do not use `dxgather` inside the [multi stream domain](multi-stream-domain.md).

## Pads

| Pad | Presence | Caps |
|---|---|---|
| `sink_%u` | request | `video/x-raw` |
| `src` | always | `video/x-raw` |

## Properties

Only the standard `name` property (default `dxgather0`). The number of inputs is the number of requested `sink_%u` pads.

## Next steps

* [Secondary inference pipeline](../pipelines.md#secondary-inference)
* [DxOsd](dxosd.md)
