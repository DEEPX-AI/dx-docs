---
title: Set up the tutorials
description: Start JupyterLab for the dx-tutorials notebooks, point them at the SDK and verify your NPU.
---

# Set up the tutorials

This page lets you start the JupyterLab tutorials and confirm that the SDK and your NPU work.

The notebooks come from the [dx-tutorials](https://github.com/DEEPX-AI/dx-tutorials) repository. Tutorial T00 is a short JupyterLab primer and T01 installs and verifies the SDK.

## Before you start

* Linux: Ubuntu 20.04, 22.04, 24.04 or 26.04, or Debian 12 or 13.
* A DEEPX NPU: DX-M1, DX-M1M or DX-H1 Quattro.
* 8 GB RAM (16 GB for DX-COM) and at least 40 GB of free disk space.
* x86_64 for DX-COM and DX-RT; aarch64 hosts run DX-RT only.
* `sudo` rights for the SDK installers.

## Steps

1. Install the system packages:

    ```bash
    sudo apt-get update
    sudo apt-get install python3-venv build-essential python3-dev git ffmpeg tree curl cmake
    ```

1. Install `uv`:

    ```bash
    sudo apt-get install -y pipx
    pipx install uv
    pipx ensurepath && exec $SHELL
    uv --version
    ```

1. Clone the tutorials and start JupyterLab:

    ```bash
    git clone --depth 1 --single-branch https://github.com/DEEPX-AI/dx-tutorials.git
    cd dx-tutorials
    ./run-jupyter-lab.sh
    ```

    The script creates `.venv` from `requirements.txt` and starts JupyterLab without activating it. Notebook cells therefore see the system `python3`, and the SDK installers create their own Python environments.

1. Open `notebooks/T00-JupyterLab-QuickStart/jupyterlab_quickstart.ipynb` if you are new to JupyterLab. It covers cells, kernels, `!` shell commands, interrupting a cell and shortcuts.

1. Open `notebooks/T01-Getting-Started/getting_started.ipynb`. It clones the SDK (`dx-all-suite`, branch `main`, release 2.5.0) to `~/dx-all-suite`, installs DX-COM and DX-RT and runs the checks below. The install commands are the ones on [Install](../get-started/install.md). Reboot after the NPU driver install.

1. Tell the notebooks where the SDK is, if it is not in `~/dx-all-suite`:

    ```bash
    python tutorial_paths.py --set ~/my/dx-all-suite
    python tutorial_paths.py --show
    ```

    The notebooks look in this order: the `DX_ALL_SUITE_DIR` environment variable, `config.json` in the repository root (written by T01), the folders `~/dx-all-suite` and `../dx-all-suite`, then the default `~/dx-all-suite`.

1. Download the 24 sample models that the later tutorials use:

    ```bash
    cd ~/dx-all-suite/dx-runtime/dx_app
    bash setup.sh --no-force --models sfa3d_608x608 deepmar_resnet50 ResNet50 \
      depth_anything_v2_vits-1 ViT-B-32-256-datacomp_s34b_b86k-1 3ddfa_v2_mobilnet0.5_120x120 \
      SCRFD500M mediapipe-hand-detector-1 HandLandmarkLite_1 DnCNN_15 zero_dce_pp-1 \
      yolo26s-seg superpoint-1 yolo26s-obb yolo26s YOLOV12N_PPU yolopv2-1 yolo26s-pose \
      pidnet-s-1 RealESRGAN_x4-1 YoloV7 YoloV7_PPU yolov8s_pose yolov8n_seg
    ```

    !!! warning
        Do not run `setup.sh` with empty answers to its prompts. That selects every model (about 500) and downloads many gigabytes.

## Expected result

Run these checks in a terminal after the reboot:

```bash
lsmod | grep dxrt
ls /dev/dxrt*
systemctl status dxrt.service
dxcli -s
```

You see the `dxrt_driver` and `dx_dma` modules, the device `/dev/dxrt0`, `dxrt.service` in the `active (running)` state and your NPU in the `dxcli` status. The models are in `~/dx-all-suite/workspace/res/models`.

## Notes on `sudo` in notebook cells

A notebook cell cannot answer a password prompt. The install cells first run `sudo -n true`: when `sudo` works without a password they run the installer in the cell, otherwise they print the commands for a terminal (File > New > Terminal). Run the printed commands in a terminal. The repository also ships `sudo_no_password.sh`, which gives the whole `sudo` group passwordless root. Use it only on a personal lab machine and undo it with `sudo rm /etc/sudoers.d/sudo-nopasswd`.

## Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| `sudo: a terminal is required to read the password` | No passwordless `sudo` | Run the printed commands in a terminal |
| `fatal: destination path ... already exists` | Other files at the target folder | Move them, or choose another folder with `tutorial_paths.py --set` |
| `ls: cannot access '/dev/dxrt*'` | Driver not loaded, usually no reboot yet | Reboot, then check `lsmod \| grep dxrt` |
| `Active: failed` for `dxrt.service` | Driver and firmware do not match | `sudo systemctl restart dxrt.service`; if it fails again, rerun `./dx-runtime/install.sh --runtime-only` |
| `setup.sh` reports an unknown model name | Names are case sensitive | Check names with `grep name scripts/modelzoo_manifest.json` in `dx_app` |

## Next steps

* [Run the DX-APP examples](dx-app.md)
* [Run models with DX-RT](runtime.md)
* [Platform notes](platform-notes.md)
