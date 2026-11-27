---
title: Tools
description: Overview of the DEEPX SDK tools for building applications, and the tools for benchmarking, AWS deployment, Kubernetes and agent driven development.
---

# Tools

This section covers the SDK tools you build applications with and the tools that help you measure, deploy and automate on the DEEPX NPU.

| Tool | What it does | Version |
|---|---|---|
| [DX-APP](app/index.md) | Ready to run C++ and Python example applications for hundreds of vision models | 3.3.0 |
| [DX-Stream](stream/index.md) | GStreamer elements for real time, multi stream video inference pipelines | 3.2.0 |
| [DX-ModelZoo](model-zoo/index.md) | Evaluate and compile ready made models with the `dxmz` command line tool | 1.0.0 |
| [DX AI Studio](ai-studio/index.md) | Browser workspace that brings the SDK tools into one hub | 0.1.1, beta |
| [DX-Benchmark](benchmark.md) | Reproducible YOLO26 benchmarks on any host and NPU combination, with reports and a dashboard | 0.2.0, beta |
| [DX-Edge](dx-edge.md) | Compile models and deploy the runtime through AWS Marketplace and AWS IoT Greengrass | |
| [Kubernetes device plugin](kubernetes.md) | Schedule DX-M1 NPUs in Kubernetes as the resource `deepx.ai/dx-m1` (Helm chart `dx-npu`) | 0.1.0 |
| [Agent driven development](agent-driven-development.md) | Build NPU apps from plain language prompts with an AI coding agent | beta |

Two more tools live in other sections:

* **DX-Fit**, part of DX-RT, is described in the [DX-RT section](../runtime/index.md).
* The **compilation summary report** (`dxcom --export_html`) shows a compiled model's structure and CPU and NPU split. It replaces DX-TRON, which was removed in SDK 2.5.0. See the [DX-COM section](../compiler/index.md).

## More pages

* [Greengrass devices](dx-edge-devices.md): set up a DX-AIPlayer N97 or a Raspberry Pi 5 kit as a Greengrass core device.
* [Agent showcases](agent-showcases.md): apps built from a single prompt.
