---
title: CLIP multi channel demo
description: Match up to 16 video channels or a camera against text sentences with CLIP on the NPU, in a PyQt or OpenCV app.
---

# CLIP multi channel demo

This demo lets you match live video against your own sentences with CLIP on up to 16 channels at once, and raise an alert when a sentence matches.

The code is in [dx_clip_demo](https://github.com/DEEPX-AI/dx_clip_demo). It has two variants:

| Variant | UI | Environment |
|---|---|---|
| `pyqt` | Full GUI: settings window, grid of up to 16 channels, sentence list you edit at run time | `venv-pyqt` |
| `opencv` | Light: results drawn on the frames, sentences typed in the terminal, works on embedded hosts | `venv-opencv` |

## Before you start

* DX-RT installed with the SDK, see [Install](../get-started/install.md). The setup needs the DX-RT source folder `~/dx-all-suite/dx-runtime/dx_rt`.
* A desktop session for the PyQt variant; a webcam for camera mode (optional).

## Steps

1. Get the code and run the setup for your variant. It downloads the videos and the CLIP model, creates the environment and installs `dx_engine` from your DX-RT:

    ```bash
    git clone https://github.com/DEEPX-AI/dx_clip_demo.git
    cd dx_clip_demo
    ./setup.sh --app_type=pyqt --dxrt_src_path=$HOME/dx-all-suite/dx-runtime/dx_rt
    ```

    !!! warning
        Always pass `--dxrt_src_path`. Without it, setup clones `dx-runtime` from `main` next to the demo, and setup runs `./build.sh --clean` in the DX-RT folder each time.

1. Start the PyQt variant:

    ```bash
    source venv-pyqt/bin/activate
    python -m clip_demo_app_pyqt.dx_realtime_demo_pyqt
    ```

    Or start everything with one command, which asks for the variant on first run: `./run_demo.sh --app_type=pyqt --dxrt_src_path=$HOME/dx-all-suite/dx-runtime/dx_rt`.

1. For the OpenCV variant, run the setup with `--app_type=opencv`, then:

    ```bash
    source venv-opencv/bin/activate
    python clip_demo_app_opencv/dx_realtime_multi_demo.py
    python clip_demo_app_opencv/dx_realtime_demo.py
    python clip_demo_app_opencv/dx_video_demo.py
    ```

    `dx_realtime_multi_demo.py` runs 16 channels; press `q` to exit. In `dx_realtime_demo.py`, type a sentence and press Enter to add it, `del` to delete the last one and `quit` to exit; add `--features_path 0` for the camera. `dx_video_demo.py` compares ground truth and predicted sentences for 29 MSRVTT videos in the terminal.

## Settings in the PyQt variant

| Setting | Meaning |
|---|---|
| Assets Path | Folder with videos and models |
| Number of Channels | 1 to 16 channels |
| Display Percentage, Display Score | Show the similarity as a percentage or as a score |
| Settings Mode | Show the panel to add, delete or clear sentences |
| Camera Mode | Single channel: camera replaces the video. Multi channel: camera is added as a channel |
| Merge the central grid | In 3x3 and 4x4 grids, merge the center cells into one large view (camera, or all 16 videos in a loop) |
| Video FPS Sync Mode | On: process at the video's frame rate. Off: as fast as the hardware allows |
| Fullscreen Mode, Dark Theme | Window options |
| Display FPS for each video | Show NPU FPS and app FPS per channel |
| Text Layout Mode | `fit`, `word_wrap`, `fit + min`, `fit + setting`, `setting + word_wrap`, `fit + large mode (show top 1)`, `fit + min + word_wrap` |
| Minimum Font Size | Lower limit, or start size, for the modes that use it |

Defaults are in `clip_demo_app_pyqt/common/config/ui_config.py` (16 channels, full screen, dark theme). Settings that you change only in code, such as `number_of_alarms` (2), `consumer_num_of_inference_per_sec` (3) and `max_producer_worker` (16), are in the same file. Videos and sentences, each with `min_score`, `max_score` and `threshold`, are in `clip_demo_app_pyqt/data/default_data.json`.

NPU FPS counts color conversion and NPU inference. App FPS also counts the similarity against every sentence and the threshold check.

## Prompt a sentence on live video

1. Connect a webcam.
1. In the Settings window, check **Settings(prompt) Mode** and **Camera Mode**, then click **Done**.
1. Click **Add** in the right panel, enter the sentence with its min, max and threshold values, and click **Submit**.
1. Act out the sentence in front of the camera. The sentence appears when its score passes the threshold.

## Expected result

A grid of videos, each showing the matching sentences in real time.

## Next steps

* [CLIP in C++](clip-cpp.md)
* [CLIP in Python](clip-python.md)
* [Tutorials](index.md)
