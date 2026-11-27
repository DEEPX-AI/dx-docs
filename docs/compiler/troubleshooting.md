---
title: DX-COM troubleshooting
description: DX-COM error types, the most common compile problems and how to fix them.
---

# DX-COM troubleshooting

This page helps you fix DX-COM errors and the most common compile problems.

## Before you start

* Compile again with `--gen_log` to get `compiler.log` in the output directory.
* Add `--verbose` (Python: `verbose=True`) when an error is reported only in summary form. It shows the origin type, the original message and one direct cause.

## Common problems

### DataLoaderError: config specifies (1, H, W, C) but model requires (1, C, H, W)

```text
DataLoaderError: Invalid JSON Configuration for input 'images': The config specifies (1, 640, 640, 3),
but model requires (1, 3, 640, 640). Please check the preprocessing configuration.
```

The default loader reads images as HWC and never transposes them. The shape in the message is the shape after your preprocessing chain. End `preprocessings` with:

```json
{"transpose": {"axis": [2, 0, 1]}},
{"expandDim": {"axis": 0}}
```

See [How the default loader reads images](config-reference.md#how-the-default-loader-reads-images).

### NHWC model fails with "Unknown error occurred during compilation"

An NHWC model whose graph starts with `Transpose(perm=[0,3,1,2])` (for example a tf2onnx export) fails with `Unknown error occurred during compilation. Please contact DEEPX.` when the chain has no final `expandDim`. With `--verbose` it shows `ValueError: axes don't match array`. Always end the chain with `{"expandDim": {"axis": 0}}`.

### Accuracy is low but the compile succeeded

| Check | Fix |
|---|---|
| Calibration preprocessing differs from training or inference (mean, std, `/255`, RGB or BGR) | Make the chain match. Put `convertColor` and `div` before `normalize`. |
| Preprocessing moved to the NPU but your app still does it | Look for `Added nodes` in `compiler.log` and remove those steps from the app. See [Preprocessing that moves to the NPU](config-reference.md#preprocessing-that-moves-to-the-npu). |
| `convertColor` is not in your app | `convertColor` never moves to the NPU: the app must do it. |
| Calibration images are few or not representative | Use about 100 or more images like your real input. |
| Quantization itself loses accuracy | Follow [Quantization](quantization.md). |

### Detection model gives wrong boxes after PPU compile

The PPU `type` does not fit the model, or the node names are wrong. There is no error in this case. Check the type table and node names on [PPU for YOLO models](ppu.md).

### pre_optimize seems to have no effect

The config also has a `ppu` block. DX-COM 2.5.0 then compiles with `ppu` and drops `pre_optimize`, and prints only `falling back to legacy: ValueError: config 'pre_optimize' and 'ppu' are mutually exclusive`. Remove one of the two. The same fallback happens in Python when `use_gpu` is not exactly `True` or `False`.

### Old pre_optimize configs fail on 2.5.0

| Message or symptom | Fix |
|---|---|
| `KeyError` with a migration hint for `yolo_postprocess` or `yolo26_postprocess` | Rename to `yolo_dfl_postprocess` or `yolo_no_dfl_postprocess`. |
| `ValueError` about `task` | Add `"task": "base"` (or `seg`, `pose`). |
| `ValueError` about `input_height` or `input_width` | Remove both keys. |

### Python arguments from 2.4 do not work

| Symptom | Fix |
|---|---|
| `InvalidValueError` for `quantization_mode` or `qat_skip_training` | Use `qmaster=QMasterConfig(...)`. See [QMasterConfig](python-api.md#qmasterconfig). |
| `qat_config` or `qat_resume_from_checkpoint` has no effect | They are ignored without an error. Use `qmaster`. |
| `UserWarning: quantization_device ... is deprecated and ignored` | Remove it. Use `use_gpu` and `CUDA_VISIBLE_DEVICES`. |
| A misspelled argument has no effect | Unknown keyword arguments are ignored. Check the spelling. |

### EnhancementSchemeError with qmaster

```text
EnhancementSchemeError: use_q_pro/enhanced_scheme (Q-PRO re-quantization) and qmaster (QAT) are mutually exclusive. Set only one.
```

Remove `use_q_pro` and `enhanced_scheme`, or remove the `qmaster` block. Q-Master problems: see [Q-Master troubleshooting](q-master.md#troubleshooting).

### ConfigFileError: Either CONFIG or DATALOADER must be provided

`dx_com.compile()` got neither `config` nor `dataloader`. Pass exactly one.

### ONNX export fails with No module named 'onnxscript'

PyTorch 2.9 and later use the dynamo exporter by default. Pass `dynamo=False` to `torch.onnx.export`, or `pip install onnxscript`. See [Export from PyTorch](onnx-models.md#export-from-pytorch).

### RequiredLibraryError: libGL.so.1 cannot be loaded

Install the OpenGL and GLib runtime: `libgl1` and `libglib2.0-0` on Debian and Ubuntu, `mesa-libGL` and `glib2` on Fedora, RHEL and CentOS (on RHEL and CentOS, enable the CRB repository first). See [Install](../get-started/install.md).

### Model with PRelu is slow on the NPU

Known issue: `PRelu` activations cause a large FPS drop. Use `LeakyRelu` or `Relu` where you can.

### Results differ between machines

Compiled results can vary with CPU architecture, OS and other hardware. Use `--float64_calibration` for the same calibration result on different CPUs.

### dxcom --version and dx_com.__version__ differ

In 2.5.0, `dxcom --version` prints `2.5.0` and `python3 -c "import dx_com; print(dx_com.__version__)"` prints `2.5.0-rc.1`. Both are the released 2.5.0 package.

## Error types

| Error type | Meaning and examples |
|---|---|
| `NotSupportError` | A feature the compiler does not support. Examples: a multi input model with the `dxcom` command, a dynamic input shape, cubic resize. |
| `ConfigFileError` | Invalid or missing JSON config (wrong path, malformed JSON), or neither config nor DataLoader given. |
| `ConfigInputError` | The `inputs` in the config do not match the ONNX model (name or shape). |
| `DataLoaderError` | The calibration tensor after preprocessing does not match the model input shape. |
| `DatasetPathError` | `dataset_path` does not exist or is not a directory. |
| `DataNotFoundError` | No valid input data in `dataset_path` (empty folder, wrong `file_extensions`). |
| `NodeNotFoundError` | The ONNX model contains a node the compiler does not support. |
| `NotsupportedPaddingError` | Unsupported padding, for example asymmetric padding in width and height. |
| `OnnxFileNotFound` | The ONNX file does not exist at the given path. |
| `RequiredLibraryError` | A system library is missing, for example `libGL.so.1` (install `libgl1` on Debian and Ubuntu). |
| `OSError` | The operating system is not supported. See [Supported environments](../get-started/compatibility.md#supported-environments). |
| `UbuntuVersionError` | The Ubuntu version is outside the supported range. |
| `LDDVersionError` | The glibc (`ldd`) version is too old. 2.31 or newer is needed. |
| `RamSizeError` | Not enough RAM. 16 GB or more is needed. |
| `DiskSizeError` | Not enough free disk space for compiling. |
| `EnhancementSchemeError` | Q-PRO (`use_q_pro` or `enhanced_scheme`) combined with `qmaster`. |
| `InvalidValueError` | An argument value is not accepted, for example the removed `quantization_mode`. |

## Next steps

* [Get started troubleshooting](../get-started/troubleshooting.md)
* [Config file reference](config-reference.md)
* [Quantization](quantization.md)
