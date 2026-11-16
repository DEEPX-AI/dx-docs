---
title: Tools
description: Overview of the extra DEEPX tools for benchmarking, AWS deployment, Kubernetes and agent driven development.
---

# Tools

This section covers the tools around the core SDK that help you measure, deploy and build on the DEEPX NPU.

| Tool | What it does | Status | Page |
|---|---|---|---|
| **DX-Benchmark** | Reproducible YOLO26 benchmarks on any host and NPU combination, with reports and a dashboard | Beta, 0.2.0 | [DX-Benchmark](benchmark.md) |
| **DX-Edge** | Compile models and deploy the runtime through AWS Marketplace and AWS IoT Greengrass | | [DX-Edge](dx-edge.md) |
| **Kubernetes device plugin** | Schedule DX-M1 NPUs in Kubernetes as the resource `deepx.ai/dx-m1` (Helm chart `dx-npu`) | 0.1.0 | [Kubernetes](kubernetes.md) |
| **Agent driven development** | Build NPU apps from plain language prompts with an AI coding agent | Beta | [Agent driven development](agent-driven-development.md) |
| **DX AI Studio** | Browser workspace for all of the above and the SDK tools | Beta, 0.1.1 | [DX AI Studio](../ai-studio/index.md) |

Two more tools live in other sections:

* **DX-Fit**, part of DX-RT, is described in the [DX-RT section](../runtime/index.md).
* The **compilation summary report** (`dxcom --export_html`) shows a compiled model's structure and CPU and NPU split. It replaces DX-TRON, which was removed in SDK 2.5.0. See the [DX-COM section](../compiler/index.md).

## Where to go

* [DX-Benchmark](benchmark.md): measure model latency, throughput, E2E FPS and channel capacity.
* [DX-Edge](dx-edge.md): DEEPX Compiler Solution and DEEPX Greengrass Solution on AWS.
* [Greengrass devices](dx-edge-devices.md): set up a DX-AIPlayer N97 or a Raspberry Pi 5 kit as a Greengrass core device.
* [Kubernetes](kubernetes.md): install the `dx-npu` chart and run NPU pods.
* [Agent driven development](agent-driven-development.md): start a coding agent on the DEEPX SDK.
* [Agent showcases](agent-showcases.md): apps built from a single prompt.

## Next steps

* [Install the DEEPX SDK](../get-started/install.md)
* [DX AI Studio](../ai-studio/index.md)
