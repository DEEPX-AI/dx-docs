---
title: YOLO26 C++ applications
description: Build the eight dx_yolo26 C++ applications for detection, classification, pose, segmentation and depth and run them on the NPU.
---

# YOLO26 C++ applications

This demo lets you build small C++ applications for each YOLO26 task and run them on images, videos, cameras or RTSP streams.

[dx_yolo26](https://github.com/DEEPX-AI/dx_yolo26) (version 0.2.0) has eight applications, each built as `<name>_sync` and `<name>_async`. The YOLO26 postprocessing is compiled into the applications. Part of the code comes from DX-APP, but the package is maintained on its own.

| Application | Task | Default model file |
|---|---|---|
| `yolo26n` | Object detection | `yolo26-n-od_640x640.dxnn` |
| `yolo26n_cls` | Classification | `yolo26-n-cls_224x224.dxnn` |
| `yolo26n_pose` | Pose estimation | `yolo26-n-pose_640x640.dxnn` |
| `yolo26n_seg` | Instance segmentation | `yolo26-n-seg_640x640.dxnn` |
| `yolo26n_depth` | Depth estimation | `yolo26-depth-n_768x768.dxnn` |
| `yolo26n_preopt` | Object detection, pre optimized model | `pre_optimized_yolo26-n-od.dxnn` |
| `yolo26n_pose_preopt` | Pose estimation, pre optimized model | `pre_optimized_yolo26n-pose.dxnn` |
| `yolo26n_seg_preopt` | Instance segmentation, pre optimized model | `pre_optimized_yolo26n-seg.dxnn` |

## Before you start

* DX-RT installed (`libdxrt` and the `dxrt/` headers, `/usr/local` by default), see [Install](../get-started/install.md).
* OpenCV 4.2 or newer (4.5.5 recommended), CMake 3.14 or newer, a C++17 compiler, Ninja or Make.

## Steps

1. Get the code and build it:

    ```bash
    git clone https://github.com/DEEPX-AI/dx_yolo26.git ~/dx_yolo26
    cd ~/dx_yolo26
    ./build.sh
    ```

    | Command | Effect |
    |---|---|
    | `./build.sh --variants async` | Build only the async applications |
    | `./build.sh --clean -j 8` | Rebuild from scratch |
    | `./build.sh --arch aarch64` | Cross build with `cmake/toolchain.aarch64.cmake` |
    | `./build.sh --install-prefix /usr --install` | Build and install |

    Binaries land in `build_<arch>/src/cpp_example/`.

1. Download the models from the Model Zoo with DX-APP's download script. The Model Zoo names for detection and classification differ from the application defaults, so we always pass `-m`:

    ```bash
    cd ~/dx-all-suite/dx-runtime/dx_app
    bash setup.sh --models yolo26n yolo26n-cls yolo26n-pose yolo26n-seg yolo26-depth-n_768x768 --no-force
    ```

    | Application | Model Zoo file |
    |---|---|
    | `yolo26n` | `yolo26-n_640x640.dxnn` |
    | `yolo26n_cls` | `yolo26-cls-n_224x224.dxnn` |
    | `yolo26n_pose` | `yolo26-n-pose_640x640.dxnn` |
    | `yolo26n_seg` | `yolo26-n-seg_640x640.dxnn` |
    | `yolo26n_depth` | `yolo26-depth-n_768x768.dxnn` |

1. Run an application. With no input option it uses a bundled image from `sample/img/`, relative to the working folder:

    ```bash
    cd ~/dx_yolo26
    M=~/dx-all-suite/workspace/res/models
    find build_* -name 'yolo26n_async' -type f
    ./build_x86_64/src/cpp_example/yolo26n_async -m $M/yolo26-n_640x640.dxnn
    ./build_x86_64/src/cpp_example/yolo26n_seg_sync -m $M/yolo26-n-seg_640x640.dxnn \
      -i sample/img --no-display
    ```

    Use the path that `find` prints if your build folder differs.

    | Option | Meaning |
    |---|---|
    | `-m, --model_path` | Model file (`.dxnn`) |
    | `-i, --image_path` | Image file or folder (jpg, png, jpeg, bmp) |
    | `-v, --video_path` | Video file |
    | `-c, --camera_index` | Camera index, for example `0` |
    | `-r, --rtsp_url` | RTSP stream URL |
    | `-s, --save` | Save the rendered output (`--save-dir`, default `artifacts/cpp_example`) |
    | `-l, --loop` | Repeat N times (image or video only) |
    | `--no-display` | Do not open a window, only print FPS |
    | `--config` | Postprocess configuration JSON |
    | `--show-log` | Verbose log |

## Pre optimized models

A pre optimized model carries the tail of the YOLO26 head inside the model. The NPU applies the DFL step, and a CPU task run by DX-RT through ONNX Runtime keeps the top 300 candidates and decodes them. The application gets a fixed table sorted by score:

| Model | Output | Row layout |
|---|---|---|
| `pre_optimized_yolo26-n-od.dxnn` | `preopt_output [1, 300, 6]` | `x1 y1 x2 y2 score class_id` |
| `pre_optimized_yolo26n-pose.dxnn` | `preopt_output [1, 300, 57]` | box, score, class and 17 x `kx ky visibility` |
| `pre_optimized_yolo26n-seg.dxnn` | `preopt_output [1, 300, 38]` and `output1 [1, 32, 160, 160]` | box, score, class and 32 mask coefficients; `output1` holds the mask prototypes |

On one stream this roughly halves detection and pose latency on DX-M1 (about 16 ms instead of 28 ms and 23 ms at 640x640). With all NPU cores busy throughput is about the same; segmentation gains about 20%. The model is NMS free: `nms_threshold` in `config.json` only merges the same box reported with two classes; set it to `1.0` to keep every row. If DX-RT is built without ONNX Runtime, the application does the same top k selection itself (`top_k` in `config.json`, default 300).

The three pre optimized models ship in the Yocto sample bundle (`meta-deepx-m1`, recipe `dx-yolo26-sample`, installed under `/etc/dx-yolo26-sample`). To make TopK optimized YOLO26 models yourself, see part 05-2 in [Compile models with DX-COM](compiler.md).

```bash
yolo26n_preopt_sync -m assets/models/pre_optimized_yolo26-n-od.dxnn
yolo26n_seg_preopt_async -m assets/models/pre_optimized_yolo26n-seg.dxnn -v input.mp4 \
  --config src/cpp_example/instance_segmentation/yolo26n_seg_preopt/config.json
```

## Expected result

Each run prints FPS and, without `--no-display`, opens a window with the boxes, keypoints, masks or depth map.

## Yocto

`meta-deepx-m1` packages the applications as `dx-yolo26`:

```text
IMAGE_INSTALL:append = " dx-yolo26 dx-yolo26-sample"
```

The recipe builds only the async variants. On a target, `yolo26n_preopt_async`, `yolo26n_pose_preopt_async` and `yolo26n_seg_preopt_async` run with no arguments; the other applications need `-m`.

## Add another YOLO26 variant

Add `src/cpp_example/<category>/<model>/{<model>_sync.cpp,<model>_async.cpp,factory/<model>_factory.hpp}`. CMake finds it from the folder layout. The factory declares the default model in `getDefaultModel()`.

## Next steps

* [YOLO26 four tasks](yolo26-four-tasks.md)
* [DX-APP reference](../tools/app/index.md)
* [Model Zoo](../tools/model-zoo/index.md)
