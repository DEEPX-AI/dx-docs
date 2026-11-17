---
title: The hub
description: The DX AI Studio home screen, navigation, tutorials, languages and the chat assistant.
---

# The hub

The hub is the DX AI Studio home screen: every tool opens from here and runs under the hub's single address.

## Before you start

* A running studio. See [Install and launch](install-and-launch.md).

## Home screen

| Element | What it does |
|---|---|
| **Prompt box** (*Describe anything. Run it on DX-M1.*) | Type a request in plain words and click **Build it**. The hub first shows suggested tool routes or an agent plan. Nothing runs until you pick a route card (opens that tool) or the agent execution button (starts the agent on the home page). |
| **Agent** row | Picks the coding agent, model, effort and mode for the prompt box. The choice is saved as the Studio agent and shared with DX Agent Dev and the chat. |
| **Tool cards** | The nine tools plus **SDK Library** and **About DEEPX**. Cards show live facts, for example *26 demos · 12 groups* for DX App. |
| **DX-M1 widget** (left) | The NPU in this computer: cores, temperature, clock and power. Click it to open DX Monitor. |
| **Measured on DX-M1** (right) | FPS measured on this device and how many models and tasks were measured. Click it to open DX Benchmark. |
| **Explore DX AI Studio** and **Physical AI ecosystem** chips | Open the platform overview and the DEEPX ecosystem page |
| Bottom link bar | Links to Get Started, S/W Download, Tech Docs, Documents, Model Zoo, GitHub and deepx.ai |

Example: enter `compile yolo26n to DXNN`, press **Build it**, then select the Compiler route card. Check the model and config in DX Compiler before you compile. An agent route needs an installed, signed in coding CLI (see [Agent driven development](../agent-driven-development.md#in-dx-ai-studio)).

## Top bar

From left to right on the right side:

* **Buy:** the DEEPX store.
* **Language:** the six UI languages.
* **Theme:** cycles dark, light and system.
* **Connected browsers:** appears when other computers can reach the studio. See [Remote access and security](install-and-launch.md#remote-access-and-security).
* **Tutorial:** opens the tutorial contents for the current view.

## Navigation

* Click a card or an icon in the **left rail** to open a tool. **Hub** at the bottom of the rail returns home.
* **Top page tabs** switch views inside a tool (for example Models or Graph Composer in DX App).
* The current tool and view are in the URL, so links are shareable and survive a reload.
* `Alt`+`1` to `Alt`+`9` open a tool directly. `Esc` closes the topmost thing first (chat, tutorial, search, dialog) and only then leaves the tool.
* Inside every tool the **NPU monitor** sits in the left rail as a thermometer button. Its dot shows the temperature state; click it to unfold the readout.

## Guided tutorials

**Tutorial Mode** (the switch at the top right of the home, next to **Replay Intro**) is on by default. The first visit to the home runs a short walkthrough, and opening a tool opens that tool's tutorial contents. Pick a section or **Start from Beginning**. Steps have **Prev**, **Skip** and **Next** (arrow keys work too); `Esc` ends the tour.

## Language

The studio is available in English, 한국어, 日本語, 简体中文, 繁體中文 and Español. A first visit opens in your browser's language (English when it is none of these). Switch from the top bar at any time. Every open tool follows, and your choice wins over the browser language.

## Chat assistant

The round chat button at the bottom right of every view opens the **DX AI Studio Help** assistant. It answers questions about DEEPX models, the SDK, the compiler and the studio tools from bundled DEEPX SDK knowledge. It is separate from the DX Agent Dev console.

The top line of the chat always says which AI answers. With nothing set, it answers through the coding agent you are signed in to (`claude`, `copilot`, `cursor-agent`, `codex` or `opencode`), the same Studio agent that Home and DX Agent Dev use. A coding agent answers from its vendor's cloud and uses that account.

**Change** asks one question, *Which AI should answer?*:

| Choice | What it uses |
|---|---|
| **Coding agent on this PC** | An installed CLI; each shows whether it is signed in, or the command that signs it in |
| **My local LLM server** | Your own Ollama compatible server (Ollama, LM Studio, llama.cpp). Its models are discovered automatically. |
| **Cloud API key** | OpenAI, Anthropic, Google, GitHub Models or a custom OpenAI compatible endpoint |

Saving tests the connection first. If the test fails, the reason is shown with **Save anyway** (which stores the choice but does not prove it works). A blank key field keeps the saved key. **Back to automatic** forgets the choice. Temperature and **Refresh knowledge** (resync the assistant's SDK knowledge) are under **Advanced**. With no AI connected, the assistant gives basic built in guidance and says how to connect one.

## Next steps

* [Browse models and compile](workflow.md)
* [Run inference in DX App](app.md)
* [SDK Library and other reference views](reference.md)
