---
title: DxTracker
description: Reference for the dxtracker element, which assigns persistent track IDs to detected objects with OC_SORT.
---

# DxTracker

`dxtracker` tracks detected objects across frames and gives each one a track ID (`DXObjectMeta._track_id`). It uses the OC_SORT algorithm ([OC_SORT repository](https://github.com/noahcao/OC_SORT)). Place it after a detection [DxPostprocess](dxpostprocess.md).

## Example

Run from the repository root:

```bash
gst-launch-1.0 urisourcebin uri=file://$PWD/dx_stream/samples/videos/boat.mp4 ! decodebin ! queue max-size-buffers=1 ! \
  dxpreprocess config-file-path=dx_stream/configs/YoloV5S_PPU/preprocess_config.json ! queue max-size-buffers=1 ! \
  dxinfer config-file-path=dx_stream/configs/YoloV5S_PPU/inference_config.json ! queue max-size-buffers=1 ! \
  dxpostprocess config-file-path=dx_stream/configs/YoloV5S_PPU/postprocess_config.json ! queue max-size-buffers=1 ! \
  dxtracker config-file-path=dx_stream/configs/tracker_config.json ! queue max-size-buffers=1 ! \
  dxosd ! videoconvert ! fpsdisplaysink sync=false
```

## Behavior

* Objects that cannot be tracked reliably are removed and not passed downstream, so the number of tracked objects is at most the number of detections.
* Without a config file, OC_SORT runs with built in defaults. With only `tracker_name` in the file, the defaults of that algorithm apply.
* Algorithm parameters can only be set in the `params` block of the JSON file, not as element properties.
* In the multi stream domain each stream gets its own OC_SORT instance and its own track ID space.

## Configuration file

`dx_stream/configs/tracker_config.json`:

```json
{
    "tracker_name": "OC_SORT",
    "params": {
        "det_thresh": 0.5,
        "max_age": 30,
        "min_hits": 3,
        "iou_threshold": 0.3,
        "delta_t": 3,
        "asso_func": "iou",
        "inertia": 0.2,
        "use_byte": false
    }
}
```

| Parameter | Value in the sample | Meaning (from OC_SORT) |
|---|---|---|
| `det_thresh` | `0.5` | Minimum detection confidence used for tracking. |
| `max_age` | `30` | Frames a track survives without a matching detection. |
| `min_hits` | `3` | Matches needed before a track is reported. |
| `iou_threshold` | `0.3` | Minimum overlap to match a detection to a track. |
| `delta_t` | `3` | Frame gap used to estimate motion direction. |
| `asso_func` | `"iou"` | Association cost function. |
| `inertia` | `0.2` | Weight of the motion direction term. |
| `use_byte` | `false` | Also match low confidence detections (ByteTrack style). |

## Pads

| Pad | Caps |
|---|---|
| sink | `video/x-raw`; `application/x-dxvideoraw` |
| src | `video/x-raw`; `application/x-dxvideoraw` |

## Properties

| Name | Type | Default | Description |
|---|---|---|---|
| `config-file-path` | string | none | JSON file with `tracker_name` and `params`. |
| `tracker-name` | string | none (OC_SORT is used) | Tracking algorithm. `OC_SORT` is the only one. |

## Next steps

* [DxOsd](dxosd.md)
* [Tracking pipeline](../pipelines.md#single-stream-with-tracking)
