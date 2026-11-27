---
title: PIDNet segmentation
description: Run PIDNet Cityscapes semantic segmentation on the NPU with a live slider for the post processing resolution.
---

# PIDNet segmentation

This demo lets you overlay Cityscapes classes on a live camera or video with PIDNet, and see the CPU and NPU trade off with a slider.

The model takes a UINT8 `[1, 1024, 2048, 3]` input and returns FLOAT32 `[1, 19, 128, 256]` logits. It runs only on the NPU, so the app does the argmax over 19 classes on the CPU. The **Argmax scale** slider sets the resolution of that argmax. The tutorial is `notebooks/T24-demo-pidnet-cityscapes` in [dx-tutorials](https://github.com/DEEPX-AI/dx-tutorials).

## Before you start

* DX-RT installed and the NPU visible (`dxcli -s`), see [Install](../get-started/install.md).
* A desktop session; a V4L2 camera for camera mode (optional).
* The build packages:

    ```bash
    sudo apt update
    sudo apt install -y build-essential cmake pkg-config libopencv-dev qtbase5-dev ffmpeg v4l-utils
    ```

## Steps

1. Get the code and the resources (about 20 MB):

    ```bash
    git clone --depth 1 https://github.com/DEEPX-AI/dx-tutorials.git ~/dx-tutorials
    cd ~/dx-tutorials/notebooks/T24-demo-pidnet-cityscapes
    ./get_resources.sh
    ```

1. Build and run on the sample video or on the camera:

    ```bash
    cd app
    ./build.sh
    ./run_video.sh
    ./run_camera.sh
    ```

1. Tune it:

    ```bash
    ./run_video.sh --pidnet-argmax-scale 0.7
    ./run_video.sh --inflight 6
    ./run_camera.sh --camera 2 --width 1920 --height 1080 --fps 30 --alpha 0.45
    ```

    | Option | Default | Meaning |
    |---|---|---|
    | `--pidnet-argmax-scale VALUE` | 0.4 | Start value of the Argmax scale slider, 0.1 to 1.0 |
    | `--alpha VALUE` | 0.6 | Overlay opacity, 0.0 to 1.0 |
    | `--inflight N` | 4 | Async requests in flight, 1 to 6 (4 matches a four core Raspberry Pi 5) |
    | `--no-pace` | off | Process a video as fast as possible |
    | `--windowed` | off | 1280 x 800 window |
    | `--full-screen` | on in the scripts | Full screen window |

    Press `Esc`, `Q` or the Exit button to close and `F` to toggle full screen.

## Expected result

The window shows the video with a colored class mask. Moving the slider toward 0.1 lowers CPU time while the NPU rate stays the same.

## Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| `pidnet.mp4` not found | Resources incomplete | Rerun `get_resources.sh`, or pass another video to `run_video.sh` |
| Low FPS while the NPU is idle | CPU argmax at full resolution | Move the slider toward 0.1, or lower `--inflight` |
| The model is rejected at load | It was compiled with DX-COM 2.3.0 | Recompile it with your DX-COM |
| `Could not find a package configuration file provided by "dxrt"` | DX-RT missing or in a custom prefix | `./build.sh -DCMAKE_PREFIX_PATH=<prefix>` |

## Next steps

* [Run models with DX-RT](runtime.md)
* [Platform notes](platform-notes.md)
* [Tutorials](index.md)
