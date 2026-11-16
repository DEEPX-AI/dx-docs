---
title: DX-ModelZoo release notes
description: Changes in each DX-ModelZoo release, newest first, starting with 1.0.0 in DEEPX SDK 2.5.0.
---

# DX-ModelZoo release notes

This page lists the changes in each DX-ModelZoo release, newest first.

## 1.0.0 (2026-10-23)

Ships with DEEPX SDK 2.5.0. Contains 497 model configurations. Needs DX-RT 3.5.0 or newer, because its `.dxnn` files use container format v9.

### Breaking changes

* The compile YAML key `compile.quantization` was renamed to `compile.calibration`. Update your own model YAML files.
* The public `--use-gpu` CLI option was removed.

### Changed

* Compile profile parameters are now passed to `dx_com.compile()`.
* PPU and pre optimized model configurations were reorganized.
* DXNN model download paths now use the latest version (`<profile>-dxnn/latest/`).

### Fixed

* Stronger validation of dataset structure, files and labels.
* More consistent model YAML metadata and compile configuration.
* CLIP embeddings are generated, cached and reused.

### Added

* Improvements to the YAML driven model registry.
* New models: YOLO26 depth, pose, classification and segmentation; PaddlePaddle models; CLIP image and text encoders; anomaly detection and person re identification.
* New datasets and evaluation, including MVTec AD.
* Dataset integrity validation and model input contract validation before evaluation starts.

## 0.10.2 (2026-08-05)

* Fixed: EfficientNet-Lite0 input size changed from 256x256 to 224x224.
* Added: YOLO26 depth models at 768x768 (n, s, m, l, x).

## 0.10.1 (2026-07-27)

* Changed: documentation layout and print formatting.
* Fixed: README typos and outdated prerequisites.

## 0.10.0 (2026-06-16)

### Changed

* Model definitions moved from Python classes to a YAML driven model registry.
* YOLO11 models renamed from `yolov11-*` to `yolo11-*` (Ultralytics naming).
* `quantization` in profiles became a nested mapping.
* The `q-pro` profile uses the DX-COM automatic Q-PRO pipeline. Accuracy per model can shift. Calibration defaults to `num_samples: 100`, `method: ema`.
* The `evaluator` type field was removed from model YAMLs. It is inferred from `task`.
* `pycocotools` was replaced by `faster_coco_eval`.

### Fixed

* YOLACT evaluation hang, NMS made deterministic (stable sort), ONNX provider accepts list and int devices.
* Numeric overflow in SSD box decoder and ULFGFD face detection, division by zero in face recognition and segmentation evaluators.
* Evaluator accuracy bugs in ESPCN, YOLOv3-tiny and hand landmark models.
* Missing `c-lite` and `q-pro` profiles in several models, grayscale output shape in preprocessing, denoising and super resolution.

### Added

* `dxmz create` for custom models.
* PPU compile configuration (types 0, 1 and 2, with validation).
* `KeypointDetectionEvaluator`, preprocessing types `add`, `mul`, `subtract`, `totensor`, and conversion of YAML preprocessing to torchvision `Compose`.
* `--seed` option for reproducible evaluation.
* Datasets BDD100K, HOPE and HPatches.
* Models: YOLOv5-Seg, YOLOv8-Seg, OpenCLIP (RN50x16, ViT-B-32, ViT-L-14), BeiT, CAS-ViT, FastViT, GhostNet, RepGhost, RepVGG, ResMLP, MediaPipe hand detector, YOLOv5-Pose, ViTPose, CenterPose, DOPE, SuperPoint, STDC-Seg, PIDNet-S, YOLOPv2, SCDepthV3, Depth-Anything-V2, Real-ESRGAN, ESPCN-x2, Zero-DCE++.

## 0.9.0 (2026-03-30)

* Changed: YOLOXS_PPU preprocessing uses letterbox (pad) mode.
* Fixed: IndexError in YOLOXS_PPU postprocessing; MobileViT, FastViT, ViT and EfficientNet fixes.
* Added: many detection models (CenterNet, DamoYolo, EfficientDet D0 to D6, NanoDet, YOLOv3 to YOLOv10 variants and PPU builds, YOLOX, YOLO26 OBB, segmentation and pose, SSD VGG16), and classification models (FastViT, RepGhost, YOLO26 classification).

## 0.7.0 (2026-01-20)

* Changed: `DXNN_DEVICES` environment variable for device selection; async evaluation for all evaluators; clearer logs and progress bar.
* Fixed: input dtype matching in the NPU session, GoogLeNet NPU preprocessing, COCO pose keypoint scaling, NMS and box handling, pad resize logic.
* Added: `dxmz compile` command; more than 85 new models (YOLO26, YOLOv3, DeepLabV3+, FCN, FastViT, EfficientFormer, DenseNet, RegNet, ShuffleNet, VGG, MnasNet and others).

## 0.6.0 (2025-12-29)

* Added: 51 models, for 110 models in total, including YOLOv10, YOLOv11, DamoYolo, SCRFD, SSD, ResNet, MobileNet, EfficientNet, RegNet, VGG, DnCNN and FastDepth.

## 0.5.1 (2025-08-18)

* Fixed: the Python install script uses the minimum required version when none is given.

## 0.5.0 (2025-08-18)

* Changed: setup merged into `setup.sh` and `install_python_and_venv.sh` (with `--symlink_target_path`); `install.sh` and `setup_venv.sh` removed.
* Fixed: output tensor order workaround removed after the DX-COM 2.0.0 fix.

## 0.4.0 (2025-07-28)

* Changed: setup script refactoring and benchmark documentation update.
* Fixed: separate virtual environment paths for host and container installs.

## 0.3.1 (2025-06-12)

* Fixed: YOLOv7 face postprocessing parsing; output tensor order mismatch between ONNX and DXNN.
* Added: `--debug` flag for `dxmz eval`.

## 0.1.x (2025-05)

* 0.1.5: image denoising fix (BSD68 evaluation type).
* 0.1.3: model list options for download scripts.
* 0.1.2: standalone `setup.sh` fixes.
* 0.1.1: `dxmz eval` argument validation; dataset, model and compile scripts.
* 0.1.0 (2025-05-12): first release with the `dxmz` CLI, sessions, datasets, evaluators and the first classification, detection, segmentation, face and denoising models.

## Next steps

* [DX-ModelZoo overview](../model-zoo/index.md)
* [All release notes](index.md)
