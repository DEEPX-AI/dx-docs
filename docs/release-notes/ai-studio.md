---
title: DX AI Studio and tools release notes
description: Changes in DX AI Studio, DX-Benchmark, DX-Edge and the Kubernetes device plugin by release.
---

# DX AI Studio and tools release notes

This page lists what changed in DX AI Studio and the extra tools in each DEEPX SDK release.

## DX AI Studio 0.1.1 (SDK 2.5.0, 2026-10-23)

### Hub and design

* New home with a prompt box (*Describe anything. Run it on DX-M1.*) that first suggests tool routes or an agent plan and waits for your choice. Tool cards with live facts, a DX-M1 widget, a "Measured on DX-M1" card and a DEEPX Developers link bar. It replaces the orbital launcher.
* Light, dark and system themes; one icon set in all tools (no emoji); variable fonts with one CJK face per language.
* New intro built from real runs on a DX-M1.
* The NPU monitor folds into a rail button above **Hub** and remembers your choice.
* A first visit opens in the browser's language; a language picked in the menu still wins.

### Remote access and security

* Other computers pair once with a 6 digit code from the launcher terminal; **Connected browsers** lists and disconnects them.
* Tool servers listen on the board only; no wildcard CORS; Host and Origin checks; compile paths limited to allowed folders.

### Tools

* **DX App:** per model example layout, **Run Demo** (26 demos on one stage), live Continuous runs with FPS, async options, Model Zoo inference that runs each model's own example, and runner errors shown as errors.
* **DX App Graph Composer** replaces the Lab composer: several models and logic blocks in one graph, checked while you edit, run once or Live with events, exported as a standalone C++ project. Nine scenario templates with real NPU results. Project history keeps the latest 50 versions.
* **DX App Lab:** **Add Model** works again, **Experiment** really runs (read, one inference, FPS), **Safety Center** rolls back changes that only created files, and **Commit with git** lists the files and commands.
* **DX App:** RTSP takes the camera's own URL; RTSP with the Python examples and multi slot camera runs work (they failed with "Input file not found").
* **DX Stream:** Demo Launcher on the shared stage with WebRTC or remote MJPEG playback; Setup as a step list; Setup step 6 checks both WebRTC packages; Pipeline Builder has a camera source (`v4l2src`). `launcher.sh` repairs a `.venv` made without system site packages.
* **DX Model Zoo:** 497 variants across 29 tasks (348 to 497); 492 run in Graph Composer. PP-ShiTu's main body detectors have their own **Main-body Detection** task. **Run Inference** finds each model's example (it failed with "Binary not found").
* **DX Cloud** (ninth tool): AWS Compiler (subscription, stacks, cloud compile with log and `.dxnn` download) and AWS Greengrass (dx-runtime devices).
* **DX Compiler:** large graphs open readable at the input node; picking a sample model draws its graph; Config Builder asks for a dataset folder (or Dummy Loader); a refused compile keeps the graph and shows the reason. Agentic Auto Compile opens on the agent CLI's default model.
* **DX Compiler, DX App, DX Stream:** Setup shows the next step and why a button is locked.
* **DX EdgeGuide:** channel counts come from measured E2E pipeline throughput, measured where a tested stream count brackets the target and estimated otherwise (capped at twice the tested count). Cards show their arithmetic and notes for throttling, NPU or host limit and unmeasured latency. 60 FPS no longer reads 0 channels almost everywhere.
* **DX Agent Dev:** a **Stop** button; a dropped connection no longer stays "Running...".
* **DX Monitor:** guidance separates unavailable, stale and explicit Mock telemetry.
* **Chat:** answers through your signed in coding agent with no setup; one settings question (coding agent, local LLM server or cloud API key) with a connection test; clear reasons when an external API fails.
* **SDK Library** follows the suite docs, with List and Cabinet browsing and a document viewer.
* Faster screens over remote access, accessibility fixes, phone width (390 px) layout fixes and many translation fixes.
* Tool servers keep their errors in `~/.local/state/dx-ai-studio/logs/`; DX App no longer stops after an idle hour.
* Managed runtime profiles target SDK 2.5.0 (DX-RT 3.5.0, NPU driver 2.7.0, firmware 2.7.6).

## DX AI Studio 0.1.0 (SDK 2.4.0, 2026-07-22)

* First beta release: one browser workspace with eight tools (DX App, DX Stream, DX Model Zoo, DX Compiler, DX EdgeGuide, DX Benchmark, DX Monitor, DX Agent Dev), the SDK Library and About DEEPX, in six languages, with a built in chat assistant.
* Pure Python standard library; `./launcher.sh` installs and boots every tool.
* Later 2.4.x releases added Model Zoo downloads, more reliable remote Stream playback, guided runtime profile install and rollback, supervised NPU telemetry (SDK 2.4.1), and Lab Composer, plugin scaffolding, batch runs and runtime diagnostics (SDK 2.4.2).

## DX-Benchmark

* **0.2.0 (SDK 2.5.0):** measurement protocol v2 and results for six environments measured on SDK 2.5.0.
* **0.1.0 (SDK 2.4.1, 2026-08-03, beta):** first release. Model level and E2E pipeline tiers, ORT ON and OFF comparison, thermal normalization with throttle detection, environment fingerprint, dashboard and analysis. Results for six environments on SDK 2.3.3 and 2.4.0.

## Kubernetes device plugin

* **0.1.0 (SDK 2.5.0):** first release. DX-M1 NPUs can be scheduled on Kubernetes (k3s) as `deepx.ai/dx-m1`, with CDI injection of devices and host libraries, node labels through node feature discovery, Prometheus metrics and the `dx-npu` Helm chart on GHCR.

## DX-Edge

* **SDK 2.4.2 (2026-08-14):** first release of the DX-Edge guides: DEEPX Greengrass Solution, DEEPX Compiler Solution and the DX-AIPlayer N97 Greengrass guide. The DX-M1 Raspberry Pi 5 kit guide followed.

## Agent driven development

* **SDK 2.4.0 (2026-07-22, beta):** first release, supporting Claude Code, Cursor, GitHub Copilot, OpenCode and Codex, with showcases.

## Next steps

* [DX AI Studio](../ai-studio/index.md)
* [Tools](../tools/index.md)
* [All release notes](index.md)
