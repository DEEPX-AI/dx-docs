---
title: Third party model licenses
description: License terms of the sample models that DX-Stream downloads, and what you need for commercial use.
---

# Third party model licenses

This page tells you what you may do with the sample models that `setup.sh` downloads.

The sample `.dxnn` models are for **evaluation and development only**. They are **not licensed for commercial deployment**.

Each file is compiled from a publicly available third party model that keeps its own license, for example AGPL-3.0, GPL-3.0 or a non commercial research license. Most of these licenses restrict commercial use, for example by requiring you to publish your full source code, or by forbidding commercial use.

For commercial use, either:

* get a license from the original model provider, or
* use your own commercially licensed models, compiled with [DX-COM](../compiler/index.md).

DEEPX is not responsible for legal issues from unauthorized commercial use of these models. You are responsible for following every license that applies.

## Models in DX-Stream 3.2.0

`model_list.json` (model version `2_5_0`, compiled with DX-COM 2.5.0) lists these files. Check the license of the upstream project of each model before you use it.

| File | Used by |
|---|---|
| `yolo26-n_640x640.dxnn` | Object detection demo |
| `yolo26-n-pose_640x640.dxnn` | Pose demo |
| `yolo26-n-seg_640x640.dxnn` | Segmentation demo |
| `yolo26-depth-n_768x768.dxnn` | Depth demo |
| `yolov5-s_640x640_ppu.dxnn` | PPU detection, tracking, multi stream, broker and secondary demos |
| `yolov5-s-face_640x640.dxnn` | Face demo |
| `scrfd-500m_640x640.dxnn` | Face demo and secondary demo |
| `efficientnet-lite0_224x224.dxnn` | Secondary demo |
| `yolov5-s_640x640.dxnn`, `yolov7_640x640.dxnn`, `yolov8-n_640x640.dxnn`, `yolov9-s_640x640.dxnn`, `yolox-s_640x640.dxnn`, `yolo11-n_640x640.dxnn`, `yolov8-m-pose_640x640.dxnn` | Extra models, no demo script |

## Next steps

* [DX-ModelZoo](../model-zoo/index.md)
* [DX-COM](../compiler/index.md)
