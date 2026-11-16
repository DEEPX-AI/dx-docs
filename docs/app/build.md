---
title: Build DX-APP
description: Install the DX-APP build dependencies, download models and sample videos, and build the C++ examples and Python modules with build.sh.
---

# Build DX-APP

This page shows how to install the DX-APP dependencies, download models and build the examples on Linux and Windows.

## Before you start

* The NPU driver and DX-RT 3.5.0 or later are installed. If not, follow [Install the DEEPX SDK](../get-started/install.md).
* `dxcli -s` shows your NPU, and the first line of `dxcli --version` is `DXRT v3.5.0` or later.
* You have a clone of [DEEPX-AI/dx_app](https://github.com/DEEPX-AI/dx_app). Run every command on this page from the `dx_app/` folder.

```bash
dxcli -s
dxcli --version
```

!!! warning "DX-RT 3.5.0 is required"
    `./setup.sh` downloads DX Model Zoo 2_5_0. These `.dxnn` files are container format v9, and DX-RT 3.5.0 is the first runtime that loads them. DX-RT 3.4.2 refuses them with `Model file format version 9 is not supported`. The C++ examples stop with `DXRT library version is too low. (required: >= 3.5.0, current: <version>)`. The Python examples only check for DX-RT 3.0.0 or later, so on DX-RT 3.0.0 to 3.4.x they start and then fail while loading the model.

## Requirements

| Item | Linux | Windows |
|---|---|---|
| OS | Ubuntu 20.04, 22.04, 24.04, 26.04 (x64) and Debian 12, 13 (x64) | Windows 10 22H2 (build 19045) or later (x64) |
| CPU | x86_64 or aarch64 | x64 |
| RAM | 8 GB (16 GB recommended) | 8 GB (16 GB recommended) |
| Disk | 4 GB free | 4 GB free |
| DX-RT | 3.5.0 or later | 3.5.0 or later |
| NPU driver | 2.7.0 or later | Included in the DX-RT Windows installer |
| Python package `dx_engine` | 3.5.x (same major.minor as DX-RT) | 3.5.x |
| Compiler | C++14 (GCC 7.5 or later, or Clang) | Visual Studio Community 2022 |
| CMake | 3.16 or later, with make or ninja | Included with Visual Studio 2022 |
| OpenCV | 4.2.0 or later (4.5.5 recommended) | Installed by vcpkg |
| Python | 3.8 or later with pip | 3.8 or later |

We test this release with DX-RT 3.5.0, NPU driver 2.7.0, firmware 2.7.6 and `dx_engine` 3.5.0 on a DX-M1 M.2 card (x86_64, Ubuntu 24.04).

Python is needed even for a C++ only build: the CMake configure step runs `scripts/gen_model_registry.py`. `import dx_engine` fails with `dx_engine and DX-RT versions do not match` when the package and the runtime differ in major.minor version.

## Build on Linux

1. Create and activate a Python virtual environment, and use it for every later step. Ubuntu 24.04 and Debian 12 and later refuse a system wide `pip install`, so a venv is required there. If you installed the SDK with the `dx-runtime` installer, you can reuse its `venv-dx-runtime` instead, which already has `dx_engine`.

    ```bash
    python3 -m venv venv-dxnn
    source venv-dxnn/bin/activate
    ```

1. Install the build dependencies (CMake, GCC, Ninja, Python packages) and OpenCV. The script uses `sudo` for the system packages.

    ```bash
    ./install.sh --all --venv_path ./venv-dxnn
    ```

1. Install the package that the model downloader needs:

    ```bash
    python3 -m pip install requests
    ```

1. Download the models that the demo uses and the sample videos:

    ```bash
    ./setup.sh --demo-models
    ```

1. Build. The default build makes the C++ examples that `run_demo.sh` uses and installs `dx_postprocess` into the active Python:

    ```bash
    ./build.sh --venv_path ./venv-dxnn
    ```

1. Check the Python modules:

    ```bash
    python3 -c "import dx_engine, dx_postprocess; print('Python OK')"
    ```

    ```text
    Python OK
    ```

The C++ executables are in `bin/`. Continue with [Run the examples](run-examples.md).

!!! note "Which Python gets dx_postprocess"
    `build.sh` installs `dx_postprocess` into the `python3` that is first on `PATH`, unless you pass `--venv_path <venv>` or `--python_exec <python>`. Activate the environment that has `dx_engine` before you build, or the Python examples cannot import both modules.

## install.sh options { #install-sh-options }

Without options, `./install.sh` does the same as `./install.sh --all`. Run `./install.sh --help` to see the options without installing anything.

| Option | What it does |
|---|---|
| `--all` | Install the core dependencies and OpenCV from the system packages |
| `--dep` | Install only the core dependencies (CMake, GCC, Ninja and more) |
| `--opencv` | Install OpenCV from the system packages |
| `--opencv-source-build` | Build and install OpenCV from source |
| `--arch <ARCH>` | Target CPU: `x86_64` or `aarch64` |
| `--python_version <VERSION>` | Python version to install, for example `3.10.4` (minimum 3.8.0). Without it, the OS default Python 3 is used |
| `--venv_path <PATH>` | Create (or use) a virtual environment at this path. Without it, no venv is created |
| `--help` | Show the help and exit |

On a Raspberry Pi with a CSI camera, `install.sh` also installs `gstreamer1.0-libcamera`.

To use CPU or GPU acceleration in OpenCV, build OpenCV yourself with `TBB=ON`, `IPP=ON` and `CUDA=ON`, then set `OpenCV_DIR` in the toolchain file `cmake/toolchain.x86_64.cmake`:

```cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR x86_64)
set(DXRT_INSTALLED_DIR /usr/local)
set(OpenCV_DIR /your/opencv/installation/dir)
```

`DXRT_INSTALLED_DIR` is where DX-RT is installed (default `/usr/local`, with libraries in `/usr/local/lib` and headers in `/usr/local/include`).

## Download models and videos

`setup.sh` downloads models into `assets/models/` and sample videos into `assets/videos/`. Without options it opens a menu where you pick categories and models.

```bash
./setup.sh --demo-models                      # only the 26 models run_demo.sh uses
./setup.sh --models yolov9-s_640x640 yolo11-n_640x640
./setup.sh --list                             # list the models and categories
./setup.sh --all                              # every registered model, no prompts
```

| Option | What it does |
|---|---|
| `--all` | Download all models without prompts |
| `--demo-models` | Download only the models used by `run_demo.sh` and `run_demo.bat` |
| `--models <m1> [m2 ...]` | Download these models. A name can be the variant (the `.dxnn` stem), the `.dxnn` file name or the registry `model_name`. Also `--models=<m1>,<m2>` |
| `--category=<name>` | Download one category, by its name as `--list` shows it |
| `--list` | List the available models without downloading |
| `--dry-run` | List the models that would be downloaded, without downloading |
| `--workers=<N>` | Parallel downloads (default 4) |
| `--no-json` | Skip the JSON metadata files |
| `--manifest=<path>` | Use another manifest JSON file |
| `--force` | Overwrite files that exist (default) |
| `--no-force` | Skip files that exist |
| `--force-remove-models` | Download the models again even with `--no-force` |
| `--force-remove-videos` | Download the sample videos again even with `--no-force` |
| `--docker_volume_path=<path>` | Asset path when `setup.sh` runs inside a container. It is required there; `setup.sh` stops without it |
| `--verbose` | Verbose logging |
| `--help` | Show the help |

!!! note "Category names"
    Category names are the manifest names that `--list` prints, such as `Classification` or `Object Detection`, not task folder names such as `object_detection`. `setup.sh` does not keep a name with a space together, so for a two word category call the downloader directly:

    ```bash
    python3 scripts/download_models.py --output assets/models --category "Object Detection"
    ```

### Disk space

| Asset | Count | Size |
|---|---:|---|
| Demo models | 26 | Changes with each Model Zoo release: `./setup.sh --demo-models --dry-run` lists them |
| All registered models | 497 | Several GB |
| Sample videos | 20 | About 1.1 GB |
| Sample images | Bundled in the repository | About 5 MB |

On a small device, download only what you need with `--models` or `--demo-models`, use image input instead of video, and remove `assets/models/*` and `assets/videos/*` when you are done.

### Downloads behind a TLS inspecting proxy

**Symptom.** `setup.sh`, or the automatic model download of an example, fails with:

```text
certificate verify failed: Missing Authority Key Identifier
```

**Cause.** Python 3.13 and later (with urllib3 2.3 or later) check certificates in X.509 strict mode, and many proxy CAs do not meet it. A conda `python3` first on `PATH` is the typical case. The system Python 3.12 of Ubuntu 24.04 is not affected.

The downloader uses the first Python it finds in this list, and prints its choice (`[DXAPP] [INFO] Downloader Python: ...`):

1. `DXAPP_SETUP_PYTHON` (a path or a command name).
1. The active virtual environment (`VIRTUAL_ENV`).
1. `../venv-dx-runtime`.
1. `python3`.

**Fix.** Try these in order:

1. Run the downloader with Python 3.12 or older:

    ```bash
    DXAPP_SETUP_PYTHON=/usr/bin/python3 ./setup.sh
    ```

1. Give the proxy root CA with `REQUESTS_CA_BUNDLE` (or `CURL_CA_BUNDLE`, `SSL_CERT_FILE`, or the OS trust store). This fixes a missing root, not strict mode.
1. Turn off only X.509 strict mode. The certificate chain and the host name are still verified, and TLS 1.2 stays the minimum:

    ```bash
    DXAPP_TLS_RELAX_X509_STRICT=1 ./setup.sh
    ```

## build.sh options { #build-sh-options }

```bash
./build.sh                                              # default: run_demo C++ targets and dx_postprocess
./build.sh --all                                        # every example, the graph CLI and dx_graph
./build.sh --category object_detection                  # every C++ example of one task folder
./build.sh --target yolov9-s_640x640_sync yolov9-s_640x640_async
./build.sh --target list                                # list the build targets
./build.sh --clean                                      # clean rebuild
```

| Option | What it does |
|---|---|
| `--minimal` | Build only the C++ sync and async targets that `run_demo.sh` uses. This is the default |
| `--all` | Build every C++ example (about 1,000 executables), the multi model graph CLI and `dx_graph`, and install them to `bin/` |
| `--category <NAME>` | Build the C++ sync and async targets of one task folder. `--category list` lists the folders |
| `--target <NAME> [NAME2 ...]` | Build one target, or every sync and async target whose name starts with NAME (for example `yolov8-m-seg`). `--target list` lists the targets. Names that start with a digit, such as `3ddfa-v2_mobilenetv1_120x120_sync`, are not listed but build |
| `--clean` | Remove previous build output first |
| `--type <TYPE>` | CMake build type: `Release`, `Debug` or `RelWithDebInfo` |
| `--arch <ARCH>` | Target CPU: `x86_64` or `aarch64` |
| `--python_exec <PATH>` | Python used for the build and for `dx_postprocess` and `dx_graph` |
| `--venv_path <PATH>` | Virtual environment to activate for the build |
| `--make_so` | With `--all`: also build each post processing module as a shared library `lib/libdxapp_<module>_postprocess.so` |
| `--coverage` | Add coverage flags (see [Testing](run-examples.md#test-the-examples)) |
| `--verbose` | Show the build commands |
| `--help` | Show the help |

Use only one of `--all`, `--minimal`, `--category` and `--target`. The build writes the executables to `bin/`.

The multi model graph binaries are built by `--all` or by `--target multi_model_graph_sync multi_model_graph_async`. `dx_graph` is built only by `--all`, and needs `pybind11`, `numpy` and the Python development headers of the target Python. Without them the build prints `dx_graph Python module skipped: <reason>`.

To install `dx_postprocess` by hand into the active Python:

```bash
cd src/bindings/python/dx_postprocess && python3 -m pip install .
```

### Cross compile for aarch64

```bash
./build.sh --arch aarch64
```

This uses `cmake/toolchain.aarch64.cmake` and builds into `build_aarch64/`. A cross build never writes the repository `bin/`, `lib/` or `include/`. `--all` installs into `build_aarch64/release`.

* `dx_postprocess` is skipped, because pip would build it for the host. Build it on the target with `./build.sh`.
* `dx_graph` is skipped. To build it for the target, pass `-DDXAPP_CROSS_PYTHON_GRAPH=ON -DPython_INCLUDE_DIR=<target include/python3.X>` to CMake. We do not test this path.
* `bash scripts/check_cross_compile.sh` compile checks the graph engine for aarch64 without linking. It needs `aarch64-linux-gnu-g++`, the DX-RT headers and the OpenCV headers.
* We test aarch64 builds by compiling only. Runtime behavior is validated on x86_64 with a DX-M1.

## Build on Windows

1. Install DX-RT and the NPU driver with our Windows installer from [DEEPX-AI/dx_rt_windows](https://github.com/DEEPX-AI/dx_rt_windows). You need administrator rights, the Microsoft Visual C++ 2015 to 2022 Redistributable (x64), and a DEEPX NPU on PCIe, M.2 or USB4 (with PCIe tunneling).
1. Install Visual Studio Community 2022 with the **Desktop development with C++** workload. Other versions are not tested.
1. Make sure vcpkg is available. It comes with Visual Studio 2022. For a separate vcpkg, set the user variable `VCPKG_ROOT` to its folder.
1. Set `DEEPX_SDK_DIR` to the DX-RT install folder and make sure CMake is on `PATH`.
1. Build from the `dx_app` folder:

    ```bat
    build.bat
    ```

`build.bat` generates `build_internal.bat` from `CMakeSettings.json`, builds and installs the examples, builds the Python C++ module and copies the DX-RT and vcpkg DLLs into `bin\`. Without options it asks for the build scope (Enter means minimal).

| Command | What it builds |
|---|---|
| `build.bat --minimal` | The `run_demo` C++ examples |
| `build.bat --all` | Every example, installed to `out\install\x64-Release` and copied to `bin\` |
| `build.bat --category <name>` | The C++ examples of one category (`list` shows them) |

To work in the IDE, open `out\build\x64-Release\dxapp.sln` with Visual Studio 2022, or open the `dx_app` folder with **Open a local folder**. Visual Studio then installs the `vcpkg.json` dependencies into `vcpkg_installed` and configures CMake. You can set `DEEPX_SDK_DIR` and `OpenCV_DIR` in `CMakeSettings.json`:

```json
{
    "name": "DEEPX_SDK_DIR",
    "value": "path/to/dx_rt/installed",
    "type": "STRING"
},
{
    "name": "OpenCV_DIR",
    "value": "${projectDir}/vcpkg_installed/x64-windows/share/opencv",
    "type": "STRING"
}
```

Download assets with `setup.bat` (a menu), `setup.bat --all` or `setup.bat --demo-models`. Run the examples like on Linux, with the `.exe` name:

```bat
bin\yolov7_640x640_sync.exe -m assets\models\yolov7_640x640.dxnn -i sample\img\sample_kitchen.jpg -l 10
```

!!! note "Windows limits in this release"
    * The multi model graph CLI is compiled on Windows by `build.bat --all`, but we do not test it there. `dx_graph` has no Windows build.
    * The configure step needs a real Python 3 (the Microsoft Store stub does not work). Otherwise it stops with `No Python 3 interpreter for the graph model registry`; pass `-DPython3_EXECUTABLE=<path to python3>`.
    * Video output supports `.mp4` and `.avi` only, because the Windows OpenCV build has no FFmpeg backend.
    * Windows N and KN editions have no H.264 or MPEG-4 encoder, so a saved video is `output.avi` (MJPG).

## Troubleshooting

| Symptom | Fix |
|---|---|
| `error: externally-managed-environment` from pip | Use a virtual environment: `./install.sh --all --venv_path ./venv-dxnn` and `./build.sh --venv_path ./venv-dxnn` |
| `error while loading shared libraries: libdxrt.so` | DX-RT is not in the library cache. Run `sudo ldconfig` after installing DX-RT to `/usr/local/lib` |
| `ModuleNotFoundError: No module named 'dx_engine'` | Activate the environment where DX-RT's Python package is installed. See [Install the DEEPX SDK](../get-started/install.md) |
| `ModuleNotFoundError: No module named 'dx_postprocess'` | Run `./build.sh` with that environment active, or install it by hand as shown above |
| `Missing dependency: requests` from `setup.sh` | `python3 -m pip install requests` in the downloader's Python |
| `--docker_volume_path must be provided in container mode` | Pass `--docker_volume_path=<path>` when you run `setup.sh` in a container |
| A target from the docs is missing in `bin/` | The default build makes only the demo set. Build it with `--target <variant>_sync <variant>_async` or `--all` |

## Next steps

* [Run the examples](run-examples.md)
* [Model catalog](models.md)
* [Troubleshooting](../get-started/troubleshooting.md)
