---
title: DX tool
description: Use scripts/dx_tool.sh and its helper scripts to add, list, validate, run, benchmark and package DX-APP examples.
---

# DX tool

This page shows how to use `scripts/dx_tool.sh`, our developer tool for adding, inspecting, validating, running, benchmarking and packaging DX-APP examples.

Use it when you add or change examples. To only build and run the existing examples, [Build DX-APP](build.md) and [Run the examples](run-examples.md) are enough.

## Before you start

* DX-APP is built and its models are downloaded:

    ```bash
    ./setup.sh
    ./build.sh --clean --all
    ```

* Run every command from the `dx_app/` folder.

## Commands

Run `./scripts/dx_tool.sh` with no command for a guided menu, or give a command:

```bash
./scripts/dx_tool.sh list
./scripts/dx_tool.sh search yolov9
./scripts/dx_tool.sh info yolov9-s_640x640
./scripts/dx_tool.sh help
```

| Command | What it does |
|---|---|
| `add` | Create a new example for a model (interactive front end of `add_model.sh`) |
| `extract` | Export one example as a standalone package |
| `list` | List the example models by task |
| `search <keyword>` | Search models by keyword |
| `info <variant>` | Show the details of one model |
| `delete <path>` | Delete example folders (`<task>/<family>/<variant>`, or a family name for the whole family). Registry and `test_models.conf` rows stay |
| `new-task` | Generate the `common/` skeleton (post processor, visualizer, factory interface, sync and async runner) for a new task type |
| `validate` | Build and run (NPU inference) every supported registry model through `validate_models.sh`, generating any example that is missing. Asks for the language and scope |
| `run` | Run examples with filters (`scripts/run_examples.sh`) |
| `bench` | Benchmark examples with filters (`scripts/bench_models.sh`) |
| `help` | Show the usage |

A typical contributor sequence:

```bash
./scripts/dx_tool.sh list
./scripts/dx_tool.sh validate
./scripts/dx_tool.sh run --lang both
./run_tc.sh --cpp --cli
./run_tc.sh --python
```

## Add a model

1. Look for an existing example first, to avoid duplicate names:

    ```bash
    ./scripts/dx_tool.sh search yolov8
    ```

1. Generate the example. `./scripts/dx_tool.sh add` asks for the language, task, reference post processor, variant name, family and whether to make sync only. Or call `add_model.sh` directly:

    ```bash
    # From a post processor family
    ./scripts/add_model.sh yolo-custom_640x640 object_detection --postprocessor yolov8

    # Copy an existing variant with a new input size
    ./scripts/add_model.sh yolov7-custom_1280x1280 object_detection --base-model yolov7_640x640 --input-size 1280x1280

    # Open a new family
    ./scripts/add_model.sh my-det_640x640 object_detection --family my_det --postprocessor yolov5

    # Generate and verify in one step
    ./scripts/add_model.sh yolo-custom_640x640 object_detection --postprocessor yolov8 \
        --verify --model assets/models/yolo-custom_640x640.dxnn
    ```

1. Review the generated files under `src/cpp_example/<task>/<family>/<variant>/` and `src/python_example/<task>/<family>/<variant>/`.
1. Build and run it:

    ```bash
    ./build.sh --target <variant>_sync <variant>_async
    ./scripts/dx_tool.sh run --lang cpp --filter <variant>
    ./scripts/dx_tool.sh run --lang py --filter <variant>
    ```

The first argument of `add_model.sh` is the variant: the `.dxnn` stem, which is also the folder name. With `--postprocessor`, the reference is the first registered variant (alphabetically) that uses that post processor, preferring the same task. `add_model.sh` writes the C++ factory (namespace `dxapp::v_<variant>`), the C++ sync and async entries, the Python factory and the four Python entry scripts that the reference has, and `config.json`. It adds the variant to `config/model_registry.json` and `config/test_models.conf` unless you pass `--no-register`. A variant that is already registered takes its family, model file and input size from its row.

| Option | What it does |
|---|---|
| `--postprocessor <type>` | Post processing family to copy from |
| `--base-model <variant>` | Copy this existing variant instead of the default reference |
| `--family <name>` | Family folder (default: the registry row's family, else the reference's) |
| `--input-size <WxH>` | Model input size (default: the registry row's, else the reference's) |
| `--dxnn <file>` | Model file name (default `<variant>.dxnn`) |
| `--no-register` | Do not add the variant to `model_registry.json` and `test_models.conf` |
| `--lang <lang>` | `cpp`, `py` or `both` (default `both`) |
| `--sync-only` | Generate only the sync entries |
| `--verify` | Build and run inference after generating |
| `--model <path>` | `.dxnn` file for `--verify` |
| `--no-video` | With `--verify`, test image input only |
| `--auto-add` | Generate the example of every registry row that has none |

Common `--postprocessor` values:

| Task | Values |
|---|---|
| Object detection | `yolov5`, `yolov7`, `yolov8`, `yolov9`, `yolov10`, `yolov11`, `yolov12`, `yolov13`, `yolov26`, `yolox`, `damoyolo`, `nanodet`, `ssd` |
| Semantic segmentation | `deeplabv3`, `bisenetv1`, `bisenetv2`, `segformer`, `fast_segmentation` |
| Instance segmentation | `yolov5seg`, `yolov8seg`, `yolov26seg` |
| Pose estimation | `yolov5pose`, `yolov8pose`, `yolov26pose` |
| Face detection | `scrfd`, `yolov5face`, `yolov7face` |

Use `fast_segmentation` for semantic segmentation models that output low resolution logits or class maps. For YOLO models, see [Customize a YOLO model](customize-yolo.md). Use `new-task` only for a task type that does not exist yet.

