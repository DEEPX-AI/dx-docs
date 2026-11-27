---
title: Evaluate models
description: Measure model accuracy and speed with dxmz eval and dxmz benchmark on ONNX Runtime or the NPU.
---

# Evaluate models

This page shows how to measure the accuracy and speed of a model with `dxmz eval`, compare ONNX and NPU results, and run many models with `dxmz benchmark`.

## Before you start

* DX-ModelZoo installed and `DATA_ROOT`, `MODEL_ROOT` and `DXMZ_MODEL_URL` set, see [Install DX-ModelZoo](install.md).
* The model's dataset under `DATA_ROOT`. Run `dxmz info <model>` to see which dataset and path it expects, and see [Datasets](datasets.md).
* For NPU profiles: DX-RT with `dx_engine` in the same Python environment, and an NPU.

## Run an evaluation

```bash
dxmz eval resnet50_224x224 --profile onnx --seed 42 --save
```

`dxmz eval` does these steps:

1. Finds the model YAML by name (or uses the YAML path you give).
1. Loads the model file for the profile. If the file is missing under `MODEL_ROOT` and `DXMZ_MODEL_URL` is set, it downloads it.
1. Loads and validates the dataset from the YAML `dataset.eval_path`.
1. Runs preprocessing, inference, postprocessing and the task evaluator on every sample.
1. Prints the metrics and FPS, and with `--save` writes `result/eval_<model>_<profile>.json`.

Evaluate several models in one command. Each model gets its own result file:

```bash
dxmz eval resnet50_224x224 mobilenetv2_224x224 --profile onnx --save
```

Override the paths for one command:

```bash
dxmz eval resnet50_224x224 --profile onnx --data-root /data/datasets --model-root /data/models
```

Use a model file you already have. The file extension must match the profile target (`.onnx` for `onnx`, `.dxnn` for NPU profiles), and you can give only one model:

```bash
dxmz eval resnet50_224x224 --profile q-lite --model-path /path/to/resnet50_224x224_q-lite.dxnn
```

See [CLI reference](cli.md#dxmz-eval) for all options.

## Evaluate on the NPU

Profiles with `target: dxnn` (`c-lite`, `q-lite`, `q-pro`, `q-master`) run the compiled model on the NPU. `dxmz eval` looks for `<model name>_<profile>.dxnn` in the model's artifact folder (`${MODEL_ROOT}/<model name>` by default).

!!! note "dxmz eval never compiles"
    When the `.dxnn` file is missing, `dxmz eval` downloads the prebuilt file from `DXMZ_MODEL_URL`. It does not compile. To build the file yourself, run `dxmz compile` first:

    ```bash
    dxmz compile resnet50_224x224 --profile q-lite
    dxmz eval resnet50_224x224 --profile q-lite --save
    ```

    `dxmz compile` does not download the ONNX file either. Run an `onnx` evaluation first, or place `<model name>.onnx` in the artifact folder yourself.

Other NPU rules:

* NPU profiles always use batch size 1. Any other `batch_size` in the YAML is ignored.
* Arithmetic preprocessing (`div`, `normalize`, `transpose`, `expanddim`, `mul`, `add`, `subtract`) is skipped when the compiled model takes `uint8` input, because the NPU does it. See [Architecture](architecture.md#npu-preprocessing-skip).
* `DXNN_DEVICES=0,1` selects NPU devices and wins over `runtime.device` in the YAML.

## Read the results

The result file has these fields:

| Field | Meaning |
|---|---|
| `model` | Model name |
| `display_name` | Readable model name, when the YAML has one |
| `task` | Task, for example `image_classification` |
| `dataset` | Dataset type, for example `ILSVRC2012` |
| `metrics` | List of `{"name": ..., "metric_value": ...}`, for example `Top-1` and `Top-5` |
| `fps` | Frames per second (see below) |
| `elapsed_time` | Total run time in seconds |
| `start_time` | Start time, `YYYY-MM-DD HH:MM:SS` |
| `profile` | Profile used |
| `operations`, `parameters`, `license`, `input_resolution` | Model facts from the YAML |
| `error` | Only present when the evaluation failed. `dxmz eval` then exits with code 1. |

### How FPS is measured

The ONNX and NPU numbers are measured differently, so do not compare them directly.

| Mode | Used by | Formula | Includes |
|---|---|---|---|
| Sync | ONNX profiles (default) | images / inference time | Inference only |
| Async | NPU profiles (default) | images / wall time | Loading, inference and postprocessing |

In sync mode `dxmz` also logs a time breakdown with the seconds and share of each phase:

| Phase | Meaning |
|---|---|
| `load` | Data loading and preprocessing |
| `infer` | Model inference |
| `post` | Postprocessing and metric update |

In async mode up to `min(device count × 4, sample count)` inference requests run at the same time. Set `runtime.async` in the YAML to change the mode (see [Runtime options](yaml-config.md#runtime-options)).

### Batch size

ONNX profiles accept a larger batch:

```yaml
profiles:
  onnx:
    target: onnx
    runtime:
      device: gpu
      batch_size: 4
```

## Common metrics

| Evaluator | Metrics |
|---|---|
| `image_classification` | Top-1, Top-5 accuracy |
| `object_detection` | COCO mAP |
| `semantic_segmentation` | mIoU |
| `instance_segmentation` | mAP |
| `pose_estimation` | AP, AR |
| `depth_estimation` | δ < 1.25, RMSE |
| `face_recognition` | Accuracy |
| `super_resolution` | PSNR |

All 31 evaluators are listed in [Python API](python-api.md#built-in-evaluators).

## Benchmark many models

`dxmz benchmark` evaluates every model that matches the filters with one profile.

```bash
# All image classification models on ONNX Runtime
dxmz benchmark --profile onnx --domain cv --task image_classification --save

# All models on four NPU devices in parallel, one model per device at a time
dxmz benchmark --profile q-lite --devices 0,1,2,3 --save
```

With `--save`, the results are written to `result/benchmark_<profile>_<YYYY-MM-DD_HH-MM-SS>.json` as a list with one entry per model.

## Next steps

* [CLI reference](cli.md)
* [YAML configuration](yaml-config.md)
* [Custom models and datasets](custom-models.md)
