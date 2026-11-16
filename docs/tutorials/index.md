---
title: Tutorials
description: Hands on tutorials and complete demo applications that run on our NPU.
---

# Tutorials

These tutorials let you learn the DEEPX SDK step by step and then run complete demo applications on our NPU.

Each page is standalone: it lists what you need, the exact commands and the result you should see. The code lives in a GitHub repository that you clone in the first step. Install the SDK first with [Install](../get-started/install.md).

## Learn the SDK

These tutorials are JupyterLab notebooks from the [dx-tutorials](https://github.com/DEEPX-AI/dx-tutorials) repository. Follow them in order.

| Tutorial | What you learn | Level | Hardware needed |
|---|---|---|---|
| [Set up the tutorials](setup.md) | Start JupyterLab, point the notebooks at the SDK, install and verify the SDK (T00, T01) | Beginner | x86_64 or aarch64 host with a DEEPX NPU |
| [Run the DX-APP examples](dx-app.md) | Run classification, detection, pose and segmentation examples, export a standalone example, chain models (T02) | Beginner | DEEPX NPU |
| [Deploy a custom model](custom-model.md) | Compile your own trained YOLOv7 detector and run it with DX-APP (T03) | Intermediate | DEEPX NPU; NVIDIA GPU only for optional training |
| [Build a DX-Stream pipeline](dx-stream.md) | Run GStreamer pipelines, add a custom postprocess, write a Python people counter (T04) | Intermediate | DEEPX NPU and a display |
| [Compile models with DX-COM](compiler.md) | ONNX to DXNN, calibration, PPU, YOLO26 TopK, quantization recovery, Python API (T05) | Beginner to advanced | x86_64 host with 16 GB RAM; NPU for the comparisons |
| [Run models with DX-RT](runtime.md) | CLI tools, Python and C++ APIs, async inference, profiling (T06) | Beginner to advanced | DEEPX NPU |

## Demos

| Demo | What it shows | Level | Hardware needed |
|---|---|---|---|
| [PP-OCRv6 camera OCR](ocr-camera.md) | Compile six OCR models and read text from a camera in Python (T10) | Intermediate | DEEPX NPU, camera, display |
| [PP-OCR web demo](ocr-web-demo.md) | OCR on images and PDFs in a browser, served by a PaddleOCR server on the NPU | Beginner | DEEPX NPU |
| [YOLO multi channel](yolo-multi-channel.md) | One detection model on up to 100 video channels in C++ (T20, dx_demo) | Beginner | DEEPX NPU, display |
| [YOLO26 four tasks](yolo26-four-tasks.md) | Detection, pose, segmentation and depth on one stream in a Qt app (T21) | Beginner | DEEPX NPU, display |
| [YOLO26 C++ applications](yolo26-apps.md) | Eight small YOLO26 C++ apps, including pre optimized models (dx_yolo26) | Intermediate | DEEPX NPU |
| [YOLO26 four channel on RK3588](yolo26-rk3588.md) | Four channel detection or segmentation built on DX-Stream with RK3588 hardware decode (dx_demo) | Intermediate | RK3588 board with a DEEPX NPU, display |
| [CLIP in C++](clip-cpp.md) | Zero shot text and image matching on a camera or video (T22) | Beginner | DEEPX NPU, display |
| [CLIP in Python](clip-python.md) | CLIP text encoder on the CPU, image encoder on the NPU, camera matching scripts (dx-clip-starter) | Beginner | DEEPX NPU; camera for the live scripts |
| [CLIP multi channel demo](clip-multi-channel.md) | Text and video matching on up to 16 channels with a PyQt or OpenCV GUI (dx_clip_demo) | Beginner | DEEPX NPU, display |
| [Hand landmarks](hand-landmarks.md) | Palm detection and 21 point hand landmarks in C++ (T23) | Beginner | DEEPX NPU, display |
| [PIDNet segmentation](pidnet.md) | Cityscapes semantic segmentation with a live post processing control (T24) | Beginner | DEEPX NPU, display |
| [RapidDoc document parsing](rapiddoc.md) | Parse PDFs into text, tables and formulas with layout and OCR models on the NPU | Intermediate | One or more DEEPX NPUs |

Platform specific setup (Raspberry Pi 5, Orange Pi 5 Plus, Intel GPU) is on [Platform notes](platform-notes.md).

## Where to go

* New to the SDK: start with [Set up the tutorials](setup.md), then [Run the DX-APP examples](dx-app.md).
* Want a first result in minutes: pick a demo above that matches your hardware.
* Want the reference behind the tutorials: [DX-COM](../compiler/index.md), [DX-RT](../runtime/index.md), [DX-APP](../app/index.md), [DX-Stream](../stream/index.md).

## Next steps

* [Set up the tutorials](setup.md)
* [Quickstart](../get-started/quickstart.md)
* [Model Zoo](../model-zoo/index.md)
