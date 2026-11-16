---
title: Run the examples
description: Run the DX-APP demo and the C++ and Python examples, with every command line option, environment variable and runtime feature, and run the test suites.
---

# Run the examples

This page shows how to run the DX-APP demo and any single C++ or Python example, lists every option, and explains how to test the examples.

## Before you start

* You built DX-APP as shown on [Build DX-APP](build.md).
* For Python, the virtual environment with `dx_engine` and `dx_postprocess` is active.
* You run every command from the `dx_app/` folder.

## Run the demo

`run_demo.sh` is the quickest way to see DX-APP work. It runs 26 demo tasks, one model each, from a menu: task, then language and mode, then input. It downloads missing demo models and videos on first run.

```bash
./run_demo.sh                               # menu
./run_demo.sh --task 0 --mode 1 --input 2   # YOLOv7, C++ sync, image
./run_demo.sh --task 0 --mode 2 --input 1   # YOLOv7, C++ async, video
./run_demo.sh --show-log                    # verbose logs
```

| Option | What it does |
|---|---|
| `--task NUM` | Pick the task, 0 to 25 (see the table below) |
| `--mode NUM` | Pick the mode, 1 to 6: 1 `cpp_sync`, 2 `cpp_async`, 3 `py_sync`, 4 `py_async`, 5 `py_sync_cpp_postprocess`, 6 `py_async_cpp_postprocess`. Tasks without a Python async example offer only `cpp_sync`, `cpp_async`, `py_sync` and `py_sync_cpp_postprocess`, numbered 1 to 4 |
| `--input NUM` | Pick the input: 1 video, 2 image |
| `--show-log` | Verbose log output (default: quiet) |
| `--help` | Show the help |

Image input (`--input 2`) uses the images bundled in the repository, so it needs no video download.

| # | Demo task | Model file |
|--:|---|---|
| 0 | Object detection (YOLOv7) | `yolov7_640x640.dxnn` |
| 1 | Object detection (YOLO11-N) | `yolo11-n_640x640.dxnn` |
| 2 | Face detection (SCRFD-500M) | `scrfd-500m_640x640.dxnn` |
| 3 | OBB detection (YOLO26-N-OBB) | `yolo26-n-obb_1024x1024.dxnn` |
| 4 | Pose estimation (YOLOv8-S-Pose) | `yolov8-s-pose_640x640.dxnn` |
| 5 | Hand landmark (MediaPipe Hands Lite) | `mediapipe-hands-lite_224x224.dxnn` |
| 6 | Face alignment (3DDFA-V2 MobileNetV1) | `3ddfa-v2_mobilenetv1_120x120.dxnn` |
| 7 | Instance segmentation (YOLOv8-N-Seg) | `yolov8-n-seg_640x640.dxnn` |
| 8 | Semantic segmentation (DeepLabV3+ MobileNet) | `deeplabv3plus_mobilenetv1_512x512.dxnn` |
| 9 | Classification (ResNet50) | `resnet50_224x224.dxnn` |
| 10 | Depth estimation (YOLO26-Depth-S) | `yolo26-depth-s_768x768.dxnn` |
| 11 | Image denoising (DnCNN-50) | `dncnn-50_512x512.dxnn` |
| 12 | Super resolution (ESPCN-X4) | `espcn-x4_17x17.dxnn` |
| 13 | Image enhancement (Zero-DCE) | `zerodce_400x600.dxnn` |
| 14 | Embedding (ArcFace) | `arcface_mobilefacenet_112x112.dxnn` |
| 15 | Attribute recognition (DeepMAR ResNet50) | `deepmar_resnet50_224x224.dxnn` |
| 16 | PPU pipeline (YOLOv7 PPU) | `yolov7_640x640_ppu.dxnn` |
| 17 | Keypoint detection (SuperPoint) | `superpoint_480x640.dxnn` |
| 18 | Object pose estimation (DOPE) | `dope-hope-ketchup_480x640.dxnn` |
| 19 | Panoptic driving (YOLOPv2) | `yolopv2_384x640.dxnn` |
| 20 | 3D object detection (SFA3D) | `sfa3d_608x608.dxnn` |
| 21 | Hand detection (MediaPipe Palm) | `mediapipe-hand-detector_192x192.dxnn` |
| 22 | Image retrieval (CLIP RN50) | `clip-img_resnet50_224x224_openai.dxnn` |
| 23 | Visual place recognition (EigenPlaces R18) | `eigenplaces-resnet18_512x512.dxnn` |
| 24 | Person re-identification (RepVGG-A0) | `repvgg-a0-reid_256x128.dxnn` |
| 25 | Image matting (PP-Matting HRNet-W48) | `ppmatting-hrnet-w48-composition_512x512.dxnn` |

## Run one example

