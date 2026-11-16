---
title: Release notes
description: What changed in each DEEPX SDK release, newest first, with migration notes and links to the release notes of each product.
---

# Release notes

This page lists what changed in each DEEPX SDK release, newest first, and what you must change when you upgrade.

Each SDK release is a tested set of component versions. For the full version table of every release, see [Compatibility](../get-started/compatibility.md#version-matrix).

## Product release notes

* [DX-COM](compiler.md)
* [DX-RT, NPU driver and firmware](runtime.md)
* [DX-APP](app.md)
* [DX-Stream](stream.md)
* [DX-ModelZoo](model-zoo.md)
* [DX AI Studio](ai-studio.md)

## DEEPX SDK 2.5.0 (2026-10-23)
| Component | Version in DEEPX SDK 2.5.0 |
|---|---|
| DX-COM (compiler) | 2.5.0 |
| DX-RT (runtime) | 3.5.0 |
| DX-APP (application examples) | 3.3.0 |
| DX-Stream (GStreamer plugins) | 3.2.0 |
| NPU driver | 2.7.0 |
| Firmware | 2.7.6 |
| DX-ModelZoo | 1.0.0 |
| DX AI Studio | 0.1.1 |
DX-TRON was removed. The Kubernetes device plugin `dx-k8s-device-plugin` 0.1.0 is new.

### Breaking changes

* **Ubuntu 18.04 is no longer supported.** The install scripts and Docker builds need Ubuntu 20.04 or later.
* **DX-TRON was removed** from the compiler. Use the HTML Compilation Summary Report: `dxcom ... --export_html`.
* **DX-RT 3.5.0 needs NPU driver 2.7.0, PCIe driver 2.7.0 and firmware 2.7.6 or later.**
* **`.dxnn` format v9.** DX-COM 2.5.0 writes only format v9, which DX-RT 3.4.2 and older cannot load.
* **The C++/CLI C# package of DX-RT was removed.** C# now calls the C API through P/Invoke; you no longer need the .NET SDK or msbuild to build DX-RT.

### New

* **Prebuilt container images on GHCR**: `ghcr.io/deepx-ai/dx-runtime` (variants `rt`, `rt-app`, `rt-stream`, `rt-app-stream`; `amd64` and `arm64`), `ghcr.io/deepx-ai/dx-compiler` and `ghcr.io/deepx-ai/dx-modelzoo` (`amd64`). See [Install](../get-started/install.md#docker).
* **One line install** for DX-COM and for the runtime stack (driver, DX-RT, firmware), plus matching uninstall scripts.
* **DEEPX APT repository** with `dxrt-driver-dkms` and `libdxrt-bin` for Ubuntu and Debian on `amd64` and `arm64`.
* **Kubernetes support**: the `dx-npu` Helm chart (`oci://ghcr.io/deepx-ai/charts/dx-npu`) and a device plugin that advertises `deepx.ai/dx-m1` as a schedulable resource, with CDI injection and node labels.
* **DX-COM**: `dx_com.pre_optimize()` now covers pose estimation (YOLOv8, v9, v11, v12, v13 and YOLO26), YOLO26 segmentation and RTMDet detection, with up to 1.9x higher throughput on CPU limited hosts such as ARM (RTMDet-S 156.56 to 290.16 FPS on DX-M1 with a Cortex-A53 host). Q-Master (QAT) now supports segmentation. 3D `Conv` and `ConvTranspose` run on the NPU. Two input `Einsum` and 2D `Gather` indices are supported. New `--use_gpu` and `--verbose` options. `install.sh` uses uv when available.
* **DX-RT**: `dxrun --max-throughput` finds the best I/O buffer count. SIMD input quantization. New E2E response time and core latency APIs. `DXRT_ERR_DEVICE_REMOVED` and `DeviceRemovedException`. `import dx_engine` checks that the Python package matches `libdxrt.so`. Fan control modes.
* **Firmware**: NPU power gating in power save mode lowers idle power by about 5 to 10%.
* **DX-Stream**: OpenGL ES GPU preprocessing with DMA-BUF zero copy on ARM (CPU use on Raspberry Pi 5 with a 1080p30 camera drops from 95.2% to 4.8%). DX-H1 V-NPU decode, encode, transform and inference elements (need the upcoming DX-H1 V-NPU SDK). YOLO26 depth and Raspberry Pi camera demos.
* **DX-APP**: multi model graphs (`multi_model_graph_sync`, `multi_model_graph_async` with `--check`, `--list-models`, `--report`), examples for 147 more DX-ModelZoo models, eight new `dx_postprocess` classes.
* **DX-ModelZoo 1.0.0** with 497 models, new datasets such as MVTec AD, and dataset and input validation before evaluation.
* **DX AI Studio 0.1.1**: new prompt home screen, light and dark themes, Graph Composer in DX App, Run Demo with 26 demos, a catalog of 497 variants across 29 tasks, and the DX Cloud module for AWS.
* **Docker**: `--nvidia_gpu` (with `--cuda_version`, default 12.8.1) for `dx-compiler` and `dx-modelzoo`, and `--intel_gpu_hw_acc` for DX-Stream pipelines in `dx-runtime`.

### Fixes

* Firmware: mailbox ACK starvation, LPDDR5X clear logic, hardware timeouts now reported as NPU hangs (2 s hardware, 3 s software), recovery from EQ failures.
* NPU driver: latency spikes while unmapping memory after inference; the driver now signals the endpoint after probe to stabilize the PCIe link.
* DX-RT: segfault on empty PPU outputs, deadlock on service shutdown, `dxrtd` memory leaks on abnormal exit, Windows service crashes, `find_package(dxrt)` on Windows, latency statistics overflow; `dxrun` rejects invalid `--loops` and `--time`.
* DX-APP: `dx_postprocess` results now match the Python and C++ examples (VitPose, classification softmax, class agnostic NMS for DAMO-YOLO and NanoDet); Python examples honor `score_threshold`; YOLOv7 PPU decoding; thread safety of async runners.
* DX-Stream: more reliable OC-SORT tracking.
* DX-COM installer: uses the OS default `python3` when `--python_version` is not given, and removes leftover `dx_tron/` folders.

### Known issues

* Models with PReLU activations run much slower. Use `LeakyRelu` or `Relu` where you can.

### Migration from 2.4.x

| If you use | Do this |
|---|---|
| Ubuntu 18.04 | Upgrade the OS to Ubuntu 20.04 or later first. |
| DX-TRON | Use `dxcom --export_html`. Remove `--target=dx_tron` from scripts and CI. Remove an old package with `sudo apt-get remove dxtron`. |
| `docker_build.sh` | Optionally pull `ghcr.io/deepx-ai/*` instead. Write the registry path in lowercase. |
| DX-RT 3.4.x | Update the NPU driver to 2.7.0 and firmware to 2.7.6 before you upgrade DX-RT, then cold boot. Recompile models or use 2.5.0 `.dxnn` files. |
| `GetLatency*` | It now returns the E2E response time. Use `GetCoreLatency*` for latency without queue and buffer waits. |
| `dx_engine` with a different `libdxrt.so` | Install matching versions. `import dx_engine` raises `RuntimeError` otherwise (bypass for debugging: `DX_ENGINE_SKIP_VERSION_CHECK=1`). |
| DX-RT from C# | Switch from the removed C++/CLI package to the C API through P/Invoke. |
| `dx_com.compile()` with QAT | Pass keyword arguments. Replace `quantization_mode`, `qat_config`, `qat_skip_training` and `qat_resume_from_checkpoint` with one `qmaster=QMasterConfig(...)`. A JSON `qmaster` block still works. |
| `pre_optimize` | Rename `yolo_postprocess` to `yolo_dfl_postprocess` and `yolo26_postprocess` to `yolo_no_dfl_postprocess`. Add the required `task` key (`base`, `seg` or `pose`). Remove `input_height` and `input_width`. Remove a `ppu` block: when both are present, DX-COM uses `ppu` and drops `pre_optimize`. |
| `quantization_device` in a DX-COM config | Remove it. Use `use_gpu` (`True` or `False` only) and `CUDA_VISIBLE_DEVICES`. |
| DX-ModelZoo compile YAML | Rename `compile.quantization` to `compile.calibration`. The `--use-gpu` CLI option was removed. |
| DX-Stream demos | The SCRFD500M PPU and YOLOv5Pose PPU demos were removed. Use the 224x224 EfficientNet-Lite0 model instead of the 256x256 one. On V3 with DSP, build with `./build.sh --dxv3`. |
| DX-APP scripts | Update task names: `classification` is `image_classification`, `obb_detection` is `oriented_object_detection`, and `embedding` is split into `face_recognition`, `image_retrieval`, `visual_place_recognition` and `zero_shot_image_classification`. |

## Earlier releases

### 2.4.3 (2026-09-03)

DX-COM 2.4.1 writes smaller `.dxnn` files and fixes minor bugs. `dx-com` 2.4.0 and 2.3.0 were removed from PyPI by mistake and cannot be uploaded again: pin `dx-com==2.4.1` or later. Runtime components unchanged from 2.4.2.

### 2.4.2 (2026-08-14)

Hotfix: one shared sanity check script in `dx-runtime/scripts/sanity_check.sh`, Windows build and packaging fixes for DX-RT and DX-Stream, depth estimation metadata and rendering in DX-Stream, YOLO26-Depth examples in DX-APP. Adds the DX-Edge documentation for AWS deployment.

### 2.4.1 (2026-08-03)

Adds DX-Benchmark (beta). Firmware 2.7.4 and driver 2.6.0 add virtual machine support through the MSI IMWR PCIe message API and kernel 4.4.0 support. DX-RT corrects the supported OS list (Ubuntu 26.04 added, 18.04 removed). DX-APP super resolution fixes.

### 2.4.0 (2026-07-22)

Adds agent driven development (beta) and DX AI Studio (beta). DX-COM: automatic Q-PRO configuration, QAT through `dx_com.compile()`, `.qxnn` resume, a quantization diagnosis HTML report, the HTML graph viewer and `dx_com.pre_optimize()`, Python 3.13 and 3.14. DX-RT: stable C ABI (`dxrt_c_api.h`) and header only C++ wrapper (`dxrt_cxx_api.h`), CLI renamed to `dxcli`, `dxparse` and `dxrun` (old names kept as aliases), `dx_engine` wheels for Python 3.8 to 3.14 in the Debian package. Red Hat family images for `dx-compiler`. **Migration:** DX-TRON and PPU type 2 are deprecated; use the HTML viewer and `dx_com.pre_optimize()`.

### 2.3.3 (2026-05-14)

Fixes a missing file in the NPU driver Debian package (driver 2.4.1).

### 2.3.2 (2026-05-11)

DX-RT 3.3.2 cleans up its Debian package and improves the Python extension build.

### 2.3.1 (2026-05-06)

The compiler `uninstall.sh` removes all installed packages and gets a `--target` option. DX-RT bundles onnxruntime 1.22.0 and openvino 25.1 for better compatibility.

### 2.3.0 (2026-04-10)

TopK optimized YOLO post processing in DX-COM, DX-COM validated on Fedora, RHEL and CentOS Stream. DX-Stream 3.0.0 is modular and installs without root. DX-APP 3.1.0 uses a five layer structure with matching C++ and Python code. New `dxtop`. **Migration:** DX-Stream 3.0.0 moves its environment variables from `/etc/profile.d/` to `~/.bashrc`; DX-RT 3.3.0 needs driver 2.4.0 and firmware 2.5.2 or later.

### 2.2.2 (2026-02-26)

GPU quantization in DX-COM (`quantization_device`, later replaced by `use_gpu`), Windows build fixes.

### 2.2.1 (2026-02-09)

DX-APP adds YOLO26 classification, pose, segmentation and OBB examples.

### 2.2.0 (2026-01-16)

DX-COM is installable with pip. DX-TRON as a Debian package. YOLO26 support. New `RuntimeEventDispatcher` in DX-RT and `pydxs` Python bindings in DX-Stream.

### 2.1.0 (2025-11-28)

`.dxnn` format v8 across the stack. DX-RT adds DX-Fit, `dxbenchmark` and a model voltage profiler. DX-Stream adds GstShark integration. Firmware adds secure debug and model profiling mode. DX-COM adds partial compilation (`--compile_input_nodes`, `--compile_output_nodes`).

### 2.0.0 (2025-09-08)

DX-COM 2.0.0, DX-RT 3.0.0 (loads `.dxnn` v6 and v7), driver 1.7.1, firmware 2.1.4.

### 1.0.0 (2025-07-23)

First release of the suite with DX-COM 1.60.1, DX-RT 2.9.5, driver 1.5.0, firmware 2.1.0, DX-Stream 1.7.0 and DX-APP 1.11.0.

## Next steps

* [Install or upgrade](../get-started/install.md)
* [Compatibility](../get-started/compatibility.md)
