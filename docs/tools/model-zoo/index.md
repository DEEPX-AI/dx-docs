---
title: DX-ModelZoo
description: Browse, evaluate and compile 497 ready made models for DEEPX NPUs with the dxmz command line tool.
---

# DX-ModelZoo

DX-ModelZoo lets you browse, evaluate and compile ready made AI models for DEEPX NPUs with one command line tool, `dxmz`.

Current version: DX-ModelZoo 1.0.0 (DEEPX SDK 2.5.0).

Every model is described by a single YAML file. The file holds the input shape, preprocessing, postprocessing, dataset, and one or more runtime profiles (ONNX Runtime on CPU or GPU, or the NPU). You can evaluate a model in ONNX Runtime, compile it with DX-COM, and evaluate the compiled `.dxnn` file on the NPU, all from the same YAML file.

DX-ModelZoo contains 497 model configurations. It is installed from source (it is not on PyPI). The source is at [github.com/DEEPX-AI/dx-modelzoo](https://github.com/DEEPX-AI/dx-modelzoo).

## Before you start

* DX-ModelZoo installed, see [Install DX-ModelZoo](install.md).
* For NPU evaluation: DX-RT 3.5.0 or newer with its Python package `dx_engine`, and a DEEPX NPU.
* For compilation: DX-COM 2.5.0 or newer (`dx-com`).

## Quick start

1. Set where your datasets and model files live. The download URL lets `dxmz` fetch missing model files.

    ```bash
    export DATA_ROOT=/path/to/datasets
    export MODEL_ROOT=/path/to/models
    export DXMZ_MODEL_URL=https://sdk.deepx.ai/modelzoo
    ```

1. List the models.

    ```bash
    dxmz list --all
    ```

1. Show the details of one model.

    ```bash
    dxmz info resnet50_224x224
    ```

1. Evaluate it with ONNX Runtime. This needs the ImageNet validation set under `$DATA_ROOT/ILSVRC2012/val` (see [Datasets](datasets.md)).

    ```bash
    dxmz eval resnet50_224x224 --profile onnx --save
    ```

1. Compile it for the NPU, then evaluate the compiled model on the NPU.

    ```bash
    dxmz compile resnet50_224x224 --profile q-lite
    dxmz eval resnet50_224x224 --profile q-lite --save
    ```

With `--save`, each result is written to `result/eval_<model>_<profile>.json` in the current directory.

## Profiles

Each model YAML defines runtime profiles. You pick one with `--profile`.

| Profile | Target | What it does |
|---|---|---|
| `onnx` | ONNX Runtime | Runs the original ONNX model on CPU or GPU. This is the accuracy baseline. |
| `c-lite` | NPU (`dxnn`) | Compiles with `opt_level: 0` and the standard calibration. |
| `q-lite` | NPU (`dxnn`) | Compiles with the standard calibration (EMA, 100 samples) and runs on the NPU. |
| `q-pro` | NPU (`dxnn`) | Compiles with the DX-COM Q-PRO pipeline (`use_q_pro: true`, 1024 samples) and runs on the NPU. |
| `q-master` | NPU (`dxnn`) | Compiles with the DX-COM `qmaster` option. Only 16 models define it. |

See [YAML configuration](yaml-config.md#profiles) for how these map to DX-COM options.

## Supported tasks

The 497 models in 1.0.0 are 420 computer vision models, 14 PPU models and 63 pre optimized models. Counts are YAML files under `src/dx_modelzoo/models`. One architecture can have several variants (input size, decode option, PPU or pre optimized build).

| Group | Task (`task` key) | Models |
|---|---|---:|
| Classification | `image_classification` | 136 |
| | `zero_shot_image_classification` | 6 |
| | `image_retrieval` | 1 |
| Detection | `object_detection` | 123 |
| | `face_detection` | 18 |
| | `oriented_object_detection` | 5 |
| | `mainbody_detection` | 2 |
| | `hand_detection` | 1 |
| | `3d_object_detection` | 1 |
| Segmentation | `instance_segmentation` | 35 |
| | `semantic_segmentation` | 24 |
| | `zero_shot_instance_segmentation` | 1 |
| | `panoptic_driving_perception` | 1 |
| Pose and landmark | `pose_estimation` | 21 |
| | `face_landmark` | 2 |
| | `hand_landmark` | 1 |
| | `keypoint_detection` | 1 |
| | `object_pose_estimation` | 1 |
| Face and person | `face_recognition` | 4 |
| | `person_attribute` | 2 |
| | `face_attribute` | 1 |
| | `person_reid` | 1 |
| Image restoration | `super_resolution` | 6 |
| | `image_denoising` | 5 |
| | `low_light_enhancement` | 2 |
| | `image_matting` | 2 |
| Other | `depth_estimation` | 10 |
| | `anomaly_detection` | 4 |
| | `visual_place_recognition` | 3 |
| PPU builds | `ppu` domain (types 0 and 1) | 14 |
| Pre optimized builds | `pre_optimize` domain | 63 |

## Where to go

* [Install DX-ModelZoo](install.md): setup steps that are specific to DX-ModelZoo.
* [Evaluate models](evaluate.md): run evaluations and benchmarks and read the results.
* [YAML configuration](yaml-config.md): every key of a model YAML file.
* [Datasets](datasets.md): dataset folders, download links and dataset classes.
* [Custom models and datasets](custom-models.md): add your own model, operations, dataset or evaluator.
* [Architecture](architecture.md): how the registry, builder and pipelines fit together.
* [CLI reference](cli.md): every `dxmz` command and option.
* [Python API](python-api.md): `ModelBuilder`, sessions, `DataLoader`, evaluators and registries.
* [Preprocessing and postprocessing](processing-ops.md): every built in operation.

## Next steps

* [Install DX-ModelZoo](install.md)
* [Evaluate models](evaluate.md)
* [Compiler overview](../../compiler/index.md)
