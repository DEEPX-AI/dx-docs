---
title: DX-APP release notes
description: What changed in each DX-APP release, newest first, from 3.3.0 back to 1.10.0.
---

# DX-APP release notes

This page lists the changes in each DX-APP release, newest first.

DX-APP 3.3.0 ships with DEEPX SDK 2.5.0:
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
## 3.3.0 (2026-10-23)

!!! warning "Breaking changes"
    Example folders, executables, build targets and Python scripts are now named after the variant (the `.dxnn` stem), for example `yolov9s_sync` became `yolov9-s_640x640_sync`. Update any script that calls the old names. DX-RT 3.5.0 or later is required.

### Changed

* **Example layout:** the C++ and Python examples are now in `<task>/<family>/<variant>/` folders. The variant is the `.dxnn` stem, and each C++ factory is in the namespace `dxapp::v_<variant>`.
* **Task renames:**
    * `classification` is now `image_classification`.
    * `embedding` is split into `face_recognition`, `image_retrieval`, `visual_place_recognition` and `zero_shot_image_classification`.
    * `attribute_recognition` is split into `person_attribute` and `face_attribute`.
    * `reid` is split into `image_classification` and the new task `person_reid`.
    * `instance_segmentation` (FastSAM) is now `zero_shot_instance_segmentation`.
    * `obb_detection` is now `oriented_object_detection`.
    * `image_enhancement` is now `low_light_enhancement`.
    * `face_alignment` is now `face_landmark`.
* **PPU models** moved under `object_detection/yolo_ppu`.
* **Classification sample:** `efficientnet-lite0_224x224` replaces `efficientnet-lite0_256x256`.
* **Model Zoo manifest** moved to the `2_5_0` URL hierarchy (`models.ver`, `modelzoo_manifest.json`).
* **DX-RT 3.5.0 required:** Model Zoo 2_5_0 `.dxnn` files are container format v9, which needs DX-RT 3.5.0 or later. The C++ examples check the version at start.
* **`add_model.sh`** takes a variant as its first argument and adds `--family`, `--input-size`, `--dxnn` and `--no-register`. `config/model_registry.json` rows gain `variant`, `family` and `task` (plus `task_legacy`, `image_only`, `zoo_canonical`, `alias_of` and `published`).
* **Package pruning:** `scripts/extract_model_package.sh` now copies only the `common/` files the model needs. Use `--no-prune` for a full copy.
* **Ubuntu 18.04** (end of life) is no longer supported.

### Fixed

* Async runners called the shared post processor from several DX-RT callback threads at once. `DXAPP_VERIFY` records now follow input order.
* Retrieval, re-id and `--check` gallery paths depended on the working folder.
* SuperPoint keypoints were drawn at the wrong vertical position in the C++ example.
* SuperPoint tracker settings (`nn_thresh`, `max_pixel_dist`, `track_max_length`) were ignored.
* All 998 `*_cpp_postprocess.py` examples ran the Python post processor instead of `dx_postprocess`. Each installs its C++ class again, and `run_entry()` passes `on_engine_init` to the runner.
* `dx_postprocess` results differed from the Python and C++ examples: `ClassificationPostProcess` applied softmax to outputs that were already a distribution and broke top 1 ties differently; `VitPosePostProcess` returned heatmap cells instead of input pixels; DAMO-YOLO and NanoDet NMS suppressed per class instead of across classes; CenterPose ranked its heads and snapped keypoints differently.
* Python post processors ignored the variant's `score_threshold` and ran at their 0.3 default. `YOLOv7PPUPostprocessor` decoded with the YOLOv5 anchors (boxes about 0.82x the C++ size).
* `dx_postprocess` rejected numpy int64 arrays (such as CLIP token ids) on LP64 platforms.
* 3D object detection C++ runners printed messages without the `[DXAPP]` prefix.
* `scripts/bench_models.sh` read `config/test_models.conf` with the wrong column count and reported every row as `NO_MODEL`. It now benchmarks each of the 497 variants.

### Added

