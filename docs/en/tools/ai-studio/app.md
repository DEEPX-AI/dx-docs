---
title: DX App
description: Run NPU inference, demos, benchmarks and multi model graphs from the DX App tool in DX AI Studio.
---

# DX App

DX App lets you run inference on the DEEPX NPU from your browser on images, video, a camera or an RTSP stream, and connect several models in Graph Composer.

## Before you start

* A running studio. See [Install and launch](install-and-launch.md).
* For real inference: a DEEPX NPU, the NPU driver, DX-RT and the DX-APP examples in `dx-runtime/dx_app`. You can browse DX App without an NPU, but it never shows a fake run in place of a missing runtime.
* For live runs: `xvfb`, `libxcb1` and Pillow (see [What each feature needs](install-and-launch.md#what-each-feature-needs)).

## Pages

| Page | What it does |
|---|---|
| **Setup** | Guided environment check. Run it first so the NPU and runtime are ready. |
| **Models** | The model list across 29 tasks, drawn from the Model Zoo catalog. Open a model for details or its graph. |
| **Run Inference** | Pick a category, model and input, then run. **Single** runs one image or video (sample, your own upload, or special inputs such as LiDAR `.bin` where they apply) with a before and after slider. **Continuous** streams video, camera or RTSP live in several slots side by side. |
| **Run Demo** | 26 ready made demos in 12 groups on one stage: choose a demo, an input, C++ or Python, Sync or Async, and run. Video runs stream live with FPS. |
| **Benchmark** / **A/B Compare** | Measure a model's throughput and compare models side by side. Benchmark runs several models in a batch and exports a report. |
| **ModelZoo** | Download more models into the app (public or air gapped source, Q-Lite or Q-Pro, batch cart) |
| **Graph Composer** | Connect sources, models, CPU operations and logic on a canvas, then validate, run and export. See [Graph Composer](#graph-composer). |
| **Lab** | Advanced tools that show a change preview before anything is written (see below) |
| **Outputs** | Browse and manage saved results (grid or table, filters, preview) |
| **Reference** | Searchable feature and parameter guides |

For RTSP, paste the camera's full URL (`rtsp://user:pass@cam:554/...`). An `IP:Port` with a stream pick still works. A model that takes only still images is refused in Continuous mode with an explanation.

From the Run page, **Export Model Package** bundles a model's source, config and file (C++, Python or both).

### Lab tools

| Tool | What it does |
|---|---|
| **Add Model** | Copies an existing example of a category (**Start from**) under a new name, in C++, Python or both. Run the Python copy with `python3 <name>_sync.py --model <your>.dxnn`; build the C++ copy with dx_app `build.sh`. |
| **Create Task** | Skeleton code for a new task type |
| **Experiment** | Checks a compiled `.dxnn` on the board: reads the file, runs one inference, then measures throughput (FPS) |
| **Generated Files** / **Safety Center** | Lists what each change wrote. A change that only created new files can be rolled back after typing `rollback:<name>`; a change that overwrote files must be restored by hand. **Commit with git** lists the files and the git commands that commit only those. |

## First inference

1. Open **Setup** and complete the checks. For a first demo, use **Demo Quick Start, Start Demo Setup** and watch the progress for failed steps.
1. When setup is ready, choose **Try demo**, pick a demo and a supported sample input, and run it. Or use **Run Inference, Single**: pick a category, model and image, and run.
1. Check the result and timings. Saved results appear in **Outputs**. If a model, binary or runtime is missing, go back to the named Setup step or download the model and retry.

Quick Start prepares the demo runners, their models and sample videos, not every per model build. A local file without a current studio completion record is **unverified**, not missing. Use **Verify** or rerun the setup step; matching files are kept.

## Graph Composer

Graph Composer builds a multi model workflow without writing the runner yourself. It is a page inside DX App.

### Prepare and validate

1. Open **Templates** and choose a scenario, for example restricted zone intrusion or line counting. Others include PPE, dwell, zone counts, gallery matching, driver attention, multi camera counts and volume alerts.
1. Check the template's models in the palette. Installed models are marked; use **Download** for missing ones. At the reference revision **492 of 497** variants run in a graph: the four anomaly detection variants are not graph ready, and the LiDAR model (`sfa3d_608x608`) needs a source that is not supported.
1. Select each **Source** and set its input. Use a local sample image or video for **Run once**; camera and RTSP sources are for **Live**. File paths refer to the studio host, not the remote browser.
1. Select nodes and connections and change properties in the **Inspector**. The graph is checked after each edit; **Validate** shows the current errors on their node or edge. Check the NPU memory bar too, and fix missing models, wrong connections or too much memory before running.

Keyboard editing: `Tab` between nodes, arrow keys to move, `Delete`, and `Ctrl+Z` / `Ctrl+Y`.

### Run once and read the result

Choose **Sync** or **Async** and **Run once**. Watch progress, FPS and per node time, then inspect the output and node results. Several sources appear as a grid. **Layers** toggle each node's drawing without changing the graph.

For a paused video, **Layers for this frame** runs the selected frame again on the NPU. It does not restore tracker, zone, dwell, condition or gallery state, so track IDs and events can differ from the original video.

### Logic, zones and events

Connect model results to **Filter**, **Zone**, **Line crossing**, **Count**, **Dwell**, **Condition → Event** or **Gallery match**, as the installed runner offers them.

* To draw a zone, set a file input first, select the Zone block and choose **Edit on the frame...**. Camera and RTSP inputs have no local first frame for this editor.
* Line crossing and dwell need detector tracking turned on. **Gallery match** needs a prepared gallery (building it uses the NPU).
* **User logic** passes data through until you implement its exported C++ stub.
* Filter the event list by node, event, track ID or time. Clicking an event jumps the video there. Download **JSONL** for later analysis. No events can simply mean the rule was never met.

### Live, save and export

* **Live** runs a camera, RTSP stream or looping video until **Stop**. Only one Graph Live runs at a time, and leaving Graph Composer stops it. Graph Run once, Graph Live, the Run page's Continuous slots and gallery builds exclude each other.
* **Save** (`Ctrl+S`) stores the project on the studio host under `outputs/dx_app/graph/projects/`. The latest 50 versions per project are kept.
* **JSON export / import** moves the editable graph definition. It is not a model bundle or a program.
* **Export C++ project** shows a plan, then produces a zip with a standalone CMake project, the engine code, `main.cpp`, `graph.json`, `setup.sh`, `run.sh` and a README. Model files are left out unless you tick **Include the model files**; otherwise the exported setup downloads them. User logic becomes stubs under `user_logic/`. Follow the exported README for DX-RT, CMake, C++17 and OpenCV. The server keeps the newest five exports under `outputs/dx_app/graph/exports/`.

If an action is blocked, read the reason: prepare the runner or model, fix the input or connection, reduce memory, or stop the NPU job named in the message. Missing hardware never switches Graph Composer to a mock mode. **Tutorial, Graph Composer** can show recorded results without starting the NPU.

## Next steps

* [Watch the NPU in DX Monitor](monitor-and-benchmark.md)
* [Build a pipeline in DX Stream](stream.md)
* [DX-APP documentation](../app/index.md)
