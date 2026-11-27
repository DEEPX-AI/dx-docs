---
title: Glossary
description: Terms and abbreviations used in the DEEPX docs, and the old product names mapped to the names we use now.
---

# Glossary

This page explains the terms and abbreviations you meet in our docs and maps old product names to the names we use now.

## Product names

We now use one name per product. If you see an old name in a repository, a video or an older guide, it means the product in the right column.

| Old or other name | Name we use now |
|---|---|
| DX-AllSuite, DX-AS, DEEPX All Suite, DEEPX All-Suite, DX All Suite, DXNN SDK, DXNN-SDK, DXNN, DXNN® SDK, DEEPX NPU SDK | DEEPX SDK |
| dx-all-suite | The GitHub repository that holds the DEEPX SDK release (`dx-all-suite`) |
| DX-Compiler, dx-compiler bundle, AI Model Compile Environment, Compiler Platform | DX-COM (the repository `dx-compiler` packages it) |
| DXNN Compiler, DEEPX Compiler, dx_com, dxcom | DX-COM (`dx_com` is the Python module, `dxcom` the CLI, `dx-com` the pip package) |
| DX-Runtime, dx-runtime bundle, AI Model Runtime Environment, Deployment Platform | The runtime stack: DX-RT, NPU driver, firmware, DX-APP and DX-Stream (the repository `dx-runtime` packages them) |
| dx_rt, DXRT, DX Runtime, DEEPX Runtime | DX-RT (`dx_engine` is the Python package) |
| dx_rt_npu_linux_driver, RT driver, DX NPU Driver, DXNN Linux Device Driver | NPU driver |
| DX-FW, DX_FW, dx_fw, FW | firmware |
| DX-STREAM, dx_stream, dx-stream | DX-Stream |
| dx_app, dx-app, User Application Example | DX-APP |
| DX ModelZoo, DEEPX ModelZoo, DEEPX Open ModelZoo, Model Zoo, dx-modelzoo, dxmz | DX-ModelZoo (`dxmz` is its CLI) |
| dx-ai-studio, DX AI Studio (Beta) | DX AI Studio |
| DX-TRON, dxtron | Removed in SDK 2.5.0. Use `dxcom --export_html` (Compilation Summary Report). |
| dxrt-cli, run_model, parse_model | `dxcli`, `dxrun`, `dxparse` (renamed in DX-RT 3.4.0; old names still work) |
| DX-M1 M.2 module, M1 | DX-M1 |
| M1M | DX-M1M |
| H1, DX-H1 Quattro, H1-Quattro | DX-H1 (product DX-H1 Quattro) |

## DEEPX terms

