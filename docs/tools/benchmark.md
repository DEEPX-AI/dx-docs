---
title: DX-Benchmark
description: Measure YOLO26 latency, throughput, E2E FPS and multi stream capacity on a DEEPX NPU with the DX-Benchmark command line tool.
---

# DX-Benchmark

DX-Benchmark lets you measure YOLO26 performance on your own host and DEEPX NPU with one standard procedure, so results compare across machines and SDK releases.

!!! warning "Beta"
    DX-Benchmark (tool 0.2.0, measurement protocol v2) is a beta release. The CLI and output schema can change. Print the version with `./run.sh --version`.

It measures two levels, both with ONNX Runtime ON and OFF and with thermal throttle detection:

| Level | Tool used | Metrics |
|---|---|---|
| Model level | `dxrun` (DX-RT) | **Latency** (single core, sync) and **Throughput** (multi core, async) |
| E2E pipeline | DX-Stream | **Single stream** E2E FPS and **multi stream** channel capacity |

## Before you start

* Linux (x86_64 or arm64) with a DX-M1 or DX-H1 NPU.
* Python 3.9 or newer. No pip packages are needed.
* The DEEPX runtime installed (see [Install the DEEPX SDK](../get-started/install.md)): `run_model` (the old name of `dxrun`), `gst-launch-1.0`, `gst-inspect-1.0` and `dxcli` on `PATH`, plus the DX-Stream plugin (`libgstdxstream.so`) and postprocess libraries under `/usr/local/share/gstdxstream/lib/`.
* System tools: GNU `time`, `jq`, `ffmpeg` (for `ffprobe`), `curl`, `tar`. `sudo ./setup_host.sh` installs them with apt; on other distros use for example `dnf install time jq ffmpeg curl tar`.
* Network access to `https://sdk.deepx.ai` to download models and videos.

The tool is in the DEEPX SDK at `dx-all-suite/dx-benchmark`.

## Quick start

```bash
cd dx-all-suite/dx-benchmark
./run.sh preflight          # check tools, print an environment fingerprint
./setup_data.sh             # download models and videos (no sudo)
sudo ./setup_host.sh        # one time host setup (see the warning below)
./run.sh run                # full suite: model level, E2E and multi stream
./run.sh dashboard results  # build the dashboard
cd results/dashboard && python3 -m http.server 8899
```

Then open `http://localhost:8899/`. The dashboard is plain HTML, CSS and JavaScript with no CDN, so it works offline.

!!! warning "setup_host.sh adds passwordless sudo"
    `setup_host.sh` writes `/etc/sudoers.d/benchmark-dxrt`, which lets the current user run `systemctl restart dxrt.service`, `dmesg`, `journalctl -u dxrt.service` and `lspci` as root without a password. The tool needs this to recover a hung NPU and collect diagnostics. To undo it, run `sudo rm -f /etc/sudoers.d/benchmark-dxrt`.

For comparable numbers, keep cooling, power, background load and CPU governor the same across the runs you compare. The fingerprint records them.

## Commands

| Command | What it does |
|---|---|
| `--version` | Print the tool version |
| `preflight` | Check tool availability and print the environment fingerprint |
| `dry-run` | Preview the benchmark matrix without running |
| `run` | Run the benchmarks |
| `report <result_dir>` | Rebuild the Markdown report from existing results |
| `aggregate <results_root> [--output PATH]` | Merge results into one `dataset.json` |
| `dashboard <results_root> [--output DIR]` | Build the static HTML dashboard |

`./run.sh` activates `venv/` if it exists and runs `python3 -m benchmark`.

### Examples

```bash
./run.sh dry-run --sizes n,s --task object_detection
./run.sh run --family model
./run.sh run --sizes n,s --family model --model-time 30
./run.sh run --resume results/<hw_id>/<run_id>
./run.sh run --resume results/<hw_id>/<run_id> --retry-failed
./run.sh report results/<hw_id>/<run_id>
./run.sh aggregate results --output /tmp/dataset.json
```

### Options for `run` and `dry-run`

