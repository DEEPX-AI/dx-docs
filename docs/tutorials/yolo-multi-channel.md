---
title: YOLO multi channel
description: Run one YOLOv5s detection model on many video channels at once with a C++ application.
---

# YOLO multi channel

This demo lets you run one YOLOv5s model on many video channels at the same time and see all of them in one window.

Every channel has its own thread and submits frames with `RunAsync()` to one shared `InferenceEngine`. The PPU model returns decoded boxes, so the host only runs NMS. There are two versions:

| Version | Channels | Where |
|---|---|---|
| Tutorial T20 | 36 video or 33 camera channels | `notebooks/T20-demo-yolo-multi` in [dx-tutorials](https://github.com/DEEPX-AI/dx-tutorials) |
| `yolo_multi_demo` | Up to 100 channels, JSON driven layouts, camera expand grid, stage profiling | [dx_demo](https://github.com/DEEPX-AI/dx_demo) |

## Before you start

* DX-RT installed and `/dev/dxrt0` present, see [Install](../get-started/install.md).
* A desktop session for the OpenCV window; a V4L2 camera at `/dev/video0` for camera mode (optional).
* The build packages:

    ```bash
    sudo apt-get update
    sudo apt-get install -y build-essential cmake pkg-config ca-certificates curl tar \
      libopencv-dev libopencv-contrib-dev libfreetype-dev ffmpeg v4l-utils \
      gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
      gstreamer1.0-plugins-bad gstreamer1.0-libav
    ```

## Steps: tutorial T20

1. Get the code and the resources (one archive of about 134 MB with the model and 45 videos):

    ```bash
    git clone --depth 1 https://github.com/DEEPX-AI/dx-tutorials.git ~/dx-tutorials
    cd ~/dx-tutorials/notebooks/T20-demo-yolo-multi
    ./get_resources.sh
    ```

1. Check the model and get a single stream baseline:

    ```bash
    dxparse -m assets/models/YOLOV5S_PPU.dxnn -v
    dxrun -m assets/models/YOLOV5S_PPU.dxnn --use-ort -t 5
    ```

1. Build and run the 36 channel video demo, or the 33 channel camera demo:

    ```bash
    cd app
    ./build.sh
    ./run_video.sh
    ./run_camera.sh
    ```

    Press `t` to show or hide boxes, `Esc` or `q` (or the EXIT button) to quit.

## Steps: dx_demo yolo_multi_demo

1. Get the code, download the models and videos, and build:

    ```bash
    git clone https://github.com/DEEPX-AI/dx_demo.git
    cd dx_demo/yolo_multi_demo
    ./setup.sh
    ./build.sh
    ```

    We build with `build.sh` directly because `install.sh` runs `apt-get upgrade` on the whole system. Install the packages listed above first.

1. Run the demo and pick a configuration (the default is `0` when you press nothing):

    ```bash
    ./run_demo.sh
    ```

    | Choice | Configuration | Demo |
    |---|---|---|
    | 0 | `config/yolo_multi_demo.json` | Multi channel detection (YOLOv5) |
    | 1 | `config/ppu_yolo_multi_demo.json` | Multi channel detection with PPU (YOLOv5, 512) |
    | 2 | `config/ppu_yolo_multi_100channel_demo.json` | 100 channel detection with PPU |

    Run another layout directly, for example `./bin/yolo_multi_demo -c config/ppu_yolo_multi_640_demo.json`. Exit with `Esc`, `q`, the window close button or `Ctrl+C`.

1. Optional: profile each stage. The summary is written when the demo exits, so do not kill it:

    ```bash
    ./run_demo.sh --profile
    python3 scripts/compare_profile.py profile_linux_8ch_*.log profile_win_8ch_*.log
    ```

    | Option | Default | Meaning |
    |---|---|---|
    | `--profile [path]` | off | Write a log, default name `profile_<os>_<N>ch_<timestamp>.log` |
    | `--profile_period <ms>` | 5000 | Interval between snapshots |
    | `--profile_warmup <ms>` | 3000 | Samples before this time are discarded |

    In the log, the `cpu-ms/s` column is the total time per second a stage uses across all channels: the largest value is the bottleneck.

## Configuration notes for yolo_multi_demo

* When `video_sources` contains a camera input (`"camera"`, `"camera_image"` or `"camera_video"`), the first camera is enlarged in the center of the grid (up to about 20% of the grid) and every camera cell gets a yellow border. This does not apply when `display_config.expand_mode` is on.
* `display_config.sidebar_font_scale` (default 1.0) and `display_config.fps_value_font_scale` (default 0.5) set the font sizes.

```json
"video_sources": [
    [ "0", "camera" ],
    [ "./assets/videos/cctv-city-road.mov", "offline", 60 ],
    [ "./assets/videos/dance-group.mov",    "offline", 60 ]
]
```

## Expected result

One window tiles all channels with boxes, and the header shows the total FPS. Compare it with the `dxrun` baseline.

## Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| `Could not find a package configuration file provided by "dxrt"` | DX-RT missing or in a custom prefix | Install DX-RT, or `./build.sh -DCMAKE_PREFIX_PATH=<prefix>` (T20) |
| `The version of the compiled model is not compatible with the version of the runtime` | The T20 model was compiled with DX-COM 2.2.0 | Recompile the model with your DX-COM |
| `cannot open /dev/video0` | No camera or no permission | `v4l2-ctl --list-devices`; `sudo usermod -aG video $USER` |
| `cannot open display` | No graphical session | Run on a desktop session |

## Next steps

* [YOLO26 four tasks](yolo26-four-tasks.md)
* [Run models with DX-RT](runtime.md)
* [Tutorials](index.md)
