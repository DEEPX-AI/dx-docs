---
title: Install DX-ModelZoo
description: Install DX-ModelZoo from source, choose the CPU or GPU ONNX Runtime, and set the model and dataset paths.
---

# Install DX-ModelZoo

This page shows the setup steps that are specific to DX-ModelZoo: installing the `dxmz` tool, picking the ONNX Runtime build and setting the paths it uses.

## Before you start

* Linux on x86-64 (on Windows, use WSL2).
* Python 3.8 to 3.14.
* The DEEPX SDK installed as described in [Install the DEEPX SDK](../../get-started/install.md). DX-ModelZoo uses two of its parts:

| Part | Needed for | Version |
|---|---|---|
| DX-RT Python package `dx_engine` | NPU evaluation (`c-lite`, `q-lite`, `q-pro` profiles) | DX-RT 3.5.0 or newer, built with ONNX Runtime support (`USE_ORT=ON`) |
| DX-COM Python package `dx-com` | `dxmz compile` | 2.5.0 or newer |

ONNX evaluation works without either of them. Install DX-ModelZoo into the same Python environment as `dx_engine`, or NPU evaluation fails with `dx_engine is required for DxRuntimeSession`.

!!! note "Compiled models need DX-RT 3.5.0"
    The `.dxnn` files that DX-ModelZoo 1.0.0 downloads use container format v9. Older DX-RT releases cannot load them.

## Option A: install with the SDK script

