---
title: Run the DX-APP examples
description: Run the ready made DX-APP C++ and Python examples, export a standalone example and chain models with a JSON graph.
---

# Run the DX-APP examples

This tutorial lets you run the DX-APP examples for classification, detection, pose and segmentation, and reuse them for your own model.

DX-APP 3.3.0 ships a C++ and a Python example for every model in the Model Zoo (497 model variants across 29 tasks). The notebook is `notebooks/T02-DX-APP/dx_app.ipynb` in [dx-tutorials](https://github.com/DEEPX-AI/dx-tutorials). It takes about 45 minutes and needs no `sudo`.

## Before you start

* [Set up the tutorials](setup.md) done: DX-RT 3.5.0 or later, DX-APP and `venv-dx-runtime` installed with `./dx-runtime/install.sh --all`.
* A display is optional. The commands below run headless with `--no-display --save` and write images you can open.

## Steps

1. Download the models and videos that are still missing:

    ```bash
    cd ~/dx-all-suite/dx-runtime/dx_app
    ./setup.sh --no-force
    ```

1. Run a classification and a detection example. Executables are named after the model variant:

    ```bash
    ./bin/resnet50_224x224_sync -m assets/models/resnet50_224x224.dxnn \
      -i sample/ILSVRC2012/1.jpeg --no-display --save --save-dir ~/dx-app-out
    ./bin/yolov7_640x640_sync -m assets/models/yolov7_640x640.dxnn \
      -i sample/img/sample_dog.jpg --no-display --save --save-dir ~/dx-app-out
    ```

1. Compare synchronous, asynchronous and PPU execution on a video:

    ```bash
    ./bin/yolov7_640x640_sync -m assets/models/yolov7_640x640.dxnn -v assets/videos/boat.mp4 --no-display
    ./bin/yolov7_640x640_async -m assets/models/yolov7_640x640.dxnn -v assets/videos/boat.mp4 --no-display
    ./bin/yolov7_640x640_ppu_async -m assets/models/yolov7_640x640_ppu.dxnn -v assets/videos/drone-city-road2.mov --no-display
    ```

1. Try pose and segmentation:

    ```bash
    ./bin/yolov8-s-pose_640x640_sync -m assets/models/yolov8-s-pose_640x640.dxnn \
      -i sample/img/sample_person_b.jpg --no-display --save --save-dir ~/dx-app-out
    ./bin/yolov8-n-seg_640x640_async -m assets/models/yolov8-n-seg_640x640.dxnn \
      -i sample/img/sample_person_b.jpg --no-display --save --save-dir ~/dx-app-out
    ```

1. Start the demo launcher (26 demos, up to 6 execution modes) or find an example with `dx_tool.sh`:

    ```bash
    ./run_demo.sh
    ./scripts/dx_tool.sh search yolo26-s
    ./scripts/dx_tool.sh info yolo26-s_640x640
    ```

1. Export a standalone example that runs outside the DX-APP tree, then run it:

    ```bash
    bash setup.sh --models yolo26-s_640x640 --no-force
    bash scripts/extract_model_package.sh object_detection/yolo26/yolo26-s_640x640 \
      --lang py --output-dir ~/standalone/py --no-prune
    cd ~/standalone/py/object_detection/yolo26/yolo26-s_640x640
    ~/dx-all-suite/dx-runtime/venv-dx-runtime/bin/python yolo26-s_640x640_sync.py \
      --model ~/dx-all-suite/workspace/res/models/yolo26-s_640x640.dxnn \
      --image ~/dx-all-suite/dx-runtime/dx_app/sample/img/sample_street.jpg \
      --no-display --save --save-dir ~/dx-app-out
    ```

    Use `--lang cpp` for the C++ package, then build it with `mkdir -p build && cd build && cmake .. && make -j$(nproc)`. Use `--no-prune` for Python packages: the default pruning can miss classes named in `config.json`.

1. Chain two models without code. This runs a palm detector followed by hand landmarks from a JSON graph:

    ```bash
    cd ~/dx-all-suite/dx-runtime/dx_app
    ./build.sh --target multi_model_graph_sync multi_model_graph_async
    bash setup.sh --models mediapipe-hand-detector_192x192 mediapipe-hands-lite_224x224 --no-force
    ./bin/multi_model_graph_async --check src/cpp_example/multi_model_graph/hand_cascade.json
    ./bin/multi_model_graph_async --graph src/cpp_example/multi_model_graph/hand_cascade.json \
      --output ~/dx-app-out/hand_cascade.jpg
    ```

    To swap a model, edit the JSON and run `--check` again. `./bin/multi_model_graph_async --list-models --consumes roi` lists the models that can take a region of interest.

## Expected result

Each example prints a performance summary, and `~/dx-app-out` holds the images with boxes, keypoints or masks drawn on them.

## Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| `./bin/yolov7_async: No such file or directory` | DX-APP 3.3.0 names executables after the variant | Use the variant name, for example `./bin/yolov7_640x640_async`; `ls bin` lists them |
| `./bin/<variant>_sync: No such file or directory` | The default build only builds the 26 demo models | `./build.sh --target <variant>` or `./build.sh --all` |
| `.dxnn container v9 needs DX-RT >= 3.5.0` | Model Zoo 2.5.0 models need DX-RT 3.5.0 | Update DX-RT, see [Install](../get-started/install.md) |
| `dx_engine and DX-RT versions do not match` | `venv-dx-runtime` holds an older `dx_engine` | Reinstall DX-RT so both are 3.5.x |
| `ModuleNotFoundError: No module named 'dx_engine'` | Example run with the Jupyter Python | Use `~/dx-all-suite/dx-runtime/venv-dx-runtime/bin/python` |
| `Could not find a package configuration file provided by "dxrt"` | DX-RT not installed or in a custom prefix | Install DX-RT or pass `-DCMAKE_PREFIX_PATH=<prefix>` |
| `Could not open camera 0` | No camera or no permission | `v4l2-ctl --list-devices`; `sudo usermod -aG video $USER`, then log in again |

## Next steps

* [Deploy a custom model](custom-model.md)
* [DX-APP reference](../app/index.md)
* [Model Zoo](../model-zoo/index.md)
