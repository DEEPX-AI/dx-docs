---
title: CLIP in C++
description: Match camera or video frames against text queries with CLIP, the image encoder on the NPU and the text encoder on the CPU.
---

# CLIP in C++

This demo lets you rank your own text queries against a live camera or video with CLIP, in a C++ Qt application.

The text encoder runs once per query on the CPU with ONNX Runtime and its embeddings are cached in `.cache/text_features_cpp/`. The ViT-L/14 image encoder runs on the NPU with `RunAsync()`. The app normalizes both embeddings and ranks the queries by dot product for every encoded frame. The tutorial is `notebooks/T22-demo-clip-single` in [dx-tutorials](https://github.com/DEEPX-AI/dx-tutorials).

## Before you start

* DX-RT installed and `/dev/dxrt0` present, see [Install](../get-started/install.md). The DX-RT install also puts the ONNX Runtime C++ library under `/usr/local`.
* A desktop session; a V4L2 camera for camera mode (optional).
* About 1.4 GB of downloads.
* The build packages:

    ```bash
    sudo apt update
    sudo apt install -y build-essential cmake pkg-config libopencv-dev qtbase5-dev zlib1g-dev
    ```

## Steps

1. Get the code and the resources (image encoder DXNN, text encoder ONNX and a sample video):

    ```bash
    git clone --depth 1 https://github.com/DEEPX-AI/dx-tutorials.git ~/dx-tutorials
    cd ~/dx-tutorials/notebooks/T22-demo-clip-single
    ./get_resources.sh
    ```

1. Build and run on the sample video or the camera:

    ```bash
    cd app
    ./build.sh
    ./run_video.sh
    ./run_camera.sh
    ```

    The scripts bring default queries, for example "A person giving a thumbs up" for the camera.

1. Use your own queries:

    ```bash
    ./build/clip_single --texts "A person" "A bicycle" "A cup" \
      --camera /dev/video0 --skip-frames 2 --full-screen --exit-btn
    ./build/clip_single --texts "Cars are driving" "An empty road" \
      --input /path/to/video.mp4 --exit-btn
    ```

    | Option | Meaning |
    |---|---|
    | `--texts` | Text queries to rank |
    | `--input SOURCE` | Camera index, camera device or video path |
    | `--camera SOURCE` | Camera to use when `--input` is omitted |
    | `--skip-frames N` | Encode one frame out of `N + 1` (default 2); higher means less NPU load |
    | `--no-normalize` | Do not L2 normalize before the similarity |
    | `--full-screen`, `--exit-btn` | Full screen window, Exit button |

    Press `Esc` or `Q` to close. `./build/clip_single --help` lists all options.

## Expected result

The window shows the video and a score bar per query, with the best match on top.

## Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| `Could not find ONNXRUNTIME` | ONNX Runtime not in `/usr/local` | `./build.sh -DONNXRUNTIME_ROOT=<prefix>` |
| `Could not find a package configuration file provided by "dxrt"` | DX-RT missing or in a custom prefix | `./build.sh -DCMAKE_PREFIX_PATH=<prefix>` |
| The image encoder is rejected | It was compiled with DX-COM 2.2.1 | Compile your own with [CLIP in Python](clip-python.md) |
| `get_resources.sh` runs for long | The archive is about 1.4 GB | Let it finish; a rerun resumes from the `.part` file |

## Next steps

* [CLIP in Python](clip-python.md)
* [CLIP multi channel demo](clip-multi-channel.md)
* [Hand landmarks](hand-landmarks.md)
