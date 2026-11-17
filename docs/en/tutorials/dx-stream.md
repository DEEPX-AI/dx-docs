---
title: Build a DX-Stream pipeline
description: Run DX-Stream GStreamer pipelines on the NPU, plug in a custom postprocess and write a Python people counter.
---

# Build a DX-Stream pipeline

This tutorial lets you build video analytics pipelines with DX-Stream 3.2.0, our GStreamer plugin set.

The notebook is `notebooks/T04-DX-STREAM/dx_stream.ipynb` in [dx-tutorials](https://github.com/DEEPX-AI/dx-tutorials). Beyond the steps below it covers each element's properties, the multi stream domain (`dxinputselector` to `dxoutputselector`), RTSP, secondary mode, MQTT and Kafka output, a custom YOLOv7 postprocess patch and a Python people counter that reads `DXObjectMeta` through `pydxs`.

## Before you start

* [Set up the tutorials](setup.md) done with `./dx-runtime/install.sh --all`, so DX-Stream is built.
* A desktop session for the video windows. Without one, end the pipeline with `fakesink`.
* `sudo apt install gstreamer1.0-tools v4l-utils jq graphviz`.
* Optional: a V4L2 camera, reachable RTSP streams, an MQTT or Kafka broker.

## Steps

1. Download the sample models and videos (about 300 MB of models and a 1.1 GB video archive) and check that GStreamer sees the plugin:

    ```bash
    cd ~/dx-all-suite/dx-runtime/dx_stream
    ./setup.sh
    gst-inspect-1.0 dxstream
    ```

    If the plugin is not found, export the path that `build.sh` printed, for example `export GST_PLUGIN_PATH=/usr/local/lib/x86_64-linux-gnu/gstreamer-1.0`.

1. Run a YOLO26n detection pipeline by hand. The pipeline is Source, Decode, `dxpreprocess`, `dxinfer`, `dxpostprocess`, `dxosd`, Sink:

    ```bash
    gst-launch-1.0 filesrc location=dx_stream/samples/videos/doughnut.mp4 ! decodebin ! \
      dxpreprocess preprocess-id=1 resize-width=640 resize-height=640 ! \
      queue max-size-buffers=1 ! \
      dxinfer preprocess-id=1 inference-id=1 \
        model-path=dx_stream/samples/models/yolo26-n_640x640.dxnn backend=auto ! \
      queue max-size-buffers=1 ! \
      dxpostprocess inference-id=1 \
        library-file-path=/usr/local/share/gstdxstream/lib/libpostprocess_yolo26od.so \
        function-name=PostProcess ! \
      queue max-size-buffers=1 ! \
      dxosd ! videoconvert ! fpsdisplaysink sync=false
    ```

    `Ctrl+C` stops it. Run `gst-inspect-1.0 dxinfer` to see every property of an element.

1. Run the bundled demos:

    ```bash
    ./run_demo.sh
    ```

    | Choice | Demo |
    |---|---|
    | 0 | Object detection (YOLO26n), the default after 10 seconds |
    | 1 | Object detection (YOLOv5s with PPU) |
    | 2 | Face detection (YOLOv5s_Face) |
    | 3 | Pose estimation (YOLO26n_Pose) |
    | 4 | Instance segmentation (YOLO26n_Seg) |
    | 5 | Depth estimation (YOLO26n_Depth) |
    | 6 | Multi object tracking |
    | 7 | Multi channel object detection |
    | 8 | Multi channel object detection (RTSP) |
    | 9 | Secondary mode (multi model cascade) |

1. Debug a pipeline with targeted logs, or export a pipeline graph:

    ```bash
    GST_DEBUG=dx*:3 ./run_demo.sh
    GST_DEBUG=dxinfer:4,dxtracker:4 ./run_demo.sh
    GST_DEBUG=2,dxinfer:4 GST_DEBUG_FILE=/tmp/dxstream.log ./run_demo.sh
    ```

    Set `GST_DEBUG_DUMP_DOT_DIR=<folder>` before `gst-launch-1.0` to get DOT files of the pipeline.

1. For Python applications, use the DX-Stream environment. The notebook writes `yolo26_people_counter.py` in section 6 and runs it like this:

    ```bash
    cd ~/dx-all-suite/dx-runtime/dx_stream
    ./venv-dx_stream/bin/python ~/yolo26_people_counter.py \
      --model ~/dx-all-suite/workspace/res/models/yolo26-s_640x640.dxnn \
      --video dx_stream/samples/videos/snowboard.mp4
    ```

## Expected result

A window shows the video with boxes and an FPS counter. The people counter adds a count overlay.

## Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| `no element "dxinfer"` | `GST_PLUGIN_PATH` not set | Export the path printed by `build.sh`, or rebuild with `./build.sh` |
| `Could not open display` | No graphical session | Use a desktop session, or end the pipeline with `fakesink` |
| `v4l2src: Cannot open device` | Wrong camera path or format | `v4l2-ctl --list-formats-ext` and fix the device and caps |
| Some frames are fully green | `dxconvert` right before the display sink | Use `videoconvert ! fpsdisplaysink` |
| A sample model is rejected | Model Zoo 2.5.0 models need DX-RT 3.5.0 | Update DX-RT |
| `[sudo] password` during `setup.sh` | `jq` is missing | `sudo apt install jq` |
| `ModuleNotFoundError: No module named 'pydxs'` | Wrong Python | Use `venv-dx_stream/bin/python` |
| `generated with an old version of meson` | Old build folder | `./build.sh --clean` |

## Next steps

* [DX-Stream reference](../tools/stream/index.md)
* [YOLO26 four channel on RK3588](yolo26-rk3588.md)
* [Platform notes](platform-notes.md)
