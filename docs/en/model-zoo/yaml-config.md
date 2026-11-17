---
title: YAML configuration
description: Reference for every key of a DX-ModelZoo model YAML file, including profiles, compile options and runtime options.
---

# YAML configuration

This page lists every key of a DX-ModelZoo model YAML file, so you can read a built in model or write your own.

Each model is one YAML file. Built in models live under `src/dx_modelzoo/models/<domain>/<task>/<family>/<model>.yaml`. `dxmz` validates the file when it loads it and stops with a `YamlValidationError` that names the wrong key.

## Full example

This is the built in `resnet50_224x224.yaml` (metadata shortened):

```yaml
name: resnet50_224x224
display_name: ResNet-50
task: image_classification
reference: https://github.com/pytorch/vision
license: BSD-3-Clause
description: >-
  ResNet residual CNN image classification model.
macs: 4.12 GMACs
params: 25.53 M
inputs:
  - name: input
    shape: [1, 3, 224, 224]
    dtype: float32
    layout: NCHW
preprocessing:
  - type: resize
    mode: torchvision
    size: [232, 232]
    interpolation: BILINEAR
  - type: centercrop
    height: 224
    width: 224
  - type: convertcolor
    form: BGR2RGB
  - type: div
    x: 255
  - type: normalize
    mean: [0.485, 0.456, 0.406]
    std: [0.229, 0.224, 0.225]
  - type: transpose
    axis: [2, 0, 1]
  - type: expanddim
    axis: 0
postprocessing:
  - type: topk
    k: [1, 5]
dataset:
  type: ILSVRC2012
  eval_path: ${DATA_ROOT}/ILSVRC2012/val
artifacts:
  path: ${MODEL_ROOT}/${MODEL_NAME}
calibration: &calibration
  method: ema
  num: 100
  seed: 42
profiles:
  onnx:
    target: onnx
    runtime:
      device: gpu
      batch_size: 1
  c-lite:
    target: dxnn
    compile:
      opt_level: 0
      calibration: *calibration
    runtime:
      device: 0
  q-lite:
    target: dxnn
    compile:
      calibration: *calibration
    runtime:
      device: 0
  q-pro:
    target: dxnn
    compile:
      calibration:
        <<: *calibration
        num: 1024
        use_q_pro: true
    runtime:
      device: 0
```

## Top level keys

