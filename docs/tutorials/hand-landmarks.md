---
title: Hand landmarks
description: Track 21 landmarks per hand from a camera or video with a palm detector and a landmark model on the NPU.
---

# Hand landmarks

This demo lets you track 21 landmarks on each hand from a camera or a video in a C++ Qt application.

A palm detector (192 x 192) finds each hand. The app rotates and crops each hand region and the landmark model (224 x 224) predicts 21 points and left or right handedness. Each hand's landmark request runs with `RunAsync()`, so several hands overlap on the NPU. The tutorial is `notebooks/T23-demo-hand-landmarks` in [dx-tutorials](https://github.com/DEEPX-AI/dx-tutorials).

## Before you start

* DX-RT installed and the NPU visible (`dxcli -s`), see [Install](../get-started/install.md).
* A desktop session; a V4L2 camera for camera mode (optional).
* The build packages:

    ```bash
    sudo apt update
    sudo apt install -y build-essential cmake pkg-config libopencv-dev qtbase5-dev ffmpeg v4l-utils
    ```

## Steps

1. Get the code and the resources (about 10 MB):

    ```bash
    git clone --depth 1 https://github.com/DEEPX-AI/dx-tutorials.git ~/dx-tutorials
    cd ~/dx-tutorials/notebooks/T23-demo-hand-landmarks
    ./get_resources.sh
    ```

    This puts `hand-detector_192x192.dxnn`, `HandLandmarkLite.dxnn` and `hands.mp4` under `assets/`.

1. Build and run on the sample video or on the camera:

    ```bash
    cd app
    ./build.sh
    ./run_video.sh
    ./run_camera.sh
    ```

1. Change the input or the drawing:

    ```bash
    ./run_camera.sh --camera 2 --width 1920 --height 1080 --fps 30
    ./build/hand_landmarks --video /path/to/input.mp4 --loop --show-palm
    ```

    | Option | Default | Meaning |
    |---|---|---|
    | `--max-hands N` | 4 | Hands per frame |
    | `--palm-conf VALUE` | 0.2 | Palm confidence threshold |
    | `--landmark-conf VALUE` | 0.5 | Landmark presence threshold |
    | `--show-palm` | off | Also draw palm boxes and rotated regions |
    | `--landmark-only` | off | Draw only the landmarks |
    | `--windowed` | off | 1280 x 720 window instead of full screen |
    | `--save` | off | Save to the next free `output-XX.mp4` in the current folder |

    Press `Esc` or `Q` to quit and `F` to toggle full screen.

## Expected result

The window shows the video with 21 connected points on each hand and an FPS counter.

## Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| A model is listed as `missing` | `get_resources.sh` did not run | Run it again and check `assets/models/` |
| Shape or dtype error at load | Wrong model file | Check the UINT8 input shape with `dxparse` |
| `cannot open camera 0` | No camera or no permission | `v4l2-ctl --list-devices`; try another `--camera` |
| `Could not find ... dxrt` | DX-RT missing or in a custom prefix | `./build.sh -DCMAKE_PREFIX_PATH=<prefix>` |

## Next steps

* [PIDNet segmentation](pidnet.md)
* [Run the DX-APP examples](dx-app.md)
* [Tutorials](index.md)
