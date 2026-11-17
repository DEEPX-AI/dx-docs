---
title: Post processing
description: The DX-APP C++ post processing library and its dx_postprocess Python bindings, how to build them, the 58 classes they provide and how to call them.
---

# Post processing

This page explains our C++ post processing library in `src/postprocess/` and the `dx_postprocess` Python module that exposes it, so Python code can decode model outputs at C++ speed.

Post processing turns raw NPU output tensors into results: it decodes boxes, scores and class ids, runs NMS (non maximum suppression) and thresholds, extracts keypoints, builds segmentation masks, and finishes the output of PPU models, whose first post processing steps already ran on the NPU.

## Before you start

* DX-RT is installed, because `dx_postprocess` links against `libdxrt`. See [Install the DEEPX SDK](../../get-started/install.md).
* Python 3.8 or later, a C++14 compiler (GCC 7.5 or later, or Clang) and CMake 3.16 or later.

## Which code each example uses

| Example | Post processing source |
|---|---|
| `bin/<variant>_sync`, `bin/<variant>_async` (C++) | `src/cpp_example/common/processors/` |
| `<variant>_sync.py`, `<variant>_async.py` | `src/python_example/common/processors/` (Python) |
| `<variant>_sync_cpp_postprocess.py`, `<variant>_async_cpp_postprocess.py` | `src/postprocess/` through `dx_postprocess` |

The C++ examples do not link `src/postprocess/`. The exceptions are four modules, `sfa3d`, `superpoint`, `dope` and `yolopv2`, whose sources are compiled into the C++ examples too.

## Install dx_postprocess

| Method | Command | Use it for |
|---|---|---|
| Default build | `./build.sh` | The normal way: also builds the demo C++ examples |
| Full build | `./build.sh --all` | Every example |
| Standalone | `cd src/bindings/python/dx_postprocess && python3 -m pip install .` | Only the Python module, for example after you change `src/postprocess/` |

