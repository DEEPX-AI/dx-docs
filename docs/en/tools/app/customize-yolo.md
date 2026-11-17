---
title: Customize a YOLO model
description: Add your own YOLO model to DX-APP, choose the right post processor, tune config.json, and build, run and verify it in C++ and Python.
---

# Customize a YOLO model

This page shows how to add your own YOLO family model to DX-APP as a C++ and Python example, pick the matching post processor and tune its thresholds.

## Before you start

* Your model is compiled to a `.dxnn` file with DX-COM. See the [DX-COM overview](../../compiler/index.md).
* Copy the file to `assets/models/<variant>.dxnn`. The variant is the file stem, for example `yolo-custom_640x640`.
* DX-APP is built. See [Build DX-APP](build.md).

## 1. Choose the post processor

The output tensor layout of the compiled model decides the post processor. The model name is only a hint.

| Model type | Typical output | `--postprocessor` | C++ post processor | Python post processor |
|---|---|---|---|---|
| YOLOv3, v4, v5 style detection with anchors | Box, objectness and class scores | `yolov5` | `YOLOv5Postprocessor` (the registered `yolov4-*` C++ examples use `EfficientDetPostprocessor`) | `YOLOv5Postprocessor` |
| YOLOv7 detection with anchors | YOLOv7 anchors and strides | `yolov7` | `YOLOv7Postprocessor` | `YOLOv5Postprocessor` with the model config |
| YOLOX | Anchor free YOLOX detection | `yolox` | `YOLOXPostprocessor` | `YOLOXPostprocessor` |
| YOLOv8, v9, v10, v11, v12, v13, YOLO26 detection | Anchor free (DFL style), no objectness | `yolov8`, `yolov9`, `yolov10`, `yolov11`, `yolov12`, `yolov13`, `yolov26` | `YOLOv8Postprocessor` (v8, v9, v11, v12, v13; `yolo11-n_640x640` uses `YOLOv11Postprocessor`), `YOLOv10Postprocessor` (v10), `YOLOv26Postprocessor` (YOLO26) | `YOLOv8Postprocessor` family |
| YOLO segmentation | Boxes and mask prototypes | `yolov8seg`, `yolov26seg`, `yolov5seg` | Task specific segmentation post processor | Task specific segmentation post processor |
| YOLO pose | Boxes and keypoints | `yolov5pose`, `yolov8pose`, `yolov26pose` | Task specific pose post processor | Task specific pose post processor |
| YOLO face detection | Face boxes and optional landmarks | `yolov5face`, `yolov7face` | Face post processor | Face post processor |
| YOLO OBB | Oriented boxes | `yolov26obb` | OBB post processor | OBB post processor |
| YOLO with PPU | Output already partly decoded on the NPU | `yolov5_ppu`, `yolov7_ppu`, `yolov8_ppu`, ... | PPU post processor | PPU post processor |

A new detection only YOLO whose output fits the YOLOv8 anchor free layout should start with `--postprocessor yolov8`. A model with explicit objectness and anchor grid decoding should start with `yolov5` or `yolov7`. `yolov12` and `yolov13` select `YOLOv8Postprocessor`, because their outputs have the YOLOv8 layout.

## 2. Generate the example

```bash
# YOLOv8 style detection
./scripts/add_model.sh yolo-custom_640x640 object_detection --postprocessor yolov8 --lang both

# YOLOv7 style detection with a new input size
./scripts/add_model.sh yolov7-custom_1280x1280 object_detection --base-model yolov7_640x640 --input-size 1280x1280 --lang both

# YOLOX style detection
./scripts/add_model.sh custom-yolox_640x640 object_detection --postprocessor yolox --lang both
```

This creates:

```text
src/cpp_example/object_detection/<family>/<variant>/
├── factory/<variant>_factory.hpp
├── <variant>_sync.cpp
├── <variant>_async.cpp
└── config.json

src/python_example/object_detection/<family>/<variant>/
├── factory/<variant>_factory.py
├── config.json
├── <variant>_sync.py
├── <variant>_async.py
├── <variant>_sync_cpp_postprocess.py
└── <variant>_async_cpp_postprocess.py
```