* The multi model graph engine and the CLI `multi_model_graph_sync` and `multi_model_graph_async` (`--check`, `--list-models`, `--report`).
* 147 more DX Model Zoo models, including RT-DETR, YOLOv12, YOLOv13, pre optimized YOLO, anomaly detection, image matting, CLIP retrieval, person re-id and visual place recognition.
* Sample galleries for re-id, image retrieval and visual place recognition.
* `dx_postprocess` classes for the eight post processors that had none (50 to 58 classes): `EfficientADPostProcess`, `AnomalyFeaturePostProcess` (PatchCore), `RTDETRPostProcess` (RT-DETR v1, v2, v3), `MaskRTDETRPostProcess`, `PreoptTopKPostProcess` (YOLO26 pre optimized detection and pose), `PicoDetPostProcess` (PP-ShiTu main body), `PPMattingPostProcess` and `CLIPTextPostProcess`. Anomaly maps, masks and alpha mattes come back at model resolution, and the examples resize them.

## 3.2.2 (2026-08-14)

### Changed

* SuperPoint point tracking moved from the keypoint post processing into the visualizer.
* The depth estimation demo uses YOLO26-Depth-S instead of Depth-Anything-V2.
* The super resolution demo uses a new low resolution video, `lowres-drone-city-road.mp4`.

### Fixed

* The Windows full build did not run in parallel; shared files are now copied once.
* On Windows, C++ async mode now runs the `_async` binary.
* Grammar errors in the installation and build documentation.

### Added

* YOLO26-Depth examples for all five sizes (n, s, m, l, x at 768x768): C++ sync and async, and the four Python variants.
* The five YOLO26-Depth models in `config/model_registry.json` and `scripts/modelzoo_manifest.json`.
* Sample video archive v3.2.2 with a low resolution video for super resolution.

## 3.2.1 (2026-08-03)

### Changed

* Example commands use the new model file names (for example `YoloV9S.dxnn` became `yolov9-s_640x640.dxnn`).
* Super resolution saves both a side by side comparison (`sr_input_output.jpg`) and the upscaled output.
* The super resolution sample images are real low resolution inputs (`sample_superresolution.png` removed).

### Fixed

* RealESRGAN output colors differed from C++: color rounding and RGB to BGR order are corrected, and 3 channel models no longer go through the luminance only tiled path.
* The C++ async runners lost the end of a saved video; they now drain the queue before stopping the display thread.
* Headless pose runs with only `DXAPP_SAVE_IMAGE` set wrote no image.
* ESPCN now gets the BT.601 limited range Y channel.
* Tile seams in tiled super resolution: tiles now overlap by the model's receptive field radius.

### Added

* `--sr-tile-halo` option (0 to 4, default 4) for the tile overlap of tiled super resolution.

## 3.2.0 (2026-07-22)

### Changed

* Image only examples (embedding, re-id, attribute) show an input hint and reject stream inputs.
* Detection examples expose score, NMS, top k and objectness settings in `config.json`, with defaults that keep the output unchanged.
* Messages use the level tags `[DXAPP] [INFO]`, `[DXAPP] [WARN]` and `[DXAPP] [ERROR]`.
* The OBB detection sample image (from DOTA8) is replaced by an AI generated satellite image, to remove a licensing risk. The third party license notice gains a clause on AI generated sample data.
* Model Zoo manifest moved to the `2_4_0` URL hierarchy.
* Float input pre processing is generalized (`runSyncInferenceTyped`, `fillModelInputBuffer`).
* `build.sh` builds the minimal set by default and prints the other options; the `build.bat` prompt defaults to minimal.

### Fixed

* Super resolution keeps the input resolution, with dynamic tile padding instead of a fixed downscale.
* The `dx_postprocess` build was missing the `<cmath>` and `<numeric>` includes.
* An invalid `--image` path prints a sample image hint and exits with code 1.
* `--save` wrote no image in the C++ sync runners for face, OBB, pose and instance segmentation.
* The order of the `inflight_current` decrement in the async runner metrics.
* DOPE: half pixel center offset and normalized output.
* YOLOPv2: vehicle only filtering, class agnostic NMS and letterbox inverse transform; the driving mask type in the visualizer.
* RetinaFace: NHWC feature map decoding (for example `retinaface_mobilenet_v1_736x1280`).
* Depth Anything V2: per model ImageNet mean and std normalization.
* The Windows x64 DX-RT library path (`lib/x64`).
* Exported C++ packages always link `Threads::Threads`.
* E2E test model matching with underscores (for example `YoloV7W6` and `yolov7_w6`).

