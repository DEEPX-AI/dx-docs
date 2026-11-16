---
title: Multi model graph
description: Run several models on one or more inputs from a JSON graph file with the multi model graph CLI or the dx_graph Python module, including zones, counting and events.
---

# Multi model graph

The multi model graph lets you run several models on one input from a single JSON file, with no C++ to write and nothing to rebuild.

Examples of what a graph can do: run a detector, a segmenter and a pose model side by side; crop every person a detector finds and run a re-identification model on each crop; super resolve an image and detect on the result; or add decisions such as zones, line crossing, counting and alerts.

```bash
./bin/multi_model_graph_async \
    --graph src/cpp_example/multi_model_graph/fanout_od_seg_pose.json \
    --output result.png
```

This runs a detector, a semantic segmenter and a pose model on one image and draws all three results on one picture.

## Before you start

* DX-APP is built with `./build.sh --all`, or with `./build.sh --target multi_model_graph_sync multi_model_graph_async`. The default build does not include the graph. See [Build DX-APP](build.md).
* DX-RT 3.5.0 or later. On an older runtime, a v9 `.dxnn` stops with `MODEL_LOAD`: `<file>: .dxnn container v9 needs DX-RT >= 3.5.0, but this runtime is 3.4.1. Use the v8 file (dxnn/2_4_0) or upgrade DX-RT.`
* Linux x86_64. aarch64 is compile checked only, and Windows is not tested in this release.

## Components