## Validate

```bash
./scripts/dx_tool.sh validate
./scripts/validate_models.sh --lang py
```

`validate_models.sh` builds and runs the example of every supported registry row whose `.dxnn` is present. A row without an example is generated first.

| Option | What it does |
|---|---|
| `--lang <lang>` | `cpp`, `py` or `both` |
| `--skip-verify` | Only generate missing examples, no inference |
| `--no-video` | Image input only |
| `--list` | Print the commands without running them |
| `--start-from <model_name>` | Resume from a registry `model_name` |
| `<task_filter>` | Filter by the registry `add_model_task` (for example `object_detection`, `classification`, `pose`, `obb`, `ppu`). Task folder names such as `image_classification` are rejected |

!!! warning "Do not use validate_models.sh --clean"
    `--clean` is a cleanup for the flat layout of releases before 3.3.0. On the current tree it deletes every `<task>/<family>/` folder whose name is not a registry `model_name`, including examples that ship with DX-APP.

## Run

`./scripts/dx_tool.sh run` with no options opens the six step menu of `scripts/run_examples.sh`. With options, it passes them on:

```bash
./scripts/dx_tool.sh run --lang cpp --category face_detection --filter scrfd
scripts/run_examples.sh --lang py --filter yolov9
scripts/run_examples.sh --lang cpp --sync-only --no-video
```

| `run_examples.sh` option | What it does |
|---|---|
| `--lang <cpp, py or both>` | Language (default `both`) |
| `--filter <STR>` | Only models whose name contains STR |
| `--category <CAT>` | Only models of this category |
| `--exe <NAME>` | One C++ executable by name, for example `yolov9-s_640x640_sync` |
| `--no-video` (or `--skip-video`) | Skip video tests |
| `--video-only` | Skip image tests |
| `--sync-only`, `--async-only` | C++ sync or async only |
| `--display`, `--no-display` | Show windows (default: off) |
| `--display-delay <s>` | Seconds between displayed tests (default 1.0) |
| `--save-images` | Save the output of each test |
| `--save-dir <dir>` | Base folder for saved output |

`BUILD_DIR=<dir>` overrides the C++ binary folder (default `bin`).

## Benchmark

`./scripts/dx_tool.sh bench` with no options asks for the language, input type, iterations, warmup and filter, then runs `scripts/bench_models.sh`:

```bash
./scripts/dx_tool.sh bench --lang both --filter yolov8 --loops 5
scripts/bench_models.sh --lang cpp --loops 5
```

| `bench_models.sh` option | What it does |
|---|---|
| `--lang <cpp, py or both>` | Language (default `both`) |
| `--loops <N>`, `-l` | Image iterations (default 3) |
| `--warmup <N>`, `-w` | Warmup runs before measuring (default 1) |
| `--filter <STR>`, `-f` | Only variants or families that contain STR |
| `--category <T>`, `--task <T>` | Only one task, for example `image_classification` |
| `--timeout <SEC>` | Time limit per run, 0 for none (default 900, or `BENCH_TIMEOUT`) |
| `--video` | Video input instead of image |
| `--output-dir <DIR>` | Output folder (default `logs/bench_<timestamp>`) |
| `--csv-only` | CSV only, no summary table |
| `--compare <CSV>` | Compare with an earlier results CSV |

The output folder holds `results.csv`, `summary.txt`, one log per variant and language, and `errors.log`. The summary shows inference latency and FPS, pre and post processing latency, overall FPS and frames. The status column is `OK`, `EXEC_ERROR`, `PARSE_ERROR`, `TIMEOUT`, `SKIP` (no binary or script), `NO_MODEL` (`.dxnn` not downloaded) or `NO_INPUT`.

## Package an example

### Standalone package

`./scripts/dx_tool.sh extract` copies one example (its folder and the `common/` files it depends on) for use outside the repository. By default it prunes `common/` to the files the model needs. Answer `n` at the `Prune unused common/ files? [Y/n]` prompt, or pass `--no-prune`, to copy the whole framework:

```bash
./scripts/extract_model_package.sh object_detection/yolov7 --output-dir out_yolov7 --no-prune
```

Pruned and full packages compile the same and give byte identical inference output. The Python visualizers use an unseeded color palette, so drawn colors change between runs.

### Visual Studio package (Windows)

`extract_sln_package.bat` extracts one C++ example into a CMake package that builds outside the full DX-APP solution:

```bat
.\scripts\extract_sln_package.bat image_classification/resnet/resnet50_224x224 --output-dir out_resnet50
cd .\out_resnet50\sln\image_classification\resnet50_224x224
.\build.bat
```

When CMake and the Visual Studio 2022 generator are available, the extractor also writes `build\dxapp_resnet50_224x224_sln_package.sln`. Pass `--no-generate-sln` to create only the package. The dependency paths it detects are written to `cmake\dxapp_package_deps.cmake` and `cmake\dxapp_package_deps.bat`. On another PC, set these variables before `build.bat`, or edit that file:

| Variable | Meaning |
|---|---|
| `DEEPX_SDK_DIR` | DEEPX SDK (DX-RT) root |
| `DXRT_INSTALLED_DIR` | DX-RT install root for `include`, `lib` and `bin` |
| `OpenCV_DIR` | OpenCV CMake package folder |
| `VCPKG_INSTALLED_DIR` | vcpkg installed tree, for runtime DLLs |

### Multi model graph project

To export a graph as its own CMake project, see [Standalone project](multi-model-graph.md#standalone-project).

## Next steps

* [Customize a YOLO model](customize-yolo.md)
* [Architecture](architecture.md)
* [Run the examples](run-examples.md#test-the-examples): the test suites.