| Key | Required | Meaning |
|---|---|---|
| `name` | yes | Unique model name. Use the file name without `.yaml`. Also sets `${MODEL_NAME}`. |
| `task` | yes | Task name, for example `image_classification`. It also selects the evaluator. |
| `inputs` | yes | List of input tensors, see [inputs](#inputs). |
| `preprocessing` | yes | List of preprocessing steps, or a mapping of input name to steps for multi input models. |
| `dataset` | yes | Dataset type and path, see [dataset](#dataset). |
| `artifacts` | yes | Where the model files are, see [artifacts](#artifacts). |
| `profiles` | yes | One or more runtime profiles, see [profiles](#profiles). |
| `postprocessing` | no | List of postprocessing steps. |
| `evaluator` | no | Evaluator override, see [evaluator](#evaluator). |
| `appendix` | no | Model specific options, see [appendix](#appendix). |
| `display_name`, `reference`, `license`, `description`, `macs`, `params` | no | Metadata. `macs`, `params` and `license` are copied into the evaluation result. |
| `calibration`, `pre_optimize_config` | no | Blocks defined once and reused in profiles with YAML anchors (`&calibration`, `*calibration`). |

### `inputs`

```yaml
inputs:
  - name: input
    shape: [1, 3, 224, 224]
    dtype: float32
    layout: NCHW
```

Each entry needs a unique `name` and a non empty `shape` of positive integers. `dtype` and `layout` are optional strings. A shape can use a named dimension (a string) when you declare it in `symbolic_dimensions`.

For a multi input model, list every input and make `preprocessing` a mapping keyed by input name:

```yaml
inputs:
  - name: input_ids
    shape: [1, 256]
    dtype: int64
  - name: attention_mask
    shape: [1, 256]
    dtype: int64
preprocessing:
  input_ids: []
  attention_mask: []
```

### `preprocessing` and `postprocessing`

Each step is a mapping with a `type` and its parameters. Steps run in order. Unknown preprocessing types are an error. Unknown postprocessing types only warn, because a `custom_ops.py` file can register them. See [Preprocessing and postprocessing](processing-ops.md) for every built in type.

### `dataset`

```yaml
dataset:
  type: ILSVRC2012
  eval_path: ${DATA_ROOT}/ILSVRC2012/val
```

`type` is a registered dataset key (see [Datasets](datasets.md)). `eval_path` is the dataset folder. Other keys (for example `split` or `category`) are passed to the dataset class when its constructor accepts them. `dxmz compile` also uses this dataset for calibration.

### `artifacts`

```yaml
artifacts:
  path: ${MODEL_ROOT}/${MODEL_NAME}
```

`path` is the folder with the model files, or a path to the `.onnx` file. File names inside the folder:

| Profile target | File name | Download URL when missing |
|---|---|---|
| `onnx` | `<name>.onnx` | `${DXMZ_MODEL_URL}/onnx/<name>.onnx` |
| `dxnn` | `<name>_<profile>.dxnn` | `${DXMZ_MODEL_URL}/<profile>-dxnn/latest/<name>_<profile>.dxnn` |

Files are downloaded only when `DXMZ_MODEL_URL` is set.

### `evaluator`

Built in models select the evaluator from `task`. Set `evaluator.type` to use another one. Models under the workspace `./custom` folder must set it.

```yaml
evaluator:
  type: image_classification
  options:
    some_attribute: value
```

`evaluator.options` sets attributes on the evaluator. The options `use_ppu`, `anchors` and `yolo_version` apply only to NPU profiles.

### `appendix`

| Key | Meaning |
|---|---|
| `npu_skip_arithmetic` | `false` keeps arithmetic preprocessing on the CPU for NPU profiles (needed by some models such as ViT, DeiT and ResMLP). `true` forces the skip. |
| `label_preprocessing` | Preprocessing steps applied to labels, for example a resize of segmentation masks. |
| `hr_preprocessing` | Preprocessing steps for high resolution targets (super resolution). |
| any other key | Set on the evaluator when it has an attribute with that name (for example `max_depth`, `upscale_factor`, `noise_level`). |

## Profiles

Each entry under `profiles` is a profile name with a `target`, a `runtime` block and, for the NPU, a `compile` block.

```yaml
profiles:
  onnx:
    target: onnx
    runtime:
      device: gpu
      batch_size: 4
  q-lite:
    target: dxnn
    compile:
      calibration: *calibration
    runtime:
      device: 0
      buffer_count: 6
      use_ort: true
```

| Key | Meaning |
|---|---|
| `target` | `onnx` (ONNX Runtime) or `dxnn` (NPU). Required. |
| `runtime` | Runtime options. Required, and must contain `device`. |
| `compile` | Options passed to DX-COM. Required for `target: dxnn`. |

The built in profiles and what they mean in DX-COM terms:

| Profile | DX-COM settings | Runs on |
|---|---|---|
| `onnx` | none (not compiled) | ONNX Runtime |
| `c-lite` | `opt_level: 0`, default calibration (EMA, 100 samples) | NPU |
| `q-lite` | default optimization, default calibration (EMA, 100 samples) | NPU |
| `q-pro` | `use_q_pro: true`, 1024 calibration samples | NPU |
| `q-master` | `qmaster` block (quantization aware training) | NPU |

### Compile options

`dxmz compile` passes every key of `compile` as a keyword argument to `dx_com.compile()`. It sets `model`, `output_dir`, `config` and `dataloader` itself, and sets `export_html: true` unless you set it. See [Compiler overview](../compiler/index.md) for the meaning of each DX-COM option.

| Key | Meaning |
|---|---|
| `calibration` | Calibration settings, see below. |
| `opt_level` | DX-COM optimization level, `0` or `1`. |
| `aggressive_partitioning` | DX-COM option to run more operations on the NPU (experimental). |
| `ppu_config` | PPU postprocessing configuration, see below. |
| `pre_optimize_config` | List of DX-COM pre optimize passes (used by the 63 pre optimized models). |
| `qmaster` | Quantization aware training configuration for DX-COM. |
| `export_html`, `gen_log`, `verbose` | DX-COM report and log options. |

!!! warning "Renamed in 1.0.0"
    The compile key `compile.quantization` was renamed to `compile.calibration` in DX-ModelZoo 1.0.0. Update your own YAML files.

### Calibration options

| Key | Type | Meaning |
|---|---|---|
| `compile.calibration.method` | str | Calibration method, for example `ema` |
| `compile.calibration.num` | int | Number of calibration samples |
| `compile.calibration.seed` | int | Random seed for sample selection |
| `compile.calibration.use_q_pro` | bool | Use the DX-COM Q-PRO pipeline |
| `compile.calibration.wbit` | int | Weight bit width |
| `compile.calibration.enhanced_scheme` | dict | DX-COM enhanced quantization scheme |

### `ppu_config`

`ppu_config` is allowed only for `target: dxnn`. It cannot be combined with `pre_optimize` in the same profile.

```yaml
compile:
  ppu_config:
    type: 1
    num_classes: 80
    conf_thres: 0.25
    layer:
      - bbox: conv2d_100
        cls_conf: conv2d_101
```

| Key | Required for | Meaning |
|---|---|---|
| `type` | all | `0` anchor based PPU, `1` anchor free single head PPU, `2` DFL based CPU TopK (no PPU hardware, deprecated) |
| `num_classes` | all | Number of classes (int) |
| `layer` | all | Type `0`: mapping of layer name to `{num_anchors: int}`. Types `1` and `2`: list of `{bbox, cls_conf}` entries, plus `obj_conf` (type 1) or `mask_coeff` (type 2). |
| `conf_thres` | types `0`, `1` | Confidence threshold |
| `activation` | type `0` | Activation name, for example `sigmoid` |
| `topk` | type `2` | Number of top candidates (int) |

!!! warning "PPU type 2 is deprecated"
    DX-COM deprecated PPU type `2` in 2.4.0. Use the DX-COM pre optimize passes (`pre_optimize_config`) instead.

### Runtime options

| Key | Type | Meaning |
|---|---|---|
| `runtime.device` | str, int or list | Required. ONNX: `cpu` or `gpu` (or CUDA device IDs). NPU: device ID or list of IDs. `DXNN_DEVICES` overrides it. |
| `runtime.batch_size` | int | Evaluation batch size, default `1`. NPU profiles always use `1`. |
| `runtime.async` | bool | Asynchronous inference. Default `false` for `onnx`, `true` for `dxnn`. |
| `runtime.buffer_count` | int | NPU only. Engine I/O buffer count, `1` to `100`. Default: the DX-RT default (6). |
| `runtime.use_ort` | bool | NPU only. Run operations the NPU does not support on ONNX Runtime. Default `true`. |
| `runtime.start_method` | str | Data loader process start method: `auto`, `forkserver` or `spawn`. Default `auto`. |

## Variables

Any string value can use `${VAR}`. `dxmz` replaces it with the environment variable of that name. An unset variable stays as written and logs a warning.

| Variable | Value |
|---|---|
| `${MODEL_NAME}` | The YAML `name` field (not an environment variable) |
| `${DATA_ROOT}` | Dataset root, from the environment, `.env` or `--data-root` |
| `${MODEL_ROOT}` | Model file root, from the environment, `.env` or `--model-root` |
| `${DXMZ_MODEL_URL}` | Download base URL |

## Pipeline YAMLs

A YAML file can chain several models. It has a `pipeline` mapping of stages instead of top level `inputs`, `preprocessing` and `artifacts`. Each stage needs `inputs`, `preprocessing` and `artifacts`. `name`, `dataset` and `profiles` stay at the top level and are shared. No built in model in 1.0.0 is a pipeline. Pass stage model files with `--model-path "det=/path/det.onnx,rec=/path/rec.onnx"`.

## Next steps

* [Custom models and datasets](custom-models.md)
* [Preprocessing and postprocessing](processing-ops.md)
* [Evaluate models](evaluate.md)
