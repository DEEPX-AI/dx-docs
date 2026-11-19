---
title: Build on Windows
description: Build the DX-Stream GStreamer plugin on Windows 10 or 11 with MSVC, run the demos and deploy it.
---

# Build on Windows

This how to builds DX-Stream on Windows 10 or 11 (x86_64, MSVC). The result is `gstdxstream.dll`, the same plugin that Linux builds as `libgstdxstream.so`, plus the custom libraries, example apps and the `pydxs` Python binding.

## Before you start

Install these by hand before you run `install.bat`:

| Software | Purpose | Notes |
|---|---|---|
| Visual Studio 2022 | MSVC compiler | Select the "Desktop development with C++" workload. |
| Git for Windows | Source control, vcpkg | `git` must be on `PATH`. |
| Python 3.9 or newer | Runs Meson | Check "Add Python to PATH" in the installer. |
| GStreamer MSVC x86_64, 1.16.3 or newer | Multimedia framework | Install both the Runtime and the Development package, same version. 1.16.3 and 1.28.4 are verified. Default path `C:\Program Files\gstreamer\1.0\msvc_x86_64`. |
| pkg-config | Finds dependencies | Only if GStreamer does not ship a working one. Use the x64 MSI from [pkgconf releases](https://github.com/pkgconf/pkgconf/releases). |
| DEEPX SDK for Windows (`DX_SDK_*.exe`) | NPU runtime `dxrt` | Sets `DEEPX_SDK_DIR` (default `C:\Program Files\DEEPX\DX_SDK_<version>`). See [Install the DEEPX SDK](../../get-started/install.md). |

You also need a DX-M1 (or compatible) NPU for inference.

!!! warning
    The GStreamer Development package is required. It provides the headers and `.pc` files.

## Build steps

Run these in `cmd.exe`, not PowerShell (`build.bat` calls `vcvarsall.bat`).

```bat
git clone https://github.com/DEEPX-AI/dx_stream.git
cd dx_stream
install.bat
build.bat
setup.bat
run_demo.bat
```

| Script | What it does |
|---|---|
| `install.bat` | Checks the prerequisites (GStreamer version, then `pkg-config`), installs `meson` and `ninja` with pip, bootstraps vcpkg, installs eigen3, opencv4, libyuv, mosquitto and librdkafka, generates `opencv4.pc`, and checks `DEEPX_SDK_DIR`. Run it once. |
| `build.bat` | Builds the plugin, custom libraries, apps and pydxs into `install\`, copies the needed DLLs to `install\bin`, and adds this checkout to your User `GST_PLUGIN_PATH` and `Path`. |
| `setup.bat` | Downloads sample models and videos to `dx_stream\samples\`. |
| `run_demo.bat` | Opens the demo menu (same menu as Linux). |

`build.bat` options:

| Option | Effect |
|---|---|
| `--clean` | Remove the build folder and rebuild. |
| `--type=debug` | Debug build. |
| `--plugin-only` | Build only the plugin (skip custom libraries, apps, pydxs). |
| `--dxvnpu` | Build the DX-H1 V-NPU backend. Needs `DEEPX_VNPU_DIR` with `%DEEPX_VNPU_DIR%\lib\cmake\dxvnpu\dxvnpuConfig.cmake`. |
| `--dxv3` or `--v3` | Build the DX V3 transform backend (needs `dxdsp`). |
| `--rkrga` | Build the RK RGA backend (needs `librga`). |
| `--uninstall` | Remove this checkout's install and build folders, `venv-dx_stream` and its entries in User `GST_PLUGIN_PATH` and `Path`. |

The custom libraries and apps have their own scripts. They need the plugin built first and only compile into each subfolder's `builddir\`:

```bat
dx_stream\custom_library\build.bat
dx_stream\apps\build.bat
```

## Check the install

Open a new `cmd.exe` so the new User variables load, then:

```bat
gst-inspect-1.0 dxpreprocess
```

For manual `gst-inspect-1.0` or `gst-launch-1.0` calls in a fresh terminal, set up GStreamer for that terminal first (from the repository root):

```bat
call scripts\setup_gstreamer.bat runtime
```

The scripts look for GStreamer in `GSTREAMER_1_0_ROOT_MSVC_X86_64`, then `GSTREAMER_1_0_ROOT_X86_64`, then the default install folder.

Check Python:

```bat
call venv-dx_stream\Scripts\activate.bat
python -c "import pydxs; print('pydxs OK')"
```

## Run single pipelines

The Windows pipeline scripts are in `dx_stream\pipelines\windows\` (object detection, face, pose, segmentation, depth, tracking, multi stream, RTSP, secondary mode, MQTT and Kafka brokers). Each one runs on its own when `DXSTREAM_ROOT` is set:

```bat
set DXSTREAM_ROOT=C:\path\to\dx_stream
dx_stream\pipelines\windows\object_detection_yolo26n.bat
```

The broker scripts need a running broker; see [Pipelines](pipelines.md#message-broker-on-windows).

## Offline (air gapped) build

On a machine with internet access:

```bat
C:\vcpkg\vcpkg install eigen3:x64-windows opencv4:x64-windows libyuv:x64-windows mosquitto:x64-windows librdkafka:x64-windows
C:\vcpkg\vcpkg export eigen3:x64-windows opencv4:x64-windows libyuv:x64-windows mosquitto:x64-windows librdkafka:x64-windows --zip
```

Copy the zip to the offline machine and extract `installed/x64-windows/` to `dx_stream\vcpkg_installed\x64-windows\`. Install `meson` and `ninja` with pip from local wheels, then run `build.bat`. Put model files in `dx_stream\samples\models\` and videos in `dx_stream\samples\videos\` by hand.

## Deploy to a target machine

DX-Stream on Windows is distributed as a source build: clone and build on the target with the steps above. The target needs the GStreamer Runtime (MSVC 64-bit), the VC++ Redistributable 2015 to 2022 (x64), the DEEPX SDK and the NPU driver.

`build.bat` adds these entries (shown for reference, do not overwrite your variables with them):

```bat
set GST_PLUGIN_PATH=%PROJECT_ROOT%\install\lib\gstreamer-1.0;%GST_PLUGIN_PATH%
set PATH=%PROJECT_ROOT%\install\bin;%PROJECT_ROOT%\install\share\gstdxstream\lib;%PROJECT_ROOT%\install\share\gstdxstream\bin;%PROJECT_ROOT%\install\lib\gstreamer-1.0;%PATH%
```

!!! warning "Do not rename the DLL"
    The plugin must be named `gstdxstream.dll`. GStreamer derives the entry symbol from the file name, so `gstdxstream-0.dll` fails with "symbol not found".

## Windows and Linux differences

| Aspect | Linux | Windows |
|---|---|---|
| Dependencies | `install.sh` (apt, source) | `install.bat` (vcpkg) |
| Compiler | GCC or Clang | MSVC |
| Plugin file | `libgstdxstream.so` | `gstdxstream.dll` |
| Custom library loading | `dlopen` | `LoadLibrary` (through `dx_dlfcn.h`) |
| Pipeline scripts | `dx_stream/pipelines/*.sh` | `dx_stream\pipelines\windows\*.bat` |
| pydxs | Built with rpath | Built with a DLL loader |

On Windows, `pydxs` registers its DLL folders itself. It looks for DX-Stream in `DX_STREAM_ROOT\install`, for GStreamer in `GSTREAMER_1_0_ROOT_MSVC_X86_64` or `GSTREAMER_1_0_ROOT_X86_64`, for DX-RT in `DEEPX_SDK_DIR\bin`, and for the optional V-NPU runtime in `DEEPX_VNPU_DIR\bin`. Use absolute paths. A wrong `DX_STREAM_ROOT` gives an import error.

## Troubleshooting

| Problem | Fix |
|---|---|
| `gst-inspect-1.0 dxpreprocess`: No such element | Check that `GST_PLUGIN_PATH` points to the folder with `gstdxstream.dll`, that `PATH` contains `install\bin`, delete the registry cache (below), and check the DLL name. |
| Plugin was blacklisted once | `del "%LOCALAPPDATA%\Microsoft\Windows\INetCache\gstreamer-1.0\registry.x86_64-msvc.bin"` |
| `[ERROR] DEEPX_SDK_DIR environment variable is not set.` | Install the DEEPX SDK, open a new terminal, or `set DEEPX_SDK_DIR=C:\Program Files\DEEPX\DX_SDK_<version>`. |
| `install.bat` stops at prerequisites | Install the listed software and run it again. |
| meson setup: dependency not found | Run `install.bat`, then check `vcpkg_installed\x64-windows\lib\pkgconfig\`. |
| Link error: unresolved external symbol | Check that `vcpkg_installed\x64-windows\lib` has the `.lib` files. |
| MSVC not found | Use `cmd.exe`, not PowerShell. |
| `build.bat --uninstall` returns 1 | Files are locked or the environment update failed. Close apps that use DX-Stream and run it again. |

## Next steps

* [Pipelines](pipelines.md)
* [Python bindings (pydxs)](python-bindings.md)
* [Debugging and troubleshooting](debugging.md)
