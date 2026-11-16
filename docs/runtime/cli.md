---
title: Command line tools
description: Reference for the DX-RT command line tools dxparse, dxrun, dxcli, dxtop and dxbenchmark.
---

# Command line tools

DX-RT ships five command line tools to inspect models, test inference, benchmark and manage devices.

| Tool | Use it to |
|---|---|
| [`dxparse`](#dxparse) | Show the structure, tensors and metadata of a `.dxnn` model |
| [`dxrun`](#dxrun) | Run a model, measure FPS and latency, and tune the buffer count |
| [`dxcli`](#dxcli) | Show device status and info, reset devices, update firmware |
| [`dxtop`](#dxtop) | Watch NPU use, temperature, voltage and clock live |
| [`dxbenchmark`](#dxbenchmark) | Benchmark every model in a folder and make an HTML report |

The build puts the tools in `bin/` of the DX-RT build, and the install puts them on your `PATH`. The old names still work as aliases:

| Name | Old alias |
|---|---|
| `dxparse` | `parse_model` |
| `dxrun` | `run_model` |
| `dxcli` | `dxrt-cli` |

## dxparse

`dxparse` reads a compiled model and prints its structure, input and output tensors and metadata.

```bash
dxparse -m model.dxnn
```

| Option | Meaning |
|---|---|
| `-m, --model FILE` | Model path. Required |
| `-v, --verbose` | Show task dependencies and memory use |
| `-o, --output FILE` | Save the console output to a file, without color codes |
| `-j, --json` | Extract the JSON data in the model (`graph_info`, `rmap_info`) to files |
| `-h, --help` | Show help |

## dxrun

`dxrun` runs a model to check that it works and to measure performance.

```bash
dxrun -m <model.dxnn> [-l <loops>] [-t <seconds>] [-d <devices>] [--use-ort] [--profiler] [--buffer-count <N>]
dxrun -m <model.dxnn> --max-throughput [--buffer-count <low>-<high>] [--probe-time <s>] [--sweep-tolerance <%>] [--cool-down-temp <°C>] [-l <loops> | -t <seconds>]
```

| Option | Default | Meaning |
|---|---|---|
| `-m, --model` | | Model file (`.dxnn`) |
| `-b, --benchmark` | on | Benchmark at a fixed buffer count. This is the mode when you give none of `--single`, `--fps` or `--max-throughput` |
| `-s, --single` | | Single run test: one input at a time, on one core |
| `-v, --verbose` | | Also print NPU processing time, queue wait time, E2E response time and latency |
| `-n, --npu` | 0 | NPU binding: 0 `NPU_ALL`, 1 `NPU_0`, 2 `NPU_1`, 3 `NPU_2`, 4 `NPU_0/1`, 5 `NPU_1/2`, 6 `NPU_0/2` |
| `-l, --loops` | 30 | Number of inferences |
| `-t, --time` | 0 | Run time in seconds. Overrides `--loops` in benchmark and target FPS modes |
| `-w, --warmup-runs` | 0 | Warmup runs before measuring |
| `-d, --devices` | `all` | Devices: `all`, `0`, `0,1,2` or `count:N` (the first N devices) |
| `-f, --fps` | 0 | Target FPS. A value above 0 turns on target FPS mode, unless `--single` is set |
| `--use-ort` | off | Run CPU tasks with ONNX Runtime. Without it, only NPU tasks run. Only in builds with ONNX Runtime |
| `--profiler` | off | Turn on the profiler and write `profiler.json` |
| `--accel-nfh` | off | Turn on format conversion acceleration. Only in accelerated builds |
| `--accel-cpu` | off | Turn on CPU op acceleration (OpenVINO or XNNPACK). Only in accelerated builds |
| `--buffer-count` | 6 | Buffer count from 1 to 100, or a range such as `3-16` with `--max-throughput` (range default `3-100`) |
| `--max-throughput` | | Search buffer counts for peak throughput and recommend one |
| `--probe-time` | 2.0 | Seconds to measure each buffer count in the search |
| `--sweep-tolerance` | 1.0 | FPS difference in % treated as noise |
| `--cool-down-temp` | 45 | Wait until the NPU is below this temperature in °C before each search measurement |
| `-h, --help` | | Show help |

### Examples

```bash
dxrun -m model.dxnn -l 100                                   # 100 inferences
dxrun -m model.dxnn --buffer-count 8 -l 100                  # fixed buffer count
dxrun -m model.dxnn --profiler --buffer-count 10 -l 200 -v   # profile with metrics
dxrun -m model.dxnn --benchmark --profiler -t 60             # 60 s benchmark with profiling
```

### Find the best buffer count

By default, `dxrun` holds the buffer count at one value for the whole run. `--max-throughput` searches for the best value instead.

```bash
dxrun -m model.dxnn --max-throughput                                     # search 3 to 100
dxrun -m model.dxnn --max-throughput --buffer-count 3-16 --probe-time 3  # measure every value from 3 to 16
dxrun -m model.dxnn --max-throughput --cool-down-temp 50                 # cool down before each measurement
dxrun -m model.dxnn --max-throughput -t 30                               # then benchmark at the result
```

How the search works:

* It measures each buffer count 3 times for `--probe-time` seconds, each time with a new engine, and averages the FPS.
* Without a range, it starts at 3 and stops at 100, or earlier when FPS stays 3% or more below the peak for 2 rounds in a row, or does not improve by more than `--sweep-tolerance` for 3 rounds in a row. With a range, it measures every value.
* It recommends the smallest buffer count whose FPS is within `--sweep-tolerance` of the peak.
* Before each measurement, it reads the highest NPU temperature once a second and waits until it is below `--cool-down-temp`. It logs each wait as `[INFO] NPU temperature ...`. If the NPU does not cool down within 300 seconds, the search fails.
* Without `-l` or `-t`, it only prints the recommendation.

A range is valid only with `--max-throughput`, and `--max-throughput` needs a range or none. `--max-throughput` does not work with `--single` or `--fps`. `--cool-down-temp` works only with `--max-throughput`.

!!! warning "Memory overflow at high buffer counts"
    A critical runtime event during the search stops it without a recommendation. An NPU memory overflow ends `dxrun` at once. If it happens at large buffer counts, lower the upper bound with `--buffer-count <low>-<high>`.

### Output

By default, `dxrun` prints only the FPS. With `-v` it prints averages over all completed inputs, or the last input with `--single`:

```text
=====================================================================================================================================
* Benchmark Result (100 inputs)
  - NPU Processing Time Average : 2.841 ms   (Actual NPU core computation time for a single request)
  - Queue Wait Time Average     : 6.512 ms   (Time spent waiting in NPU/CPU task queues; included in E2E Response Time)
  - E2E Response Time Average   : 11.204 ms  (End-to-end time per request including data transfer and overheads)
  - Latency Average             : 4.180 ms   (Core latency per request excluding buffer pool and queue wait times)
  - FPS                         : 351.27     (Overall user-observed inference throughput (inputs/second), reflecting perceived speed)
=====================================================================================================================================
```

| Metric | Meaning | API |
|---|---|---|
| NPU Processing Time | NPU core compute time per request, summed over NPU tasks | `GetNpuInferenceTime*()` |
| Queue Wait Time | Time in the NPU and CPU task queues. Part of the E2E response time | `GetQueueWaitTime*()` |
| E2E Response Time | From request start to the end of all tasks, with waits and transfers | `GetE2EResponseTime*()`, same as `GetLatency*()` |
| Latency | Core latency: E2E response time without the buffer pool wait and the queue wait | `GetCoreLatency*()` |
| FPS | Completed inputs per second of wall clock time | |

In benchmark mode the queue stays full, so queue wait and E2E response time grow with `--buffer-count`. Latency shows the per request processing time.

### Validation messages and exit codes

`dxrun` checks values before it starts:

| Condition | Message |
|---|---|
| `--loops` below 1 | `[ERR] --loops must be >= 1.` |
| `--time` negative | `[ERR] --time must be >= 0 (seconds).` |
| `--buffer-count` outside 1 to 100 | `Please check --buffer-count option value. Must be between 1 and 100` |
| Range not `1 <= low <= high <= 100` | `[ERR] --buffer-count range must satisfy 1 <= low <= high <= 100 (got ...).` |
| Range without `--max-throughput` | `[ERR] --buffer-count range (e.g. 3-16) is only valid together with --max-throughput.` |
| `--max-throughput` with a single value | `[ERR] --max-throughput requires a buffer-count RANGE (e.g. 3-16), not a single value.` |
| `--max-throughput` with `--single` or `--fps` | `[ERR] --max-throughput cannot be combined with --single or --fps.` |
| `--probe-time` below 0.1 | `[ERR] --probe-time must be >= 0.1 (seconds).` |
| `--sweep-tolerance` not in 0 to under 100 | `[ERR] --sweep-tolerance must be >= 0 and < 100 (%).` |
| `--cool-down-temp` without `--max-throughput` | `[ERR] --cool-down-temp is only valid together with --max-throughput.` |
| `--cool-down-temp` not in 1 to 125 | `[ERR] --cool-down-temp must be > 0 and <= 125 ('C).` |

| Exit code | Meaning |
|---|---|
| `0` | Inference completed |
| `1` | Bad or missing arguments |
| `-1` (`255` on Linux) | Inference failed, a critical runtime event occurred, no inference completed, or the search gave no recommendation |

Check the exit code when you run `dxrun` from a script.

## dxcli

`dxcli` talks to the device. Use it for status, info, reset and firmware updates. It works only with accelerator (PCIe) devices.

```bash
dxcli <option> <argument>
```

| Option | Meaning |
|---|---|
| `-s, --status` | Show device status |
| `-i, --info` | Show device info |
| `-m, --monitor N` | Show status every N seconds (N > 0) |
| `-r, --reset[=N]` | Reset the device. `0` (default) resets only the NPU |
| `-d, --device ID` | Device to send the command to. Default `-1`, all devices |
| `-u, --fwupdate FILE [force] [unreset]` | Update the firmware. `force` updates even to an equal or older version. `unreset` skips the reset after the update |
| `-g, --fwversion FILE` | Show the firmware version in a firmware file |
| `-C, --fwconfig_json FILE` | Update firmware settings from a JSON file |
| `--fan-ctrl MODE` | Cooling fan: `on` (forced on), `off` (forced off) or `auto` (controlled by temperature) |
| `-v, --version` | Show the minimum versions this runtime needs |
| `-h, --help` | Show help |

```bash
dxcli -s
dxcli -r
dxcli --reset=1
dxcli -u fw.bin
dxcli -m 1
dxcli --fan-ctrl auto
```

The first line of every `dxcli` command shows the installed DX-RT version. With `-v`, the rest shows the minimum versions this build needs, not the installed ones:

```text
DXRT v<version> (build: <build id>)
Minimum Driver Versions
  Device Driver: v<version>
  PCIe Driver: v<version>
  Firmware: v<version>
Minimum Compiler Versions
  Compiler: v<version>
  .dxnn File Format: v<version>
```

For the firmware update steps, see [NPU driver and firmware](driver-firmware.md#update-the-firmware).

## dxtop

`dxtop` shows the live state of every NPU, like `top`. It also works without the `dxrtd` service. Then it reads data straight from the shared memory of the runtime process and retries until a runtime process is running.

```bash
dxtop
```

The header shows the DX-RT, NPU driver and `dxtop` versions. Each device shows:

| Field | Meaning |
|---|---|
| Device ID | Device number, such as `Device :0` |
| Variant | Chip variant, such as `M1` or `M1M`. A trailing `M` means LPDDR4 memory |
| PCIe bus number | PCIe location, such as `02:00:00` |
| Firmware | Firmware version on the device |
| NPU memory | Used MiB, total GiB and use in % |

For each core it shows `Util` (% busy), `Temp` (°C), `Voltage` (mV) and `Clock` (MHz).

| Key | Action |
|---|---|
| `q` | Quit |
| `n` | Next page of devices |
| `p` | Previous page |
| `h` | Help |

## dxbenchmark

`dxbenchmark` runs every model in a folder and writes an HTML report with FPS, latency and stability charts, plus raw data files.

```bash
dxbenchmark --dir models/ -t 60
dxbenchmark --dir models/ --recursive --sort latency --order desc -d 0,1
```

| Option | Default | Meaning |
|---|---|---|
| `--dir` | | Folder with the models. Required |
| `--result-path` | `.` | Where to write the results |
| `--sort` | `name` | Sort by `name`, `fps`, `time` (NPU inference time) or `latency` |
| `--order` | `asc` | `asc` or `desc` |
| `-l, --loops` | 0 | Inferences per model |
| `-t, --time` | 0 | Seconds per model. Takes priority over `-l` |
| `--warmup` | 10 | Warmup time |
| `-n, --npu` | 0 | NPU binding, as in `dxrun` |
| `-d, --devices` | `all` | Devices, as in `dxrun` |
| `--only-data` | | Write only the CSV and JSON data |
| `--recursive` | | Also search subfolders |
| `--use-ort` | | Run CPU tasks with ONNX Runtime |
| `-v, --verbose` | | Show NPU processing time and latency |
| `-h, --help` | | Show help |

Give `--dir` and either `-t` or `-l`. Time based runs suit benchmarks, but very different inference times between models can skew the charts.

Output files:

* `DXBENCHMARK_<YYYY_MM_DD_HHMMSS>.html`: the report.
* `rt_<runtime>_dd_<device driver>_pd_<PCIe driver>.json` and `.csv`: raw data tagged with the versions, such as `rt_3.5.0_dd_2.7.0_pd_2.7.0.json`. Use them to compare versions.

## dxrtd on Windows

On Windows, `dxrtd` runs as a Windows service. It takes `--install` (`-i`), `--uninstall` (`-u`), `--start` and `--stop`. The service manager starts it with `--run` (`-r`). See [Install](../get-started/install.md) for the Windows setup.

## Next steps

* [Run inference](run-inference.md)
* [Configuration](configuration.md)
* [NPU driver and firmware](driver-firmware.md)
* [Troubleshooting](troubleshooting.md)
