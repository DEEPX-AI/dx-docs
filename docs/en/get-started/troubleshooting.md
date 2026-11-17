---
title: Troubleshooting
description: Fixes for common install and environment errors with the DEEPX SDK, from missing packages to driver, firmware and Docker problems.
---

# Troubleshooting

This page helps you fix the install and environment errors that people hit most often. Search this page for the error message you see.

Errors that belong to one product (compiler options, pipeline elements, app flags) are on that product's pages.

## Before you start

Collect the basic facts first:

```bash
lspci -d 1ff4:
dxcli -s
dkms status
python3 -c "import dx_engine; print(dx_engine.__version__)"
```

Compare the versions with the [version matrix](compatibility.md#version-matrix).

## Install errors

### Package libgl1-mesa-glx has no installation candidate

```text
E: Package 'libgl1-mesa-glx' has no installation candidate
```

The package does not exist on Ubuntu 24.04, Ubuntu 26.04 and Debian 12. Install `libgl1` instead:

```bash
sudo apt-get install -y --no-install-recommends libgl1 libglib2.0-0 make
```

### ImportError: libGL.so.1 when you import dx_com

```text
ImportError: libGL.so.1: cannot open shared object file: No such file or directory
```

DX-COM uses `opencv-python`, which needs the system OpenGL and GLib libraries. Install `libgl1 libglib2.0-0` (Debian, Ubuntu) or `mesa-libGL glib2` (Fedora, RHEL, CentOS) as shown in [Install](install.md#option-a-pip-recommended).

### No matching distribution found for dx-com

```text
ERROR: No matching distribution found for dx-com==2.4.0
```

`dx-com` 2.4.0 and 2.3.0 were removed from PyPI and cannot be uploaded again. Use `pip install dx-com==2.4.1` or newer (2.5.0 is current). Also check that you are on x86_64 Linux with Python 3.8 to 3.14 and glibc 2.31 or later (`ldd --version`): there are no wheels for other platforms.

### pip install dx-engine fails

The only `dx-engine` release on PyPI (3.4.0) is yanked. Install the `dx_engine` wheel that comes with DX-RT instead. With the APT or one line route the wheels are in `/usr/share/libdxrt-bin/python`, see [Install](install.md#option-a-apt-repository-recommended). With the suite clone, `./dx-runtime/install.sh` installs it into `dx-runtime/venv-dx-runtime`.

### RuntimeError on import dx_engine about a version mismatch

`import dx_engine` checks that the Python package and `libdxrt.so` have the same major.minor version. Install the wheel from `/usr/share/libdxrt-bin/python` that matches your installed `libdxrt-bin`. Only for debugging, you can skip the check with `DX_ENGINE_SKIP_VERSION_CHECK=1`.

### Crash messages after building dx_engine yourself

```text
malloc(): corrupted top size
free(): invalid pointer
double free or corruption (out)
```

The Python extension was built for a different Python version than the one you run. Rebuild it with the same interpreter, ideally in a fresh virtual environment:

```bash
python3 --version
cd python_package
pip install .
```

### The dx-runtime or dx-compiler folders are empty

You cloned `dx-all-suite` without its submodules. Fetch them:

```bash
git submodule update --init --recursive
git submodule status
```

### Modules not found: dxmz, dx_engine or dx_com

```text
bash: dxmz: command not found
ImportError: dx_engine is required for DxRuntimeSession. Please install the DeepX runtime package.
ImportError: dx_com is not installed. Install it to use compile: pip install dx_com
TypeError: compile() got an unexpected keyword argument 'calibration'
```

`dxmz`, `dx_engine` and `dx_com` must be in the same Python environment. In the suite clone, DX-ModelZoo goes into `dx-runtime/venv-dx-runtime` (`/venv-dxnn` in Docker), which has `dx_engine` but not `dx_com`. The `TypeError` means your `dx_com` is too old for DX-ModelZoo.

```bash
./getting-started/runtime-0_install_dx-runtime.sh
./getting-started/modelzoo-0_install_dx-modelzoo.sh
./getting-started/modelzoo-2_run_first_npu_model.sh
source ./dx-runtime/venv-dx-runtime/bin/activate
python3 -c "import dx_engine, dx_com; print('OK')"
```

`modelzoo-2_run_first_npu_model.sh` installs the `dx_com` version from `dx-compiler/compiler.properties` when it is missing. Use `--dx-com-wheel /path/to/dx_com-*.whl` for a local wheel whose Python tag matches the environment. For NPU evaluation only, `--skip-onnx --skip-compile` needs no `dx_com`.

## Device and driver errors

### dxcli -s shows no device

1. Check that the card is on the PCIe bus: `lspci -d 1ff4:`. If nothing is listed, reseat the card and check the BIOS settings.
1. Check that the driver modules are loaded: `lsmod | grep -E 'dxrt_driver|dx_dma'`. If not, run `sudo modprobe dx_dma` and `sudo modprobe dxrt_driver`, or restart the machine.
1. Check that DKMS built the driver for your running kernel: `dkms status` must list `dxrt-driver-dkms` as `installed` for `uname -r`.
1. If Secure Boot is on (`mokutil --sb-state`), the kernel may refuse the unsigned DKMS modules. Enroll the DKMS signing key or turn off Secure Boot, then restart.
1. Run the driver sanity check (`sudo ./sanity_check.sh` in the `dx_rt_npu_linux_driver` repository). It writes logs to `sanity/result/`; send those files to tech-support@deepx.ai if you need help.

The driver and firmware do not work in a virtual machine with PCI passthrough. Use the physical machine.

### Fail to initialize device

The sanity check or `install.sh` stops with `Fail to initialize device`. The NPU is in an unstable state. Do a cold boot: power the machine off completely, wait 10 to 30 seconds, power it on, then run `dxcli -s`.

### Firmware version mismatch

```text
The current firmware version is 2.7.4.
Please update your firmware to version 2.7.6 or higher.
```

The firmware on the NPU is older than DX-RT needs (DX-RT 3.5.0 needs 2.7.6). Update it, then cold boot:

```bash
./dx-runtime/install.sh --target=dx_fw
```

To do it by hand, see [Update the firmware](install.md#update-the-firmware). After the cold boot, `dxcli -s` must show the new `FW version`. If you cannot remove power (remote machine), `sudo reboot` is usually enough.

### Device driver version is too old

```text
[dxrt-exception] Invalid operation exception {"The current device driver version is 2.6.0.
Please update your device driver to version 2.7.0 or higher.":lib/device_version.cpp:217:CheckVersion}
```

The NPU driver is a host kernel module. Update it on the host, never inside a container, then reboot:

```bash
sudo apt update && sudo apt install dxrt-driver-dkms
sudo reboot
dxcli -s | grep -A2 Version
```

In the suite clone, `./dx-runtime/install.sh --target=dx_rt_npu_linux_driver` does the same. Rebuilding a Docker image updates DX-RT inside it but never the host driver, so always update both together.

### Model compiler version is not compatible

```text
The model's compiler version(2.5.0) is not compatible with this RT library.
Please downgrade the RT library version to ... or use a model file generated with a compiler version ... or higher.
```

The `.dxnn` file and DX-RT come from different SDK releases. The safest fix is to recompile the model with the DX-COM from the same row of the [version matrix](compatibility.md#version-matrix) as your DX-RT. The other fix is to install the DX-RT that matches the model; then also check the driver and firmware minimums for that DX-RT ([table](compatibility.md#minimum-driver-and-firmware-for-dx-rt)).

## Docker errors

### Container keeps restarting: Other instance of dxrtd is running

`docker ps` shows `Restarting (255)` and `docker logs dx-runtime-ubuntu-24.04` prints `Other instance of dxrtd is running`. Only one `dxrtd` may run on the whole machine (host plus containers).

Stop the host service and start the container again:

```bash
sudo systemctl stop dxrt.service
./docker_run.sh --target=dx-runtime --ubuntu_version=24.04
```

If the host service must keep running, start the container without its own `dxrtd`. With plain Docker, use `--entrypoint bash` together with `--ipc=host --pid=host --network=host`. With our compose file, override the entrypoint of the `dx-runtime` service in `docker/docker-compose.yml`:

```yaml
services:
  dx-runtime:
    entrypoint: ["/bin/sh", "-c"]
    command: ["sleep infinity"]
```

To run several runtime containers, keep `dxrtd` in only one of them (or on the host) and start it by hand there with `dxrtd &`.

### IPC_CONNECT_FAILED inside a container

The container cannot reach `dxrtd`. The service listens on an abstract Unix socket, which is private to each network namespace. Start the container with `--network=host` (plus `--ipc=host --pid=host`).

### No such container: dx-runtime-24.04

The containers are named `dx-<target>-<os>-<version>`, for example `dx-runtime-ubuntu-24.04` and `dx-compiler-ubuntu-24.04`. List them:

```bash
docker ps --format '{{.Names}}'
docker exec -it dx-runtime-ubuntu-24.04 bash
```

### python: command not found or No module named dx_engine in a container

`dx_engine` is installed in `/venv-dxnn`. Interactive shells activate it, non interactive commands do not:

```bash
docker run --rm --privileged --ipc=host --pid=host --network=host -v /dev:/dev \
    --entrypoint bash ghcr.io/deepx-ai/dx-runtime:rt-app-stream \
    -c 'source /venv-dxnn/bin/activate && python -c "import dx_engine"'
```

### Insufficient shared memory (shm)

```text
[ResourceError]: Insufficient shared memory (shm). Increase the available /dev/shm size (e.g. --shm-size for Docker).
```

Docker gives containers 64 MB of `/dev/shm`, which DX-COM can exceed on large models. With plain Docker, add `--shm-size=256m` (or `--shm-size=1g` for large models) to `docker run`. With `docker_run.sh`, enable the `shm_size` line of the `dx-compiler` service in `docker/docker-compose.yml`, then recreate the container:

```yaml
services:
  dx-compiler:
    shm_size: '1gb'
```

```bash
docker compose -f docker/docker-compose.yml down --remove-orphans
./docker_run.sh --target=dx-compiler --ubuntu_version=24.04
```

### X11 warnings or error mounting /tmp/.docker.xauth

`docker_run.sh` warns that you should use an X11 session, or the container fails with `error mounting /tmp/.docker.xauth` after a reboot or logout. Wayland sessions lose the X authentication data. Switch the login session to Xorg (Ubuntu with GDM):

```bash
sudo nano /etc/gdm3/custom.conf
```

Set this line in the `[daemon]` section (remove the `#` in front of it):

```text
WaylandEnable=false
```

Then restart GDM (or the machine) and recreate the containers:

```bash
sudo systemctl restart gdm3
docker compose -f docker/docker-compose.yml down --remove-orphans
./docker_run.sh --target=dx-runtime --ubuntu_version=24.04
```

### Mount error after you recreated a host folder

```text
Error response from daemon: mount .../dx-all-suite/dummy_xauthority:..., flags: 0x5000: not a directory
```

A bind mount points to the folder or file that existed when the container started. If you delete and recreate it (for example `workspace/` or `dummy_xauthority`), Docker may create a directory where a file belongs. Restore the file and restart the container:

```bash
rmdir dummy_xauthority && touch dummy_xauthority
./docker_run.sh --target=dx-modelzoo --ubuntu_version=24.04
```

### The NVIDIA GPU image does not start: unsatisfied condition cuda>=12.8

The default CUDA 12.8.1 image needs NVIDIA driver R570 or newer (`nvidia-smi` must show CUDA Version 12.8 or higher). Update the driver, or build with an older `--cuda_version` that your driver supports. Also install the NVIDIA Container Toolkit: `sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker`.

## Model Zoo download and dataset errors

### Model download times out

`dxmz eval` downloads missing models from `DXMZ_MODEL_URL` (by default `https://sdk.deepx.ai/modelzoo`). If outbound TCP 443 to `sdk.deepx.ai` is blocked, the download fails after a 60 second timeout per address:

```bash
getent ahosts sdk.deepx.ai
timeout 15 nc -4 -vz -w 10 sdk.deepx.ai 443
env | grep -i proxy
```

Allow the connection or set a proxy (`export HTTPS_PROXY=http://<proxy_host>:<port>`). Offline, copy the files to `getting-started/modelzoo/models/<model>/<model>.onnx` and `<model>_<profile>.dxnn`. If the log says `To enable auto-download, set DXMZ_MODEL_URL environment variable`, the file `dx-modelzoo/.env` is missing: run `./getting-started/modelzoo-1_prepare_assets.sh`.

### Dataset not found

```text
DatasetValidationError: Dataset validation failed for ILSVRC2012: Expected 50000 images in .../ILSVRC2012/val, but found 0.
```

DX-ModelZoo never downloads datasets. Put the full ImageNet validation set (1,000 class folders, 50,000 images) in `getting-started/modelzoo/datasets/ILSVRC2012/val`, or link an existing copy:

```bash
ln -s /path/to/ILSVRC2012 getting-started/modelzoo/datasets/ILSVRC2012
```

In Docker, mount it read only with `DX_DATASETS_PATH=/mnt/datasets ./docker_run.sh --target=dx-modelzoo --ubuntu_version=24.04` and run the script with `DATA_ROOT=/deepx/datasets`.

## Windows errors

| Problem | What to check |
|---|---|
| Device not detected | Seating of the PCIe or M.2 card, warnings in Device Manager. Use **Installation Status Diagnostics** and **Rescan** in the installer, or run **Repair**. |
| `dxrtd` does not start | Run `dxrtd.exe` from the intended `bin` folder to see the error; check permissions, Windows Firewall and antivirus. |
| Source build fails | Visual Studio 2022 with **Desktop development with C++**. Run `build.bat rebuild`. |
| `dxrt.dll` or `onnxruntime.dll` not found | Keep `dxrt.dll`, `onnxruntime.dll` and `onnxruntime_providers_shared.dll` together, ideally next to your executable. |

## Next steps

* [Install again step by step](install.md)
* [Check component versions](compatibility.md)
* [NPU driver and firmware details](../runtime/driver-firmware.md)