If you cloned the DEEPX SDK repository ([dx-all-suite](https://github.com/DEEPX-AI/dx-all-suite)), its `getting-started` folder has scripts that install DX-ModelZoo into the DX-RT environment and run a first model.

```bash
cd dx-all-suite
./getting-started/modelzoo-0_install_dx-modelzoo.sh
./getting-started/modelzoo-1_prepare_assets.sh
./getting-started/modelzoo-2_run_first_npu_model.sh
```

| Script | What it does |
|---|---|
| `modelzoo-0_install_dx-modelzoo.sh` | Runs `pip install -e "dx-modelzoo[cpu]"` in the DX-RT environment (`dx-runtime/venv-dx-runtime` on the host, `/venv-dxnn` in a container). Skips the install when `dxmz` already works. |
| `modelzoo-1_prepare_assets.sh` | Creates `getting-started/modelzoo` with `models/`, `datasets/` and `result/`, and copies `dx-modelzoo/.env.example` to `dx-modelzoo/.env` when `.env` is missing. |
| `modelzoo-2_run_first_npu_model.sh` | Runs `dxmz info`, ONNX evaluation, `dxmz compile` and NPU evaluation for `resnet50_224x224` with the `q-lite` profile. Installs `dx-com` when it is missing. |

Options of `modelzoo-0_install_dx-modelzoo.sh`:

| Option | Meaning | Default |
|---|---|---|
| `--source PATH` | DX-ModelZoo source folder | `<dx-all-suite>/dx-modelzoo` |
| `--venv PATH` | Python environment to install into | `dx-runtime/venv-dx-runtime` (host), `/venv-dxnn` (container) |
| `--extra NAME` | pip extra: `cpu` or `gpu` | `cpu` |
| `-f`, `--force` | Reinstall even if `dxmz` already works | off |

Options of `modelzoo-2_run_first_npu_model.sh`:

| Option | Meaning | Default |
|---|---|---|
| `--model NAME` | Model name or YAML path | `resnet50_224x224` |
| `--profile NAME` | NPU profile: `c-lite`, `q-lite` or `q-pro` | `q-lite` |
| `--venv PATH` | Python environment with `dxmz` | same as above |
| `--dx-com-wheel PATH` | Install DX-COM from a local wheel instead of pip | pip package |
| `--skip-onnx` | Skip the ONNX baseline evaluation | off |
| `--skip-compile` | Skip compilation and use an existing or downloaded `.dxnn` | off |

The scripts read `DATA_ROOT` and `MODEL_ROOT` from the environment, so you can point them at existing folders:

```bash
DATA_ROOT=/data/datasets ./getting-started/modelzoo-2_run_first_npu_model.sh
```

## Option B: install from source

1. Clone the repository.

    ```bash
    git clone https://github.com/DEEPX-AI/dx-modelzoo.git
    cd dx-modelzoo
    ```

1. Activate the Python environment that has `dx_engine` (and `dx-com` if you want to compile).

1. Install DX-ModelZoo with exactly one ONNX Runtime build.

    === "CPU"

        ```bash
        pip install -e ".[cpu]"
        ```

    === "GPU (CUDA)"

        ```bash
        pip install -e ".[gpu]"
        ```

1. Check that the CLI works.

    ```bash
    dxmz --help
    ```

You can use `uv pip install -e ".[cpu]"` instead of pip for faster dependency resolution.

!!! warning "Do not install both ONNX Runtime builds"
    `onnxruntime` and `onnxruntime-gpu` provide the same Python module. Remove one before you install the other, then check that `pip list | grep onnxruntime` shows exactly one entry.

    ```bash
    # CPU to GPU
    pip uninstall -y onnxruntime && pip install -e ".[gpu]"
    # GPU to CPU
    pip uninstall -y onnxruntime-gpu && pip install -e ".[cpu]"
    ```

## Extras

| Extra | Installs | Use it for |
|---|---|---|
| `cpu` | `onnxruntime>=1.15` | ONNX evaluation on CPU |
| `gpu` | `onnxruntime-gpu>=1.17` and the NVIDIA CUDA 12 libraries (`nvidia-cublas-cu12`, `nvidia-cudnn-cu12` and others) | ONNX evaluation on an NVIDIA GPU |
| `dev` | `pytest`, `pytest-asyncio`, `pytest-cov`, `ruff`, `pre-commit`, `yamllint` | Testing and linting |
| `all` | `cpu`, `dev` and `docs` | Everything for contributors |

The core dependencies are large: they include `torch`, `torchvision`, `transformers` and `open_clip_torch`, next to `numpy`, `opencv-python`, `pyyaml` and others. See `pyproject.toml` in the repository for the full list.

## GPU setup

The `gpu` extra installs the CUDA and cuDNN libraries with pip. You need an NVIDIA GPU supported by CUDA 12 and NVIDIA driver 535 or newer.

After installing `.[gpu]`, add the NVIDIA library paths to `LD_LIBRARY_PATH` (for example in `~/.bashrc`, after you activate the environment):

```bash
export LD_LIBRARY_PATH=$(python -c "import nvidia.cublas.lib; print(nvidia.cublas.lib.__path__[0])"):$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$(python -c "import nvidia.cudnn.lib; print(nvidia.cudnn.lib.__path__[0])"):$LD_LIBRARY_PATH
```

The `onnx` profile of most models sets `runtime.device: gpu`. Without a working GPU, ONNX Runtime falls back to the CPU.

## Set paths and the download URL

`dxmz` reads these environment variables. It also loads a `.env` file (copy `.env.example` in the repository root to `.env`). Variables that are already exported win over `.env`, and the `--data-root` and `--model-root` options win over both.

```bash
cp .env.example .env
```

```text
DXMZ_MODEL_URL=https://sdk.deepx.ai/modelzoo
MODEL_ROOT=download/models
DATA_ROOT=download/datasets
# DXNN_DEVICES=0
# ONNX_ASYNC_WORKERS=4
```

| Variable | Meaning | CLI override |
|---|---|---|
| `DATA_ROOT` | Root folder of the evaluation datasets. Model YAMLs use `${DATA_ROOT}/<dataset>`. | `--data-root` |
| `MODEL_ROOT` | Root folder of the model files. Model YAMLs use `${MODEL_ROOT}/<model name>`. | `--model-root` |
| `DXMZ_MODEL_URL` | Base URL for downloading missing `.onnx` and `.dxnn` files. Without it, a missing model file is an error. | none |
| `DXNN_DEVICES` | NPU device IDs for NPU sessions, comma separated, for example `0,1`. | none |
| `ONNX_ASYNC_WORKERS` | Thread count for asynchronous ONNX inference. Default: the number of CPU cores, at least 4. | none |

Relative paths such as `download/models` are relative to the folder you run `dxmz` in.

## Use the container image

DEEPX SDK 2.5.0 publishes a prebuilt DX-ModelZoo image for `linux/amd64`:

```bash
docker pull ghcr.io/deepx-ai/dx-modelzoo:latest
```

## Next steps

* [Evaluate models](evaluate.md)
* [Datasets](datasets.md)
* [CLI reference](cli.md)
