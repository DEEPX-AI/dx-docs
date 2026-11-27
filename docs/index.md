---
description: Compile AI models for our NPUs and run them in Python, C++ or GStreamer.
hide:
  - navigation
  - toc
---

<div class="dx-hero" markdown>

# SDK Docs

Run AI models on DEEPX NPUs
{ .dx-hero__lead }

[ONNX](compiler/onnx-models.md) <span class="dx-hero__arrow">→</span>
[DX-COM](compiler/index.md) <span class="dx-hero__arrow">→</span>
`.dxnn` <span class="dx-hero__arrow">→</span>
[DX-RT](runtime/index.md) <span class="dx-hero__arrow">→</span>
[Python](runtime/python-api.md) · [C++](runtime/cpp-api.md) · [GStreamer](tools/stream/index.md)
{ .dx-hero__flow }

</div>

## Start here

| If you want to | Read |
|---|---|
| Understand how the pieces fit together | [Overview](get-started/index.md) |
| Install the SDK on your host and your device | [Install](get-started/install.md) |
| Compile and run your first model | [Quickstart](get-started/quickstart.md) |
| Check which versions work together | [Compatibility](get-started/compatibility.md) |
| Fix a common problem | [Troubleshooting](get-started/troubleshooting.md) |

## Tools

<div class="grid cards" markdown>

- :material-cog: **DX-COM**

    ---

    Compiles ONNX models into `.dxnn` files for the NPU with INT8 quantization.

    [:octicons-arrow-right-24: Compiler](compiler/index.md)

- :material-lightning-bolt: **DX-RT**

    ---

    Runs `.dxnn` models on the NPU with Python and C++ APIs.

    [:octicons-arrow-right-24: Runtime](runtime/index.md)

- :material-application: **DX-APP**

    ---

    Ready to run example applications for hundreds of vision models.

    [:octicons-arrow-right-24: App](tools/app/index.md)

- :material-video-input-component: **DX-Stream**

    ---

    GStreamer elements for real-time video inference pipelines on the NPU.

    [:octicons-arrow-right-24: Stream](tools/stream/index.md)

- :material-database: **DX-ModelZoo**

    ---

    Pretrained models you can compile, run and evaluate out of the box.

    [:octicons-arrow-right-24: Model Zoo](tools/model-zoo/index.md)

- :material-monitor-dashboard: **DX AI Studio**

    ---

    A browser workspace that runs the whole workflow in one place.

    [:octicons-arrow-right-24: AI Studio](tools/ai-studio/index.md)

</div>

## What's new in 2.5.0

* **DX-AllSuite:** Kubernetes support with the `dx-npu` Helm chart, one-line and APT installation, and prebuilt container images on GHCR.
* **DX-COM:** Up to 1.9× faster post-processing on ARM hosts. The compilation summary report (`--export_html`) replaces DX-TRON.
* **DX-RT:** `dxrun --max-throughput` auto-tuning, new end-to-end and core latency APIs, and V9 `.dxnn` support.
* **DX-Stream:** GPU preprocessing on ARM cuts CPU usage from 95.2% to 4.8% on Raspberry Pi 5.
* **DX-ModelZoo:** 1.0.0 with 497 models and the `dxmz` CLI.

Ubuntu 18.04 and DX-TRON are no longer supported.

## Get help

Ask questions, share projects and connect with DEEPX engineers in the [DEEPX Developer Community](https://community.deepx.ai/).
