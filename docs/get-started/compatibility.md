---
title: Compatibility
description: Component versions of every DEEPX SDK release, supported OS, Python and hardware, and how to check the versions you have installed.
---

# Compatibility

This page tells you which component versions belong together, what hardware and software each part supports, and how to check what you have installed.

## Version matrix

Each DEEPX SDK release is a set of component versions that we test together. Install components from the same row. Newest first. The SDK version is the release of the `dx-all-suite` repository, called DX-AllSuite in older material.

| SDK | Date | DX-COM | Firmware | NPU driver | DX-RT | DX-Stream | DX-APP | DX-ModelZoo |
|---|---|---|---|---|---|---|---|---|
| 2.5.0 | 2026-10-23 | 2.5.0 | 2.7.6 | 2.7.0 | 3.5.0 | 3.2.0 | 3.3.0 | 1.0.0 |
| 2.4.3 | 2026-09-03 | 2.4.1 | 2.7.4 | 2.6.0 | 3.4.2 | 3.1.2 | 3.2.2 | n/a |
| 2.4.2 | 2026-08-14 | 2.4.0 | 2.7.4 | 2.6.0 | 3.4.2 | 3.1.2 | 3.2.2 | n/a |
| 2.4.1 | 2026-08-03 | 2.4.0 | 2.7.4 | 2.6.0 | 3.4.1 | 3.1.1 | 3.2.1 | n/a |
| 2.4.0 | 2026-07-22 | 2.4.0 | 2.7.3 | 2.5.1 | 3.4.0 | 3.1.0 | 3.2.0 | n/a |
| 2.3.3 | 2026-05-14 | 2.3.0 | 2.5.6 | 2.4.1 | 3.3.2 | 3.0.1 | 3.1.1 | n/a |
| 2.3.2 | 2026-05-11 | 2.3.0 | 2.5.6 | 2.4.1 | 3.3.2 | 3.0.1 | 3.1.1 | n/a |
| 2.3.1 | 2026-05-06 | 2.3.0 | 2.5.6 | 2.4.1 | 3.3.1 | 3.0.1 | 3.1.1 | n/a |
| 2.3.0 | 2026-04-10 | 2.3.0 | 2.5.6 | 2.4.1 | 3.3.0 | 3.0.0 | 3.1.0 | n/a |
| 2.2.2 | 2026-02-26 | 2.2.1 | 2.5.0 | 2.1.0 | 3.2.0 | 2.2.1 | 3.0.2 | n/a |
| 2.2.1 | 2026-02-09 | 2.2.0 | 2.5.0 | 2.1.0 | 3.2.0 | 2.2.0 | 3.0.1 | n/a |
| 2.2.0 | 2026-01-16 | 2.2.0 | 2.5.0 | 2.1.0 | 3.2.0 | 2.2.0 | 3.0.0 | n/a |
| 2.1.0 | 2025-11-28 | 2.1.0 | 2.4.0 | 1.8.0 | 3.1.0 | 2.1.0 | 2.1.0 | n/a |
| 2.0.0 | 2025-09-08 | 2.0.0 | 2.1.4 | 1.7.1 | 3.0.0 | 2.0.0 | 2.0.0 | n/a |
| 1.0.0 | 2025-07-23 | 1.60.1 | 2.1.0 | 1.5.0 | 2.9.5 | 1.7.0 | 1.11.0 | n/a |

n/a: DX-ModelZoo was not part of the SDK before 2.5.0. DX AI Studio 0.1.1 ships with SDK 2.5.0. DX-TRON was removed in SDK 2.5.0; use `dxcom --export_html` instead.

!!! note "Older DX-COM wheels on PyPI"
    `dx-com` 2.4.0 and 2.3.0 are no longer on PyPI, so `pip install dx-com==2.4.0` fails. Use 2.4.1 or later.

??? info "Repository release tags"

    The `dx-compiler` and `dx-runtime` repositories have their own release numbers, which you see in their `release.ver` files and Git tags. Use this table to pick the Git tag when you clone an older SDK release. Older material calls them the DX-Compiler and DX-Runtime bundles.

    | SDK | `dx-compiler` repository | `dx-runtime` repository |
    |---|---|---|
    | 2.5.0 | 2.5.0 | 2.5.0 |
    | 2.4.3 | 2.4.2 | 2.4.2 |
    | 2.4.2 | 2.4.1 | 2.4.2 |
    | 2.4.1 | 2.4.1 | 2.4.1 |
    | 2.4.0 | 2.4.0 | 2.4.0 |
    | 2.3.3 | 2.3.1 | 2.3.3 |
    | 2.3.2 | 2.3.1 | 2.3.2 |
    | 2.3.1 | 2.3.1 | 2.3.1 |
    | 2.3.0 | 2.3.0 | 2.3.0 |
    | 2.2.2 | 2.2.1 | 2.2.2 |
    | 2.2.1 | 2.2.0 | 2.2.1 |
    | 2.2.0 | 2.2.0 | 2.2.0 |
    | 2.1.0 | 2.1.0 | 2.1.0 |
    | 2.0.0 | 2.0.0 | 2.0.0 |
    | 1.0.0 | 1.0.0 | 1.0.0 |

## When you mix versions

