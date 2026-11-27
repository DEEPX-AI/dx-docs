---
title: Agent driven development
description: Build DEEPX NPU apps and compile models from plain language prompts with an AI coding agent and the DEEPX knowledge base.
---

# Agent driven development

Agent driven development (`dx-agent-dev`) lets you describe an NPU app or a model task in plain words and have an AI coding agent build it with the DEEPX SDK.

!!! warning "Beta"
    Agent driven development is a beta feature. Skills and routing can change between releases. An agent's output is not verified until you run it: always check the generated files and run them before you rely on them.

## What it is

The DEEPX SDK checkout ships a knowledge base that coding agents load automatically when you open the project folder. It holds instructions, skills and validation scripts for the SDK parts:

| Part | What the agent can do |
|---|---|
| dx-compiler | Export PyTorch to ONNX and compile ONNX to `.dxnn` with DX-COM, including the config, calibration data and optional PPU |
| dx_app | Generate Python or C++ inference apps in the DX-APP example style |
| dx_stream | Generate DX-Stream GStreamer pipelines (single model, cascaded, parallel, MQTT or Kafka output) |
| dx-runtime | Route work across dx_app and dx_stream and validate the result |

Each task follows the same process: brainstorm (the agent asks questions first), plan, test driven build, and verify before it reports done.

## Supported agents

| Agent | Start it in the `dx-all-suite` folder |
|---|---|
| Claude Code | `claude` |
| GitHub Copilot | Open the folder in VS Code and use Copilot Chat |
| Cursor | `cursor-agent`, or open the folder in Cursor |
| OpenCode | `opencode` |
| Codex CLI | `codex` |

No extra setup is needed: each agent reads its configuration files from the project when it starts.

!!! note "Submodule boundary"
    Copilot, Claude Code and Codex only see files in the current git root. Opened at `dx-all-suite/`, they do not load the files of `dx-compiler/` or `dx-runtime/`, which are separate git submodules. Open the submodule folder for submodule specific work. OpenCode bridges the boundary through `opencode.json`.

## Before you start

* The DEEPX SDK installed, including DX-RT. See [Install the DEEPX SDK](../get-started/install.md).
* DX-COM for compile tasks (`pip install dx-com`).
* Python 3.8 to 3.14.
* One of the agents above, installed and signed in.
* A DEEPX NPU to run and verify the generated apps.

## How to start

1. Open the `dx-all-suite` folder in your agent (for example `cd dx-all-suite && claude`).
1. Type a prompt. At the suite level the agent routes the task to the right part:

    ```text
    Compile yolo26n.onnx to DXNN and build a person detection Python app with it
    ```

1. Answer the agent's questions. Compile tasks ask about NMS free export, ONNX simplification and PPU; app tasks ask about language and variant, AI task and model.
1. Check the output folder, then run `setup.sh` and `run.sh` from it.

In Copilot and OpenCode you can also call a builder directly, for example `@dx-suite-builder`, `@dx-compiler-builder`, `@dx-app-builder` or `@dx-stream-builder`, followed by the prompt.

More example prompts:

| Where | Prompt |
|---|---|
| dx-compiler | `Convert my yolo26x.pt to ONNX and compile it to DXNN for DX-M1` |
| dx-compiler | `Compile model.onnx to DXNN with INT8 quantization using EMA calibration with 200 samples from ./calibration_images/` |
| dx_app | `Build a yolo26n person detection app using Python` |
| dx_stream | `Build a detection pipeline with RTSP camera and tracking` |
| suite | `Compile yolo26n.onnx to DXNN and build a detection streaming pipeline with RTSP output` |

## Where the output goes

The agent never edits existing source by default. It writes into `dx-agent-dev/<session_id>/` inside the part it worked on (for example `dx-runtime/dx_app/dx-agent-dev/...`). The session ID has the form `YYYYMMDD-HHMMSS_<agent>_<coding_model>_<target_model>_<task>`. Code goes to `src/` only when you ask for it. Cross project tasks run from the suite also get links in `dx-all-suite/dx-agent-dev/`.

| Part | Typical session content |
|---|---|
| dx-compiler | `config.json`, `model.onnx`, `model.dxnn`, `compiler.log`, an inference script, `verify.py` (ONNX versus DXNN comparison), `setup.sh`, `run.sh`, `README.md` |
| dx_app | `README.md`, `session.json`, `setup.sh`, `run.sh`, `session.log`, `config.json`, `factory/`, `{model}_sync.py` and the variants you asked for |
| dx_stream | `README.md`, `session.json` and the pipeline script |

## Facts the agent relies on

These DX-COM limits also apply when you compile by hand:

* Batch size must be 1, and input shapes must be static.
* ONNX opset 11 to 21; we recommend opset 17.
* Models with several inputs compile through the Python API only, not the CLI.
* Find the input name for `config.json` with `onnx.load(model).graph.input[0].name`.

## In DX AI Studio

The **DX Agent Dev** tool in [DX AI Studio](ai-studio/index.md) runs the same agents from the browser.

1. **Connect an agent.** The console detects installed CLIs: Claude Code (`claude`), GitHub Copilot CLI (`copilot`), Cursor (`cursor-agent`), Codex (`codex`) and OpenCode (`opencode`). A badge shows whether each is signed in; if not, it shows the command to run, then checks again.
1. **Set the run:**
    * **Agent** and **Model:** saved as the Studio agent (`~/.dx-ai-studio/agent.json`) and shared with the hub prompt box and the chat. Copilot, Cursor and OpenCode list their models live; others use a built in list. A hint warns if a model is too weak.
    * **Reasoning effort:** the levels that agent supports.
    * **Target:** Suite, dx-runtime, dx_app, dx_stream or dx-compiler.
    * **Interaction:** Interactive (asks questions) or Autopilot (no questions).
1. **Describe the task.** The agent streams its progress; the **activity panel** shows each turn's shell and tool output. You can also start and follow the run from the hub prompt box.
1. **Stop** requests cancellation; wait for **Stopped**. Stopping does not undo files already written. After a dropped connection, reconnect and check the existing run before you submit again.
1. **Showcases** opens the gallery of example apps. Viewing one does not start an agent or an NPU run.

A wall clock timeout frees the slot when a run gets stuck. If the tool says the agent knowledge folder is not found, set `DX_HARNESS_ROOT` to your `dx-all-suite` checkout, or start the studio from inside the suite, and reload.

## Next steps

* [See what agents built from one prompt](agent-showcases.md)
* [Compiler skills and example scenarios](../compiler/agent-driven-development.md)
* [Compile by hand with DX-COM](../compiler/index.md)
* [DX-APP examples](app/index.md)
