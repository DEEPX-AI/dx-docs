---
title: Agent showcases
description: Apps built on the DEEPX NPU by a coding agent from a single prompt, with what each one demonstrates and how to run it.
---

# Agent showcases

This page lists the apps a coding agent built on the DEEPX SDK from a single plain language prompt, and how to run them yourself.

!!! warning "Beta"
    These showcases demonstrate [agent driven development](agent-driven-development.md), a beta feature. Agents are not deterministic: the same prompt does not always give the same code, time or cost.

Each showcase folder in the `dx-all-suite` repository holds the exact prompt, the generated code, measured results, `setup.sh` and `run.sh`, and the full recorded build session. All of them were built with Claude Code.

## Showcases

| Showcase | Folder | What it demonstrates |
|---|---|---|
| Squat counting mini game | `mini-game-squat-fitness` | YOLO26n-pose on the NPU counts squats from knee and hip angles, with an arcade HUD. Video file or live camera. |
| Stretching coach mini game | `mini-game-stretching-coach` | YOLO26n-pose guides three stretches with an animated coach avatar and stage progress |
| Ultralytics YOLO export | `ultralytics-yolo-deepx-export` | Exports an Ultralytics YOLO26n `.pt` to `.dxnn` with one `yolo export ... format=deepx` command, then runs NPU inference and a check |
| African wildlife monitoring | `ultralytics-retrain-eval-deepx-export-wildlife` | Retrains YOLO26n on `african-wildlife` and compares base and retrained models in fp32 (GPU) and INT8 (DX-M1) |
| Construction PPE safety | `ultralytics-retrain-eval-deepx-export-ppe` | Same flow on `construction-ppe` (helmet, gloves, vest, boots, goggles) |
| Brain tumor screening | `ultralytics-retrain-eval-deepx-export-braintumor` | Same flow on `brain-tumor` (MRI and CT) |
| Pill inspection | `ultralytics-retrain-eval-deepx-export-pills` | Same flow on `medical-pills` |
| Video and webcam OCR | `paddleocr-video-ocr` | PaddleOCR PP-OCRv5 detection, orientation and recognition on the DX-M1, on a video file or a webcam |
| PDF to Markdown | `rapiddoc-pdf2md` | RapidDoc (PP-StructureV3) layout, OCR, table and formula recognition on the DX-M1; outputs Markdown and JSON, with `--parse-method auto`, `txt` or `ocr` |

The one command `format=deepx` export works only for **detection** models on an **x86_64 Linux** host, with INT8. Segmentation, pose, classification and OBB models use the two step path: export to ONNX, then compile with `dxcom`.

### Example result: construction PPE

Measured on the `construction-ppe` validation split at 640×640. fp32 ran on an NVIDIA RTX 5060 Ti; INT8 ran on the DX-M1 through `format=deepx`.

| Model | Form | Device | mAP50-95 | mAP50 | FPS |
|---|---|---|---|---|---|
| base yolo26n | `.pt` fp32 | GPU | 0.0001 | 0.0008 | 219.4 |
| base yolo26n | `.dxnn` INT8 | DX-M1 | 0.0001 | 0.0005 | 46.5 |
| retrained | `.pt` fp32 | GPU | 0.2519 | 0.4892 | 336.3 |
| retrained | `.dxnn` INT8 | DX-M1 | 0.2533 | 0.5058 | 62.3 |

Retraining makes the model useful for the new domain, and INT8 on the NPU keeps the fp32 accuracy. FPS here is `1000 / latency` of single image validation, not a pipeline benchmark; see [DX-Benchmark](benchmark.md) for that.

## Run a showcase

### Before you start

* An x86_64 Linux host with a DEEPX NPU and DX-RT (`dx_engine`). See [Install the DEEPX SDK](../get-started/install.md).
* For the retrain showcases: a local GPU for training.

### Steps

```bash
git clone --recurse-submodules https://github.com/DEEPX-AI/dx-all-suite.git
cd dx-all-suite/dx-agent-dev-showcase/mini-game-squat-fitness
./setup.sh
./run.sh
```

Replace the folder with any showcase from the table. The mini games also accept a camera (for example `./run.sh --camera 0` for the stretching coach, or `DISPLAY_MODE=1 ./run.sh` for a live window in the squat game). Each folder's README lists its own options.

To rebuild a showcase with your own agent, open `dx-all-suite` in the agent and paste the prompt from the showcase README.

## Next steps

* [Start with agent driven development](agent-driven-development.md)
* [Compile models with DX-COM](../compiler/index.md)
