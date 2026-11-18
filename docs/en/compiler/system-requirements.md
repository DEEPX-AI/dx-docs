# System requirements

DX-COM runs on the **host machine** that performs compilation — not on the NPU device itself.

## Hardware

| Component | Requirement |
|---|---|
| **CPU** | x86_64 (amd64) only — aarch64 / arm64 is **not** supported |
| **RAM** | ≥ 16 GB |
| **Disk** | ≥ 8 GB free space (dependency set includes PyTorch and ONNX Runtime) |

## Operating system

| OS | Supported versions | Notes |
|---|---|---|
| **Ubuntu** | 20.04, 22.04, 24.04, 26.04 | Primary supported environment |
| **Debian** | 11+ | Requires glibc ≥ 2.31 |
| **Fedora** | 42–45 | Validated since DX-COM v2.3.0 |
| **RHEL** | 9–10 | Validated since DX-COM v2.3.0 |
| **CentOS Stream** | 9–10 | Validated since DX-COM v2.3.0 |
| **Windows** | 10 / 11 | Supported via PyPI wheel |

!!! warning "Ubuntu 18.04 is not supported"
    Ubuntu 18.04 ships glibc 2.27, which is below the minimum requirement.

## Python

Supported versions: **3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14**

DX-COM wheels are built with the `manylinux_2_31_x86_64` platform tag, which requires **glibc ≥ 2.31**.

To check your glibc version:

```bash
ldd --version
```

## System libraries

The following system libraries must be installed before `pip install dx-com`:

| Library | Debian / Ubuntu | Fedora / RHEL / CentOS | Purpose |
|---|---|---|---|
| OpenGL runtime | `libgl1` | `mesa-libGL` | Required by OpenCV |
| GLib | `libglib2.0-0` | `glib2` | Required by OpenCV |
| GNU make | `make` | `make` | Used by some build steps |

See [Install the compiler](index.md#install-the-compiler) for the exact install commands per distribution.

## Output compatibility

DX-COM v2.4.0+ produces `.dxnn` files in **format v9**, which requires **DX-RT v3.5.0 or later** to load. DX-RT v3.4.2 and earlier cannot load format v9 files.

| DX-COM version | Output format | Minimum DX-RT |
|---|---|---|
| v2.4.0+ | `.dxnn` v9 | DX-RT 3.5.0 |
| v2.3.x | `.dxnn` v8 | DX-RT 3.4.x |
