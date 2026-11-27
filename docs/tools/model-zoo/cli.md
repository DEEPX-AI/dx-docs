---
title: dxmz CLI reference
description: Every dxmz command, argument and option in DX-ModelZoo 1.0.0, with examples.
---

# dxmz CLI reference

This page lists every `dxmz` command and option in DX-ModelZoo 1.0.0.

## Before you start

* DX-ModelZoo installed, see [Install DX-ModelZoo](install.md). Check with `dxmz --help`.

## Commands

| Command | What it does |
|---|---|
| [`dxmz eval`](#dxmz-eval) | Evaluates one or more models on their datasets |
| [`dxmz compile`](#dxmz-compile) | Compiles a model to `.dxnn` with DX-COM |
| [`dxmz benchmark`](#dxmz-benchmark) | Evaluates many models with one profile |
| [`dxmz list`](#dxmz-list) | Lists the available models |
| [`dxmz info`](#dxmz-info) | Shows the details of one model |
| [`dxmz create`](#dxmz-create) | Creates a custom model scaffold with a wizard |

Every command that takes a model accepts a model name (as printed by `dxmz list --all`) or a path to a YAML file. An argument that ends in `.yaml` or `.yml`, or contains `/`, is treated as a path.

## `dxmz eval`

```bash
dxmz eval <model> [<model> ...] --profile <profile> [options]
```

| Option | Meaning | Default |
|---|---|---|
| `--profile` | Profile name from the YAML, for example `onnx`, `c-lite`, `q-lite`, `q-pro` | required |
| `--data-root` | Dataset root. Overrides `DATA_ROOT`. | from environment |
| `--model-root` | Model file root. Overrides `MODEL_ROOT`. | from environment |
| `--model-path` | Model file to use. The extension must match the profile target (`.onnx` or `.dxnn`). Only with one model. For pipeline YAMLs use `stage=path,stage=path`. | from `artifacts.path` |
| `--save` | Write `result/eval_<model>_<profile>.json` | off |
| `--seed` | Random seed for reproducible results | `42` |

`dxmz eval` exits with code 1 when a model fails.

```bash
# One model
dxmz eval resnet50_224x224 --profile onnx

# Several models
dxmz eval resnet50_224x224 mobilenetv3-large_224x224 --profile onnx

# Explicit paths
dxmz eval resnet50_224x224 --profile onnx --data-root /data/datasets --model-root /data/models

# Your own compiled model file, results saved
dxmz eval resnet50_224x224 --profile q-lite --model-path /path/to/resnet50_224x224_q-lite.dxnn --save

# A YAML file
dxmz eval ./my_models/my_model.yaml --profile onnx
```

## `dxmz compile`

```bash
dxmz compile <model> --profile <profile> [options]
```

| Option | Meaning | Default |
|---|---|---|
| `--profile` | A profile with `target: dxnn`, for example `c-lite`, `q-lite`, `q-pro` | required |
| `--output` | Output folder, or a `.dxnn` file path | folder of the ONNX file |
| `--model-path` | Source ONNX file. For pipeline YAMLs use `stage=path,stage=path`. | from `artifacts.path` |
| `--data-root` | Dataset root for calibration data. Overrides `DATA_ROOT`. | from environment |
| `--model-root` | Model file root. Overrides `MODEL_ROOT`. | from environment |

The output file is `<onnx name>_<profile>.dxnn`. DX-COM also writes its HTML summary report. Compiling an `onnx` profile is an error. `dxmz compile` needs DX-COM (`dx-com`) and a local ONNX file: it does not download one.

```bash
dxmz compile resnet50_224x224 --profile q-lite
dxmz compile resnet50_224x224 --profile q-pro --output ./compiled/
dxmz compile yolov8-n_640x640 --profile q-lite
```

## `dxmz benchmark`

```bash
dxmz benchmark --profile <profile> [options]
```

| Option | Meaning | Default |
|---|---|---|
| `--profile` | Profile name | required |
| `--models-dir` | Folder with model YAMLs | built in models |
| `--data-root` | Dataset root | from environment |
| `--model-root` | Model file root | from environment |
| `--domain` | Domain filter, for example `cv`, `ppu`, `pre_optimize` | all |
| `--task` | Task filter, for example `image_classification` | all |
| `--devices` | Comma separated NPU device IDs. Each device runs one model at a time in parallel. | sequential |
| `--save` | Write `result/benchmark_<profile>_<YYYY-MM-DD_HH-MM-SS>.json` | off |

```bash
dxmz benchmark --profile onnx --task image_classification
dxmz benchmark --profile q-lite --devices 0,1,2,3 --save
```

## `dxmz list`

```bash
dxmz list [--domain <domain>] [--task <task>] [--all]
```

| Option | Meaning | Default |
|---|---|---|
| `--domain` | Domain filter (exact match) | all |
| `--task` | Task filter (exact match, for example `image_classification`, not `classification`) | all |
| `--all`, `-a` | Print plain text instead of the interactive browser | off |

Without `--all`, `dxmz list` opens an interactive tree browser. Use the arrow keys and Enter to see a model, and start `eval` or `compile` from it. In a non interactive terminal it prints plain text. Each line is `<domain>/<task>/<name>`.

```bash
dxmz list --all
dxmz list --all --domain cv --task object_detection
```

```text
cv/image_classification/resnet50_224x224
```

## `dxmz info`

```bash
dxmz info <model>
```

Prints the YAML path, name, inputs, profiles, dataset and preprocessing of a model.

```bash
dxmz info resnet50_224x224
```

```text
Model YAML: .../dx_modelzoo/models/cv/image_classification/resnet/resnet50_224x224.yaml
Name: resnet50_224x224
Inputs: [{'name': 'input', 'shape': [1, 3, 224, 224], 'dtype': 'float32', 'layout': 'NCHW'}]
Profiles: ['onnx', 'c-lite', 'q-lite', 'q-pro']
Dataset: {'type': 'ILSVRC2012', 'eval_path': '/data/datasets/ILSVRC2012/val'}
Preprocessing: [...]
```

## `dxmz create`

```bash
dxmz create
```

Starts a wizard that asks for the model name, domain, task, input shape, dataset and profiles, and writes `./custom/<domain>/<task>/<family>/<model>.yaml` (and a `custom_ops.py` helper when needed). It needs an interactive terminal. See [Custom models and datasets](custom-models.md).

## Environment variables

| Variable | Meaning | CLI override |
|---|---|---|
| `DATA_ROOT` | Dataset root | `--data-root` |
| `MODEL_ROOT` | Model file root | `--model-root` |
| `DXMZ_MODEL_URL` | Base URL for downloading missing model files | none |
| `DXNN_DEVICES` | NPU device IDs, comma separated | none |
| `ONNX_ASYNC_WORKERS` | Threads for asynchronous ONNX inference | none |

`dxmz` loads a `.env` file at start. Exported variables win over `.env`, and CLI options win over both. See [Install DX-ModelZoo](install.md#set-paths-and-the-download-url).

!!! note "Removed option"
    The `--use-gpu` option was removed in 1.0.0.

## Next steps

* [Evaluate models](evaluate.md)
* [YAML configuration](yaml-config.md)
* [Python API](python-api.md)
