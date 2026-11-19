---
title: Build from source
description: Build options, CMake settings and cross compilation for building DX-RT from source.
---

# Build from source

This page covers the options for building DX-RT yourself: `build.sh` flags, CMake options and cross compilation.

## Before you start

* The basic source install, with its dependencies, is in [Install](../get-started/install.md). Do that first.
* Clone [dx_rt](https://github.com/DEEPX-AI/dx_rt).

## build.sh

```bash
./build.sh [options]
```

| Option | Meaning |
|---|---|
| `--help` | Show help |
| `--clean` | Clean build. Removes old build output. With ONNX Runtime on, it also reinstalls ONNX Runtime |
| `--verbose` | Show the build commands |
| `--type <TYPE>` | CMake build type: `Release`, `Debug` or `RelWithDebInfo` |
| `--arch <ARCH>` | Target CPU: `x86_64` or `aarch64` |
| `--install <PATH>` | Install path |
| `--uninstall` | Remove installed DX-RT files |
| `--docker` | Build inside Docker |
| `--clang` | Build with Clang |
| `--strip-install` | Make stripped and unstripped files (Release builds only) |
| `--python-exec <PATH>` | Python interpreter for the Python package. Default `python3` |
| `--venv_path <PATH>` | Virtual environment to activate for the build |
| `--use_service_on`, `--use_service_off` | Build with or without the `dxrtd` service |
| `--use_ort_on`, `--use_ort_off` | Build with or without ONNX Runtime |
| `--python-break-system-packages` | Allow pip installs in a system managed Python |

```bash
./build.sh --type Release --arch x86_64
./build.sh --clean --install /opt/dx-rt
./build.sh --python-exec /usr/local/bin/python3.8
./build.sh --use_service_off --use_ort_off
```

`--clean` already does a full build. You do not need to run `build.sh` again after it.

The build writes `dxrtd`, `dxcli`, `dxparse`, `dxrun`, `dxtop`, `dxbenchmark` and the C++ examples (in `bin/examples`) to `bin/`.

!!! warning "Build with the Python you run"
    Build the Python package with the same Python version you use to run it. A mismatch can crash with `malloc(): corrupted top size`, `free(): invalid pointer` or `double free or corruption (out)`. Use `--python-exec` or `--venv_path` to pick the interpreter.

## Build options

`cmake/dxrt.cfg.cmake` holds the CMake options. Edit it, then do a clean build.

| Option | Default | Meaning |
|---|---|---|
| `USE_ORT` | `ON` | Run CPU tasks with ONNX Runtime |
| `USE_PYTHON` | `ON` | Build the `dx_engine` Python package |
| `USE_SERVICE` | `ON` | Use the `dxrtd` service. Needed when several processes share the NPU |
| `ENABLE_SHOW_MODEL_INFO` | `OFF` | Default of the `SHOW_MODEL_INFO` setting |
| `ENABLE_DEBUG_INFO` | `ON` | Include debug information |
| `USE_SHARED_DXRT_LIB` | `ON` | Build `libdxrt` as a shared library |
| `USE_DXRT_TEST` | `ON` | Build the unit tests |
| `USE_NPU_FORMAT_CONVERSION_ACCELERATION` | `OFF` | Include format conversion acceleration. See [Acceleration](configuration.md#acceleration) |
| `USE_CPU_OP_ACCELERATION` | `OFF` | Include CPU op acceleration |
| `FORCE_NPU_FORMAT_CONVERSION_ACCELERATION` | `OFF` | Always turn on format conversion acceleration |
| `FORCE_CPU_OP_ACCELERATION` | `OFF` | Always turn on CPU op acceleration |
| `USE_MT` | `OFF` | Windows only: link the static MSVC runtime (`/MT`) |

## Cross compile

Toolchain files are in `cmake/`: `toolchain.aarch64.cmake`, `toolchain.arm64.cmake`, `toolchain.riscv64.cmake` and `toolchain.x86_64.cmake`. For aarch64:

```bash
./build.sh --arch aarch64
```

The Python package cannot be cross compiled. Build it on the target, or turn off `USE_PYTHON`.

To cross compile the NPU driver, see [NPU driver and firmware](driver-firmware.md#with-make).

## Use DX-RT in your CMake project

```cmake
find_package(dxrt REQUIRED)
target_link_libraries(my_app PRIVATE dxrt::dxrt)
```

The package files install to `lib/cmake/dxrt`. For another install prefix, pass `-DCMAKE_PREFIX_PATH=<prefix>`. See [C++ API](cpp-api.md#headers-and-linking).

## Next steps

* [C++ API](cpp-api.md)
* [Configuration](configuration.md)
* [Troubleshooting](troubleshooting.md)
