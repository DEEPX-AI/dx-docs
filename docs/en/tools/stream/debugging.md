---
title: Debugging and troubleshooting
description: Turn on DX-Stream debug logs, and fix common display, build, multi stream and message broker problems.
---

# Debugging and troubleshooting

This page shows you how to get debug logs from DX-Stream elements and how to fix the problems users meet most often.

## Debug logs with GST_DEBUG

Every DX-Stream element logs to its own GStreamer debug category. Set `GST_DEBUG` before any `gst-launch-1.0` command or your app. In the examples, `PIPELINE` stands for your pipeline description.

```bash
GST_DEBUG=dx*:4 gst-launch-1.0 PIPELINE
GST_DEBUG=2,dxinfer:5,dxpreprocess:5 gst-launch-1.0 PIPELINE
GST_DEBUG=dx*:4 GST_DEBUG_FILE=/tmp/debug.log GST_DEBUG_NO_COLOR=1 gst-launch-1.0 PIPELINE
```

| Level | Name | Use |
|---|---|---|
| 0 | NONE | No output |
| 1 | ERROR | Failures that stop the element |
| 2 | WARNING | Problems that may change behavior |
| 3 | FIXME | Rarely used |
| 4 | INFO | State changes, loaded configuration |
| 5 | DEBUG | Detailed operation |
| 6 | LOG | One line per buffer |
| 7 | TRACE | Internal details, for example each inference request |

Categories:

| Category | Covers |
|---|---|
| `dxpreprocess`, `dxinfer`, `dxpostprocess`, `dxtracker`, `dxosd`, `dxrate`, `dxgather`, `dxinputselector`, `dxoutputselector`, `dxscale`, `dxconvert`, `dxmsgconv`, `dxmsgbroker`, `dxvnpudec`, `dxvnpuenc` | One per element |
| `dxmeta` | Frame, object, message and user metadata |
| `transform_kernel` | libyuv, RGA and V3 DSP kernels, backend choice and fallback to libyuv |
| `inference_backend` | DX-RT backend start, inference requests (TRACE) and timeouts |
| `broker` | MQTT and Kafka client code |

List the categories your build has:

```bash
gst-launch-1.0 --gst-debug-help | grep -E "dx|transform_kernel|inference_backend|broker"
```

Useful messages (level in brackets):

| Goal | Command filter | Message |
|---|---|---|
| Inference speed | `GST_DEBUG=dxinfer:5` and `grep "Inference throughput"` | `Inference throughput: <fps> fps, latency: ...` (5) |
| Config loaded | `GST_DEBUG=dxinfer:4` and `grep "Config loaded"` | `Config loaded: model=..., preproc_id=..., infer_id=...` (4) |
| Dropped frames | `GST_DEBUG=dxpreprocess:5,dxinfer:6` and `grep Dropping` | `Dropping buffer due to QoS` (preprocess 5, infer 6), `Dropping buffer due to throttling` (infer 6) |
| Throttling events | `GST_DEBUG=dxinfer:5` and `grep QoS` | `QoS THROTTLE event`, `QoS UNDERFLOW event` (5) |
| Buffer flow | `GST_DEBUG=dx*:6` and `grep "Processing buffer"` | `Processing buffer: pts=...` (6) |
| Tracking | `GST_DEBUG=dxtracker:5` and `grep Tracking` | `Tracking N objects in stream S`, `Tracking results: ...` (5) |
| Drawing | `GST_DEBUG=dxosd:5` and `grep Drawing` | `Drawing on NV12: N objects`, `Drawing on I420: N objects` (5) |
| Publishing | `GST_DEBUG=dxmsgbroker:6` and `grep Publishing` | `Publishing message (N bytes) to topic: T` (6) |

```bash
GST_DEBUG=dxinfer:5 gst-launch-1.0 PIPELINE 2>&1 | grep "Inference throughput"
```

For normal operation keep `GST_DEBUG` at 2 or lower; high levels slow the pipeline. Add `GST_DEBUG=dx*:4` logs when you report a problem.

## Display problems

### Nothing shows or the window is broken

The sink that GStreamer picked may not work with your graphics driver or display server.

* Put `videoconvert` right before the sink.
* On CPU only systems use `ximagesink` or `xvimagesink`; with a GPU use `glimagesink`.
* Without a display (SSH, container) use `fakesink sync=false`.

### Raspberry Pi 5: drmModeSetPlane failed: Permission denied

```text
ERROR: from element .../GstKMSSink:fps-display-video_sink-actual-sink-kms: GStreamer encountered a general resource error.
drmModeSetPlane failed: Permission denied (13)
ERROR: pipeline doesn't want to preroll.
```

`fpsdisplaysink` picks the highest ranked sink, `kmssink`, which fails here. Replace `fpsdisplaysink` with `ximagesink`.

### Orange Pi 5 Plus with Debian 12 shows corrupted video

On Orange Pi 5 Plus (RK3588) with the official Debian 12 image, the format that `videoconvert` negotiates with the display sink can give garbled or flickering video. Other ARM boards may show the same. Force I420 before the sink:

```text
... ! dxosd ! videoconvert ! video/x-raw,format=I420 ! fpsdisplaysink sync=false
```

The demo scripts contain this fix as a commented block. Uncomment it in the script you run:

```bash
if grep -q "rk3588" /proc/device-tree/compatible 2>/dev/null; then
    if [ "$(lsb_release -rs)" = "12" ]; then
        echo "Detected Orange Pi 5 Plus with Debian 12 - using I420 format"
        VIDEOCONVERT_PIPELINE="videoconvert ! video/x-raw,format=I420"
    fi
fi
```