### Added

* Agent driven development (beta): an AI agent generates standalone Python or C++ inference apps from plain language.
* Native C++ post processing for the example models (YOLO families, semantic segmentation, Face3D, embedding, classification, attribute, restoration, YOLO PPU).
* The opt in `--fast-postprocess` path for object detection and instance segmentation.
* The YOLO customizing guide.
* Windows standalone Visual Studio solution packages for C++ examples, with automatic OpenCV and DX-RT configuration.
* The `--demo-models` option to download only the `run_demo` models.
* Minimal and category builds, and a Windows build selection menu.
* 69 net new models (86 added, 17 removed): the registry grows from 280 to 347 models in 22 tasks.
* Five new tasks: 3D object detection (SFA3D), keypoint detection (SuperPoint), object pose estimation (DOPE), panoptic driving perception (YOLOPv2) and hand detection (MediaPipe Hand).
* Seven post processors with Python bindings (43 to 50 classes): DOPE, MediaPipe Hand, RealESRGAN, SFA3D, SuperPoint, VitPose, YOLOPv2.
* C++ factory interfaces `IObjectPoseFactory`, `IKeypointDetectionFactory` and `IPanopticDrivingFactory`, and visualizers for DOPE (3D cuboid), SuperPoint and YOLOPv2 (lane and drivable area).
* The four Python variants and the C++ sync and async examples for every new model.
* `build.sh --all` for a full build and install in one command.
* `build.bat` command line options (`--minimal`, `--all`, `--category`, `-h`, `--help`).

## 3.1.1 (2026-05-06)

### Fixed

* Typos in the DX-APP user manual.

### Added

* License information for third party models and datasets.

## 3.1.0 (2026-04-10)

### Changed

* One five layer architecture for Python and C++: app (entry point), runner (sync or async), factory (per model), components (pre processor, post processor, visualizer) and interfaces, with a one to one mapping of common modules between the languages.
* `--model`, `--image` and `--video` are optional: without them, a default model and a task specific sample are used.
* `setup_sample_models.sh` uses a Python downloader with `--list`, `--dry-run`, `--category`, `--models` and more. `setup.sh` accepts the same model options.
* `run_demo.sh` is redesigned: 18 demo models, a three step menu (task, mode, input), C++ and Python, and `--task`, `--mode`, `--input` for non interactive use.
* The display window shows frames at their original resolution, sized to about a quarter of the screen.

### Added

* Depth estimation (FastDepth) and image restoration (DnCNN, Zero-DCE, ESPCN) tasks.
* The full DX Model Zoo: 280 models in 17 tasks with 560 C++ and Python examples.
* YOLOv8, v9, v10, v11 and v12 PPU models and examples.
* Manifest based automatic model download (`scripts/download_models.py`), also called by the examples when a model or video is missing.
* An interactive mode for `scripts/run_examples.sh`, also used by `dx_tool.sh run`.
* A live performance table while examples run.
* `--show-log` for the Python examples.

## 3.0.2 (2026-02-26)

### Changed

* MSVC builds copy the DX-RT and vcpkg DLLs into `bin`.

### Fixed

* Windows build errors from experimental filesystem includes and float literals.
* `apply_argmax` refactored to fix gcovr warnings.

### Added

* A vcpkg install script for the Windows build.

## 3.0.1 (2026-02-09)

### Fixed

* The attribute size in YOLO post processing follows the model output shape instead of a fixed value.

### Added

* YOLO26 classification, pose, segmentation and OBB examples.

## 3.0.0 (2026-01-16)

!!! warning "Breaking changes from 2.x"
    The `demos/` folder and the JSON configuration files in `example/` are removed. Use the examples in `src/cpp_example/` and `src/python_example/`, configured from the command line. Some YOLO post processing type names changed; aliases keep the old names working.

### Changed