| Term | Meaning |
|---|---|
| `.dxnn` | Compiled model file for the DEEPX NPU. DX-COM writes it, DX-RT loads it. DX-COM 2.5.0 writes format v9, which needs DX-RT 3.5.0. |
| `.qxnn` | Quantization checkpoint that DX-COM writes so you can rerun quantization with other settings without a full recompile. |
| Calibration dataset | Sample input images that DX-COM uses to choose INT8 quantization ranges. |
| Compilation Summary Report | HTML report from `dxcom --export_html` that shows the compiled graph and which parts run on the NPU or the CPU. |
| c-lite, q-lite, q-pro | DX-ModelZoo compile profiles that select the quantization effort. |
| DXQ | DX-COM quantization techniques used by Q-PRO. |
| Q-PRO | DX-COM high accuracy quantization mode (`--use_q_pro`). |
| Q-Master | DX-COM Quantization Aware Training, set with `QMasterConfig`. |
| `pre_optimize` | `dx_com.pre_optimize()`, ONNX level transforms that move YOLO post processing into a faster form. Replaces PPU type 2. |
| PPU | Post Processing Unit: post processing compiled into the `.dxnn` file. PPU type 2 is deprecated. |
| DX-Fit | DX-RT tuning toolkit. |
| `dxrtd` | DX-RT service daemon. It schedules NPU access for all processes. Only one instance may run per machine (host or one container). |
| `dxrt.service` | systemd unit that runs `dxrtd` on Linux. |
| `dxcli` | DX-RT CLI for device status (`-s`), info (`-i`), reset (`-r`) and firmware update (`-u`). |
| `dxrun` | DX-RT CLI that runs a model and reports latency and FPS. |
| `dxparse` | DX-RT CLI that prints the inputs, outputs and layout of a `.dxnn` file. |
| `dxtop` | Live NPU monitor. |
| `dxbenchmark` | DX-RT CLI that benchmarks several models. |
| `dx_engine` | DX-RT Python package (`InferenceEngine`, `InferenceOption`, `Configuration`, `DeviceStatus`). |
| `libdxrt-bin` | Debian package with the prebuilt DX-RT library, headers, tools and `dx_engine` wheels. |
| `dxrt-driver-dkms` | Debian package with the NPU driver as DKMS source. |
| `dxrt_driver`, `dx_dma` | The two NPU kernel modules (runtime driver and PCIe DMA driver). |
| `mdot2`, `h1` | Firmware folders: M.2 module and DX-H1 Quattro board. |
| Cold boot | Full power off of the machine, wait 10 to 30 seconds, power on. Needed after a firmware update. |
| `venv-dx-runtime`, `venv-dx-compiler`, `/venv-dxnn` | Python environments that our install scripts and Docker images create. |
| Variant (`rt`, `rt-app`, `rt-stream`, `rt-app-stream`) | Flavors of the `dx-runtime` Docker image. |
| E2E response time | DX-RT latency from submitting a job to getting its result, including queue and buffer waits (`GetLatency*`). |
| Core latency | DX-RT latency of the NPU work alone (`GetCoreLatency*`). |
| V-NPU | Video and NPU hardware on DX-H1 used by DX-Stream elements such as `dxvnpudec`. |

## General abbreviations

| Abbreviation | Meaning |
|---|---|
| API | Application Programming Interface |
| CDI | Container Device Interface, used to inject the NPU into Kubernetes pods |
| CLI | Command Line Interface |
| CPU | Central Processing Unit |
| CUDA | NVIDIA GPU compute platform, used for GPU quantization and evaluation |
| DFL | Distribution Focal Loss, a YOLO box decoding step |
| DKMS | Dynamic Kernel Module Support: rebuilds the NPU driver on kernel updates |
| DMA | Direct Memory Access |
| FP32 | 32 bit floating point |
| FPS | Frames Per Second |
| GHCR | GitHub Container Registry (`ghcr.io`) |
| GPU | Graphics Processing Unit |
| GStreamer | Open source multimedia pipeline framework that DX-Stream extends |
| INT8 | 8 bit integer, the NPU number format after quantization |
| IPC | Inter Process Communication |
| M.2 | Small form factor slot for expansion cards |
| mAP | mean Average Precision, a detection accuracy metric |
| NFD | Node Feature Discovery, labels Kubernetes nodes that have an NPU |
| NMS | Non Maximum Suppression, removes duplicate detection boxes |
| NPU | Neural Processing Unit |
| OBB | Oriented Bounding Box |
| ONNX | Open Neural Network Exchange, the model format DX-COM reads |
| ORT | ONNX Runtime. DX-RT can use it for operations that the NPU does not support |
| PCIe | PCI Express bus |
| QAT | Quantization Aware Training |
| RTSP | Real Time Streaming Protocol |
| SDK | Software Development Kit |
| shm | Shared memory (`/dev/shm`) |
| TDD | Test Driven Development |
| UAC | Windows User Account Control |
| uv | Fast Python package installer that our scripts use when available |
| VA-API | Video Acceleration API for Intel GPU decoding |
| venv | Python virtual environment |
| YAML | Configuration file format used by DX-ModelZoo |