The module installs into the active Python (see [Build DX-APP](build.md#build-sh-options)). `pybind11` is installed by pip as a build dependency, and the build uses CMake with scikit-build-core. Check the install:

```bash
python3 -c "import dx_postprocess; print('dx_postprocess successfully installed!')"
```

!!! warning "Rebuild after changes"
    After you edit a module in `src/postprocess/`, rebuild `dx_postprocess`. A stale module gives wrong results; for example, a stale SFA3D module breaks the camera view of 3D detection.

## When it helps

The C++ class makes the post processing stage itself faster. The whole pipeline gets faster only when post processing is the bottleneck, or when the CPU is busy (for example on an embedded board), so less CPU time in post processing helps reading and pre processing. If inference or reading is the slowest stage, FPS barely changes, but CPU use still drops. Check the performance summary of a run to see which stage is slowest.

## Use it from the examples

Run the `*_cpp_postprocess.py` variant of any example:

```bash
python3 src/python_example/object_detection/yolov9/yolov9-s_640x640/yolov9-s_640x640_sync_cpp_postprocess.py \
    --image sample/img/sample_kitchen.jpg

python3 src/python_example/object_detection/yolov9/yolov9-s_640x640/yolov9-s_640x640_async_cpp_postprocess.py \
    --video assets/videos/dance-group.mov
```

Each of these scripts defines an `on_engine_init(runner)` callback and passes it to `run_entry()`. When the engine reports the model input size, the callback creates the model's `dx_postprocess` class and sets it as `runner._cpp_postprocessor`, which replaces the Python post processor. This is the callback of `yolov9-s_640x640_sync_cpp_postprocess.py`:

```python
def on_engine_init(runner):
    from dx_engine import InferenceOption
    from dx_postprocess import YOLOv8PostProcess

    input_w = runner.input_width
    input_h = runner.input_height
    use_ort = InferenceOption().get_use_ort()
    config = runner.factory.config
    score_thr = config.get("score_threshold", 0.3)
    nms_thr = config.get("nms_threshold", 0.45)
    runner._cpp_postprocessor = YOLOv8PostProcess(input_w, input_h, score_thr, nms_thr, use_ort)
    runner._cpp_convert_fn = convert_cpp_detections
```

`dx_postprocess` is imported inside the callback, so `--help` works before the module is built. YOLOv9 uses `YOLOv8PostProcess` because its output has the YOLOv8 layout.

## Call it directly

Create the post processor once, before the inference loop, and pass it the list of output arrays that `InferenceEngine.run()` returns.

=== "Python"

    ```python
    from dx_engine import InferenceEngine, InferenceOption
    from dx_postprocess import YOLOv8PostProcess

    ie = InferenceEngine("assets/models/yolov9-s_640x640.dxnn")
    pp = YOLOv8PostProcess(input_w=640, input_h=640, score_threshold=0.25,
                           nms_threshold=0.45,
                           is_ort_configured=InferenceOption().get_use_ort())

    for input_tensor in inputs:          # letterboxed RGB uint8 images, 640x640x3
        outputs = ie.run([input_tensor]) # list of numpy arrays
        detections = pp.postprocess(outputs)
        # numpy array of shape (N, 6): x1, y1, x2, y2, confidence, class_id
    ```

=== "C++"

    ```cpp
    #include "yolov5_postprocess.h"

    // Create once: input width, input height, objectness, score and NMS thresholds, ORT flag
    YOLOv5PostProcess post_processor(640, 640, 0.25f, 0.3f, 0.45f, false);

    // In the loop, for each frame's output tensors
    auto final_results = post_processor.postprocess(npu_output_tensors);  // std::vector<YOLOv5Result>
    ```

`is_ort_configured` tells the class whether DX-RT runs the model with ONNX Runtime enabled, which changes the output tensors it receives. Read it from `InferenceOption().get_use_ort()` as the examples do. Box coordinates are in model input pixels: undo the letterbox scale and padding yourself to map them to the original image. The Python examples use `LetterboxPreprocessor` from `src/python_example/common/processors/` for this.

The detection classes have these constructors:

| Class | Python arguments |
|---|---|
| `YOLOv5PostProcess`, `YOLOv7PostProcess` | `input_w, input_h, obj_threshold, score_threshold, nms_threshold, is_ort_configured` |
| `YOLOv8PostProcess`, `YOLOv9PostProcess` | `input_w, input_h, score_threshold, nms_threshold, is_ort_configured` |

For any other class, run `python3 -c "import dx_postprocess; help(dx_postprocess.<Class>)"` to see its arguments.

## Classes

`dx_postprocess` wraps 58 C++ classes:

| Task | Classes |
|---|---|
| Object detection | `YOLOv4PostProcess`, `YOLOv5PostProcess`, `YOLOv7PostProcess`, `YOLOv8PostProcess`, `YOLOv9PostProcess`, `YOLOv10PostProcess`, `YOLOv11PostProcess`, `YOLOv12PostProcess`, `YOLOv26PostProcess`, `YOLOXPostProcess`, `NanoDetPostProcess`, `DamoYOLOPostProcess`, `SSDPostProcess`, `EfficientDetPostProcess`, `RTDETRPostProcess` (RT-DETR v1, v2, v3), `PicoDetPostProcess` (PP-ShiTu main body), `PreoptTopKPostProcess` (YOLO26 pre optimized detection and pose) |
| Face detection | `SCRFDPostProcess`, `YOLOv5FacePostProcess`, `RetinaFacePostProcess`, `ULFGFDPostProcess` |
| Face landmark | `Face3DPostProcess` (3DDFA-v2) |
| Pose estimation | `YOLOv5PosePostProcess`, `YOLOv8PosePostProcess`, `VitPosePostProcess`, `CenterPosePostProcess` |
| Keypoint detection | `SuperPointPostProcess` |
| Object pose estimation | `DOPEPostProcess` |
| 3D object detection | `SFA3DPostProcess` |
| Panoptic driving | `YOLOPv2PostProcess` |
| Hand detection and landmarks | `MediaPipeHandPostProcess`, `HandLandmarkPostProcess` |
| Semantic segmentation | `DeepLabv3PostProcess`, `SemanticSegPostProcess` (BiSeNet, SegFormer) |
| Instance segmentation | `YOLOv5SegPostProcess`, `YOLOv8SegPostProcess`, `YOLACTPostProcess`, `MaskRTDETRPostProcess` |
| Image matting | `PPMattingPostProcess` (alpha matte at model resolution) |
| OBB detection | `OBBPostProcess` (YOLO26-OBB) |
| Classification | `ClassificationPostProcess` (all image classification families) |
| Attribute recognition | `AttributePostProcess` (person and face attributes) |
| Depth estimation | `DepthPostProcess` (FastDepth, SCDepth, Depth Anything V2, YOLO26-Depth) |
| Image restoration | `DnCNNPostProcess`, `ESPCNPostProcess`, `RealESRGANPostProcess`, `ZeroDCEPostProcess` |
| Embedding | `EmbeddingPostProcess` (ArcFace and others), `CLIPTextPostProcess` |
| Anomaly detection | `EfficientADPostProcess`, `AnomalyFeaturePostProcess` (PatchCore) |
| PPU models | `YOLOv5PPUPostProcess`, `YOLOv7PPUPostProcess`, `YOLOv8PPUPostProcess`, `YOLOXPPUPostProcess`, `YOLOv3TinyPPUPostProcess`, `SCRFDPPUPostProcess`, `YOLOv5PosePPUPostProcess` |

Anomaly maps, masks and alpha mattes come back at the model resolution, because the module does not use OpenCV; the examples resize them. `SCRFDPPUPostProcess` and `YOLOv5PosePPUPostProcess` exist as classes only: there are no registered SCRFD PPU or YOLOv5-Pose PPU examples.

## The C++ library

`src/postprocess/` has one folder per model family. Folders that end in `_ppu` are for models compiled with PPU (post processing unit) support.

| File | Content |
|---|---|
| `<module>_postprocess.h` | The class (for example `YOLOv5PostProcess`) and its result type (for example `YOLOv5Result`) |
| `<module>_postprocess.cpp` | Decoding, coordinate scaling and filtering |
| `CMakeLists.txt` | For the modules listed in `src/postprocess/CMakeLists.txt` |

The module folders are: `anomaly`, `attribute`, `centerpose`, `classification`, `clip_text`, `damoyolo`, `deeplabv3`, `depth`, `dncnn`, `dope`, `efficientdet`, `embedding`, `espcn`, `face3d`, `hand_landmark`, `mediapipe_hand`, `nanodet`, `obb`, `picodet`, `ppmatting`, `preopt`, `realesrgan`, `retinaface`, `rtdetr`, `scrfd`, `scrfd_ppu`, `semantic_seg`, `sfa3d`, `ssd`, `superpoint`, `ulfgfd`, `vitpose`, `yolact`, `yolopv2`, `yolov3tiny_ppu`, `yolov4`, `yolov5`, `yolov5_ppu`, `yolov5face`, `yolov5pose`, `yolov5pose_ppu`, `yolov5seg`, `yolov7`, `yolov7_ppu`, `yolov8`, `yolov8_ppu`, `yolov8pose`, `yolov8seg`, `yolov9`, `yolov10`, `yolov11`, `yolov12`, `yolov26`, `yolox`, `yolox_ppu`, `zero_dce`.

To use a module from your own C++ code as a shared library, build them with:

```bash
./build.sh --all --make_so
```

This writes `lib/libdxapp_<module>_postprocess.so` for each module listed in `src/postprocess/CMakeLists.txt`. `--make_so` has no effect on the default, `--target` or `--category` builds.

### Fast segmentation

Both example trees also have a generic `FastSegmentationPostprocessor` for semantic segmentation models that output low resolution logits or class maps: it runs argmax before a nearest neighbor resize. It lives in `src/cpp_example/common/processors/segmentation_postprocessor.hpp` and `src/python_example/common/processors/fast_segmentation_postprocessor.py`, and you select it with `--postprocessor fast_segmentation` when you add a model (see [DX tool](dx-tool.md)). It is not a `dx_postprocess` class.

## Next steps

* [Run the examples](run-examples.md)
* [Architecture](architecture.md)
* [Customize a YOLO model](customize-yolo.md)
