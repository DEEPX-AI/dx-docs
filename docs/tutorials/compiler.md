---
title: Compile models with DX-COM
description: Three DX-COM tutorials from a first ONNX to DXNN compile to PPU, YOLO26 TopK optimization and quantization recovery.
---

# Compile models with DX-COM

These three tutorials let you compile ONNX models to DXNN with DX-COM 2.5.0, from a first compile to accuracy recovery.

The notebooks are in `notebooks/T05-DX-Compiler/` of [dx-tutorials](https://github.com/DEEPX-AI/dx-tutorials). Everything they create goes to `notebooks/T05-DX-Compiler/workspace/`.

## Before you start

* [Set up the tutorials](setup.md) done: DX-COM in `~/dx-all-suite/dx-compiler/venv-dx-compiler-local` with its sample calibration dataset.
* An x86_64 host with 16 GB RAM. DX-COM does not run on aarch64.
* DX-RT and a DEEPX NPU for the `dxparse` and `dxrun` comparisons.

## What each part covers

| Part | Notebook | You learn | Time |
|---|---|---|---|
| 05-1 Beginner | `dx_com_01_beginner.ipynb` | Export MobileNetV2 to ONNX, write a calibration config, compile, inspect, compile ResNet50 from the Model Zoo | About 20 minutes |
| 05-2 Intermediate | `dx_com_02_intermediate.ipynb` | Calibration and preprocessing order, PPU Type 0 (YOLOv7) and Type 1 (YOLOX-S), YOLO26 TopK first optimization for detection, segmentation and pose | Tens of minutes (YOLOv7 compile) |
| 05-3 Advanced | `dx_com_03_advanced.ipynb` | Q-Lite, Q-PRO and Q-Master (QAT), quantization diagnosis, QXNN resume, the `dx_com.compile()` Python API for a two input model | About an hour (two Q-PRO compiles) |

## Steps

1. Activate the compiler environment and check the version:

    ```bash
    source ~/dx-all-suite/dx-compiler/venv-dx-compiler-local/bin/activate
    dxcom --version
    ```

    You can also install DX-COM from PyPI into your own environment with `pip install dx-com`, see [Install](../get-started/install.md).

1. Compile the bundled sample model and write a log and an HTML report:

    ```bash
    cd ~/dx-all-suite/dx-compiler/dx_com
    dxcom -m sample_models/onnx/MobileNetV2-1.onnx \
          -c sample_models/json/MobileNetV2-1.json \
          -o output/MobileNetV2-1 \
          --gen_log --export_html
    ```

    The DXNN file, `compiler.log` and the HTML report land in `output/MobileNetV2-1`.

1. Inspect and benchmark the result on the NPU:

    ```bash
    dxparse -m output/MobileNetV2-1/MobileNetV2-1.dxnn -v
    dxrun -m output/MobileNetV2-1/MobileNetV2-1.dxnn --use-ort -t 5
    ```

    A benchmark measures speed only. Check accuracy separately on your own validation data.

1. In 05-2, compare a PPU model with a non PPU model. The PPU filters detections in hardware so the host only runs NMS:

    ```bash
    dxrun -m models/yolov7_640x640_non_ppu.dxnn --use-ort -t 5
    dxrun -m outputs/yolov7_type0_ppu/<compiled-model>.dxnn --use-ort -t 5
    ```

    Choose PPU Type 0 for anchor based heads such as YOLOv7 and Type 1 for decoupled heads such as YOLOX. The PPU section of the compiler JSON sets `type`, `conf_thres`, `num_classes`, `activation` and the head `layer` mapping.

1. In 05-3, try the accuracy recovery options on the same model and data:

    | Goal | Command options |
    |---|---|
    | Baseline (Q-Lite PTQ) | `dxcom -m model.onnx -c config.json -o out/q_lite --gen_log --export_html` |
    | Automatic enhanced PTQ (Q-PRO) | add `--use_q_pro --opt_level 1` |
    | Find the layers that lose accuracy | add `--quant_diagnosis` |
    | Requantize without a full compile | `dxcom --checkpoint <out>/quant_diagnosis/<model>.qxnn -o out/iqr --recalibration_method iqr --dataset_path calibration_dataset` |
    | Requantize with Q-PRO from a checkpoint | `dxcom --checkpoint <model>.qxnn -o out/q_pro --use_q_pro --dataset_path calibration_dataset` |
    | Quantization aware training (Q-Master) | a compiler JSON with the QAT settings, see the notebook template |

    Use the Python API (`dx_com.compile()`) when a model needs a calibration `DataLoader`, for example a model with two named inputs. Check the signature with:

    ```bash
    python -c 'import inspect, dx_com; print(inspect.signature(dx_com.compile))'
    ```

## Expected result

Each compile prints its stages and writes a `.dxnn` file. `dxparse` lists the inputs, outputs and the NPU and CPU tasks, and `dxrun` prints the FPS.

## Next steps

* [Run models with DX-RT](runtime.md)
* [DX-COM reference](../compiler/index.md)
* [Deploy a custom model](custom-model.md)
