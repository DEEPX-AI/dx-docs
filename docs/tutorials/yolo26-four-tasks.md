---
title: YOLO26 four tasks
description: Run YOLO26s detection, pose, segmentation and depth on one camera or video stream in a Qt C++ application.
---

# YOLO26 four tasks

This demo lets you run four YOLO26s models on one camera or video stream and see the four results live in a 2 x 2 window.

One capture thread feeds four asynchronous workers: object detection, pose estimation, instance segmentation and depth estimation. Each worker has its own `InferenceEngine` on the same NPU. The tutorial is `notebooks/T21-demo-yolo26-od-pose-seg-depth` in [dx-tutorials](https://github.com/DEEPX-AI/dx-tutorials).

## Before you start

* DX-RT installed and `/dev/dxrt0` present, see [Install](../get-started/install.md).
* A desktop session; a V4L2 camera for camera mode (optional).
* The build packages:

    ```bash
    sudo apt-get update
    sudo apt-get install -y build-essential cmake pkg-config qtbase5-dev libopencv-dev ffmpeg v4l-utils
    ```

## Steps

1. Get the code and the resources (about 80 MB: four models and a sample video):

    ```bash
    git clone --depth 1 https://github.com/DEEPX-AI/dx-tutorials.git ~/dx-tutorials
    cd ~/dx-tutorials/notebooks/T21-demo-yolo26-od-pose-seg-depth
    ./get_resources.sh
    ```

    The models are `yolo26-s_640x640.dxnn`, `yolo26-s-pose_640x640.dxnn`, `yolo26-s-seg_640x640.dxnn` and `yolo26-depth-s_768x768_q-lite.dxnn`.

1. Optional: get a baseline per model:

    ```bash
    cd assets/models
    dxrun -m yolo26-s_640x640.dxnn --use-ort -t 3 -v
    cd ../..
    ```

1. Build and run on the sample video or on the camera:

    ```bash
    cd app
    ./build.sh
    ./run_video.sh
    ./run_camera.sh
    ```

    `run_video.sh` accepts another video path as its first argument. Camera mode uses `/dev/video0`; pass `--camera`, `--width`, `--height` and `--fps` to change it. Press `Esc` or `q`, or click EXIT, to quit.

## Expected result

A full screen window with four panels and an FPS label each. The sum of the four rates shows how the models share the NPU. All four models end in a CPU task, so CPU load grows with each model.

## Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| `Could not find a package configuration file provided by "Qt5"` | Qt5 missing | `sudo apt install qtbase5-dev` |
| `Could not find a package configuration file provided by "dxrt"` | DX-RT missing or in a custom prefix | Install DX-RT, or `./build.sh -DCMAKE_PREFIX_PATH=<prefix>` |
| A model is rejected at load | These models were compiled with DX-COM 2.4.0 | Recompile from the Model Zoo ONNX with your DX-COM |
| `cannot open /dev/video0` | No camera or no permission | `v4l2-ctl --list-devices`; add your user to the `video` group |
| `could not connect to display` | No graphical session | Run on a desktop session |

## Next steps

* [YOLO26 C++ applications](yolo26-apps.md)
* [CLIP in C++](clip-cpp.md)
* [Tutorials](index.md)