The default build includes YOLO11-N, so these commands work right after `./build.sh`. Without `-m`, an example uses its own model, here `assets/models/yolo11-n_640x640.dxnn`, and downloads it if it is missing.

=== "Python"

    ```bash
    # Image, sync, Python post processing
    python3 src/python_example/object_detection/yolo11/yolo11-n_640x640/yolo11-n_640x640_sync.py \
        --image sample/img/sample_street.jpg

    # Video, async, C++ post processing: the fastest Python variant
    python3 src/python_example/object_detection/yolo11/yolo11-n_640x640/yolo11-n_640x640_async_cpp_postprocess.py \
        --video assets/videos/snowboard.mp4
    ```

=== "C++"

    ```bash
    # Image, sync
    ./bin/yolo11-n_640x640_sync -i sample/img/sample_street.jpg

    # Video, async
    ./bin/yolo11-n_640x640_async -v assets/videos/snowboard.mp4
    ```

A window shows the result and the console prints a performance summary (latency per stage and FPS). Add `--no-display` on a machine without a display, and `--save` to keep the result under `artifacts/`.

To run any other model, find its variant in the [model catalog](models.md). The Python script is `src/python_example/<task>/<family>/<variant>/<variant>_sync.py` and the C++ executable is `bin/<variant>_sync` after `./build.sh --target <variant>_sync <variant>_async`.

### Run many examples at once

`scripts/run_examples.sh` (also `./scripts/dx_tool.sh run`) runs a filtered set of the 497 variants and prints a performance table for each. Without options it opens a menu in six steps: language, category, model filter, sync or async, input type, display and save options.

```bash
scripts/run_examples.sh
scripts/run_examples.sh --lang cpp --category face_detection --filter scrfd
./scripts/dx_tool.sh bench --lang both --filter yolov8 --loops 5
```

See [DX tool](dx-tool.md) for the full tool.

## Command line options

C++ and Python examples share the same options. The short forms are the same, the long forms differ.

| Short | C++ long | Python long | What it does |
|---|---|---|---|
| `-m` | `--model_path` | `--model` | `.dxnn` model file. Without it, the example uses its own model `assets/models/<variant>.dxnn` and downloads it if missing |
| `-i` | `--image_path` | `--image` | Input image file or folder |
| `-v` | `--video_path` | `--video` | Input video file |
| `-c` | `--camera_index` | `--camera` | Camera device index |
| `-r` | `--rtsp_url` | `--rtsp` | RTSP stream URL |
| `-s` | `--save` | `--save` | Save the rendered output to a run folder |
|  | `--save-dir` | `--save-dir` | Base output folder. C++ default `artifacts/cpp_example` under the current folder, Python default `artifacts/python_example/` under the `dx_app` root |
|  | `--dump-tensors` | `--dump-tensors` | Dump raw input and output tensors (C++ `.bin`, Python `.npy`) |
| `-l` | `--loop` | `--loop` | Inference repeat count. C++ default: auto. Python default 1; a bare `--loop` means 2 |
|  | `--no-display` | `--no-display` | No window, print FPS only |
|  | `--show-log` | `--show-log` | Verbose log output (default: quiet) |
|  | `--config` | `--config` | Model config JSON. Python reads the variant's `config.json` when you leave it out. C++ reads a config only when you pass it, otherwise it uses the defaults built into its factory |
|  | `--drop-frames` |  | C++ only: the preview drops stale frames instead of pacing the pipeline |
|  |  | `--variant` | Python only: pick the model by variant name from `config/model_registry.json`. `--model` wins |
|  |  | `--display` | Python only: show the window (default: on) |
|  |  | `--fast-postprocess` | Python only: use the faster post processor where one exists (see below) |
|  |  | `--sr-tile-halo` | Python only: tile overlap for tiled super resolution, 0 to 4 (default 4) |
| `-h` | `--help` | `--help` | Show the options |

Rules for inputs:

* `--image`, `--video`, `--camera` and `--rtsp` are mutually exclusive. With none of them, the example uses the default sample image of its task, for example `sample/img/sample_street.jpg` for detection, and logs `[DXAPP] [INFO] No input specified. Using default sample: ...`.
* Some tasks take images only: `face_recognition`, `face_attribute`, `person_attribute`, `person_reid`, `image_retrieval`, `visual_place_recognition`, `object_pose_estimation` and `3d_object_detection`, plus some CLIP and CasViT variants. They reject video, camera and RTSP input. The embedding and attribute models expect a crop of an already detected subject, or rank against a gallery; on a raw frame they give no useful result. Use a [multi model graph](multi-model-graph.md) to feed them crops from a detector.
* `3d_object_detection` (SFA3D) reads a LiDAR point cloud (`sample/kitti/velodyne/*.bin`), not an image.
* On a Raspberry Pi, `-c N` opens CSI camera N (as listed by `rpicam-hello --list-cameras`) through libcamera. A USB webcam uses V4L2.
* Thresholds are not command line options. Change `score_threshold`, `nms_threshold` and similar keys in the variant's `config.json` (and pass it with `--config` for C++).

