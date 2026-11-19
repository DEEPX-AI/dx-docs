---
title: Install
description: Install the NPU driver, DX-RT and firmware on the device, DX-COM on the host, or use our Docker images, then verify the setup.
---

# Install

<!-- ----------------------------------------------------------------
  EDITING NOTE
  The two quick-install blocks below are pulled in from shared snippet
  files. Do NOT edit them here — your changes will be overwritten.
  Edit the source files instead:
    - docs/snippets/install-compiler.md  (compiler / DX-COM)
    - docs/snippets/install-runtime.md   (runtime / DX-RT)
  These snippets are also included in:
    - docs/en/compiler/index.md
    - docs/en/runtime/index.md
----------------------------------------------------------------- -->
--8<-- "en/snippets/install-compiler.md"

For more install options (one-line script, repository clone, Docker), see [Host: DX-COM](#host-dx-com) below.

---

--8<-- "en/snippets/install-runtime.md"

For full details — firmware flashing, Python package, Windows, Docker and building from source — see the [detailed sections below](#device-driver-runtime-and-firmware).

---

This page covers the full DEEPX SDK 2.5.0: the runtime stack on the machine with the NPU and both parts together through Docker.

## Before you start

Find out which part you need. A machine with an NPU that you also compile on needs both parts.

| Machine | You install | Architecture | Operating system |
|---|---|---|---|
| Device (has a DEEPX NPU) | NPU driver, DX-RT, firmware. Optional: DX-APP, DX-Stream, DX-ModelZoo | x86_64 (`amd64`), aarch64 (`arm64`) | Ubuntu 20.04, 22.04, 24.04, 26.04; Debian 12, 13. Windows 10 22H2 or later, see [Windows](#windows) |
| Host (compiles models) | DX-COM | x86_64 only | Ubuntu 20.04 to 26.04, Debian 11 or later, Fedora 42 to 45, RHEL 9 and 10, CentOS Stream 9 and 10 (glibc 2.31 or later) |

You also need:

* `sudo` rights on the machine.
* Internet access to GitHub, PyPI and `apt.releases.deepx.ai`.
* For the device: the NPU seated in a PCIe or M.2 slot of a bare metal machine. Virtual machines with PCI passthrough are not supported for the driver and firmware.
* For the host: at least 16 GB RAM and 8 GB free disk space. A first DX-COM install downloads several GB (it pulls in `torch` and `onnxruntime`).

Check that the device sees the NPU on the PCIe bus (vendor ID `1ff4`):

```bash
lspci -d 1ff4:
```

If this prints nothing, the card is not detected. Check the slot and BIOS settings before you continue.

## Choose a route

| Route | Installs | Best for |
|---|---|---|
| [Device: APT repository](#option-a-apt-repository-recommended) (recommended) | NPU driver, DX-RT, `dx_engine`; firmware in a separate step | Most Ubuntu and Debian devices; upgrades with `apt` |
| [Device: one line script](#option-b-one-line-script) | NPU driver, DX-RT, firmware | A quick runtime only setup without cloning |
| [Device: full suite clone](#option-c-full-suite-clone) | Everything, including DX-APP, DX-Stream and DX-ModelZoo, plus the getting started scripts | Running our demos and example apps |
| [Device: from source](#option-d-from-source) | Driver and DX-RT built on your machine | Custom kernels, cross compiling, development |
| [Host: pip](#option-a-pip-recommended) (recommended) | DX-COM | Every supported host |
| [Docker](#docker) | Prebuilt or locally built images for runtime, compiler and model zoo | Isolated setups and CI |

## Device: driver, runtime and firmware

### The restart rule

You restart the device once, at the end of the install:

* **The firmware was updated** (any route that flashes firmware): do a cold boot. Shut the machine down, remove power for 10 to 30 seconds, then power it on. A plain `sudo reboot` may not reset the NPU. On a remote machine where you cannot remove power, use `sudo reboot`; in most cases it is enough.
* **Only the driver or DX-RT changed**: run `sudo reboot` once so the kernel loads the new NPU driver.

One cold boot covers both cases. You never need a cold boot followed by a reboot.

### Option A: APT repository (recommended)

The NPU driver and DX-RT are published as Debian packages for Ubuntu and Debian on `amd64` and `arm64`.

1. Download our signing key and check its fingerprint:

    ```bash
    wget -O deepx-archive-keyring.asc https://apt.releases.deepx.ai/gpg
    gpg --show-keys deepx-archive-keyring.asc
    ```

    The output must contain exactly this fingerprint:

    ```text
    pub   rsa4096 2026-08-11 [SCEA]
          3A20CC853C64AE328D0F58CFD816AAC6689DBDEA
    ```

    !!! warning "Stop if the fingerprint differs"
        If the fingerprint is not `3A20CC853C64AE328D0F58CFD816AAC6689DBDEA`, do not install the key. Delete `deepx-archive-keyring.asc` and contact tech-support@deepx.ai.

1. Install the key and add the repository:

    ```bash
    sudo gpg --dearmor -o /usr/share/keyrings/deepx-archive-keyring.gpg deepx-archive-keyring.asc
    rm deepx-archive-keyring.asc
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/deepx-archive-keyring.gpg] https://apt.releases.deepx.ai $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") main" | sudo tee /etc/apt/sources.list.d/deepx.list
    ```

1. Install the driver and the runtime:

    ```bash
    sudo apt update
    sudo apt install dxrt-driver-dkms
    sudo apt install libdxrt-bin
    ```

    | Package | Contents |
    |---|---|
    | `dxrt-driver-dkms` | NPU kernel driver. DKMS builds it for your running kernel and rebuilds it on every kernel update. Pulls in `dkms` and `build-essential`. |
    | `libdxrt-bin` | Prebuilt DX-RT library (`/usr/local/lib/libdxrt.so`), headers (`/usr/local/include/dxrt`), CMake package (`/usr/local/lib/cmake/dxrt`), the tools `dxcli`, `dxrun`, `dxparse`, `dxtop`, `dxbenchmark`, and the `dxrt` service (`dxrtd`), which it enables and starts. |

1. Install the `dx_engine` Python package into a virtual environment. `libdxrt-bin` does not install it for you; it stages one wheel per Python version (3.8 to 3.14) in `/usr/share/libdxrt-bin/python`:

    ```bash
    sudo apt install python3-venv
    python3 -m venv ~/dx-venv
    source ~/dx-venv/bin/activate
    PYTAG=cp$(python -c 'import sys; print(f"{sys.version_info[0]}{sys.version_info[1]}")')
    pip install /usr/share/libdxrt-bin/python/dx_engine-*-${PYTAG}-${PYTAG}-*.whl
    ```

    !!! note "Do not use `pip install dx-engine`"
        The only `dx-engine` release on PyPI (3.4.0) is yanked and does not match DX-RT 3.5.0. Always install the wheel that comes with your `libdxrt-bin`. `import dx_engine` raises `RuntimeError` when the Python package and `libdxrt.so` have different major.minor versions.

1. Update the firmware, see [Update the firmware](#update-the-firmware). The APT repository does not ship firmware.

1. Restart as described in [The restart rule](#the-restart-rule), then [verify](#verify).

Later releases arrive with `sudo apt update && sudo apt upgrade`. After an upgrade, install the matching `dx_engine` wheel again.

### Option B: one line script

This script downloads and installs the NPU driver, DX-RT and firmware without cloning a repository. It needs `curl`, `dpkg` and `sudo`.

```bash
curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-runtime/main/oneline-install.sh | sh
```

The script installs the same `dxrt-driver-dkms` and `libdxrt-bin` packages as the APT route and then flashes the M1, M1M and H1 firmware for the devices it finds. If no NPU is detected, it skips the firmware step; run the same command again after the restart.

By default each component tracks the newest build on its own `main` branch, and the downloads are not checksum verified. To install the exact 2.5.0 set, pin all three versions:

```bash
curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-runtime/main/oneline-install.sh | DX_RT_VERSION=3.5.0 DX_DRIVER_VERSION=2.7.0 DX_FW_VERSION=2.7.6 sh
```

| Variable | Pins | Example |
|---|---|---|
| `DX_RT_VERSION` | DX-RT (`libdxrt-bin`) | `3.5.0` |
| `DX_DRIVER_VERSION` | NPU driver (`dxrt-driver-dkms`) | `2.7.0` |
| `DX_FW_VERSION` | Firmware for M1, M1M and H1 together (one firmware set) | `2.7.6` |

Then install `dx_engine` as in step 4 of [Option A](#option-a-apt-repository-recommended), restart as described in [The restart rule](#the-restart-rule) and [verify](#verify). This route does not install DX-APP or DX-Stream.

### Option C: full suite clone

Clone the `dx-all-suite` repository with all submodules. This gives you the runtime stack, DX-APP, DX-Stream, DX-ModelZoo, the compiler repository and the getting started scripts in one tree, at versions tested together.

```bash
git clone --recurse-submodules https://github.com/DEEPX-AI/dx-all-suite.git
cd dx-all-suite
```

If the `dx-runtime/` or `dx-compiler/` folders are empty, fetch the submodules:

```bash
git submodule update --init --recursive
git submodule status
```

Every line of `git submodule status` must start with a space or `+`, not with `-`.

Install the runtime modules:

```bash
./dx-runtime/install.sh --all
```

This installs the driver (as a DKMS package), DX-RT (as the `libdxrt-bin` package), firmware, DX-APP and DX-Stream, and creates the Python environment `dx-runtime/venv-dx-runtime` with `dx_engine`. Restart as described in [The restart rule](#the-restart-rule), then [verify](#verify).

Common `dx-runtime/install.sh` options:

| Option | Effect |
|---|---|
| `--all` | Install all modules: `dx_rt_npu_linux_driver`, `dx_fw`, `dx_rt`, `dx_app`, `dx_stream` |
| `--runtime-only` | Install only the driver, DX-RT and firmware |
| `--target=<module>[,<module>]` | Install the named modules, for example `--target=dx_rt,dx_app` |
| `--exclude-fw`, `--exclude-driver`, `--exclude-rt`, `--exclude-app`, `--exclude-stream` | Skip one module; works with `--all` or `--target` |
| `--driver-source-build` | Build the NPU driver from source instead of the DKMS package |
| `--rt-source-build` | Build DX-RT from source instead of the Debian package |
| `--skip-uninstall` | Do not uninstall the modules before installing |
| `--use-ort=y`, `--use-ort=n` | Build DX-RT with or without ONNX Runtime support (default `y`) |
| `--sanity-check=y`, `--sanity-check=n` | Run the sanity check for DX-RT or skip it (default `y`) |
| `--venv_path=<path>` | Python environment path (default `dx-runtime/venv-dx-runtime`) |
| `-f`, `--venv-force-remove` | Remove and recreate the environment (default on) |
| `-r`, `--venv-reuse` | Reuse an existing valid environment |
| `-v`, `--verbose` | Verbose logging |

To use DX-ModelZoo, install it into the same runtime environment:

```bash
./getting-started/modelzoo-0_install_dx-modelzoo.sh
./getting-started/modelzoo-1_prepare_assets.sh
```

You can also clone only the runtime repository: `git clone --recurse-submodules https://github.com/DEEPX-AI/dx-runtime.git`, then run `./install.sh --all` inside it.

### Option D: from source

Use this route for custom kernels or development. First remove a DKMS driver package if one is installed (`sudo dpkg -r dxrt-driver-dkms`), because a manual driver install conflicts with it.

Build and load the driver:

```bash
sudo apt-get update
sudo apt-get install -y git build-essential linux-headers-$(uname -r) pciutils
git clone https://github.com/DEEPX-AI/dx_rt_npu_linux_driver.git
cd dx_rt_npu_linux_driver/modules
./build.sh
sudo ./build.sh -c install --reload
cd ..
sudo ./sanity_check.sh
```

`--reload` stops related services, unloads the old modules and loads the new ones (`dx_dma` and `dxrt_driver`). Use it only when you can interrupt running applications.

Build DX-RT from the `dx_rt` repository:

```bash
git clone https://github.com/DEEPX-AI/dx_rt.git
cd dx_rt
./install.sh --all
./build.sh --clean
./build.sh --install /usr/local
sudo cp ./service/dxrt.service /etc/systemd/system
sudo systemctl start dxrt.service
cd python_package
pip install .
```

Check the `ExecStart` path in `service/dxrt.service` before you copy it. The full list of driver and DX-RT build options, cross compiling and the build configuration live with the product pages: see [NPU driver and firmware](../runtime/driver-firmware.md) and [DX-RT](../runtime/index.md).

### Update the firmware

Every route except the APT repository can flash the firmware for you (`./dx-runtime/install.sh --target=dx_fw` in a clone, or the one line script). To flash it by hand, get the firmware files and use `dxcli`:

```bash
git clone --depth 1 https://github.com/DEEPX-AI/dx_fw.git
sudo systemctl stop dxrt.service
dxcli -g ./dx_fw/m1/2.7.6/mdot2/fw.bin
dxcli -u ./dx_fw/m1/2.7.6/mdot2/fw.bin
sudo systemctl start dxrt.service
```

`dxcli -g` reads the version header of the file and checks it against the device before you write anything. Pick the file for your product (`dxcli -s` shows the device type):

| Product | Firmware file |
|---|---|
| DX-M1 M.2 module | `dx_fw/m1/<version>/mdot2/fw.bin` |
| DX-M1M M.2 module | `dx_fw/m1m/<version>/mdot2/fw.bin` |
| DX-H1 Quattro | `dx_fw/m1/<version>/h1/fw.bin` |

Use `2.7.6` for DEEPX SDK 2.5.0, or `latest` for the newest published firmware. Then do a cold boot as described in [The restart rule](#the-restart-rule).

!!! warning "Firmware cannot be rolled back by uninstalling"
    Uninstalling the SDK does not revert firmware that is already on the NPU. DX-RT 3.5.0 needs firmware 2.7.6 or later.

## Host: DX-COM

### Option A: pip (recommended)

DX-COM is a wheel on PyPI for x86_64 Linux and Python 3.8 to 3.14.

1. Install the system libraries that DX-COM needs (`opencv-python` inside DX-COM fails to import without them):

    === "Ubuntu and Debian"
        ```bash
        sudo apt-get update
        sudo apt-get install -y --no-install-recommends libgl1 libglib2.0-0 make python3-venv
        ```

    === "Fedora"
        ```bash
        sudo dnf install -y mesa-libGL glib2 make
        ```

    === "RHEL and CentOS Stream 9, 10"
        ```bash
        sudo dnf install -y dnf-plugins-core
        sudo dnf config-manager --set-enabled crb
        sudo dnf install -y mesa-libGL glib2 make
        ```

    !!! note "`libgl1-mesa-glx` is gone"
        Older guides install `libgl1-mesa-glx`. That package does not exist on Ubuntu 24.04, Ubuntu 26.04 or Debian 12. Use `libgl1`, which exists on every supported Ubuntu and Debian release. Our install scripts install `libgl1-mesa-dev`, which also works because it pulls in `libgl1`.

1. Create a virtual environment and install DX-COM:

    ```bash
    python3 -m venv ~/dx-com-venv
    source ~/dx-com-venv/bin/activate
    pip install dx-com
    ```

    To pin this release, use `pip install dx-com==2.5.0`. With [uv](https://docs.astral.sh/uv/) the install is faster: `uv pip install dx-com`.

1. Check the install:

    ```bash
    dxcom -v
    python3 -c "import dx_com; print(dx_com.__version__)"
    ```

!!! note "Older DX-COM versions"
    `dx-com` 2.4.0 and 2.3.0 were removed from PyPI and cannot be installed with pip. Use 2.4.1 or later, or get the wheel from the S/W Download page of our developer portal.

### Option B: one line script

This script creates a virtual environment, installs `dx-com` from PyPI into it, and links the `dxcom` launcher into your `PATH`. It supports Debian and Ubuntu, and installs `libgl1-mesa-dev` and `libglib2.0-0` with `apt`, so it needs root or `sudo`.

```bash
curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-compiler/main/oneline-install.sh | sh
dxcom --help
```

| Variable | Meaning | Default |
|---|---|---|
| `DX_VERSION` | `dx-com` release to install | Newest on PyPI |
| `DX_INSTALL_DIR` | Install root; the environment is `$DX_INSTALL_DIR/venv-dx-compiler` | `~/deepx` |
| `DX_BIN_DIR` | Where the `dxcom` launcher is linked | `~/.local/bin` |
| `DX_NO_UV` | Set to `1` to install with pip instead of uv | unset |
| `UV_PIN` | uv release to bootstrap | pinned in the script |

Example of a system wide install on a shared machine:

```bash
curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-compiler/main/oneline-install.sh | sudo DX_INSTALL_DIR=/opt/deepx DX_BIN_DIR=/usr/local/bin sh
```

This route does not download the sample models. Clone the repository for those.

### Option C: install script in the repository

Use this route when you want the sample models and calibration data, or when you work in the full suite clone (the folder is `dx-all-suite/dx-compiler`).

```bash
git clone https://github.com/DEEPX-AI/dx-compiler.git
cd dx-compiler
./install.sh
source ./venv-dx-compiler/bin/activate
dxcom -v
```

`install.sh` installs the system packages, creates `venv-dx-compiler`, and installs DX-COM 2.5.0 (the version in `compiler.properties`). It uses uv when uv is installed and pip otherwise. Without `--python_version` it uses the OS default `python3`.

| Option | Effect |
|---|---|
| `--target=<module>` | Module to install: `dx_com` or `all` (default `all`) |
| `--python_version=<version>` | Python version to use, for example `3.12` |
| `--venv_path=<path>` | Environment path (default `venv-dx-compiler` in the repository) |
| `--venv_symlink_target_path=<dir>` | Create the environment there and link to it |
| `--system-site-packages` | Create the environment with access to system packages |
| `-f`, `--venv-force-remove` | Remove and recreate the environment (default on) |
| `-r`, `--venv-reuse` | Reuse an existing valid environment |
| `--uv=true`, `--uv=false` | `true` installs uv if missing and uses it; `false` forces pip |
| `--force=true`, `--force=false` | Reinstall even if already installed (default `true`) |
| `--archive_mode=y` | Download wheels for offline use with pip (default `n`) |
| `--docker_volume_path=<path>` | Docker volume path (container builds only) |
| `--verbose` | Verbose logging |

!!! note "DX-TRON was removed"
    DX-TRON is no longer part of the SDK. `--target=dx_tron` now fails with a migration message. To inspect a compiled model, run `dxcom` with `--export_html` and open the generated `<model>_summary.html`.

## Docker

All our images are based on Ubuntu 24.04. Docker containers share the host kernel, so **the NPU driver must be installed on the host** before a runtime container can see the NPU.

1. On the host, install the NPU driver with any device route above (for example `sudo apt install dxrt-driver-dkms`, or `./dx-runtime/install.sh --target=dx_rt_npu_linux_driver` in a clone), then `sudo reboot`.
1. Only one `dxrtd` may run on the whole machine (host plus all containers). If DX-RT also runs on the host, stop its service before you start a runtime container that runs its own `dxrtd`:

    ```bash
    systemctl is-active --quiet dxrt.service && sudo systemctl stop dxrt.service
    ```

### Prebuilt images

| Image | Tags | Platforms |
|---|---|---|
| `ghcr.io/deepx-ai/dx-runtime` | `rt`, `rt-app`, `rt-stream`, `rt-app-stream`, `latest`; pinned `v<ver>-rt`, `v<ver>-rt-app`, `v<ver>-rt-stream`, `v<ver>-rt-app-stream`, `v<ver>` | `linux/amd64`, `linux/arm64` |
| `ghcr.io/deepx-ai/dx-compiler` | `latest`; pinned `v<ver>` | `linux/amd64` only |
| `ghcr.io/deepx-ai/dx-modelzoo` | `latest`; pinned `v<mz-ver>` | `linux/amd64` only |

Write `deepx-ai` in lowercase: GHCR rejects uppercase names. Tags with a version number never change, so use them in production and CI. `latest` and the bare variant tags move to each new release. The three images have independent version numbers.

| `dx-runtime` variant | Contains |
|---|---|
| `rt` | DX-RT only (`dxrtd`, CLI tools, `dx_engine`) |
| `rt-app` | `rt` plus DX-APP |
| `rt-stream` | `rt` plus DX-Stream |
| `rt-app-stream` | `rt` plus DX-APP and DX-Stream (same as `latest`) |

Pull and start the runtime image with NPU access:

```bash
docker pull ghcr.io/deepx-ai/dx-runtime:rt-app-stream
docker run --rm -it \
    --privileged --ipc=host --pid=host --network=host \
    -v /dev:/dev \
    --entrypoint bash \
    ghcr.io/deepx-ai/dx-runtime:rt-app-stream
```

The image entrypoint is `dxrtd`. With `--entrypoint bash` you get a shell instead, and the container uses the `dxrtd` of the host (through `--ipc=host --pid=host --network=host`). Without `--network=host`, apps fail with `IPC_CONNECT_FAILED`. Inside the container, `dx_engine` lives in `/venv-dxnn`; an interactive shell activates it, a non interactive command must run `source /venv-dxnn/bin/activate` first.

Start the compiler image (pass your user and group ID so the container does not change the owner of your files):

```bash
docker pull ghcr.io/deepx-ai/dx-compiler:latest
docker run --rm -it \
    --privileged --network=host \
    --shm-size=1g \
    -e HOST_UID="$(id -u)" -e HOST_GID="$(id -g)" \
    -v "$PWD/workspace:/deepx/workspace" \
    ghcr.io/deepx-ai/dx-compiler:latest bash
```

Start the model zoo image (it reuses the `dxrtd` of the host or of a runtime container):

```bash
docker pull ghcr.io/deepx-ai/dx-modelzoo:latest
docker run --rm -it \
    --privileged --ipc=host --pid=host --network=host \
    -v /dev:/dev \
    -v "$PWD/workspace:/deepx/workspace" \
    --entrypoint bash \
    ghcr.io/deepx-ai/dx-modelzoo:latest
```

On an arm64 device, compile your models on an x86_64 host: there is no arm64 compiler image.

### Build images locally

In the full suite clone (`dx-all-suite`), build and start the images with our scripts:

```bash
./docker_build.sh --all --ubuntu_version=24.04
./docker_run.sh --all --ubuntu_version=24.04
docker exec -it dx-runtime-ubuntu-24.04 bash
```

The containers are named `dx-compiler-<os>-<version>`, `dx-runtime-<os>-<version>` and `dx-modelzoo-<os>-<version>`, for example `dx-compiler-ubuntu-24.04`. Run `docker ps --format '{{.Names}}'` to see them. Stop them with `./docker_down.sh --all`.

| `docker_build.sh` option | Effect |
|---|---|
| `--all` | Build `dx-compiler`, `dx-runtime` and `dx-modelzoo` |
| `--target=<image>` | Build one image: `dx-compiler`, `dx-runtime` or `dx-modelzoo` |
| `--ubuntu_version=<version>` | Ubuntu base for all images: `20.04`, `22.04`, `24.04` or `26.04` |
| `--debian_version=12` | Debian base (`dx-runtime`, `dx-modelzoo`) |
| `--fedora_version=<version>`, `--rhel_version=<version>`, `--centos_version=<version>` | Red Hat family base for `dx-compiler` only: Fedora `42` to `45`, RHEL `9` or `10`, CentOS `stream9` or `stream10` |
| `--variant=<variant>` | `dx-runtime` variant: `rt`, `rt-app`, `rt-stream` or `rt-app-stream` (default) |
| `--driver_update` | Also install the NPU driver on the host |
| `--nvidia_gpu`, `--cuda_version=<ver>` | CUDA base image for `dx-compiler` and `dx-modelzoo` (default CUDA 12.8.1, Ubuntu only) |
| `--intel_gpu_hw_acc` | Intel VA-API media acceleration for `dx-runtime` (DX-Stream pipelines only, Ubuntu only) |
| `--no-cache` | Build without the Docker cache |
| `--skip-archive` | Reuse the source archives from the previous build |

`docker_run.sh` and `docker_down.sh` take the same `--all`, `--target`, OS version, `--nvidia_gpu`, `--cuda_version` and `--intel_gpu_hw_acc` options. `--nvidia_gpu` and `--intel_gpu_hw_acc` cannot be combined, and `--variant` cannot be combined with `--nvidia_gpu`.

!!! note "GPU images"
    `--nvidia_gpu` needs the NVIDIA driver and the NVIDIA Container Toolkit on the host. The default CUDA 12.8.1 image needs driver R570 or newer. In GPU images, do not upgrade `onnxruntime-gpu` inside the container. `--intel_gpu_hw_acc` needs `/dev/dri/renderD*` on the host.

## Windows

DX-RT runs on Windows 10 22H2 (build 19045) or later and Windows 11, x64 only. The NPU can sit in a PCIe slot, an M.2 slot, or behind USB4 or Thunderbolt with PCIe tunneling (plain USB 3.x does not work). DX-COM does not run on Windows; compile on a Linux host.

1. Seat the NPU.
1. Download the DEEPX SDK installer for your NPU from the S/W Download page of our developer portal.
1. Run the installer. In the UAC prompt, check that the publisher is **DEEPX Co., Ltd.** It checks for Windows and the .NET Desktop Runtime 10 x64.
1. Select the components. **Driver** and **Runtime** are required; **C/C++ SDK**, **Python SDK** and **Examples** are optional.
1. Open a new terminal and check the device:

    ```bat
    dxcli -s
    tasklist | findstr dxrtd
    python -c "import dx_engine"
    ```

Run the installer again to upgrade, repair, modify or uninstall. To build DX-RT from source on Windows you need Visual Studio 2022 (not 2019, not 2026) with **Desktop development with C++**. In the `dx_rt` repository, `build.bat install` builds and installs to `out\install\x64-Release`, and `build.bat setup` (as Administrator) adds it to `PATH` and registers `dxrtd` as a service. `build.bat unsetup` removes it again.

## Verify

On the device, check the NPU, driver, firmware and DX-RT:

```bash
dxcli -s
```

```text
DXRT v3.5.0
=======================================================
 * Device 0: M1, Accelerator type
---------------------   Version   ---------------------
 * RT Driver version   : v2.7.0
 * PCIe Driver version : v2.7.0
-------------------------------------------------------
 * FW version          : v2.7.6
-------------------------------------------------------
```

Check that you see `Device 0`, real version numbers for the drivers and firmware, and no error such as `Other instance of dxrtd is running`. Then check the Python package and run the full sanity check:

```bash
python3 -c "import dx_engine; print(dx_engine.__version__)"
./dx-runtime/scripts/sanity_check.sh
```

The sanity check script is in the `dx-runtime` repository (run it on the host, not inside a container). `--dx_driver` checks only the driver, `--dx_rt` only DX-RT. If you have no clone, the driver repository has `sudo ./sanity_check.sh` and the APT package has `/usr/share/libdxrt-bin/SanityCheckForDebian.sh`.

On the host, check DX-COM in its environment:

```bash
dxcom -v
python3 -c "import dx_com; print(dx_com.__version__)"
```

## Uninstall

Remove DX-RT and the NPU driver (works for every Linux route):

```bash
curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-runtime/main/oneline-uninstall.sh | sh
```

Or with `apt`:

```bash
sudo apt purge libdxrt-bin dxrt-driver-dkms
```

Remove a DX-COM one line install (pass the same `DX_INSTALL_DIR` and `DX_BIN_DIR` you installed with):

```bash
curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-compiler/main/oneline-uninstall.sh | sh
```

Remove a pip install of DX-COM with `pip uninstall dx-com`, or delete its virtual environment. For clone installs, including DX-APP and DX-Stream, run `./uninstall.sh` in the `dx-runtime` or `dx-compiler` repository.

The `dx_engine` wheel and the firmware on the NPU stay in place; remove `dx_engine` with `pip uninstall dx-engine` in its environment.

## Next steps

* [Run your first model](quickstart.md)
* [Check versions and compatibility](compatibility.md)
* [Fix install errors](troubleshooting.md)
* [NPU driver and firmware details](../runtime/driver-firmware.md)