| Option | Default | Description |
|---|---|---|
| `--task` | `all` | `all`, `object_detection`, `pose_estimation`, `segmentation`, `oriented_bbox`, `classification` |
| `--sizes` | `n,s,m,l,x` | Model sizes, comma separated |
| `--family` | `all` | `model`, `e2e`, `multi` or `all` |
| `--model-time` | 30 | Throughput duration in seconds (`dxrun -t`). Latency always uses 300 loops (`-l`). |
| `--warmup` | 1 | Warm up runs |
| `--runs` | none | Set all repetition counts to one value. Defaults: latency 1, throughput 3, E2E 3. |
| `--fps-threshold` | 30 | Minimum FPS per channel for multi stream |
| `--video` | per task | Input video for all tasks |
| `--output` | `results/` | Output root. Results go to `<output>/<hw_id>/<run_id>/`. |
| `--resume` | none | Continue an existing result folder |
| `--retry-failed` | off | With `--resume`, rerun only entries not in `ok` or `partial` status |
| `--allow-hot-start` | off | Allow a start at or above the 55 °C cap (the run is flagged) |
| `--product-name` | none | Use this name instead of the host name in the HW_ID (for example `DX-AIPlayer-N97`) |
| `--dx-all-suite-version VER` | from `release.ver` | SDK release for the Version Trend axis (for example `v2.5.0`) |

The HW_ID is `{product_name}_{hw_config}` with `--product-name`, otherwise `{hostname}_{hw_config}`. The SDK version comes from `--dx-all-suite-version`, else from the suite root `release.ver`; with neither, the run is recorded as `unknown` with a warning. There is no interactive prompt.

To track versions, run on the same hardware before and after an SDK upgrade and open the **Version Trend** tab.

## Supported tasks

| Task | Model level | E2E pipeline | Multi stream |
|---|---|---|---|
| Object Detection | yes | yes | yes |
| Pose Estimation | yes | yes | yes |
| Segmentation | yes | yes | yes |
| Oriented BBox (OBB) | yes | yes | yes |
| Classification | yes | yes | no |

OBB uses 1024×1024 input, classification 224×224 (keep ratio off), all others 640×640. Classification has no multi stream test because a 224×224 classifier does not represent real video analytics.

## How a run works

```mermaid
flowchart LR
  P[preflight] --> S[setup_data] --> R[run per model and ORT mode] --> RP[report] --> AG[aggregate] --> DB[dashboard]
```

For each model and ORT mode the tool runs, in order:

1. **Cooldown** until the NPU is at or below `min(settled idle + 10 °C, 55 °C)`. A start above 60 °C idle is rejected.
1. **Latency**, single core sync, 300 loops, from cold.
1. **Throughput**, after a buffer count sweep: 3 runs of 30 s, each after its own cooldown and a 2 s throw away run.
1. **Cooldown** to remove the throughput heat.
1. **E2E single stream**: the full GStreamer pipeline, 3 runs.
1. **Multi stream**: jump to the estimate single stream FPS ÷ 30, then search up and down for the most channels that all hold 30 FPS (not one by one; safety cap 128 streams).

E2E and multi stream run back to back as sustained load, so on a board that throttles the mean includes the thermal ramp. Throttling is flagged, never hidden.

### Measurement protocol v2

| Parameter | Value |
|---|---|
| Throughput duration | 30 s |
| Latency loops | 300 |
| Throughput runs | 3, each after a cooldown |
| E2E runs | 3 |
| ORT modes | ON and OFF |
| Cooldown target | `min(settled idle + 10 °C, 55 °C)`, timeout 1000 s |
| Multi stream threshold | 30 FPS per channel |
| NPU clock monitoring | `dxtop` core clock during the run, `dxcli` snapshots before and after |
| Process timeout | `dxrun` 600 s per run; E2E and multi stream 90 s without progress, 1800 s hard cap |

Throughput, E2E and multi stream report NPU **core use** sampled by `dxtop`. Latency reports NPU **occupancy** (`npu_task_ms / total_ms`) because a short single core run is too fast for the sampler.

### Recovery from hangs