`add_model.sh` also adds the variant to `config/model_registry.json` and `config/test_models.conf`. Pass `--no-register` for a local experiment. All options are on [DX tool](dx-tool.md#add-a-model). Review both trees afterwards: the generated factory is a safe starting point, not a final result.

## 3. Tune config.json

Put your settings inside the `config` object of each variant's `config.json`, and keep the C++ and Python files the same.

| Key | Meaning | Use it for |
|---|---|---|
| `obj_threshold` | Objectness threshold | YOLOv5, v7 and YOLOX style models |
| `score_threshold` | Class confidence threshold (Python reads it as `conf_threshold`; C++ ignores `conf_threshold`) | All detection models |
| `nms_threshold` | IoU threshold for NMS | All detection models |
| `num_classes` | Number of classes | Datasets other than the 80 COCO classes |
| `class_names` | Display labels (C++ only; Python labels come from `custom_labels` in the `visualizer` kwargs of `config.json`) | Custom labels |
| `strides` | Output strides of the Python PPU decoders (`YOLOv5PPUPostprocessor`, `YOLOv7PPUPostprocessor`) | PPU models with non standard heads |

A custom YOLOv5 style model with 3 classes:

```json
{
  "config": {
    "obj_threshold": 0.25,
    "score_threshold": 0.30,
    "nms_threshold": 0.45,
    "num_classes": 3,
    "class_names": ["person", "vehicle", "animal"]
  }
}
```

A custom YOLOv8 style model has no `obj_threshold`:

```json
{
  "config": {
    "score_threshold": 0.30,
    "nms_threshold": 0.45,
    "num_classes": 3,
    "class_names": ["person", "vehicle", "animal"]
  }
}
```

!!! warning "num_classes must match the compiled model"
    If the model was compiled with another class count, changing `config.json` does not change the tensor shape. Recompile the model instead.

!!! note "How each language reads config.json"
    Python reads the `config.json` next to the script automatically. C++ reads it only with `--config <path>`; without it, the factory defaults apply. In C++ the members of `config` override top level keys; in Python top level keys override `config`, so keep your keys inside `config`. Custom anchors are not read from `config.json`: C++ uses the post processor presets, and Python variants that need them set them in the variant's `custom_ops.py`.

## 4. Review the factory

Factories assemble the pre processor (`LetterboxPreprocessor` or `DetectionPreprocessor`), the YOLO post processor and `DetectionVisualizer`.

=== "Python"

    The post processor class is set in the variant's `config.json`, and the family factory builds it:

    ```json
    "postprocessor": {
      "class": "YOLOv8Postprocessor",
      "args": [{"token": "input_width"}, {"token": "input_height"}, {"token": "config"}]
    }
    ```

=== "C++"

    ```cpp
    PostprocessorPtr<DetectionResult> createPostprocessor(
        int input_width, int input_height, bool is_ort_configured = false) override {
        return std::make_unique<YOLOv8Postprocessor>(
            input_width, input_height,
            score_threshold_, nms_threshold_,
            is_ort_configured,
            num_classes_,
            class_names_
        );
    }

    void loadConfig(const dxapp::ModelConfig& config) override {
        score_threshold_ = config.get<float>("score_threshold", score_threshold_);
        nms_threshold_ = config.get<float>("nms_threshold", nms_threshold_);
        class_names_ = config.get_string_list("class_names");
        num_classes_ = config.get<int>("num_classes", num_classes_);
    }
    ```

Check that:

* `get_model_name()` returns the new name and `get_task_type()` stays `object_detection`.
* C++ and Python use the same post processor family.
* Thresholds and class data come from `config.json`.
* Other tasks (segmentation, pose, OBB) use their own visualizer and runner.

## 5. Check the output shape

Typical YOLOv5 and v7 outputs are one decoded tensor `[1, N, 5 + num_classes]`, or multi scale tensors `[1, C, H, W]` with `C = anchors * (5 + num_classes)`, with objectness. YOLOv8 and later detection outputs are anchor free, with no objectness field.

If verification fails because of an unexpected tensor shape:

1. Run with `--show-log`.
1. Dump the tensors with `--dump-tensors`.
1. Compare the output tensor names, shapes and value ranges with the reference model.
1. Adjust the factory or config only if the output family is compatible.
1. Write a new post processor only when the tensor layout is really different.

## 6. Build and run

```bash
./build.sh --type debug --target <variant>_sync <variant>_async
```

=== "Python"

    ```bash
    python3 src/python_example/object_detection/<family>/<variant>/<variant>_sync.py \
        --model assets/models/<variant>.dxnn --image sample/img/sample_kitchen.jpg --no-display --loop 1

    python3 src/python_example/object_detection/<family>/<variant>/<variant>_async.py \
        --model assets/models/<variant>.dxnn --video assets/videos/dance-group.mov --no-display --loop 1
    ```

=== "C++"

    ```bash
    ./bin/<variant>_sync -m assets/models/<variant>.dxnn -i sample/img/sample_kitchen.jpg --no-display -l 1 \
        --config src/cpp_example/object_detection/<family>/<variant>/config.json

    ./bin/<variant>_async -m assets/models/<variant>.dxnn -v assets/videos/dance-group.mov --no-display -l 1 \
        --config src/cpp_example/object_detection/<family>/<variant>/config.json
    ```

Add `--save` to keep the rendered output for a visual check.

## 7. Verify before you register it

```bash
./scripts/dx_tool.sh run --lang cpp --filter <variant>
./scripts/dx_tool.sh run --lang py --filter <variant>
./scripts/dx_tool.sh validate
./run_tc.sh --cpp --cli
./run_tc.sh --python
```

When the model is meant to ship as an example, review the rows that `add_model.sh` added to `config/model_registry.json` and `config/test_models.conf`. A row names the model, `.dxnn` file, task, post processor family, input size, support status and config. Do not register local experiments, and do not register metadata that points to a `.dxnn` that is not available.

## Troubleshooting

| Symptom | What to check |
|---|---|
| No detections | Lower `score_threshold` for a test. Check that the post processor family matches the output layout, that `num_classes` matches the model, and that the model expects letterbox pre processing |
| Boxes shifted or scaled wrong | Check the input width and height, letterbox versus plain resize, and compare C++ and Python on the same image |
| NMS removes too many boxes | Change `nms_threshold`; lower `score_threshold` to see whether candidates exist before NMS |
| C++ and Python results differ | Same thresholds, class count and labels in both `config.json` files, pass `--config` to C++, same post processor family. Compare with `--no-display` and `DXAPP_VERIFY=1`. Check whether one side uses a `*_cpp_postprocess` script |
| Build target missing | The variant folder must be the `.dxnn` stem under `<family>/`. Run `./build.sh --target list` |

## Checklist

* The post processor family matches the output tensor layout.
* C++ and Python use matching pre and post processing.
* `config.json` has the right thresholds and `num_classes`.
* The model runs on an image, and the async example runs on image or video.
* The saved output looks right.
* `./scripts/dx_tool.sh validate` passes, and the sync and async targets build.
* Registry and test rows are updated only for models that ship.

## Next steps

* [DX tool](dx-tool.md)
* [Post processing](post-processing.md)
* [Run the examples](run-examples.md)
