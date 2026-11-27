---
title: Build and install DX-Stream
description: Build DX-Stream from source on Ubuntu or Debian, set up the environment, download sample assets and run the demos.
---

# Build and install DX-Stream

This page shows you how to build DX-Stream from source on Linux, check that GStreamer finds it, and run the demo pipelines.

## Before you start

* A host with amd64 (x86_64) or aarch64 (arm64) CPU, 8 GB RAM (16 GB recommended) and 4 GB free disk space.
* Ubuntu 20.04, 22.04, 24.04 or 26.04, or Debian 12 or 13.
* A DX-M1 M.2 module connected to the host.
* The NPU driver and DX-RT 3.5.0 or newer installed. Follow [Install the DEEPX SDK](../../get-started/install.md). The DEEPX SDK installer can also build DX-Stream for you; use this page when you build DX-Stream on its own.

For Windows see [Build on Windows](build-windows.md). For the Orange Pi 5 Plus see [Build on Orange Pi 5 Plus](build-orange-pi.md).

## Build steps

1. Clone the repository. Clone it two folders deep in a folder you own (for example `~/deepx/sdk/dx_stream`), because `setup.sh` stores downloads in a `workspace/res` folder two levels above the clone (see [Sample models and videos](#sample-models-and-videos)).

    ```bash
    mkdir -p ~/deepx/sdk && cd ~/deepx/sdk
    git clone https://github.com/DEEPX-AI/dx_stream.git
    cd dx_stream
    ```

1. Install the dependencies (build tools, CMake 3.17+, Meson 1.3+, GStreamer 1.16.3+, OpenCV 4.2.0+, json-glib, eigen3, librdkafka, libmosquitto, libyuv, jq, and librga on Rockchip boards).

    ```bash
    ./install.sh
    ```

    | Option | Effect |
    |---|---|
    | `--wo-gst` | Skip GStreamer. Use only if GStreamer 1.16.3 or newer is already installed. |
    | `--wo-opencv` | Skip OpenCV. Use only if OpenCV 4.2.0 or newer is already installed. |
    | `--help` | Show the options. |

1. Build and install. Run `build.sh` from the repository root; it fails when you start it from another folder.

    ```bash
    ./build.sh
    ```

    The script asks for your sudo password because it runs `sudo meson install` and `sudo ldconfig`, also for a custom `--prefix`.

1. Load the environment that `build.sh` added to `~/.bashrc`, then check the plugin.

    ```bash
    source ~/.bashrc
    gst-inspect-1.0 dxstream
    ```

    The output lists the plugin and its elements (`dxpreprocess`, `dxinfer`, `dxpostprocess`, `dxscale`, `dxconvert` and the others).

## Build options

| Option | Effect |
|---|---|
| `--prefix=PATH` | Install to `PATH` (default `/usr/local`). A relative path is turned into an absolute one. |
| `--type=debug` or `--type=release` | Build type (default release). |
| `--clean` | Delete previous build files before building. |
| `--plugin-only` | Build only the GStreamer plugin. Skip custom libraries, apps and pydxs. |
| `--dxvnpu` | Also build the DX-H1 V-NPU plugin (`dxvnpudec`, `dxvnpuenc`, the `dxvnpu` inference backend). Needs the DX-H1 V-NPU SDK (`dxvnpu` pkg-config package). |
| `--dxv3` or `--v3` | Build the DEEPX V3 DSP transform backend (needs `dxdsp`). In this mode `build.sh` skips the apps, test plugin and pydxs. |
| `--rkrga` | Force the Rockchip RGA transform backend. It is built automatically when `librga` is installed. |
| `--uninstall` | Remove installed files (add `--prefix` if you used one). |
| `--sonar` | Build with coverage for SonarQube analysis. |
| `--help` | Show all options. |

Options combine, for example `./build.sh --dxv3 --type=debug`.

## What gets installed

| Item | Default location |
|---|---|
| GStreamer plugin | `/usr/local/lib/<arch>-linux-gnu/gstreamer-1.0/libgstdxstream.so` |
| Headers | `/usr/local/include/gstdxstream/` |
| Custom libraries (postprocess, message convert) | `/usr/local/share/gstdxstream/lib/` |
| Example apps | `/usr/local/share/gstdxstream/bin/` |
| pkg-config file | `/usr/local/lib/pkgconfig/gstdxstream.pc` |
| Python binding `pydxs` | `venv-dx_stream/` in the repository root |

`<arch>-linux-gnu` is `x86_64-linux-gnu` on amd64 and `aarch64-linux-gnu` on arm64. With `--prefix` every path starts with your prefix instead of `/usr/local`.

`build.sh` creates `venv-dx_stream` from the system Python (`/usr/bin/python3`) with `--system-site-packages`, so the venv can use the system `python3-gi` package. Activate it before you run Python apps; see [Python bindings](python-bindings.md).

!!! warning "Custom prefix and the demo scripts"
    The demo scripts and `dx_stream/configs/*.json` load libraries from `/usr/local/share/gstdxstream/lib/...`. After `--prefix=/opt/dx-stream`, change these paths to `/opt/dx-stream/share/gstdxstream/lib/...`, or the postprocess library fails to load.

## Environment variables

`build.sh` writes this block to `~/.bashrc` (between `# DeepX Stream GStreamer Plugin` markers). It only takes effect in an interactive bash shell. In scripts, other shells or services, set the variables yourself:

```bash
PREFIX=/usr/local
LIBDIR=$PREFIX/lib/$(uname -m)-linux-gnu
export PKG_CONFIG_PATH="$PREFIX/lib/pkgconfig:${PKG_CONFIG_PATH}"
export GST_PLUGIN_PATH="$LIBDIR/gstreamer-1.0:${GST_PLUGIN_PATH}"
export LD_LIBRARY_PATH="$LIBDIR/gstreamer-1.0:$PREFIX/share/gstdxstream/lib:${LD_LIBRARY_PATH}"
export PATH="$PREFIX/share/gstdxstream/bin:${PATH}"
```

| Variable | Purpose | Needed at |
|---|---|---|
| `PKG_CONFIG_PATH` | pkg-config finds `gstdxstream.pc` | Build time, when you compile against DX-Stream |
| `GST_PLUGIN_PATH` | GStreamer finds the plugin | Run time |
| `LD_LIBRARY_PATH` | The loader finds the custom `.so` libraries | Run time |
| `PATH` | The shell finds the example apps | Run time |

If `gst-inspect-1.0 dxstream` says "No such element or plugin", clear the GStreamer cache and check that the plugin file exists:

```bash
rm -rf ~/.cache/gstreamer-1.0/
ls -la /usr/local/lib/$(uname -m)-linux-gnu/gstreamer-1.0/libgstdxstream.so
echo $GST_PLUGIN_PATH
gst-inspect-1.0 dxstream
```

## Sample models and videos

Download the sample models (listed in `model_list.json`) and videos:

```bash
./setup.sh
```

| Option | Effect |
|---|---|
| `--model=<file>` | Download only this model, for example `--model=yolo26-n_640x640.dxnn`. |
| `--force` | Download again and overwrite. |
| `--docker_volume_path=<path>` | Required inside a container. |
| `--verbose` | Debug logging. |

The files land in `<two folders above the clone>/workspace/res/` and `dx_stream/samples/models` and `dx_stream/samples/videos` link to them. With the clone at `~/deepx/sdk/dx_stream` that is `~/deepx/workspace/res/`. If the clone is at `~/dx_stream`, the script tries `/home/workspace/res` and fails with "Cannot create or write to directory". Move the clone, or create that folder with write rights for your user.

## Run the demos

```bash
./run_demo.sh
```

```text
0: Object Detection (YOLO26n)
1: Object Detection (YOLOv5s with PPU)
2: Face Detection (YOLOv5s_Face)
3: Pose Estimation (YOLO26n_Pose)
4: Instance Segmentation (YOLO26n_Seg)
5: Depth Estimation (YOLO26n_Depth)
6: Multi-Object Tracking
7: Multi-Channel Object Detection
8: Multi-Channel Object Detection (RTSP)
9: Secondary Mode (Multi-Model Cascade)
which AI demo do you want to run:(timeout:10s, default:0)
```

Type a number. Without input the script runs demo 0 after 10 seconds. `run_demo.sh` runs `setup.sh` first when the sample folders are missing. Demos marked PPU use the Post Processing Unit: the NPU decodes boxes and applies score thresholds, so the CPU does less work.

On a Raspberry Pi with `gstreamer1.0-libcamera` and a CSI camera, the menu also offers camera demos: `c` (object detection), `p` (pose), `s` (segmentation) and `d` (depth).

Each demo is a shell script under `dx_stream/pipelines/`. [Pipelines](pipelines.md) explains them.

!!! warning "Sample model licenses"
    The sample models are for evaluation and development only. See [Third party model licenses](licenses.md).

## Uninstall

| Command | Removes |
|---|---|
| `./uninstall.sh` | Everything below, plus the `~/.bashrc` block, `pydxs` from the current Python environment, `venv-dx_stream` and the downloaded models and videos. Default prefix only. |
| `./build.sh --uninstall` | Plugin, headers, `share/gstdxstream/`, `gstdxstream.pc`, build folder and pydxs build cache. Does not clean `~/.bashrc`. |
| `./build.sh --uninstall --prefix=/opt/dx-stream` | The same for a custom prefix. Remove the `~/.bashrc` block by hand afterwards. |

## Next steps

* [Run your first pipelines](pipelines.md)
* [Write an application](write-an-application.md)
* [Debugging and troubleshooting](debugging.md)