| Component | What it is |
|---|---|
| `bin/multi_model_graph_sync` | Runs the graph one stage at a time. The reference: slower, and the first thing to try when a result looks wrong |
| `bin/multi_model_graph_async` | Submits every node whose inputs are ready, and keeps several frames in flight. Use it for throughput |
| `dx_graph` | Python module that runs the same graphs with the same engine (see [Python](#python-dx-graph)) |
| `src/cpp_example/multi_model_graph/*.json` | 22 sample graphs |
| `run_multi_model_demo.sh` | Checks every sample graph and runs the demo scenarios |
| `docs/graph_models.md` (in the repository) | The 492 models that can run in a graph, with what each one produces and consumes |

Both binaries give the same result: their `--report` files are byte identical (without `--report-timing`).

## Run your first graph

1. Check the graph without the NPU. `--check` validates the graph and shows each node, its model and whether the `.dxnn` file is present:

    ```bash
    ./bin/multi_model_graph_sync --check src/cpp_example/multi_model_graph/fanout_od_seg_pose.json
    ```

    ```text
    OK: graph "od-seg-pose" is valid (4 nodes, 3 edges, 3 models)

    node      model                         produces   consumes   artifact
    cam       (source)                      frame      -          sample/img/sample_people.jpg
    od        yolov8-n_640x640              boxes      full_frame yolov8-n_640x640.dxnn  [present, v9]
    seg       bisenetv2_1024x2048           labelmap   full_frame bisenetv2_1024x2048.dxnn  [present, v9]
    pose      yolov8-s-pose_640x640         keypoints  full_frame yolov8-s-pose_640x640.dxnn  [present, v9]
    ```

1. Download missing models. A missing model shows as `[MISSING]` with the command to fetch it:

    ```bash
    python3 scripts/download_models.py --models yolov8-n_640x640 bisenetv2_1024x2048 yolov8-s-pose_640x640
    ```

1. Run it:

    ```bash
    # One image, result saved as an image
    ./bin/multi_model_graph_async --graph src/cpp_example/multi_model_graph/fanout_od_seg_pose.json \
        --output result.png

    # A video instead of the graph's own input, result saved as a video
    ./bin/multi_model_graph_async --graph src/cpp_example/multi_model_graph/fanout_od_seg_pose.json \
        --input assets/videos/dance-group.mov --output result.mp4

    # A camera in a window (q or ESC stops)
    ./bin/multi_model_graph_async --graph src/cpp_example/multi_model_graph/fanout_od_seg_pose.json \
        --input camera:0 --display
    ```

    The first command prints:

    ```text
    graph:  od-seg-pose (4 nodes, 3 edges)
    input:  Image file: sample/img/sample_people.jpg
    frame 0: od boxes=4 seg labelmap pose keypoints=2
    output: result.png
    1 frame, 0 failed
    ```

### Demo script

```bash
bash run_multi_model_demo.sh                         # menu
bash run_multi_model_demo.sh --check                 # check every sample graph, no NPU
bash run_multi_model_demo.sh --all                   # --check, then each scenario
bash run_multi_model_demo.sh --scenario hand_cascade
```

| Option | What it does |
|---|---|
| `--scenario <id or number>` | Run one scenario: `hand_cascade` (0), `logistics_volume` (1) or `dms` (2) |
| `--async` | Use `multi_model_graph_async` instead of `multi_model_graph_sync` |
| `--check` | Validate every sample graph, without the NPU |
| `--all` | `--check`, then each scenario with `multi_model_graph_sync` |
| `--list` | Print the scenarios and sample graphs |
| `--output-dir <dir>` | Reports and saved frames (default `reports/dev/multi_model_demo`) |
| `--models-dir <dir>` | `.dxnn` folder (default `assets/models`) |

## Sample graphs

All samples are in `src/cpp_example/multi_model_graph/`. Use them as starting points.

**Model pipelines**

| File | What it shows | Models |
|---|---|---|
| `fanout_od_seg_pose.json` | Three models in parallel on one frame | `yolov8-n_640x640`, `bisenetv2_1024x2048`, `yolov8-s-pose_640x640` |
| `fanout_od_seg_depth.json` | The same, with depth instead of pose | `yolov8-n_640x640`, `bisenetv2_1024x2048`, `fastdepth_224x224` |
| `cascade_od_reid_track.json` | Detector, a crop per person, an embedding per crop, with tracking | `yolov8-n_640x640` to `casvit-t_224x224` |
| `cascade_od_attr.json` | Detector, a crop per person, attributes | `yolov8-n_640x640` to `deepmar_resnet50_224x224` |
| `cascade_obb_cls.json` | Oriented detector, an un-rotated crop, a classifier | `yolo26-l-obb_1024x1024` to `resnet50_224x224` |
| `handoff_denoise_od.json` | Denoise, then detect on the denoised image | `dncnn-color_512x512` to `yolov5-n_640x640` |
| `handoff_sr_od_cls.json` | Super resolve x2, detect, classify each person (1) | `realesrgan-x2_192x192`, `yolov8-n_640x640`, `resnet50_224x224` |
| `chain_sr_od_pose.json` | Super resolve x2, detect, top down pose per person (1) | `realesrgan-x2_192x192`, `yolov8-n_640x640`, `vitpose-s_256x192` |
| `chain_zerodce_od_pose_emb.json` | Low light enhancement, detect, pose and embedding per person | `zerodce_400x600`, `yolov8-n_640x640`, `vitpose-s_256x192`, `casvit-t_224x224` |
| `hand_cascade.json` | Palm detector, a crop per palm, 21 hand landmarks | `mediapipe-hand-detector_192x192` to `mediapipe-hands-lite_224x224` |
| `dms_headpose.json` | Face detector, then head pose (pitch, yaw, roll) on a cpu node | `scrfd-500m_640x640` to `headpose` |
| `logistics_volume.json` | Detection, instance mask and depth in parallel, then a relative package volume on a cpu node | `yolo26-n_640x640`, `yolo26-n-seg_640x640`, `yolo26-depth-n_768x768` to `volume` |
| `multistream_od_two_sources.json` | Two sources, each its own stream, through one tracked detector and one re-id model | `yolov8-n_640x640` to `casvit-t_224x224` |

(1) Not part of the DX-M1 sample runs: with `realesrgan-x2_192x192` these graphs reach the limit of DX-M1 device memory. See [Device memory](#device-memory).

**Decision graphs (logic nodes)**

| File | What it decides |
|---|---|
| `zone_intrusion.json` | People in a restricted zone raise `intrusion` (cooldown 10 s) |
| `line_counting.json` | Tracked people crossing a line are counted per direction, with a `cross` event each |
| `ppe_zone_check.json` | People in a zone are cropped for attributes; one without a hat raises `no_hat` |
| `loitering_dwell.json` | Time each tracked person stays in a zone; `dwell` after 5 s |
| `zone_people_count.json` | People counted in two zones |
| `gallery_known_person.json` | Each person's re-id embedding is named after the nearest gallery entry, or `unknown` |
| `driver_attention.json` | Head pose raises `looking_away` (yaw beyond 30 degrees either way) or `head_down` (pitch below minus 20 degrees) |
| `multistream_people_count.json` | People counted per stream; `crowded` in a stream with 5 or more |
| `logistics_volume_alert.json` | The summed package volume raises `load_high` above 100 (relative: tune per camera) |

The decision graphs ship with a sample image, but their scenes are videos. Run them with, for example, `--input assets/videos/person-pair-hallway.mp4 --loop --display`.

**Changing a model is a text edit.** To use another detector in `cascade_od_reid_track.json`, change `"model": "yolov8-n_640x640"` to `"model": "yolo26-s_640x640"`, download the model and run the same binary:

```bash
python3 scripts/download_models.py --models yolo26-s_640x640
./bin/multi_model_graph_async --graph src/cpp_example/multi_model_graph/cascade_od_reid_track.json \
    --output swapped.png
```

Any model whose `produces` and `consumes` fit the slot works. `--check` tells you before the run.

## Write a graph

A graph is a strict JSON file (no comments) with `version`, `name`, `nodes` and `edges`. This is `cascade_od_reid_track.json`: a detector finds people, each person is cropped, and a re-identification model computes an embedding per crop.

```json
{
  "version": 1,
  "name": "person-reid",
  "nodes": [
    { "id": "cam",  "type": "source", "uri": "sample/img/sample_people.jpg" },
    { "id": "od",   "model": "yolov8-n_640x640",
      "params": { "score_threshold": 0.35 },
      "track":  { "algo": "iou", "iou": 0.3, "max_age": 30 } },
    { "id": "reid", "model": "casvit-t_224x224" }
  ],
  "edges": [
    { "from": "cam", "to": "od" },
    { "from": "od",  "to": "reid",
      "roi": { "classes": ["person"], "pad": 0.05, "max": 16 } }
  ]
}
```

| Key | Meaning |
|---|---|
| `version` | Always `1` in this release |
| `name` | Free text, shown in messages and in `--report` |
| `nodes[].id` | The node name, used by edges and in every message |
| `nodes[].params` | Overrides the model's `config.json` for this node only |
| `nodes[].track` | Gives each box the node outputs a track id |
| `nodes[].engine` | Device memory settings (see [Device memory](#device-memory)) |
| `edges[].roi` | Makes the edge a crop edge: the consumer runs once per box |

A model is named by its variant (the `.dxnn` stem). An old registry name such as `yolov8n` still works; `--check` and the run print a note naming the variant.

### Nodes

| Kind | Written as | Meaning |
|---|---|---|
| source | `{ "id": "cam", "type": "source", "uri": "..." }` | Where frames come from: an image, a video, `camera:0` or an `rtsp://` URL. A relative `uri` is read from the current folder if it exists there, else from the repository root. `--input` replaces it |
| model | `{ "id": "od", "model": "yolov8-n_640x640" }` | One registered model. A model node has no `"type"` |
| cpu | `{ "id": "hp", "type": "cpu", "op": "headpose" }` | A fixed CPU computation: `headpose` (pitch, yaw, roll from five face landmarks) or `volume` (relative package volume from boxes, masks and depth) |
| logic | `{ "id": "zone", "type": "logic", "op": "zone", "params": { } }` | A decision: `filter`, `zone`, `line`, `count`, `dwell`, `condition`, `gallery` or `user` |

### Edges

| Kind | Written as | The consumer receives |
|---|---|---|
| frame | `{ "from": "cam", "to": "od" }` | The whole frame, or the image the producer made |
| ROI | `{ "from": "od", "to": "reid", "roi": { } }` | One cropped region per box. The consumer runs once per crop |
| result | `{ "from": "face", "to": "hp", "carry": "result" }` | The producer's result. The consumer must be a cpu or logic node |

Every model `produces` one shape (`boxes`, `obboxes`, `instances`, `keypoints`, `labelmap`, `densemap`, `image`, `scores`, `vector`) and `consumes` a `frame`, a `roi` or `either`. The rules:

* A frame edge from a model is allowed only when the producer outputs an `image` (denoising, low light enhancement, super resolution). The consumer then runs on that image (image hand off), and results are mapped back to the source frame for drawing.
* An ROI edge needs a producer of `boxes`, `obboxes` or `instances`, and a consumer of `roi` or `either`.
* A node cannot receive both a full frame and ROI crops. Split it into two nodes.
* Two edges cannot share the same `from` and `to`, and the graph must have no cycle.
* Two sources feeding one node are two streams, not two inputs (see [Several sources](#several-sources)).

### ROI options

All options are optional; `"roi": {}` crops every box as it is.

| Key | Meaning | Default |
|---|---|---|
| `classes` | Keep only these class names, for example `["person"]` | All classes |
| `min_score` | Confidence floor, 0 to 1 (`0.35`, not `35`) | The producer's threshold |
| `min_area` | Pixel area floor, checked on the box and again on the crop | `0` |
| `pad` | Grow each box by this fraction of its size on every side, 0 to 1 | `0` |
| `max` | Keep at most this many boxes, highest score first | No limit |
| `align` | `"face5"`: align the crop from five face landmarks (face detectors only) | None |

The options apply in this order: class, score and area filter, `max`, tracking, `pad` and clipping, alignment (or un-rotation of an oriented box), then the crop. Every result is drawn in source frame coordinates. In `--report`, a result keeps the coordinates of the crop it ran on, with `origin.inv_align` (a 2x3 affine) and `origin.src_box` to map it back. Logic nodes always work in source frame pixels.

### Tracking

`"track"` on a detector node gives every box a `track_id` that follows the object across frames. Every consumer of its boxes sees the same ids. `"track": {}` uses the defaults.

| Key | Meaning | Default |
|---|---|---|
| `algo` | The tracker. `"iou"` is the only one | `"iou"` |
| `iou` | Overlap a box needs to continue a track, above 0 and at most 1 | `0.3` |
| `max_age` | Frames an unmatched track survives (0 or more) | `30` |

Tracking runs in frame order, so in `multi_model_graph_async` a tracked node adds some latency but no throughput cost.

### Parameters

A node's `"params"` overrides the model settings for that node only, so one model can appear twice with two thresholds:

```text
factory defaults  <  <task>/<family>/<variant>/config.json  <  node "params"
```

Values are numbers (`score_threshold`, `nms_threshold`, ...), or strings and string arrays for text keys such as `class_names`. `class_names` renames a model's classes for one node:

```json
{ "id": "od", "model": "yolov8-n_640x640", "params": { "class_names": ["pedestrian"] } }
```

### Device memory

Every model node opens its own engine on the NPU, even two nodes with the same model. A graph that does not fit fails while loading, with `MODEL_LOAD` on the first node that does not fit. Two `"engine"` settings lower the memory a graph needs:

```json
{ "id": "od",  "model": "yolov8-n_640x640", "engine": { "share": true, "buffers": 2 } },
{ "id": "od2", "model": "yolov8-n_640x640", "engine": { "share": true, "buffers": 2 } }
```

* `"share": true`: all nodes with it and the same model use one engine. They must have the same `params` and `buffers`. Results do not change.
* `"buffers": N` (1 to 100): how many inputs DX-RT keeps in flight for the model (DX-RT default 6). Most device memory is this pool, so 2 buffers need about a third. Fewer buffers can lower async throughput; results do not change.

## Decision logic

Logic nodes run on the CPU once per frame and read their inputs on `"carry": "result"` edges.

| Op | Reads | Main params | Outputs | Events |
|---|---|---|---|---|
| `filter` | boxes | `classes`, `min_score`, `min_area` | The boxes it keeps | None |
| `zone` | boxes | `polygon` (required), `mode` (`inside` or `outside`), `anchor` (`bottom` or `center`) | The boxes in the region | `enter`, `exit` (tracked boxes only) |
| `line` | tracked boxes | `line` (required), `direction` (`both`, `in` or `out`) | Counts `in`, `out`, `total` | `cross` |
| `count` | 1 to 8 box inputs | `classes` | A total and a count per class | None |
| `dwell` | tracked boxes | `threshold_s` (default 10), `grace_s` (default 1) | Seconds per track | `dwell` |
| `condition` | boxes, records, or per crop scores or vectors | `value`, `comparator`, `threshold`, `reduce`, `cooldown_s`, `event` | `value`, `active` | Its `event` |
| `gallery` | embeddings | `gallery` (required), `threshold` (default 0.5), `events` (`known`, `all` or `none`) | A name per crop, or `unknown` | `match`, and `unknown` with `"events": "all"` |
| `user` | any one input | `name`, `input`, `output` | Its input, unchanged | None |

* **Coordinates** are fractions of the frame, 0 to 1, so one graph fits any resolution: `"polygon": [x0, y0, x1, y1, ...]` (at least 3 points), `"line": [x0, y0, x1, y1]`.
* **Track ids** come from a detector's `"track"`. `line` and `dwell` need them. `--check` names the detector to add `"track"` to.
* **`condition`** raises its event when the comparison becomes true. With `cooldown_s` above 0, it raises it again at most every `cooldown_s` seconds while the comparison holds.
* **`gallery`** compares embeddings with a gallery file you build once from a folder of images: `python3 scripts/build_gallery_database.py --variant <model> --images <folder> --out <file>.bin`.
* **`user`** passes its input through. In an exported project it becomes a C++ function you write (see [Standalone project](#standalone-project)).
* `--list-ops` lists every logic and cpu op; `--list-ops --json` adds events and parameters with types, defaults and ranges.

`zone_intrusion.json` raises `intrusion` when a person stands in the lower right part of the frame:

```json
{
  "version": 1,
  "name": "zone-intrusion",
  "nodes": [
    { "id": "cam",    "type": "source", "uri": "sample/img/sample_people.jpg" },
    { "id": "od",     "model": "yolov8-n_640x640",
      "params": { "score_threshold": 0.35 },
      "track":  { "algo": "iou", "iou": 0.3, "max_age": 30 } },
    { "id": "person", "type": "logic", "op": "filter", "params": { "classes": ["person"] } },
    { "id": "zone",   "type": "logic", "op": "zone",
      "params": { "polygon": [0.45, 0.35, 1.0, 0.35, 1.0, 1.0, 0.45, 1.0] } },
    { "id": "alarm",  "type": "logic", "op": "condition",
      "params": { "value": "count", "comparator": ">", "threshold": 0,
                  "cooldown_s": 10, "event": "intrusion" } }
  ],
  "edges": [
    { "from": "cam",    "to": "od" },
    { "from": "od",     "to": "person", "carry": "result" },
    { "from": "person", "to": "zone",   "carry": "result" },
    { "from": "zone",   "to": "alarm",  "carry": "result" }
  ]
}
```

Events are printed after the frame line, written one JSON object per line to `--events <file>`, and included in `--report`:

```text
frame 0: od boxes=3 person boxes=2 zone boxes=1 alarm records=1 value=1 active=1
[EVENT] {"frame":0,"time":0,"stream":"cam","node":"zone","event":"enter","track_id":1,"data":{"count":1}}
[EVENT] {"frame":0,"time":0,"stream":"cam","node":"alarm","event":"intrusion","track_id":1,"data":{"value":1,"threshold":0,"track_ids":"1"}}
```

On the picture, zones are tinted, lines have an arrow toward their `in` side, counts and conditions appear in a panel at the top left, and the last five events are listed in a corner.

!!! note "Lines have no hysteresis"
    A box whose anchor moves back and forth across a line counts a crossing each time. Place a line where people walk through, not where they stand.

## Several sources

A graph can have several source nodes. Each source is its own stream: the models are loaded once and shared, but every stream has its own frames, tracks, logic state and output.

```bash
./bin/multi_model_graph_async \
    --graph src/cpp_example/multi_model_graph/multistream_od_two_sources.json \
    --input cam1=camera:0 --input cam2=assets/videos/dance-group.mov \
    --output run.avi --frames 300
```

* `--input <source_id>=<uri>` replaces one source's `uri`. With several sources the `<source_id>=` form is required.
* `--output run.avi` writes one video per stream: `run_cam1.avi`, `run_cam2.avi`.
* `--display` shows one window with a grid of the streams.
* `--frames N` stops after N frames of each stream.
* Every frame in `--report` and every event names its `stream`.

## Command line options

| Option | Default | What it does |
|---|---|---|
| `--graph <file>` | None | The graph to run |
| `--input [<source>=]<uri>` | Each source's `uri` | An image, a video, `camera:<N>` or `rtsp://...`. Repeat once per source |
| `--output <file>` | None | The rendered result. `.mp4`, `.avi` or `.mkv` write a video (Windows: `.mp4` or `.avi` only). Other extensions write images (`<stem>_<index><ext>` per frame of a video). A camera or RTSP source with image output needs `--frames N` |
| `--display` | Off | Show each frame in a window; `q` or ESC stops. Needs a desktop session |
| `--draw <id,...>` | Every node | Draw only these nodes; every node still runs and reports |
| `--report <file>` | None | Every frame's results as JSON |
| `--report-timing` | Off | With `--report`: add the time per node |
| `--events <file>` | None | Every logic node event, one JSON object per line |
| `--output-layers <dir>` | None | Per frame, the clean frame and each node's drawing as transparent PNGs, with `layers.json`. A video, camera or RTSP source needs `--frames N` |
| `--model-dir <dir>` | `assets/models` | Where the `.dxnn` files are |
| `--frames <N>` | All | Stop after N frames of each stream |
| `--loop` | Off | Restart a video at its end, until Ctrl+C, `q`, ESC or `--frames N` |
| `--max-inflight <N>` | `16` | Frames in flight (async only) |
| `--max-jobs-per-stage <N>` | `0` (no limit) | Jobs one stage may have outstanding (async only) |
| `--stall-timeout-ms <N>` | `0` (wait forever) | Fail when work is outstanding and nothing completes for N ms (async only) |
| `--check [<file>]` | None | Validate the graph and list its models without the NPU, then exit |
| `--list-models` | None | List the models; filter with `--consumes <roi, frame or either>` and `--produces <shape>` |
| `--list-ops` | None | List the logic and cpu ops |
| `--json` | Off | With `--check`, `--list-models` or `--list-ops`: print JSON |
| `--help` | None | Show usage |

Exit codes: `0` success, `1` the graph or its models cannot run or a frame failed, `2` a usage error.

Ctrl+C or SIGTERM stops gracefully: frames in flight finish and `--report` and `--output` are finalized. A second Ctrl+C more than 200 ms later ends the process at once. If a run may be killed, write `.avi` rather than `.mp4`, which cannot be played without its closing index.

`DXAPP_PROGRESS=1` prints a `[PROGRESS] frames=N fps=F avg_fps=A node_ms=<id>:<ms>,...` line about once a second.

## Check and troubleshoot

**Validate before running.** `--check` names any missing `.dxnn` file without failing, so you can check a graph before downloading its models. It fails on a file that cannot be loaded, such as a v9 file on DX-RT older than 3.5.0. Whether all models fit in device memory shows only when they load.

**Find a model for a slot.** `--list-models` answers which model can go where:

```bash
./bin/multi_model_graph_async --list-models --consumes roi --produces scores
```

The `file` column shows whether the model is downloaded (`v8`, `v9`, `missing`) and `ready` whether the graph engine can run it.

**Error messages** have this form:

```text
ERROR [CODE] <where>: <what>
  -> <how>
```

| Code | When |
|---|---|
| `GRAPH_SCHEMA` | Malformed JSON, a wrong type, a missing or unknown key, or a value out of range |
| `GRAPH_EDGE` | The shapes of an edge do not fit (for example `"seg" produces labelmap, not boxes` on an ROI edge), or a logic node's inputs are wrong |
| `GRAPH_ALIGN` | `"align": "face5"` from a producer without face landmarks |
| `GRAPH_CYCLE`, `GRAPH_ORPHAN` | The graph has a cycle, or a node no source reaches |
| `GRAPH_VERSION`, `GRAPH_RESERVED` | An unsupported `version`, or something reserved for a later release (the `"prompt"` key, `"type": "fuse"`) |
| `MODEL_UNKNOWN` | The model name is not registered; the message suggests the closest name |
| `MODEL_NOT_READY` | The model is registered but cannot run in a graph (the anomaly detection models) |
| `MODEL_MISSING` | The `.dxnn` file is not in `--model-dir`; the message gives the download command |
| `MODEL_LOAD` | The file is present but cannot be loaded: device memory, device state, or a v9 file on DX-RT older than 3.5.0 |

**A run that finds nothing says why.** When an ROI edge produces no crops although its producer found boxes (for example `"classes": ["persons"]` when the detector emits `person`), the run prints a warning with the filter and the classes the producer actually emitted.

## Python: dx_graph { #python-dx-graph }

`dx_graph` runs the same graph files from Python. It links the same engine as the CLI, so reports, pictures and error messages are the same.

1. Build it for the Python you will use:

    ```bash
    /path/to/python -m pip install pybind11 numpy
    ./build.sh --all --python_exec /path/to/python
    ```

1. Use it from `bin/python`:

    ```python
    import dx_graph

    with dx_graph.Graph("src/cpp_example/multi_model_graph/cascade_od_reid_track.json") as g:
        for report in g.stream(source="my_video.mp4"):   # like --input, pipelined like the async CLI
            d = report.to_dict()                         # this frame's --report entry
            canvas = g.render(report)                    # this frame's --output image (numpy, BGR)
    ```

    ```bash
    PYTHONPATH=bin/python python3 my_script.py
    ```

### API

`dx_graph.Graph(path, model_dir=None, executor="async", max_frames_in_flight=16, max_jobs_per_stage=0, stall_timeout_ms=0)` parses, validates and builds the graph and loads every model. It raises `dx_graph.GraphError` where the CLI would exit 1 before running. It is a context manager; `close()` releases everything.

| Argument | CLI equivalent | Notes |
|---|---|---|
| `path` | `--graph` | The graph JSON |
| `model_dir` | `--model-dir` | Default `<repo>/assets/models` |
| `executor` | The binary | `"async"` or `"sync"` |
| `max_frames_in_flight` | `--max-inflight` | Async only; at least 1 |
| `max_jobs_per_stage` | `--max-jobs-per-stage` | Async only; 0 means no limit |
| `stall_timeout_ms` | `--stall-timeout-ms` | Async only; raises `RuntimeError` on a stall; 0 waits forever |

| Member | What it does |
|---|---|
| `g.run(frame, stream=None)` | Runs one frame (a `uint8` BGR numpy array of shape `(H, W, 3)`, as `cv2.imread` returns) and returns a `Report`. With several sources, `stream` names the source |
| `g.stream(frames=None, *, source=None, sources=None, limit=None)` | Yields a `Report` per frame, pipelined. With no `frames`, the graph reads its own sources; `source=` replaces the one source like `--input`; `sources={"cam1": uri, ...}` for several sources; `frames=` takes numpy frames (or `(source_id, frame)` pairs); `limit` is `--frames` |
| `g.render(report)` | The `--output` image for that report, drawn on the report's own frame |
| `g.streams` | The source node ids, in order |
| `g.executor`, `g.options` | The executor in use and its options |

| `Report` member | Meaning |
|---|---|
| `frame_index` | The frame index in its stream |
| `stream` | The source node id |
| `error` | `""` when every stage succeeded, else the first error |
| `frame` | A copy of the frame |
| `to_dict(arrays=True)` | This frame's `--report` entry; with `arrays=True`, dense data also comes as numpy arrays under `<key>_array` |

`dx_graph.GraphError` is a `ValueError` with `.code` set to the CLI error code (for example `"MODEL_LOAD"`). Every `run()` and `stream()` starts with fresh trackers. One thread may use a `Graph` at a time.

Limits: `dx_graph` is not on PyPI (use it from `bin/python`), has no Windows build, cannot build or edit graphs or add Python stages, and has no SIGTERM handler.

## Standalone project

`scripts/export_graph_project.py` writes a graph as a CMake project that builds and runs wherever the DEEPX runtime is installed. It needs only the DEEPX runtime, CMake, a C++17 compiler and OpenCV 4, and gives the same events and picture as `multi_model_graph_async`.

```bash
python3 scripts/export_graph_project.py --graph my_graph.json --out ~/my_graph
cd ~/my_graph && ./setup.sh && ./run.sh      # writes results/result.jpg and results/events.jsonl
```

| Option | What it does |
|---|---|
| `--name <name>` | Project and program name (default: the graph `name`) |
| `--no-models` | Leave out the `.dxnn` files; the project's `setup.sh` downloads them |
| `--model-dir <dir>` | Where the `.dxnn` files are (default `assets/models`) |
| `--dry-run` | Write nothing; with `--json`, print what would be exported and its size |

A `user` logic node becomes a C++ class in `user_logic/<name>.cpp` with a `Run()` stub. Edit it and rebuild with `cmake --build build`.

## Limits in this release

| Item | Status |
|---|---|
| Anomaly detection | The four models cannot run in a graph (`MODEL_NOT_READY`) |
| 3D and LiDAR models | Rejected: every source is a camera frame |
| Text prompts and model fusion | Reserved, rejected with `GRAPH_RESERVED` |
| CLIP prompt scores | Not a graph node; a CLIP image model outputs its embedding |
| SuperPoint tracks | Not in a graph; the `descriptors` output is available |
| DnCNN image hand off | The denoised image stays at 512x512 |
| `handoff_sr_od_cls.json`, `chain_sr_od_pose.json` | Not part of the DX-M1 sample runs (device memory) |
| Windows, aarch64 | Not tested on Windows; aarch64 is compile checked only |

## Next steps

* [Model catalog](models.md): pick models for your graph.
* [Run the examples](run-examples.md): the single model examples.
* [Architecture](architecture.md): where the graph engine lives in the source tree.
