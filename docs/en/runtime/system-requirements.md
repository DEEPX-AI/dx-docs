# System requirements

DX-Runtime runs on the **target machine** where the DEEPX NPU is physically installed.

## Hardware

| Component | Requirement |
|---|---|
| **NPU** | DEEPX DX-M1, DX-M1M, or DX-H1 M.2 module |
| **CPU** | x86_64 or **arm64** (aarch64) |
| **RAM** | ≥ 4 GB recommended |
| **Interface** | PCIe (M.2 slot) |

!!! tip "arm64 support"
    Unlike the compiler (x86_64 only), DX-Runtime supports **both x86_64 and arm64** — suitable for boards such as Orange Pi 5 Plus and other aarch64 SBCs.

## Operating system

| OS | Supported versions |
|---|---|
| **Ubuntu** | 20.04 LTS, 22.04 LTS, 24.04 LTS, 26.04 |
| **Debian** | 12, 13 |

Debian-based distributions only. RPM-based distributions (Fedora, RHEL, CentOS) are not supported by the runtime.

## Component versions

DX-Runtime bundles five components, each with its own version number. The table below shows the latest validated set:

| Component | Version | Description |
|---|---|---|
| **DX-Runtime (suite)** | 2.5.0 | Umbrella release |
| **NPU Driver** | 2.7.0 | DKMS kernel module |
| **DX-FW** | 2.7.6 | NPU firmware (covers M1, M1M and H1) |
| **DX-RT** | 3.5.0 | Runtime library, `dxcli` and `dxrtd` service |
| **DX-Stream** | 3.2.0 | GStreamer plugin suite |
| **DX-APP** | 3.3.0 | C++ and Python example applications |

!!! note "DX-RT 3.5.0 required for DX-COM v2.4.0+ output"
    DX-COM v2.4.0 and later produce `.dxnn` files in format v9. These require **DX-RT 3.5.0 or later** to load. Earlier DX-RT versions cannot run v9 models.

## Python

The `dx_engine` Python package is supported on Python **3.8–3.14**. Wheels are staged in `/usr/share/libdxrt-bin/python/` after the APT install — one wheel per Python version.

## Reboot requirement

A **reboot** is required after the NPU driver installs for the DKMS module to load. For firmware updates, a **cold boot** is needed: shut the machine down, remove power for 10–30 seconds, then power on. A plain reboot may not reset the NPU.
