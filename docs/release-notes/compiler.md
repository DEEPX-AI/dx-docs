---
title: DX-COM release notes
description: Changes in each DX-COM compiler release, newest first.
---

# DX-COM release notes

This page lists what changed in each DX-COM release, newest first. DX-COM ships in the DX-Compiler bundle of the DEEPX SDK; we list each change under the DX-COM version that brought it.

## DX-COM 2.5.0 (2026-10-23)

Part of DEEPX SDK 2.5.0.

!!! warning "Upgrade notes"
    * `.dxnn` files from 2.5.0 use file format v9 and need DX-RT 3.5.0 or later. DX-RT 3.4.2 and earlier cannot load them.
    * DX-TRON is removed. Use the [summary report](../compiler/summary-report.md) (`--export_html`).
    * `pre_optimize` pass names and keys changed. See [Changed](#changed).

### Added

* `--use_gpu {True,False}` (CLI) and `use_gpu` (Python): quantize on GPU (default, when available) or force CPU. Pick a GPU with `CUDA_VISIBLE_DEVICES`.
* `--verbose` (CLI) and `verbose` (Python): expand masked error messages with the origin type, the original message and one direct cause.
* `QMasterConfig`, the public Q-Master configuration object, exported from `dx_com`.
* Q-Master for segmentation models: `task_type`, `seg_root`, `seg_pairs_train`, `seg_pairs_val`, `seg_ignore_index`, `seg_binary` and the `seg_ce` loss.
* `pre_optimize`: `task` key (`base`, `seg`, `pose`) with pose support for both YOLO passes and segmentation for YOLO26.
* `pre_optimize`: new `rtmdet_postprocess` pass for RTMDet detection.
* `Gather` accepts 2D `indices`.
* `Einsum` with two inputs that reduce to a (batched) matrix multiplication, for example `ij,jk->ik`.
* `Conv` and `ConvTranspose` with 5D input (3 spatial axes) run on the NPU, with constraints such as `group` 1, no dilation and a constant weight.
* Installer: one line install from PyPI (`oneline-install.sh`) and `oneline-uninstall.sh`; `install.sh` uses uv when available (`--uv=true` or `--uv=false`).

### Changed

* `.dxnn` file format v9 only. Needs DX-RT 3.5.0 or later.
* `dx_com.compile()` takes keyword arguments (`**kwargs`). Call it with keyword arguments.
* `quantization_device` (JSON and Python) is deprecated and ignored with a `UserWarning`. Use `use_gpu` and `CUDA_VISIBLE_DEVICES`.
* QAT Python arguments `quantization_mode`, `qat_config`, `qat_skip_training` and `qat_resume_from_checkpoint` are replaced by `qmaster=QMasterConfig(...)`. A JSON `qmaster` block works as before.
* Breaking: `pre_optimize` passes renamed: `yolo_postprocess` to `yolo_dfl_postprocess`, `yolo26_postprocess` to `yolo_no_dfl_postprocess`. Old names raise an error.
* Breaking: YOLO `pre_optimize` passes need `task`. `input_height` and `input_width` are removed and raise `ValueError`.
* Documented `Resize` scale factors: `nearest` upsampling by powers of two only; `linear` upsampling by integers 2 or larger except primes above 8; downsampling only `linear` at 0.5.
* Installer: `install.sh` without `--python_version` uses the OS default `python3`.

### Removed

* DX-TRON: the `dx_tron` install target, the `dxtron` app and its launcher scripts. `--target=dx_tron` now exits with an explanation. Remove an installed DEB with `sudo apt-get remove dxtron`.

## DX-COM 2.4.1 (2026-09-03)

Part of DEEPX SDK 2.4.3 (DX-Compiler bundle 2.4.2).

### Changed

* Smaller `.dxnn` files: redundant metadata removed.

### Fixed

* Minor bug fixes and stability improvements.

!!! note
    `dx-com` 2.4.0 and 2.3.0 were removed from PyPI by mistake and cannot be installed with `pip`. Use 2.4.1 or later.

## DX-COM 2.4.0 (2026-07-22)

The DX-Compiler bundle 2.4.1 (2026-08-14) contained DX-COM 2.4.0 with documentation fixes only.

### Added

* Automatic Q-PRO (`--use_q_pro`): DX-COM creates DXQ combinations and picks the stages for you.
* Q-Master quantization aware training, turned on by a `qmaster` block in the JSON config, with the `fast_run` smoke test.
* QXNN resume: re-quantize from a checkpoint without recompiling (`--checkpoint`).
* Quantization diagnosis report (`--quant_diagnosis`).
* Interactive HTML graph viewer (`--export_html`), the replacement for DX-TRON.
* `dx_com.pre_optimize()` API with YOLO post processing passes.
* Python 3.13 and 3.14 support.
* Validated on Ubuntu 26.04.

### Changed

* PPU type 2 is deprecated and prints a warning. Use `dx_com.pre_optimize()`.
* DX-TRON is deprecated.
* Faster compile and lower memory use, mostly on large models.
* Installer: supports Fedora 42 to 45, RHEL 9 to 10 and CentOS Stream 9 to 10; installs `dx-com` from PyPI; runs without prompts.

### Fixed

* Python API: models that expect integer inputs were sometimes fed float data.
* Several Q-PRO and DXQ crashes.
* Compile and runtime errors from tiling, partitioning and memory allocation in models with `Split`, `Concat`, `Reshape`, bilinear `Resize`, `Clip` or odd spatial sizes.
* Compatibility with NumPy 2.4 and later and onnxruntime 1.25.0 and later.
* Grayscale conversion no longer squeezes the channel axis, so grayscale configs look like RGB configs.

### Known issues

* Models with `PRelu` activations show a large FPS drop.

## DX-COM 2.3.0 (2026-04-10)

The DX-Compiler bundle 2.3.1 (2026-05-06) contained DX-COM 2.3.0 with uninstaller fixes only.

### Added

* TopK first post processing for DFL based YOLO models (PPU type 2).
* Batched convolution.
* Validated on Fedora 42 to 45, RHEL 9 to 10 and CentOS Stream 9 to 10.

### Changed

* Looser Python package dependency limits.
* The standalone DX-COM executable is deprecated. Use the Python wheel.
* Lower NPU latency for most models and faster compiles.

### Fixed

* Compiler stability issues.

### Known issues

* `PRelu` models show a large FPS drop.
* OSNet0_5, RepVGGA2, YoloV9C and the DnCNN models show accuracy that varies with the host CPU and calibration dataset.

## DX-COM 2.2.1 (2026-02-09)

### Added

* `quantization_device` in the JSON config for GPU quantization from the CLI (deprecated in 2.5.0).
* GPU auto detection: without `quantization_device`, DX-COM uses a CUDA GPU when available.

### Fixed

* DXQ enhanced quantization bugs.
* PPU compile bug in the wheel for Python 3.8, 3.9 and 3.10.
* Invalid model input names no longer compile without an error.

## DX-COM 2.2.0 (2026-01-16)

### Added

* Python wheel package (`dx_com.compile()`) for Python 3.8 to 3.12, with calibration from a PyTorch `DataLoader`.
* Multi input models through the Python API.
* PPU support for YOLOv8, YOLOv9, YOLOv10, YOLOv11 and YOLOv12.

### Fixed

* Accuracy drop of the DX-ModelZoo `DeepLabV3PlusMobilenet-1` model.

## DX-COM 2.1.0 (2025-11-28)

### Added

* CLI options `--aggressive_partitioning`, `--opt_level {0,1}`, `--compile_input_nodes` and `--compile_output_nodes`.
* `Gather` operator.
* DXQ enhanced quantization (`enhanced_scheme`, DXQ-P0 to DXQ-P5) is back.
* PPU support is back, for YOLOv3, YOLOv4, YOLOv5, YOLOv7 and YOLOX.

### Changed

* Removed CLI options `--jobs`, `--shrink` and `--info` (`-i`).
* No more restrictions on `Split`, `Transpose`, `Reshape`, `Flatten` and `Slice`.
* ONNX opset 11 to 21 supported; 22 and later are not.

### Known issues

* Accuracy drop of the DX-ModelZoo `DeepLabV3PlusMobilenet-1` model.

## DX-COM 2.0.0 (2025-09-08)

### Added

* `Softmax` and `Slice` supported again; new `ConvTranspose`.
* Partial support for Vision Transformer models, checked with OpenCLIP ViT-L-14, ViT-L-14-336, ViT-L-14-quickgelu, RN50x64, RN50x16, ViT-B-16, ViT-B-32-256 and ViT-B-16-quickgelu.

### Changed

* Compatibility with DX-RT before 3.0.0 is not guaranteed.
* DXQ (`enhanced_scheme`) and the PPU were removed in this version (both came back in 2.1.0).

## DX-COM 1.0.0 (2025-07-23)

### Added

* `-v` prints the DX-COM version. `-i` printed internal module information (removed in 2.1.0).

### Changed

* `Softmax` and `Slice` were deprecated (supported again in 2.0.0).
* Internal bug fixes.

## Next steps

* [DX-COM compiler](../compiler/index.md)
* [All release notes](index.md)
