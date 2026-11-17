---
title: DX Stream
description: Build and run DX-Stream GStreamer pipelines with live playback from the DX Stream tool in DX AI Studio.
---

# DX Stream

DX Stream lets you build and run real time GStreamer vision pipelines on the DEEPX NPU and watch the result live in your browser.

## Before you start

* A running studio. See [Install and launch](install-and-launch.md).
* System GStreamer and PyGObject (`python3-gi`, `gstreamer1.0-*`).
* For WebRTC playback: `gstreamer1.0-nice` and `gir1.2-gst-plugins-bad-1.0` (Setup step 6 checks both).

## Pages

| Page | What it does |
|---|---|
| **Setup** | Guided install of everything a pipeline needs in six steps: Build Tools & Libraries, DX-Runtime Dependencies, NPU Linux Driver, GStreamer Plugin Build, Model & Video Download, and WebRTC Dependencies. Run one step or **Set up the rest**. An environment check and **Deep Diagnostics** show what is ready. |
| **Dashboard** | Tool status, quick launch demo cards, and live FPS, latency and NPU use with sparklines |
| **Demo Launcher** | Preset pipelines by category (object and face detection, pose, segmentation, depth, multi stream, RTSP and more). **Terminal command ›** shows the equivalent command line. |
| **Pipeline Builder** | Drag and drop GStreamer editor: pick elements from a searchable palette (including a camera source, `v4l2src`), wire them, edit properties, then **Run** and **Stop**. Start from a preset, export or import JSON, and see the equivalent `gst-launch` command. |
| **Model Catalog** | Browse, search and download models for pipelines |
| **Element Reference** | DX-Stream GStreamer elements by category, with properties and pads |
| **Custom Library** | Upload and build your own C post processing library (with a build log), or upload a `.dxnn` model for DxInfer |
| **Reference** | Searchable in app documentation |

Playback has two modes, shared by Demo Launcher and Pipeline Builder:

| Playback | Use it when |
|---|---|
| **Local (WebRTC)** | You are on the board or the same LAN segment |
| **Remote (MJPEG)** | You watch from another computer or through an SSH tunnel |

## First pipeline

1. Open **Setup** and check runtime and driver, plugin, models and playback dependencies. Installing is an explicit action and can need administrator rights.
1. Open **Demo Launcher**, choose a demo and a supported input, select **Playback**, then **Start**. FPS, resolution and model appear next to the video.
1. To change the pipeline, open **Pipeline Builder**, load a preset, select an element to edit its properties and check model and input paths on the studio host. Choose **Playback**, then **Run**. **Stop** before you start a different job.

JSON export keeps the pipeline definition. It does not package models or install plugins on another host.

## Troubleshooting

| Symptom | What to do |
|---|---|
| A stream fails or stalls | The studio shows a persistent error with retry instead of a black screen. Check **Playback**, connectivity and the message before restarting. |
| Runtime validation blocks the launch | Open **Setup, DX-Runtime Dependencies** and **NPU Linux Driver**, read the failed check or **Deep Diagnostics** and follow the fix. Check again after an approved runtime change or reboot. Unsupported runtime versions are never replaced silently. |
| A model or plugin is missing | Finish the matching Setup step and confirm its status |
| Files show as unverified | Run **Model & Video Download** to verify or complete them. Unverified does not mean missing. |
| WebRTC shows nothing | Finish Setup step 6. `launcher.sh` also repairs a `.venv` made without system site packages, which hides the GStreamer bindings. |

## Next steps

* [DX-Stream documentation](../stream/index.md)
* [Watch the NPU in DX Monitor](monitor-and-benchmark.md)
* [Compile a model for your pipeline](workflow.md#dx-compiler)