### Stuttering, lag, "dropped frames"

* Close background programs, use lower resolution input or scale early.
* Add `queue` elements between stages so slow and fast stages decouple.
* Set `sync=false` on the sink to render as fast as possible.

## Pipeline problems

| Symptom | Cause | Fix |
|---|---|---|
| No detections, no error | `preprocess-id` of `dxpreprocess` and `dxinfer`, or `inference-id` of `dxinfer` and `dxpostprocess`, do not match | Use the same IDs, and different IDs per model. |
| Postprocess library fails to load | Wrong path, or a custom `--prefix` | Use the full path under `<prefix>/share/gstdxstream/lib/`. |
| Model not found with a shipped config | `model_path` in the JSON is relative to the current folder | Start from the repository root, or pass `model-path=` with an absolute path. |
| Pipeline hangs at start | No `queue` between stages, or no `queue` on a `dxoutputselector` output | Add `queue` elements. |
| `no property "..." in element "dx..."` | Property name not in this release | Check with `gst-inspect-1.0 <element>` and the [element pages](elements/index.md). |
| `dxrate` fails to start | `framerate` not set | Set `framerate`. |
| `dxmsgbroker` fails to start | `conn-info` or `topic` empty, or wrong `broker-name` | Set all three. |
| `gst-inspect-1.0 dxstream`: no such plugin | Environment not loaded, stale cache, or DX-RT missing | `source ~/.bashrc`, `rm -rf ~/.cache/gstreamer-1.0/`, check DX-RT with `dxcli -s`. |

### Could not link after dxinputselector

```text
WARNING: erroneous pipeline: could not link dxinputselector0 to videoconvert0
```

`dxinputselector` outputs `application/x-dxvideoraw`; `videoconvert`, `videoscale`, `compositor`, `videorate`, `dxscale`, `dxconvert` and `dxgather` cannot take it. Move those elements before `dxinputselector` (per stream) or after `dxoutputselector`. Inside, use only `dxpreprocess`, `dxinfer`, `dxpostprocess`, `dxtracker`, `dxosd`, `dxrate`, `dxmsgconv` and `dxmsgbroker`. See [Multi stream domain](elements/multi-stream-domain.md).

### Missing DXFrameMeta inside the multi stream domain

```text
ERROR dxinfer ... No DXFrameMeta in push buffer
LOG   dxpostprocess ... No DXFrameMeta, passing through
LOG   dxosd ... No frame metadata, passing through
```

A buffer entered the domain without passing `dxinputselector`, for example from an `appsrc` placed after it. Dual mode elements then fall back to `stream_id=0` or pass the buffer through.

* Feed every stream through a `dxinputselector` sink pad.
* If you create buffers yourself, attach `DXFrameMeta` with `dx_create_frame_meta()` and set `_stream_id`.
* In a custom buffer pool, honor the `DXFrameMeta` request in the `ALLOCATION` query.

## Build problems

### meson install fails with several meson versions

`build.sh` runs `sudo env PYTHONPATH=... $(which meson) install`. If meson is installed in more than one place (pip user, venv, `sudo pip`, apt), the `meson` binary and the `mesonbuild` module can come from different versions:

```text
ModuleNotFoundError: No module named 'mesonbuild'
```

Keep exactly one meson:

```bash
which -a meson
pip show meson
apt list --installed 2>/dev/null | grep meson
python3 -c "import mesonbuild, os; print(os.path.dirname(os.path.dirname(mesonbuild.__file__)))"
```

Remove the extra ones (`pip uninstall meson`, `sudo apt remove meson`), then check that `which meson` and the `mesonbuild` path share the same prefix. Any single install (pip user, venv, `sudo pip`, apt) works.

### Root owned files in the build folder

Because `meson install` runs as root, a later build may hit root owned files. `build.sh` detects this and runs `sudo chown` on the build folder. You can also use `./build.sh --clean`.

## Message broker problems

| Problem | Check |
|---|---|
| MQTT connection refused | `sudo systemctl status mosquitto`, then `mosquitto_pub -h localhost -p 1883 -t test -m "hello"`. For remote clients add `listener 1883 0.0.0.0` (see [Pipelines](pipelines.md#mqtt)). |
| MQTT TLS fails | `openssl verify -CAfile ca.crt server.crt`, then `mosquitto_pub -h localhost -p 8883 --cafile ca.crt -t test -m "ssl_test"`. |
| Kafka consumer lag | `bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-group --describe` |
| Kafka TLS handshake fails | `bin/kafka-console-producer.sh --bootstrap-server localhost:9093 --topic test --producer.config ssl.properties` |
| Converter library does not load | Check `library_file_path` and that json-glib is installed. |
| Wrong message format | Check that the library exports all three functions and the JSON you expect. |
| Too many messages | Raise `message-interval` on `dxmsgconv`. |

Kafka not running:

```text
%3|...|FAIL|rdkafka#producer-1| [thrd:localhost:9092/bootstrap]: localhost:9092/bootstrap: Connect to ipv4#127.0.0.1:9092 failed: Connection refused (after 0ms in state CONNECT)
ERROR: Pipeline doesn't want to pause.
```

Check with `ps -ef | grep kafka` and start the broker as in [Pipelines](pipelines.md#kafka). Keep its terminal open while the pipeline runs.

## Next steps

* [Performance with GstShark](performance.md)
* [Get started troubleshooting](../../get-started/troubleshooting.md)
* [Elements](elements/index.md)