* **Graceful stop:** on a timeout the tool sends SIGTERM, waits 10 s, then SIGKILL.
* **Retry:** one retry for a timed out warm up, and up to 2 extra measured runs to reach the target count.
* **NPU recovery:** after a SIGKILL the tool kills leftover `gst-launch-1.0` and `run_model` processes and runs `sudo -n systemctl restart dxrt.service`. This is needed because a killed pipeline breaks the `dxrtd` message queue (Error 43: Identifier removed).
* **Circuit breaker:** if a model fully fails, the tool probes the device with `dxcli -s`. A dead device stops the run (power cycle, then `--resume <dir> --retry-failed`). Two fully failed models in a row also stop it.
* **Diagnostics:** on a timeout or runtime error a snapshot goes to `incidents/` (at most 40 per run).

## Output

```text
results/{hw_id}/{run_id}/
├── environment.json            # fingerprint and timing
├── model_results.json          # latency and throughput
├── pipeline_results.json       # E2E single stream
├── multi_stream_results.json   # multi stream search
├── REPORT.md                   # full Markdown report
├── *_results.csv               # CSV copy of the JSON (not in git)
├── raw/                        # raw logs (not in git)
└── incidents/                  # timeout snapshots (not in git)
```

JSON is the source of truth; every command reads it.

## Published results

We measured six environments with SDK 2.5.0. The table shows YOLO26-n single stream E2E FPS and channel capacity at 30 FPS per channel (ORT mode in brackets) on 1920×1080 30 FPS H.264 video. Classification shows single stream FPS only.

| Environment | Host | NPU | PCIe | Detection | Pose | Segmentation | OBB | Classification FPS |
|---|---|---|---|---|---|---|---|---|
| BIOSTAR_H1-Quattro | AMD Ryzen 5 9600X | H1-Quattro card (4 chips) | Gen3 ×4 | 493.6 / 17 (ON) | 554.6 / 20 (OFF) | 359.1 / 11 (ON) | 394.6 / 14 (ON) | 809.7 |
| DX-AIPlayer-N97_M1 | Intel N97 | M1 | Gen3 ×2 | 178.0 / 6 (OFF) | 192.2 / 7 (OFF) | 106.5 / 3 (OFF) | 105.3 / 3 (OFF) | 276.7 |
| OrangePi5+_M1 | Rockchip RK3588 | M1 | Gen3 ×4 | 149.2 / 4 (ON) | 248.0 / 8 (OFF) | 100.8 / 3 (ON) | 104.7 / 3 (OFF) | 1086.4 |
| ROCK5B+_M1 | Rockchip RK3588 | M1 | Gen3 ×2 | 140.7 / 4 (ON) | 227.5 / 8 (OFF) | 87.9 / 2 (ON) | 105.4 / 3 (OFF) | 972.9 |
| RPi5B_M1 | Raspberry Pi 5 | M1 | Gen3 ×1 | 80.0 / 2 (OFF) | 113.5 / 3 (OFF) | 55.5 / 1 (OFF) | 82.7 / 2 (OFF) | 189.7 |
| RPi5B_M1M | Raspberry Pi 5 | M1M | Gen3 ×1 | 79.5 / 2 (OFF) | 112.0 / 3 (OFF) | 54.9 / 1 (OFF) | 74.0 / 2 (OFF) | 192.8 |

Key findings from our analysis:

* **Heavy models (sizes l, x):** inference throughput is the same on every host; the NPU is the bottleneck. Cooling decides sustained E2E FPS.
* **Light models (sizes n, s):** the host (decode, pre and post processing) sets E2E FPS, not the NPU.
* **A hardware video decoder** is the first host requirement. Without one, the Raspberry Pi 5 fits 2 YOLO26-n detection channels, against 4 to 6 on hosts with a decoder and the same M1.
* **Throughput scales with the module:** the H1-Quattro reaches about 4× one M1; the M1M reaches 0.72 to 0.82× of the M1.
* **ORT mode:** both modes give the same detections; choose per host by measurement.

The full analysis, per run reports and dashboard data are in the [dx-all-suite repository](https://github.com/DEEPX-AI/dx-all-suite) under `dx-benchmark/`. The same data feeds DX Benchmark and DX EdgeGuide in [DX AI Studio](../ai-studio/monitor-and-benchmark.md#dx-benchmark).

## Next steps

* [Compare results in DX AI Studio](../ai-studio/monitor-and-benchmark.md#dx-benchmark)
* [Pick hardware with DX EdgeGuide](../ai-studio/edge-guide.md)
* [DX-RT runtime](../runtime/index.md)
