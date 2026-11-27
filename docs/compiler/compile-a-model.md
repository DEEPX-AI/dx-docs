---
title: Compile a model
description: Run dxcom to turn an ONNX model and a JSON config into a .dxnn file, with every command line option.
---

# Compile a model

This page shows you how to compile an ONNX model with the `dxcom` command and lists every command line option.

## Before you start

* Install DX-COM: see [Install](../get-started/install.md). Check it with `dxcom --version`.
* An ONNX model with batch size 1 and a static input shape. See [Prepare an ONNX model](onnx-models.md).
* A JSON config file. See [Config file reference](config-reference.md).
* A folder of calibration images (about 100 images that look like your real input).

## Compile in one command

```bash
dxcom -m model.onnx -c config.json -o output/
```

DX-COM writes `output/model.dxnn`. The `.dxnn` file name comes from the ONNX file name. `-o` is a directory, and DX-COM creates it if it does not exist.

For development, also write the log and the summary report:

```bash
dxcom -m model.onnx -c config.json -o output/ --gen_log --export_html
```

```text
output/
├── model.dxnn            # compiled model for the DEEPX NPU
├── compiler.log          # with --gen_log
└── model_summary.html    # with --export_html
```

!!! warning "Check compiler.log before you write inference code"
    DX-COM can move preprocessing steps (for example `div` and `normalize`) into the NPU graph. The log line `[INFO] - Added nodes:` lists them. Remove those steps from your host code, or they run twice. See [Preprocessing that moves to the NPU](config-reference.md#preprocessing-that-moves-to-the-npu).

## Try it with our sample models

The [dx-compiler repository](https://github.com/DEEPX-AI/dx-compiler) has three scripts that download sample models (`YOLOV5S-1`, `YOLOV5S_Face-1`, `MobileNetV2-1`), their JSON configs and a calibration image set, and then compile them.

```bash
git clone https://github.com/DEEPX-AI/dx-compiler.git
cd dx-compiler
./example/1-download_sample_models.sh
./example/2-download_sample_calibration_dataset.sh
./example/3-compile_sample_models.sh
```

The scripts use these folders:

| Folder | Content |
|---|---|
| `dx_com/sample_models/onnx/` | Sample ONNX models |
| `dx_com/sample_models/json/` | Matching JSON configs |
| `dx_com/calibration_dataset/` | Calibration images |
| `dx_com/output/` | Compiled `.dxnn` files |

If `dxcom` is not on your `PATH`, the third script first tries to activate the DX-COM virtual environment. To compile one sample by hand:

```bash
cd dx_com
dxcom -m sample_models/onnx/MobileNetV2-1.onnx -c sample_models/json/MobileNetV2-1.json -o output/mobilenetv2
```

## Command format

```text
dxcom -m MODEL_PATH -c CONFIG_PATH -o OUTPUT_DIR [OPTIONS]
dxcom --checkpoint CHECKPOINT.qxnn -o OUTPUT_DIR [RESUME OPTIONS]
```

The second form is QXNN resume mode. It re-runs quantization from a checkpoint without the model and config. See [Diagnose and re-quantize](quantization.md#diagnose-and-re-quantize).

The `dxcom` CLI compiles single input models from image files only. For models with more than one input, or for non image data, use the [Python API](python-api.md) with a `DataLoader`.

## CLI options

### Required

| Option | Short | Description |
|---|---|---|
| `--model_path MODEL_PATH` | `-m` | Path to the ONNX model (`.onnx`). Not used in resume mode. |
| `--config_path CONFIG_PATH` | `-c` | Path to the JSON config (`.json`). Not needed in resume mode. |
| `--output_dir OUTPUT_DIR` | `-o` | Directory for the compiled model and other outputs. Always required. |

### Performance and resources

| Option | Default | Description |
|---|---|---|
| `--opt_level {0,1}` | `1` | `0`: fast compile with basic optimizations, NPU latency can be higher. `1`: full optimization for the lowest NPU latency, compile takes longer. |
| `--aggressive_partitioning` | off | Experimental. Puts as many operations as possible on the NPU. Helps hosts with a weak CPU (embedded, edge). Can increase compile time and memory use. On a fast host CPU the default partitioning can give better end to end performance. Some models can give unexpected results. |
| `--use_gpu {True,False}` | `True` | New in 2.5.0. `True` quantizes on a CUDA GPU when one is available and falls back to CPU otherwise. `False` forces CPU. Pick a GPU with the `CUDA_VISIBLE_DEVICES` environment variable. |
| `--float64_calibration` | off | Uses float64 precision in calibration and offset calculations, for the same result on different CPUs. |

### Quantization quality and tuning

Available from DX-COM 2.4.0. See [Quantization](quantization.md) for the workflow.

| Option | Default | Description |
|---|---|---|
| `--use_q_pro` | off | Automatic Q-PRO: DX-COM picks the DXQ enhancement stages for you. ONNX compile path and resume mode. Do not combine with a manual `enhanced_scheme` or with `qmaster`. |
| `--quant_diagnosis` | off | Writes `quant_diagnosis/diagnosis_report.html` and a resume checkpoint `quant_diagnosis/<model>.qxnn` in the output directory. |
| `--checkpoint PATH.qxnn` | none | Selects QXNN resume mode: re-quantize from a `.qxnn` checkpoint without recompiling. The extension must be `.qxnn`. Do not combine with `-m`. |
| `--recalibration_method {minmax,ema,iqr}` | none | Resume mode only. Calibration method to use for re-calibration. |
| `--enhanced_scheme SCHEME` | none | Resume mode only. Manual DXQ scheme, for example `P3:num_samples=1024`. Do not combine with `--use_q_pro`. For a normal compile, set `enhanced_scheme` in the JSON config. |
| `--dataset_path PATH` | none | Resume mode only. Replaces the calibration dataset path stored in the checkpoint. |

### Debugging, logging and partial compile

| Option | Default | Description |
|---|---|---|
| `--gen_log` | off | Writes all compiler logs to `compiler.log` in the output directory. |
| `--export_html` | off | Writes the self contained report `<model_name>_summary.html` in the output directory. See [Summary report](summary-report.md). |
| `--verbose` | off | New in 2.5.0. Expands masked error messages with the origin type, the original message and one direct cause. |
| `--compile_input_nodes NODES` | none | Comma separated ONNX node names where compilation starts. |
| `--compile_output_nodes NODES` | none | Comma separated ONNX node names where compilation ends. |
| `--version` | | Short form `-v`. Prints the DX-COM version and exits. |
| `--help` | | Short form `-h`. Prints the option list and exits. |

!!! warning "Use node names, not tensor names"
    `--compile_input_nodes` and `--compile_output_nodes` take ONNX operator node names (the boxes in Netron), not tensor names (the lines between them).

### Environment variables

| Variable | Description |
|---|---|
| `CUDA_VISIBLE_DEVICES` | Selects the physical GPU used for quantization, for example `CUDA_VISIBLE_DEVICES=1 dxcom ...`. |

`dxcom` exits with code `0` on success and a non zero code on any error.

## Examples

Fast compile while you iterate:

```bash
dxcom -m model.onnx -c config.json -o output/ --opt_level 0
```

Put as many operations as possible on the NPU (experimental):

```bash
dxcom -m model.onnx -c config.json -o output/ --aggressive_partitioning --gen_log
```

Force CPU quantization, or pick the second GPU:

```bash
dxcom -m model.onnx -c config.json -o output/ --use_gpu False
CUDA_VISIBLE_DEVICES=1 dxcom -m model.onnx -c config.json -o output/
```

Compile only a part of the graph:

```bash
dxcom -m model.onnx -c config.json -o output/ \
  --compile_input_nodes Conv12,Conv13 \
  --compile_output_nodes Conv123,Conv124
```

Automatic Q-PRO for better accuracy:

```bash
dxcom -m model.onnx -c config.json -o output/ --use_q_pro
```

## Compile from Python

The same compile in Python:

```python
import dx_com

dx_com.compile(model="model.onnx", output_dir="output/", config="config.json")
```

| CLI option | Python argument |
|---|---|
| `-m`, `--model_path` | `model` |
| `-c`, `--config_path` | `config` |
| `-o`, `--output_dir` | `output_dir` |
| `--opt_level` | `opt_level` |
| `--aggressive_partitioning` | `aggressive_partitioning=True` |
| `--use_gpu` | `use_gpu` |
| `--float64_calibration` | `float64_calibration=True` |
| `--use_q_pro` | `use_q_pro=True` |
| `--quant_diagnosis` | `quant_diagnosis=True` |
| `--checkpoint` | `checkpoint` |
| `--recalibration_method` | `recalibration_method` |
| `--enhanced_scheme` | `enhanced_scheme` (a dict) |
| `--dataset_path` | `dataset_path` |
| `--gen_log` | `gen_log=True` |
| `--export_html` | `export_html=True` |
| `--verbose` | `verbose=True` |
| `--compile_input_nodes a,b` | `input_nodes=["a", "b"]` |
| `--compile_output_nodes a,b` | `output_nodes=["a", "b"]` |

See [Python API](python-api.md) for every parameter.

## Next steps

* [Config file reference](config-reference.md)
* [Python API](python-api.md)
* [Use cases](use-cases.md)
* [Run the model with DX-RT](../runtime/index.md)
