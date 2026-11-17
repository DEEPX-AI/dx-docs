---
title: Monitor and benchmark
description: Watch live NPU telemetry in DX Monitor and compare stored benchmark results in DX Benchmark.
---

# Monitor and benchmark

This page shows you how to watch the NPU live in DX Monitor and compare stored results in DX Benchmark.

## Before you start

* A running studio. See [Install and launch](install-and-launch.md).
* For real telemetry: the NPU driver and DX-RT (`dx_engine`). Check with `dxcli -s`.

## DX Monitor

DX Monitor is a live dashboard for the NPU and the host: temperature, voltage, clock, DRAM and use, next to CPU and memory, plus the installed versions.

1. Open the dashboard. It shows NPU telemetry per device (temperature, voltage, clock, DRAM, per core use) and system stats (CPU per core, load, memory).
1. Pick a **time range** (Realtime, 5m, 15m, 30m, 1h, All, up to about 12 hours) and the metric the charts show, or **View All** as a grid.
1. Keep it open while you run inference in the other tools. Charts stream over SSE, with a polling fallback.

Example: keep DX Monitor open, start a video run in DX App, and compare NPU use and temperature before and during the run.

### Read the state before the numbers

| State | Meaning | What to do |
|---|---|---|
| Real, current | The telemetry worker supplies current NPU samples | Read each device's values with the selected time window |
| **NPU telemetry unavailable** | No usable NPU samples. Host stats still work. | Check the diagnostic, DX-RT (`dx_engine`), the driver and `dxcli -s` |
| **NPU telemetry is not current** (stale) | The source stopped sending current samples | Do not treat old values as live; check the diagnostic |
| **Mock** | Demo data, enabled only by `DX_MONITOR_EXPLICIT_MOCK=1` | Never use it as a measurement |

An SSE connection only shows that the browser is connected, not that the NPU is healthy. Chart history lives in your browser while it receives samples; it is not a server recording, and samples missed while disconnected cannot be recovered. `DX_MONITOR_SKIP_HARDWARE_INIT=1` skips hardware setup and leaves NPU telemetry unavailable; it is not mock mode.

### Features

* Warn and critical **threshold alerts** with limit lines, per core NPU temperature and per channel DRAM temperature.
* **NPU Topology:** firmware, chip and variant, board, DDR type, frequency and size, per core use.
* **DDR ECC alerts:** single bit (SBE) and double bit (DBE) error warnings.
* **Runtime Events** log: INFO, WARN, ERROR and CRITICAL entries from the runtime.
* **Version info:** DX-RT, PCIe driver, DX Engine, SDK, OS and Python versions, and uptime. `dxcli -s` shows the same device information on the command line.

## DX Benchmark

DX Benchmark shows stored DEEPX NPU benchmark results in the browser: throughput, latency and multi stream numbers per model, with charts. It is **read only**. New results come from the standalone [DX-Benchmark](../tools/benchmark.md) command line tool (`./run.sh run`), and the same data feeds DX EdgeGuide.

| Tab | What it shows |
|---|---|
| **Dashboard** | FPS, latency and channel figures per model. Compare host and NPU environments side by side, filter by task and model size, and toggle ONNX Runtime on or off. Click a bar or row to drill in. |
| **Results** | Past runs by hardware and run ID, with each run's Markdown report and raw JSON |
| **Settings** | The read only deployment config (folders, thermal cooldown, iterations, warm up, FPS threshold). Changes are refused with HTTP 501 "deployment-fixed"; edit the config files before starting the server instead. |

The **Dashboard** has five sub tabs:

| Sub tab | What it shows |
|---|---|
| **E2E FPS Overview** | End to end FPS by model size, with a run selector per environment |
| **Full Metrics** | Latency, throughput, E2E FPS and max channels per model, plus the NPU identity (product, SKU, modules, device count) and host, driver and firmware details |
| **Detailed Data** | Per model and per task table with NPU thermal data (min and max temperature and clock, a **Throttled** badge) and a run status column (**Partial**, **Timeout**, **Error**) |
| **Version Trend** | A metric across historical runs, to see performance change between versions |
| **ORT ON/OFF** | ONNX Runtime on versus off, per model size |

*Max channel* is the highest number of simultaneous video streams a model sustains on that NPU while every stream meets the FPS threshold.

### Compare a model fairly

1. In **E2E FPS Overview**, pick the environments and their runs. Keep task, model size and ORT setting the same, and compare the shown software versions.
1. Click a bar to see the environment, then open **Full Metrics** for latency, throughput, E2E FPS and channels.
1. Open **Detailed Data** and check thermal values, **Throttled** and run status. **Partial**, **Timeout** or **Error** is not a zero result; read the run's report in **Results**.
1. A link hands the current selection to [DX EdgeGuide](edge-guide.md).

## Next steps

* [Run your own benchmark with DX-Benchmark](../tools/benchmark.md)
* [Get a hardware recommendation in DX EdgeGuide](edge-guide.md)
* [NPU driver and firmware](../runtime/driver-firmware.md)