## Environment variables

| Variable | What it does |
|---|---|
| `DXAPP_SAVE_IMAGE` | Save the rendered output to this file path, without `--save` |
| `DXAPP_VERIFY` | `1`: write the post processing results to `logs/verify/<model>.json` (last frame) and `<model>.frames.jsonl` (one record per frame, in input order) |
| `DXAPP_VERIFY_DIR` | Folder for `DXAPP_VERIFY` output (default `logs/verify`) |
| `DXAPP_PROGRESS` | `1`: print `[PROGRESS] frames=N fps=F avg_fps=A read_ms=R pre_ms=P infer_ms=I post_ms=Q` about once a second and once at exit, for front ends such as DX AI Studio |
| `DXAPP_ROOT` | C++: the folder that repository relative paths (`sample/...`, galleries, `config.json`) are read from. Default: the repository the program was built from |
| `DXAPP_SCREEN_W`, `DXAPP_SCREEN_H` | Screen size used to size the preview window (set both) |
| `DXAPP_SR_TILE_HALO` | Python: tile overlap for tiled super resolution, 0 to 4 (`--sr-tile-halo` and `config.json` override it) |
| `OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS` | Windows: the examples set it to `0` (faster camera open, reliable video decode). Set it to `1` yourself to keep the hardware transforms |

## Runtime features

### Model download

When you leave out `-m`, the example reads its model file from `config/model_registry.json` and, if the file is missing, downloads it with `setup_sample_models.sh`. An explicit `-m` path that does not exist is an error and nothing is downloaded. Input files, videos included, are never downloaded on demand: run `./setup.sh` or `./setup_sample_videos.sh` first.

### Saved output

With `--save`, each run gets its own folder:

```text
artifacts/cpp_example/
  <model>_sync-image-<name>-<YYYYMMDD-HHMMSS>/
    run_info.txt        # script, model and input paths
    output.jpg          # image mode
    output.mp4          # video mode (output.avi with MJPG when no mp4 encoder exists)
    dump_tensors/       # with --dump-tensors
```

Video, camera and RTSP runs are named `<model>_sync-stream-<name>-...`, async binaries use `_async`. Python uses the same pattern under `artifacts/python_example/`, starts the name with the script name, saves images as `<image>_result.jpg` and writes tensors to `tensors/` as `.npy`. A stream that stops before its first frame saves only `run_info.txt` and prints `No frames were received from <input> before the run was stopped; no output video was saved.`

### Stopping a run

The first Ctrl+C or a SIGTERM stops gracefully: the video writer is finalized and the summary printed. A later Ctrl+C, more than 200 ms after the first, ends the process at once; presses within 200 ms count as one. SIGTERM is always graceful.

### Preview window and headless runs

The window opens at half the screen size. Every frame is shown by default, so a slow window slows the pipeline: measure throughput with `--no-display`. On Linux without `DISPLAY` or `WAYLAND_DISPLAY`, the examples skip the window automatically.

### Output order

Async runners return results in input order, so saved output and `DXAPP_VERIFY` records equal the sync runner frame by frame. In C++, if no frame arrives for 5 s at the end of a video, the runner prints `[DXAPP] [WARN] Output frames stopped draining; saved video may be truncated.` and stops. The Python live window, when nothing is saved, is a best effort preview: it draws at most about 60 frames a second and drops the oldest waiting frame when it falls behind.

### Debugging

* `--dump-tensors` writes the raw tensors. On an exception, tensors are dumped automatically (C++ sync runners; Python with a `reason.txt`).
* `DXAPP_VERIFY=1` serializes every result type (detection, classification, pose, segmentation, panoptic, 3D, keypoints) for numerical checks. Frame numbers count per process, so with `-l N` on a video, later loops continue the numbering.

### Fast post processing (Python)

`--fast-postprocess` selects a faster post processor for the model families that have one. Other models keep the standard path and print a warning, so the flag is always safe. It does not change the `*_cpp_postprocess` scripts.

| Tier | Result compared to the standard path | Model families |
|---|---|---|
| Exact | Byte identical | Detection with `YOLOv5Postprocessor` (YOLOv3, v4, v5, v6, v7) and EfficientDet |
| Approximate | Differs only at sub pixel mask edges | YOLOv8-seg family, YOLACT, SegFormer, depth estimation (values differ by up to about 3/255) |

```bash
python3 src/python_example/object_detection/yolov7/yolov7_640x640/yolov7_640x640_sync.py \
    --image sample/img/sample_street.jpg --fast-postprocess
```

