---
title: Models and compiler
description: Browse and download models in DX Model Zoo and compile ONNX models to .dxnn in DX Compiler.
---

# Models and compiler

This page shows you how to find a model in DX Model Zoo and turn an ONNX model into a `.dxnn` file in DX Compiler.

## Before you start

* A running studio. See [Install and launch](install-and-launch.md).
* For in browser inference: DX App **Setup** finished, the model downloaded and the NPU runtime ready.
* For compilation: the DX-COM compiler SDK (DX Compiler **Setup** can install it).

## DX Model Zoo

DX Model Zoo shows the DEEPX model catalog. The October 2026 reference holds **497 model variants across 29 tasks**. Variants count sizes, input shapes and training variants separately, so 497 is not 497 different architectures. The counts and sync date in the explorer describe the catalog your studio loaded. The hub and Model Zoo group the variants under 31 category labels; the Graph Composer palette uses the 29 tasks.

### Use it

1. **Browse or search** the catalog. Filter by category (image classification, object detection, segmentation, pose and more), switch card or list view, and sort. Cards show the available **Q-Lite** and **Q-Pro** artifacts; **Q-Master** appears only where provided.
1. **Open a model** to see task, input shape, accuracy metrics, license, source, copyright and example images. A before and after slider is available for suitable examples, including super resolution.
1. **Download** an artifact: a Q-Lite or Q-Pro `.dxnn` (with progress and cancel), ONNX or JSON. Not every model offers every artifact.
1. **Try it in the browser:** upload an image or use a sample, then see the result image, predictions, FPS and a per stage latency table. Switch the execution path between C++ or Python and Sync or Async. This needs DX App to be reachable, the model downloaded, its example built and the NPU runtime ready. It needs DX-RT 3.5 or newer. Tasks that do not take images may not support this demo.
1. **Continue** in DX App or DX Compiler. The detail view also links to **View Model Graph** and a compile guide.

The detail view also offers copyable demo code (C++, Python and CLI) and saves a model card as HTML.

### Read the numbers correctly

* Card FPS and accuracy are published catalog measurements, not a promise for your board. Keep the metric name (mAP, top 1, NME), dataset and quantization tier with each number.
* In **DX App, ModelZoo**, an **Unverified** badge means the local file has no current studio completion record. It does not mean the file is missing. Add it to the cart and run the download to verify it; matching content is kept. This checks the transfer, not whether the model runs on your NPU.
* If inference is disabled or fails, finish DX App **Setup**, download the selected tier and build its example, then retry.
* The full catalog is not the Graph Composer list: **492** variants run in Graph Composer at the reference revision. The four anomaly detection models and the LiDAR model are excluded.

!!! note "Model licenses"
    Each model keeps its own license. Check the license fields in the detail view before any commercial use. See [Third party licenses](reference.md#third-party-licenses).

## DX Compiler

DX Compiler turns a trained ONNX model into a `.dxnn` file for the DEEPX NPU. It drives DX-COM with a config wizard, a live graph view, quantization tuning and diagnosis, partial (range) compile, re-quantization and an optional AI agent.

### Compile a model

1. **Setup (first run).** In the **Setup** panel, check the SDK and sample status. If the compiler SDK is missing, click **Install**. Optionally **Download** sample models and calibration data. **Compile** stays disabled until the SDK is ready; a loaded graph alone does not mean the compiler is installed.
1. **Choose the model.** In **Compile ONNX Model**, drag and drop an `.onnx` file or type its path. Turn on **Use server path** to point at a file that is already on the studio host. **Select Sample Model** fills the path from a downloaded sample.
1. **Choose the config.** Drag and drop a config `.json`, or tick **Build Config** to open the wizard:
    1. **Input Shapes:** **Auto Detect from Model**, or add input rows by hand.
    1. **Data Loader:** **Default Loader** (real calibration data) or **Dummy Loader** (random tensors for a quick check).
    1. **Dataset & Preprocessing:** dataset path, file extensions, the preprocessing steps (resize, normalize and more), number of calibration samples and method. Skipped for Dummy Loader.
    1. **Review:** check the generated JSON, then click **Use This Config**.
1. **Set options.** Choose **Output Directory** and **Optimization Level**. Optional toggles: **Aggressive Partitioning** (more nodes on the NPU), **Generate Log**, **Quant Diagnosis** and **Compile Range Selection**. Under **Advanced Options, DXQ Enhancement Scheme**, enable presets **DXQ-P0** to **DXQ-P5** or **Auto (Q-Pro)** for automatic tuning. Auto cannot be combined with the manual presets.
1. **Compile.** Click **Compile** and follow the **Current Phase** card and the live **Compiler Log**. Graph tabs unlock as each phase finishes (Input, Prepared, Surgery, Partition, DXNN). On success, **Save Model Summary** downloads an HTML report of the compile.

!!! warning "Dummy Loader is not calibration"
    Use **Dummy Loader** only to check that a model compiles. Its random data says nothing about accuracy. **Default Loader** needs a dataset folder on the studio host.

### More features

| Feature | How it works |
|---|---|
| **Quant Diagnosis** | Tick it before compiling. It writes a Quantization Diagnosis HTML report (in the **Quant Diagnosis** tab) with the model **Status**, plus **Action Items** and **Evidence** (left out when Status is **GOOD**). A diagnosis failure does not fail the compile. |
| **Resume from QXNN** (re-quantization) | Re-quantizes an existing `.qxnn` into a new `.dxnn` without running the whole pipeline. Change the **Recalibration Method** (`minmax`, `ema`, `iqr`) and/or apply Q-Pro or DXQ presets. **Dataset Path (optional)** overrides the calibration data. The diagnosis report's **Resume from this QXNN** button fills the form. |
| **Compile Range Selection** | After the Prepare phase, use **Set Input Nodes** and **Set Output Nodes** on the graph, **Calculate Range**, then **Resume Compilation** to compile only that subgraph. |
| **Graph Viewer** | Pan, zoom, **Fit**, **Collapse / Expand All**, `Ctrl+F` node search, click a node or tensor for details, and a color coded **Legend** |
| **Agentic Auto Compile** | Give a model name, path or URL and pick an installed agent, its model and reasoning effort. It downloads, converts, configures, compiles and verifies, either hands off or **interactive** (you can reply during the run). |
| **AI Assistant** | The floating chat explains errors and settings. |

### If compilation fails

Read the Setup reason or the last failing phase in **Compiler Log**, fix the SDK, input, dataset or config, and retry. A graph preview or an unfinished job is not a produced `.dxnn`. For DX-COM options and config keys, see the [DX-COM section](../../compiler/index.md).

The compiled `.dxnn` runs in [DX App](app.md) and [DX Stream](stream.md). To compile in the cloud instead, see [DX Cloud on AWS](cloud-aws.md).

## Next steps

* [Run the compiled model in DX App](app.md)
* [Build a pipeline in DX Stream](stream.md)
* [DX-COM compiler documentation](../../compiler/index.md)