* The demo applications are replaced by an example system split by task, model, execution mode (sync, async) and post processing (Python, pybind), with `run_demo.sh` and `run_demo.bat` on top.
* CMake configuration and shared library support improved; C++17 and Visual Studio 2022 (v143) for Windows; DX-RT include and link folders adjusted for cross compiling.
* All examples support sync and async modes; image, video, camera and RTSP input; `--no-display`; and a profiler with per stage latency, end to end FPS and timestamped reports.
* New models: YOLOv10, YOLOv11, YOLOv12, YOLOv8 segmentation, DeepLabV3, and PPU versions of YOLOv5, YOLOv7 and SCRFD in Python and C++.
* New example and installation guides.

### Fixed

* Error handling with try and catch in all projects, `std::invalid_argument` for unmet layer requirements, no more `using namespace std`, and better argument checks and messages.
* Camera and RTSP use a buffer size of 1 for speed; input tensors stay alive until async inference completes.

### Added

* The `dx_postprocess` pybind11 module, installed into the current Python.
* A pytest test system with E2E tests for all Python examples (93.65% coverage or more) and `.coveragerc`.
* Examples for EfficientNet, YOLO26, YOLOv5, v7, v8, v9, YOLOX, SCRFD, YOLOv5-Face, YOLOv5-Pose (with skeleton drawing), YOLOv8-seg and DeepLabV3.

### Removed

* `demos/` (classification, object detection, segmentation, pose, face recognition, denoiser and the combined demos), `example/` JSON files, Debian packaging, the Docker build file, `demo_utils/`, old YOLOv5 post processing and RISC-V 64 support.

### Known issues

* DX-COM 2.1.0 and 2.2.0 cannot convert face and pose models to PPU format. The PPU demo models were converted with DX-COM 1.60.1.

## 2.1.0 (2025-11-28)

### Changed

* Build script documentation; `build.bat` uses C++17 and v143 (Visual Studio 2022).
* Model package 2.1.0 with PPU models; the demo script gains PPU demos (1, 4, 6, 8, 11).
* CPU PyTorch wheel source in `templates/python/requirements.txt`.

### Fixed

* MSBuild warnings from implicit casts; tensor allocation in the ImageNet example; `numBoxes` in `LayerReorder`; YOLO post processing type names (with aliases); VAAPI with camera input; final FPS shown after a forced stop; a 20 s countdown in the demo menu.

### Added

* Windows support: Windows 10 and 11, NPU driver 1.7.1 or later, DX-RT 3.1.0 or later, Python 3.8 or later, Visual Studio Community 2022, and `build.bat` with solution generation.
* PPU data types BBOX, POSE and FACE, and post processing for PPU output.

### Known issues

* DeepLabV3 accuracy may be slightly lower with DX-COM 2.1.0; the demo model was compiled with DX-COM 2.0.0.
* DX-COM 2.1.0 cannot convert face and pose models to PPU format.

## 2.0.0 (2025-09-08)

### Changed

* The YOLO pybind11 post processing guide got its own document; `yolo_pybind_example.py` uses `RunAsync()` and `Wait()` instead of callbacks.
* Demo code refactored, common utilities consolidated, legacy code removed.
* `YoloPostProcess` picks the output tensor by name when `USE_ORT=ON`.
* Clearer help messages, a YOLOv5s-6 JSON example, and OS and architecture checks in the build script.

### Fixed

* FPS in `yolo_multi`, legacy PPU post processing removed, new YOLO output shapes with `USE_ORT=OFF`, a framebuffer path typo, and clearer tensor size errors.

### Added

* An uninstall script, version guards for DX-RT 3.0.0 and model format 7, `target_output_tensor_name` and per layer `name` in the JSON config, automatic reordering of layer parameters, SCRFD decoding, and yolo_pose and yolo_face post processing (with `USE_ORT=ON`).

## 1.11.0 (2025-07-23)

### Changed

* `build.sh --clean` also removes pybind artifacts; model files updated from 1.40.2 to 1.60.1; a missing file runs the setup script or prints a guide.

### Fixed

* Colored, reordered error messages in the install and build scripts; YOLO layer tensor index; `dx_postprocess` build errors.

## 1.10.0 (2025-06-17)

* First release: demos for classification, object detection, pose estimation, detection with segmentation, semantic segmentation and multi channel detection, and templates for classification, object detection and Python (sync, async and pybind C++).

## Next steps

* [DX-APP overview](../app/index.md)
* [All release notes](index.md)