### Version checks

| Language | What the example checks at start | What an old DX-RT shows |
|---|---|---|
| C++ | DX-RT 3.5.0 or later and model format v7 or later, after the engine is created | `DXRT library version is too low. (required: >= 3.5.0, current: <version>)`, or DX-RT's own error if loading fails first |
| Python | DX-RT 3.0.0 or later, and a warning for a model format older than v7 | DX-RT 3.0.0 to 3.4.x pass the check, then loading fails with DX-RT's error, for example `Model file format version 9 is not supported` |

If a Python example fails while loading a model, check `dxcli --version` first.

## Test the examples

DX-APP has pytest suites for both languages. `run_tc.sh` runs them with the right settings.

```bash
./run_tc.sh --cli                  # CLI tests, both languages (fast, no NPU for most)
./run_tc.sh --cpp --e2e-quick      # C++ image inference tests (about 2 to 3 minutes)
./run_tc.sh --python --e2e-short   # Python image and video tests, one model per task
./run_tc.sh                        # CLI and video tests for all models
```

| Option | What it runs |
|---|---|
| `--python`, `--cpp` | Only that language (default: both) |
| `--cli` (or `--quick`) | CLI tests |
| `--e2e` | Video inference tests for all models |
| `--e2e-quick` | Image inference tests only |
| `--e2e-short` | Image and video tests for one representative model per task |
| `--vis` | Visualization output tests |
| `--signal` | Ctrl+C handling tests |
| `--camera --camera-index <N>` | Camera input tests |
| `--rtsp --rtsp-url <URL>` | RTSP input tests |
| `--stream-duration <N>` | Seconds per camera or RTSP test (default 10) |
| `--loop <N>` | Loop count for image tests (default: C++ 20, Python 1) |
| `--coverage` | Coverage run. Cannot be combined with other test options |

To test every C++ executable, build with `./build.sh --all` first; the default build tests only the demo set. End to end tests need the models (`./setup.sh --all`) and videos (`./setup_sample_videos.sh`). Without a display, the suites set `QT_QPA_PLATFORM=offscreen`.

### Run pytest directly

Run each suite in its own pytest session from its folder. One session over both folders is not supported.

=== "Python"

    ```bash
    cd tests/python_example
    python3 -m pip install -r requirements.txt
    pytest unit/                 # mocked unit tests, no NPU
    pytest -m cli                # CLI tests
    pytest -m e2e -k "yolov7 or yolov8"
    E2E_DISPLAY=1 pytest -m e2e  # show windows; image tests wait for q or ESC
    ```

=== "C++"

    ```bash
    cd tests/cpp_example
    python3 -m pip install -r requirements.txt
    pytest -m cli
    pytest -m e2e -k "yolov7 and not async"
    pytest "test_e2e.py::test_image_inference_e2e[scrfd-500m_640x640_async]"
    ```

The Python suite starts the examples with the first of: `$DXAPP_TEST_PYTHON`, `dx-runtime/venv-dx-runtime/bin/python3`, or the Python that runs pytest. `pytest -m "not e2e"` still runs feature tests on the NPU; for a run without hardware use `pytest unit/` and `pytest -m cli`.

Common markers: `cli`, `help`, `e2e`, `e2e_image`, `e2e_stream`, `e2e_camera`, `e2e_rtsp`, `e2e_short`, `visualization`, `sync_exec`, `async_exec`, `save_mode`, `dump_tensors`, `verify`, `multi_loop`, `signal_handling`. The C++ suite adds `contract`, `golden`, `graph`, `graph_e2e`, `graph_parity` and `graph_export`. The Python suite also registers one marker per model family and variant, for example `pytest -m yolov7_640x640`.

End to end video runs write a performance report (E2E, read, pre process, inference and post process FPS) to `tests/<suite>/performance_reports/performance_report_*.csv`. For async variants, the slowest stage is marked with `*`.

### Coverage

```bash
sudo apt-get install gcovr -y
./build.sh --clean --coverage --type debug --all && ./run_tc.sh --cpp --coverage
xdg-open tests/cpp_example/coverage/html/index.html
```

`--type relwithdebinfo` builds faster with less accurate coverage. `lcov` works as a fallback for `gcovr`.

### Repository checks

After you change examples or add a model, run the checks that need no NPU:

```bash
bash scripts/ci_checks.sh          # every check, then a PASS / SKIP / FAIL summary
bash scripts/ci_checks.sh --list   # list the checks
```

A check whose prerequisite is missing prints `SKIP` and the run still exits 0. Only a `FAIL` exits 1.

## Next steps

* [Model catalog](models.md)
* [Multi model graph](multi-model-graph.md)
* [Post processing](post-processing.md)
