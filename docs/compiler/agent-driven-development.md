---
title: Agent driven development for DX-COM
description: Compile models with an AI coding agent that uses the DX-COM skills in the dx-compiler repository.
---

# Agent driven development for DX-COM

!!! warning "Beta"
    Skill definitions and routing can change between releases.

This page covers the compiler skills. For how agent driven development works across the SDK, see [Agent driven development](../tools/agent-driven-development.md).

Compile ONNX models to DXNN format using natural language instructions. AI coding agents understand the DX-COM compilation pipeline (config.json generation, calibration data preparation, quantization strategies and PPU configuration), so you can describe *what* you want and let the agent handle the implementation details.

Supported workflows:

- PyTorch model export to ONNX with automatic opset and shape configuration
- ONNX to DXNN compilation with INT8 quantization via DX-COM CLI or Python API
- End-to-end pipeline: PT → ONNX → DXNN with calibration and validation

## Prerequisites

| Requirement | Details |
|---|---|
| **DX-COM** | Installed via [the install guide](index.md#install-the-compiler) |
| **AI coding agent** | Claude Code, GitHub Copilot (VS Code), Cursor, OpenCode, or Codex CLI |
| **Python** | 3.8 to 3.14 |
| **ONNX** | opset 11 to 21 |
| **OS** | Debian Linux (Ubuntu 20.04 to 26.04), x86_64 |

## How it works

The agent knowledge base lives in a `.deepx/` directory in the `dx-compiler` repository. Each supported AI tool auto-loads it through its own configuration mechanism (CLAUDE.md, `.cursorrules`, etc.). The agents read the compilation pipeline definition, constraints, and skill files from this directory at task time. No extra setup is required beyond cloning the repo.

```
PyTorch (.pt)      ONNX (.onnx)                   DXNN (.dxnn)
     │                  │                               │
     ├─torch.onnx.export►├─── DX-COM compile ──────────►│
     │                  │    + config.json               │
     │                  │    + calibration data          │
     │  dx-model-converter   dx-dxnn-compiler            │
     └──────────────────┴───────────────────────────────┘
              dx-compiler-builder (router)
```

### Key constraints

- Batch size must be **1**
- Input shapes must be **static**: no dynamic axes
- ONNX opset: **11 to 21**
- Multi-input models require the **Python API** (not CLI)
- Target device is always **DX-M1**: agents do not ask about hardware selection

## Agents

| Agent | Description |
|---|---|
| `@dx-compiler-builder` | Master router: classifies tasks and routes to specialist agents |
| `@dx-model-converter` | Converts PyTorch models to ONNX format |
| `@dx-dxnn-compiler` | Compiles ONNX models to DXNN using DX-COM |

## Skills

### DEEPX build skills

| Skill | Description |
|---|---|
| `/dx-agent-compiler-compile` | Step-by-step ONNX to DXNN compilation workflow |
| `/dx-agent-compiler-convert` | Step-by-step PyTorch to ONNX conversion workflow |
| `/dx-agent-compiler-validate` | Validate a compiled `.dxnn` model output |
| `/dx-agent-compiler-pre-optimize` | Build a verified `pre_optimize` config (YOLO / RTMDet head tensor names) |
| `/dx-agent-brainstorm` | Brainstorm a build plan with model registry check and sub-project routing |
| `/dx-agent-tdd` | Validation order: factory, pipeline, and integration checks |
| `/dx-agent-verify` | Verification checklists across dx_app, dx_stream, and cross-project |

### General SWE skills

| Skill | Description |
|---|---|
| `/dx-swe-writing-plans` | Write implementation plans from specs or requirements |
| `/dx-swe-executing-plans` | Execute implementation plans with review checkpoints |
| `/dx-swe-debugging` | Systematic debugging before proposing fixes |
| `/dx-swe-parallel-agents` | Dispatch independent tasks to parallel agents |

## Supported AI tools

| Tool | Setup |
|---|---|
| **Claude Code** | Open the `dx-compiler` folder. `CLAUDE.md` is auto-loaded |
| **GitHub Copilot** | Open folder in VS Code. `.github/copilot-instructions.md` is auto-loaded |
| **Cursor** | Open folder in Cursor. `.cursorrules` is auto-loaded |
| **OpenCode** | Open the folder. `AGENTS.md` is auto-loaded |
| **Codex CLI** | Open the folder. `AGENTS.md` is auto-loaded |

## Example scenarios

### Scenario 1: Convert PyTorch to ONNX

```
@dx-compiler-builder Convert my YOLOv8n model from PyTorch to ONNX
```

The agent asks for the `.pt` file path, verifies batch size = 1 and static shapes, then runs `torch.onnx.export` with the correct opset and verifies the output with `onnxruntime`.

### Scenario 2: Compile ONNX to DXNN

```
@dx-compiler-builder Compile yolov8n.onnx to DXNN with INT8 quantization
```

The agent generates a `config.json` with calibration settings, selects the calibration dataset, runs `dxcom` or `dx_com.compile()`, and verifies the `.dxnn` output.

### Scenario 3: Full pipeline PT → DXNN

```
@dx-compiler-builder Full pipeline: convert my ResNet50 from PyTorch and compile to DXNN
```

The agent routes through `@dx-model-converter` then `@dx-dxnn-compiler` sequentially, handling calibration and validation at each stage.

## Config auto-inference

When you provide an ONNX model without a `config.json`, the agent inspects the model graph and infers a starter configuration automatically: input shape, normalization parameters, and calibration method. You can review and adjust before compilation runs.
