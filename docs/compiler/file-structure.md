---
title: File structure
description: The folders that the dx-compiler install script creates for sample models, calibration data and compiled output.
---

# File structure

After running `install.sh` from the cloned repository, the working directory is organised as follows.

```
dx_com/
├── sample_models/        # Sample model assets
│   ├── onnx/             # Sample ONNX models
│   └── json/             # Sample JSON config files
├── calibration_dataset/  # Sample calibration dataset
└── output/               # Compiled .dxnn files (created by 3-compile_sample_models.sh)
```

!!! note
    This structure applies to the **local repository install** only. If you installed via `pip install dx-com` or the one-line script, only the `dxcom` command and `dx_com` Python module are placed on your system. There is no `dx_com/` working directory.

## Directories

**`sample_models/`**

Contains the ONNX models and JSON configuration files downloaded during `install.sh`. These are used by the sample compilation scripts.

- `onnx/`: sample ONNX model files used as compiler input
- `json/`: sample JSON configuration files paired with each model; see [Config file reference](config-reference.md)

**`calibration_dataset/`**

Sample image dataset used for INT8 quantization calibration. Downloaded during `install.sh` via `example/2-download_sample_calibration_dataset.sh`.

**`output/`**

Output directory for compiled `.dxnn` files. Created automatically when you run `example/3-compile_sample_models.sh` or specify it with `-o output/` in `dxcom`.

## Sample scripts

The `example/` directory in the repository contains three helper scripts:

| Script | Purpose |
|---|---|
| `1-download_sample_models.sh` | Downloads the sample ONNX models and JSON configs to `dx_com/sample_models/` |
| `2-download_sample_calibration_dataset.sh` | Downloads the calibration dataset to `dx_com/calibration_dataset/` |
| `3-compile_sample_models.sh` | Runs all sample compilations and writes `.dxnn` files to `dx_com/output/` |

Run them in order on a fresh clone:

```bash
./example/1-download_sample_models.sh
./example/2-download_sample_calibration_dataset.sh
./example/3-compile_sample_models.sh
```