If you install every component from one row of the [version matrix](#version-matrix), you can skip this section. The tables below help when you upgrade only one part, keep older firmware on a fleet, or load a `.dxnn` file made with another SDK release.

### Minimum driver and firmware for DX-RT

DX-RT refuses to start when the driver or firmware is older than it needs. The error message names the version it wants (see [Troubleshooting](troubleshooting.md#firmware-version-mismatch)).

| DX-RT | Linux driver | Linux PCIe driver | Firmware |
|---|---|---|---|
| 3.5.0 | 2.7.0 | 2.7.0 | 2.7.6 |
| 3.4.0 to 3.4.2 | 2.5.0 | 2.4.0 | 2.7.0 |
| 3.3.0 to 3.3.2 | 2.4.0 | 2.2.0 | 2.5.2 |
| 3.1.0 to 3.2.0 | 1.8.0 | 1.5.1 | 2.4.0 |
| 3.0.0 | 1.7.1 | 1.4.1 | 2.1.0 |
| 2.9.5 | 1.5.0 | 1.4.0 | 2.0.5 |

On Windows, DX-RT 3.5.0 needs driver 1.8.0 or later, PCIe driver 2.0.1 or later and firmware 2.7.6 or later.

### Model files and DX-RT

A `.dxnn` file records the DX-COM version that made it. DX-RT only loads formats it knows.

| `.dxnn` made with | File format | Needs DX-RT |
|---|---|---|
| DX-COM 2.5.0 | v9 | 3.5.0 or later |
| DX-COM 2.1.0 to 2.4.1 | v8 | 3.1.0 or later |
| DX-COM 2.0.x | v7 | 3.0.0 or later |
| DX-COM 1.40.2 to 1.60.x | v6 | 2.7.0 or later |

When DX-RT reports that the model's compiler version is not compatible, recompile the model with the DX-COM from the same SDK row as your DX-RT. DX-ModelZoo 1.0.0 `.dxnn` files are format v9 and need DX-RT 3.5.0.

## Supported environments

| | Host (DX-COM) | Device (DX-RT, driver, firmware, DX-APP, DX-Stream) |
|---|---|---|
| CPU | x86_64 only | x86_64, aarch64 |
| Linux | Ubuntu 20.04, 22.04, 24.04, 26.04; Debian 11 or later; Fedora 42 to 45; RHEL 9, 10; CentOS Stream 9, 10 | Ubuntu 20.04, 22.04, 24.04, 26.04; Debian 12, 13 |
| Windows | Not supported | Windows 10 22H2 (build 19045) or later, Windows 11, x64 |
| glibc | 2.31 or later | 2.31 or later for the prebuilt `libdxrt-bin` package |
| Python | 3.8 to 3.14 | 3.8 to 3.14 (`dx_engine` wheels); Windows source builds 3.10 to 3.14 |
| C++ | n/a | C++14 or later; C++17 with MSVC |
| RAM | 16 GB or more | 8 GB, 16 GB recommended |
| Disk | 8 GB free | 4 GB free |
| NPU | Not needed | DX-M1, DX-M1M or DX-H1 Quattro in a PCIe or M.2 slot (Windows also USB4 or Thunderbolt with PCIe tunneling) |

Ubuntu 18.04 is not supported since SDK 2.5.0. The NPU driver and firmware need a bare metal machine: virtual machines with PCI passthrough are not supported. DX-COM and DX-ModelZoo do not need the NPU and run in a VM or a container.

### Docker base images

| Image | Base OS options |
|---|---|
| `dx-compiler` | Ubuntu 20.04 to 26.04, Fedora 42 to 45, RHEL (UBI) 9 and 10, CentOS Stream 9 and 10 |
| `dx-runtime` | Ubuntu 20.04 to 26.04, Debian 12 |
| `dx-modelzoo` | Ubuntu 20.04 to 26.04, Debian 12 |

The prebuilt GHCR images use Ubuntu 24.04.

### NPU products

| Product | PCI device ID | Firmware folder |
|---|---|---|
| DX-M1, DX-M1 M.2 module | `0x0100` (legacy `0x0000`) | `m1/<version>/mdot2` |
| DX-M1M, DX-M1M M.2 module | `0x0110` | `m1m/<version>/mdot2` |
| DX-H1 Quattro | `0x0101` | `m1/<version>/h1` |

All products use PCI vendor ID `1ff4`.

## Check your versions

| Component | Command | Where |
|---|---|---|
| Firmware, NPU driver, PCIe driver, DX-RT | `dxcli -s` | Device |
| DX-RT Python package | `python3 -c "import dx_engine; print(dx_engine.__version__)"` | Device, in your environment |
| NPU driver package | `dkms status` | Device |
| DX-COM | `dxcom -v` | Host, in your environment |
| DX-COM Python module | `python3 -c "import dx_com; print(dx_com.__version__)"` | Host |
| DX-APP | `cat dx-runtime/dx_app/release.ver` | Device, in the suite clone |
| DX-Stream | `cat dx-runtime/dx_stream/release.ver` | Device, in the suite clone |
| DX-ModelZoo | `python3 -c "from importlib.metadata import version; print(version('dx-modelzoo'))"` | Where `dx-modelzoo` is installed |
