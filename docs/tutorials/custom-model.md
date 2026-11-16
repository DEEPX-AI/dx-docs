---
title: Deploy a custom model
description: Compile a custom trained YOLOv7 forklift and worker detector and run it on the NPU with DX-APP.
---

# Deploy a custom model

This tutorial lets you take a custom trained YOLOv7 model (two classes: forklift and worker), compile it and run it with the standard DX-APP executable.

The notebook is `notebooks/T03-E2E-AI-Workflow/e2e_ai_workflow.ipynb` in [dx-tutorials](https://github.com/DEEPX-AI/dx-tutorials). It also explains model choice, data annotation and training; training is optional and needs an NVIDIA GPU with 24 GB of memory.

## Before you start

* [Set up the tutorials](setup.md) done: DX-COM, DX-RT and DX-APP installed, NPU visible.
* About 230 MB of downloads: the ONNX model (139 MB), the compiled DXNN (71 MB) and a test video (19 MB).
* The notebook writes into `notebooks/T03-E2E-AI-Workflow/workspace/`. The commands below use `~/t03` so you can run them in a terminal.

## Steps

1. Clone the tutorials (for the compiler JSON and test image) and download the model and video:

    ```bash
    git clone --depth 1 https://github.com/DEEPX-AI/dx-tutorials.git ~/dx-tutorials
    mkdir -p ~/t03/output && cd ~/t03
    cp ~/dx-tutorials/notebooks/T03-E2E-AI-Workflow/assets/yolov7_640x640.json yolov7-forklift-person.json
    wget -nc https://cs.deepx.ai/_deepx_fae_archive/dx-tutorials/yolov7-forklift-person.onnx
    wget -nc https://cs.deepx.ai/_deepx_fae_archive/dx-tutorials/forklift-worker.mp4
    ```

1. Compile the model. First set `dataset_path` in `yolov7-forklift-person.json` to the absolute path of `~/dx-all-suite/dx-compiler/dx_com/calibration_dataset`. The compile takes more than 10 minutes on the CPU:

    ```bash
    cd ~/dx-all-suite/dx-compiler
    source venv-dx-compiler-local/bin/activate
    dxcom -m ~/t03/yolov7-forklift-person.onnx -c ~/t03/yolov7-forklift-person.json \
      -o ~/t03/output --gen_log
    deactivate
    ```

    To skip the compile, download the compiled model instead:

    ```bash
    cd ~/t03/output
    wget -nc https://cs.deepx.ai/_deepx_fae_archive/dx-tutorials/yolov7-forklift-person.dxnn
    ```

1. Write the DX-APP runtime configuration. It sets the class count and the labels in training order (class 0 is Forklift, class 1 is Worker):

    ```bash
    cat > ~/t03/yolov7-forklift-runtime.json <<'JSON'
    {
        "obj_threshold": 0.25,
        "score_threshold": 0.25,
        "nms_threshold": 0.45,
        "num_classes": 2,
        "class_names": ["Forklift", "Worker"]
    }
    JSON
    ```

    | Field | Meaning |
    |---|---|
    | `obj_threshold` | Drops candidates with a lower objectness score |
    | `score_threshold` | Drops detections with a lower final confidence |
    | `nms_threshold` | IoU threshold for Non Maximum Suppression |
    | `num_classes` | Number of classes the model outputs (2 here) |
    | `class_names` | Labels per class ID, in training order |

1. Build the YOLOv7 executable and run the model on the image and the video:

    ```bash
    cd ~/dx-all-suite/dx-runtime/dx_app
    ./build.sh --target yolov7_640x640_async
    ./bin/yolov7_640x640_async -m ~/t03/output/yolov7-forklift-person.dxnn \
      --config ~/t03/yolov7-forklift-runtime.json \
      -i ~/dx-tutorials/notebooks/T03-E2E-AI-Workflow/assets/forklift-worker.png \
      --no-display --save --save-dir ~/t03/outputs
    ./bin/yolov7_640x640_async -m ~/t03/output/yolov7-forklift-person.dxnn \
      --config ~/t03/yolov7-forklift-runtime.json -v ~/t03/forklift-worker.mp4 \
      --no-display --save --save-dir ~/t03/outputs
    ```

    Remove `--no-display` on a desktop session to see the window.

## Expected result

`~/t03/outputs` holds frames with boxes labeled forklift and worker.

## Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| `No images found` or a calibration error | `dataset_path` in the compiler JSON is wrong | Set the absolute path of `dx_com/calibration_dataset` |
| Compile takes more than 10 minutes | YOLOv7 640x640 is CPU bound | Wait, or download the compiled model |
| Forklifts labeled as workers | `class_names` order differs from training | Fix the order in the runtime JSON; keep `num_classes` at 2 |

## Next steps

* [Compile models with DX-COM](compiler.md)
* [Build a DX-Stream pipeline](dx-stream.md)
* [DX-COM reference](../compiler/index.md)
