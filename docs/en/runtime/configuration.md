---
title: Configuration
description: How to set inference options, global runtime settings, acceleration, device status and profiling in DX-RT.
---

# Configuration

This page covers the settings you can change in DX-RT: per engine options, global settings, acceleration, device monitoring, profiling and runtime events.

## Inference option

`InferenceOption` sets how one `InferenceEngine` uses the hardware. Pass it when you create the engine.

| Python property | C++ field | Default | Meaning |
|---|---|---|---|
| `devices` | `std::vector<int> devices` | empty (all devices) | Device IDs the engine may use |
| `bound_option` | `uint32_t boundOption` | `NPU_ALL` | NPU cores the engine may use |
| `buffer_count` | `int bufferCount` | `0` (library default, 6) | Inference buffers, and so requests in flight. Valid range 1 to 100 |
| `use_ort` | `bool useORT` | `true` if built with ONNX Runtime | Run CPU tasks with ONNX Runtime |
| `show_model_info` | `bool showModelInfo` | `true` | Print model details when the engine loads. Also needs the global setting |

Python also has `get_` and `set_` methods for each property, such as `set_buffer_count()`.

=== "Python"

    ```python
    from dx_engine import InferenceEngine, InferenceOption

    option = InferenceOption()
    option.devices = [0]
    option.bound_option = InferenceOption.BOUND_OPTION.NPU_0
    option.buffer_count = 10
    option.use_ort = True

    ie = InferenceEngine("model.dxnn", option)
    ```

=== "C++"

    ```cpp
    dxrt::InferenceOption option;
    option.devices = {0};
    option.boundOption = dxrt::InferenceOption::BOUND_OPTION::NPU_0;
    option.bufferCount = 10;
    option.useORT = true;

    dxrt::InferenceEngine ie("model.dxnn", option);
    ```

### Bound option

A DX-M1 has three NPU cores. The bound option ties an engine to some of them.

| Value | Cores |
|---|---|
| `NPU_ALL` (0) | All cores |
| `NPU_0` (1) | Core 0 |
| `NPU_1` (2) | Core 1 |
| `NPU_2` (3) | Core 2 |
| `NPU_01` (4) | Cores 0 and 1 |
| `NPU_12` (5) | Cores 1 and 2 |
| `NPU_02` (6) | Cores 0 and 2 |

Use it to run several models side by side on fixed cores. An engine with `NPU_ALL` waits while other engines hold bindings to cores 0, 1 and 2.

### Buffer count

Each in flight request needs an inference buffer. With more buffers, more async requests run at once, at the cost of host and NPU memory. If the profiler shows long **Buffer Wait** events, raise the buffer count. `dxrun --max-throughput` can find a good value for you. See [dxrun](cli.md#dxrun).

## Global configuration

`Configuration` is a singleton. Its settings apply to the whole process, in C++ and Python alike. Set them before you create engines.

=== "Python"

    ```python
    from dx_engine import Configuration

    config = Configuration()          # wraps the shared C++ instance
    config.set_enable(Configuration.ITEM.PROFILER, True)
    print(config.get_version(), config.get_driver_version(), config.get_pcie_driver_version())
    ```

=== "C++"

    ```cpp
    auto& config = dxrt::Configuration::GetInstance();
    config.SetEnable(dxrt::Configuration::ITEM::PROFILER, true);
    std::cout << config.GetVersion() << " " << config.GetDriverVersion() << "\n";
    for (auto& fw : config.GetFirmwareVersions()) {
        std::cout << "device " << fw.first << " firmware " << fw.second << "\n";
    }
    ```

In C++, always use `GetInstance()`. Only C++ has `GetFirmwareVersions()` and `GetONNXRuntimeVersion()`.

### Items

Turn features on and off with `SetEnable(ITEM, bool)` or `set_enable()`.

| Item | What it turns on |
|---|---|
| `DEBUG` | Debug mode |
| `PROFILER` | The profiler |
| `SERVICE` | Use of the `dxrtd` service |
| `DYNAMIC_CPU_THREAD` | Dynamic ONNX Runtime thread count |
| `TASK_FLOW` | Task flow output |
| `SHOW_THROTTLING` | Throttling messages |
| `SHOW_PROFILE` | Profile results output |
| `SHOW_MODEL_INFO` | Model details when an engine loads |
| `CUSTOM_INTRA_OP_THREADS` | A custom ONNX Runtime intra op thread count |
| `CUSTOM_INTER_OP_THREADS` | A custom ONNX Runtime inter op thread count |
| `NFH_ASYNC` | Asynchronous NPU format handling. On by default |
| `NFH_ACCELERATION` | SIMD acceleration of format conversion. Exists only in builds with it |
| `CPU_OP_ACCELERATION` | Faster ONNX Runtime execution providers. Exists only in builds with it |

### Attributes

Attributes are string values that belong to an item. Set them with `SetAttribute(ITEM, ATTRIBUTE, value)`.

| Attribute | Item | Value |
|---|---|---|
| `PROFILER_SHOW_DATA` | `PROFILER` | `"ON"` prints profiler data |
| `PROFILER_SAVE_DATA` | `PROFILER` | `"ON"` saves `profiler.json` in the working directory when the program exits |
| `CUSTOM_INTRA_OP_THREADS_NUM` | `CUSTOM_INTRA_OP_THREADS` | Thread count, 1 to the number of hardware threads |
| `CUSTOM_INTER_OP_THREADS_NUM` | `CUSTOM_INTER_OP_THREADS` | Thread count, 1 to the number of hardware threads |

Other methods: `GetEnable`, `GetAttribute`, `GetIntAttribute`, `LockEnable` (C++ only) and `SetFWConfigWithJson(file)` (`set_fw_config_with_json` in Python).

### Configuration file

You can load settings from a `KEY=VALUE` file with `LoadConfigFile(path)` (`load_config_file` in Python). The keys and the defaults DX-RT ships with:

```text
DEBUG_DXRT=0
SHOW_TASK_FLOW=0
USE_PROFILER=0
SHOW_PROFILER_DATA=0
SAVE_PROFILER_DATA=0
DXRT_DYNAMIC_CPU_THREAD=0
USE_CUSTOM_INTRA_OP_THREADS=0
USE_CUSTOM_INTER_OP_THREADS=0
CUSTOM_INTRA_OP_THREADS_COUNT=0
CUSTOM_INTER_OP_THREADS_COUNT=0
DXRT_NFH_ACCELERATION=0
DXRT_CPU_OP_ACCELERATION=0
```

Each key is 0 (off) or 1 (on), except the thread counts.

* A key takes effect only if it is in the file. A missing key keeps the compiled default.
* You can also add `USE_SERVICE=0` or `USE_SERVICE=1`. It applies only to builds with service support.
* Thread counts are clamped to 1 to the number of hardware threads. A value that is not a number becomes 1. An empty value (`KEY=`) is ignored.
* The acceleration keys apply only to builds with acceleration.

ONNX Runtime threads by default: intra op uses an automatic count, and inter op runs sequentially with 1 thread. Set the `USE_CUSTOM_*` key to 1 to use your counts.

`SHOW_MODEL_INFO` has no file key. Its default comes from the `ENABLE_SHOW_MODEL_INFO` build option, which is off. Set it with `SetEnable` before you create the engine. `InferenceOption.showModelInfo` must also be true.

## Speed up CPU side work

When the host CPU is the bottleneck, try these options. Use the [profiler](#profiler) first to see where time goes. None of them helps when NPU compute dominates.

### Dynamic CPU threads

Set this environment variable to let DX-RT add ONNX Runtime threads when its CPU task queue backs up:

```bash
export DXRT_DYNAMIC_CPU_THREAD=ON
```

When DX-RT sees a high CPU task load, it prints this hint:

```text
To improve FPS, set: 'export DXRT_DYNAMIC_CPU_THREAD=ON'
```

It does not raise FPS in every case. The effect depends on the workload, the input size and the CPU.

### Acceleration

DX-RT can use platform libraries for two CPU side jobs:

* **Format conversion (NFH)**: padding and layout conversion of input and output tensors. NFH stands for NPU Format Handler.
* **CPU ops**: ONNX Runtime CPU tasks run on a tuned execution provider.

| Target | x86_64 | aarch64 |
|---|---|---|
| Format conversion | Intel IPP | ARM NEON |
| CPU ops | OpenVINO EP | XNNPACK EP |

Acceleration works on x86_64 with Ubuntu 22.04 to 24.04 and on aarch64 with Ubuntu 20.04 to 24.04. Windows support is planned. CPU op acceleration helps compute heavy ops such as Conv and MatMul. It does little for Reshape, Transpose or Concat.

To use it:

1. Set `USE_NPU_FORMAT_CONVERSION_ACCELERATION` and `USE_CPU_OP_ACCELERATION` to `ON` in `cmake/dxrt.cfg.cmake`. Both are off by default.
1. Do a clean build with `./build.sh --clean`. The build downloads the libraries, so it needs internet access. If a library is not available, its option is turned off. See [Build from source](build-from-source.md).
1. Turn it on at run time. It is off by default even in an accelerated build.

=== "Python"

    ```python
    config = Configuration()
    config.set_enable(Configuration.ITEM.NFH_ACCELERATION, True)
    config.set_enable(Configuration.ITEM.CPU_OP_ACCELERATION, True)
    ```

=== "C++"

    ```cpp
    auto& config = dxrt::Configuration::GetInstance();
    config.SetEnable(dxrt::Configuration::ITEM::NFH_ACCELERATION, true);
    config.SetEnable(dxrt::Configuration::ITEM::CPU_OP_ACCELERATION, true);
    ```

To try it without code changes, run `dxrun -m model.dxnn --accel-nfh --accel-cpu`.

!!! warning "Acceleration items exist only in accelerated builds"
    In a default build, `NFH_ACCELERATION`, `CPU_OP_ACCELERATION`, `--accel-nfh` and `--accel-cpu` do not exist. C++ code that uses them does not compile, and `dxrun` reports an unrecognized argument.

Reference results in FPS, measured with `dxrun` on an Orange Pi 5 Plus (aarch64, Ubuntu 22.04) with a DX-M1 on PCIe Gen3 x4, DX-RT 3.3.0, `USE_ORT=ON`, 2000 iterations and Q-PRO models from DX-ModelZoo:

| Model | Baseline | Format conversion | CPU ops | Both |
|---|---|---|---|---|
| YoloV8S | 84 | 86 | 128 | 131 |
| YoloV10S | 68 | 68 | 96 | 98 |
| YoloXS | 250 | 288 | 258 | 288 |
| YoloV11S | 82 | 82 | 127 | 131 |

Your results depend on the device, the input size, the system load and your pre and post processing.

## Device status

`DeviceStatus` gives a snapshot of one device. The data refreshes about once a second, so polling faster returns the same values.

=== "Python"

    ```python
    from dx_engine import DeviceStatus

    for dev_id in range(DeviceStatus.get_device_count()):
        s = DeviceStatus.get_current_status(dev_id)
        if not s.is_valid():
            continue
        for ch in range(3):
            print(dev_id, ch, s.get_temperature(ch), s.get_npu_voltage(ch),
                  s.get_npu_clock(ch), s.get_core_utilization(ch))
        print(s.get_memory_used(), s.get_memory_free())
    ```

=== "C++"

    ```cpp
    for (int id = 0; id < dxrt::DeviceStatus::GetDeviceCount(); ++id) {
        auto s = dxrt::DeviceStatus::GetCurrentStatus(id);
        if (!s.IsValid()) continue;
        std::cout << s.GetInfoString() << "\n" << s.GetStatusString() << "\n";
    }
    ```

| Metric | Python | C++ | Unit |
|---|---|---|---|
| Device ID | `get_id()` | `GetId()` | |
| Temperature | `get_temperature(ch)` | `GetTemperature(ch)` | °C |
| NPU voltage | `get_npu_voltage(ch)` | `GetNpuVoltage(ch)` | mV |
| NPU clock | `get_npu_clock(ch)` | `GetNpuClock(ch)` | MHz |
| Core utilization | `get_core_utilization(core)` | `GetCoreUtilization(core)` | % (0 to 100) |
| Memory used | `get_memory_used()` | `GetMemoryUsed()` | bytes |
| Memory free | `get_memory_free()` | `GetMemoryFree()` | bytes |
| Valid data | `is_valid()` | `IsValid()` | |

In C++, `GetInfoString()` prints the same as `dxcli -i`, and `GetStatusString()` the same as `dxcli -s`. C++ has more getters, listed in the [C++ API](cpp-api.md#devicestatus). In Python, `get_current_status()` does not raise. Check `is_valid()`.

## Profiler

The profiler records a timeline of each inference. Turn it on in one of three ways:

* Run `dxrun -m model.dxnn --profiler`. It writes `profiler.json` in the working directory.
* Set `USE_PROFILER=1` and `SAVE_PROFILER_DATA=1` in a configuration file.
* Turn it on in code:

=== "Python"

    ```python
    config = Configuration()
    config.set_enable(Configuration.ITEM.PROFILER, True)
    config.set_attribute(Configuration.ITEM.PROFILER,
                         Configuration.ATTRIBUTE.PROFILER_SAVE_DATA, "ON")
    ```

=== "C++"

    ```cpp
    auto& config = dxrt::Configuration::GetInstance();
    config.SetEnable(dxrt::Configuration::ITEM::PROFILER, true);
    config.SetAttribute(dxrt::Configuration::ITEM::PROFILER,
                        dxrt::Configuration::ATTRIBUTE::PROFILER_SAVE_DATA, "ON");
    ```

### Per job metrics

Call `GetJobMetrics(jobId)` right after `Wait()` returns to get a timing breakdown of that job.

=== "Python"

    ```python
    from dx_engine import Profiler

    profiler = Profiler.get_instance()
    job_id = ie.run_async([input_array])
    outputs = ie.wait(job_id)

    jm = profiler.get_job_metrics(job_id)
    if jm.valid:
        npu = jm.get_task("npu_0")
        if npu.valid:
            dev = npu.devices[0]
            print(dev.h2d_us, dev.inference_core_all_us, dev.d2h_us, dev.total_us)
    ```

=== "C++"

    ```cpp
    auto& profiler = dxrt::Profiler::GetInstance();
    int jobId = ie.RunAsync(input.data());
    auto outputs = ie.Wait(jobId);

    auto jm = profiler.GetJobMetrics(jobId);
    if (jm.valid) {
        auto npu = jm.GetTask("npu_0");
        if (npu.valid) {
            auto& dev = npu.devices[0];
            std::cout << dev.h2d_us << " " << dev.inference_core_all_us << "\n";
        }
        auto cpu = jm.GetTask("cpu_0");       // CPU task, when ONNX Runtime is used
        if (cpu.valid) std::cout << cpu.cpu_task_us << "\n";
    }
    ```

A job has one `TaskMetrics` per task (`task_name`, `devices`, `cpu_task_us`, `valid`). NPU tasks have per device `NpuDeviceMetrics`, all in microseconds:

| Field | Meaning |
|---|---|
| `input_format_us` | Input format conversion |
| `h2d_us` | Host to device PCIe transfer |
| `inference_core_all_us` | NPU compute, all cores |
| `inference_core_0_us`, `_1_us`, `_2_us` | NPU compute per core |
| `d2h_us` | Device to host PCIe transfer |
| `output_format_us` | Output format conversion |
| `total_us` | The whole NPU task |

`GetPerformanceData()` and `GetPerformanceDataByDevice()` are deprecated. Use `GetJobMetrics()`.

You can add your own events to the timeline with `Start(name)` and `End(name)` (`start` and `end` in Python). Other methods are `Show`, `Save(file)`, `Clear` and `UserClear`.

### Profiler events

| Event | What it is | If it is the bottleneck |
|---|---|---|
| Buffer Wait | Waiting for a free inference buffer | Set `DXRT_DYNAMIC_CPU_THREAD=ON` or raise the buffer count |
| NPU Input Format Handler | Padding and layout conversion of the input | Turn on format conversion acceleration |
| PCIe Write | Input transfer to the NPU | |
| NPU Core | NPU compute | |
| PCIe Read | Output transfer from the NPU | |
| NPU Output Format Handler | Padding removal and layout conversion of the output | Turn on format conversion acceleration |
| CPU Task Queue Wait | Waiting in the CPU task queue | Turn on CPU op acceleration |
| cpu_N | CPU op execution on thread N | Turn on CPU op acceleration |

The NPU task time is the sum of the input format, PCIe write, NPU core, PCIe read and output format events.

### Plot the timeline

Install the plot dependencies, then draw `profiler.json`:

```bash
pip install -r tool/profiler/requirements.txt
pip install matplotlib
python3 tool/profiler/plot.py -i profiler.json
python3 tool/profiler/plot_html.py -i profiler.json -o result.html
```

`plot.py` writes PNG timelines, one per device (such as `profiler_Device_0.png`), and splits them into parts when there are more jobs than the limit. `plot_html.py` writes one interactive HTML file and needs `pandas` and `plotly`.

| `plot.py` option | Meaning |
|---|---|
| `-i, --input` | Input `.json` file |
| `-o, --output` | Output base file name. Default `profiler.png` |
| `-s, --start` | Start of the time window, as a ratio from 0.0 to 1.0 |
| `-e, --end` | End of the time window, as a ratio from 0.0 to 1.0 |
| `-j, --jobs-per-image` | Jobs per image before a split. Default 200 |
| `-t, --show_text` | Show durations on the bars |
| `-a, --auto-select` | Pick 200 jobs from the stable middle of the run |

`plot_html.py` takes `-i, --input` (required) and `-o, --output` (default: the input name with `.html`).

## Runtime events

`RuntimeEventDispatcher` reports device errors, warnings and other runtime events to your handler. Only one handler is active. Registering a new one replaces the old one.

=== "Python"

    ```python
    from dx_engine import RuntimeEventDispatcher

    d = RuntimeEventDispatcher()

    def on_event(level, type, code, message, timestamp):
        print(timestamp, level, type, code, message)

    d.register_event_handler(on_event)
    d.set_current_level(RuntimeEventDispatcher.LEVEL.WARNING)
    ```

=== "C++"

    ```cpp
    auto& d = dxrt::RuntimeEventDispatcher::GetInstance();
    d.RegisterEventHandler([](dxrt::RuntimeEventDispatcher::LEVEL level,
                              dxrt::RuntimeEventDispatcher::TYPE type,
                              dxrt::RuntimeEventDispatcher::CODE code,
                              const std::string& message,
                              const std::string& timestamp) {
        std::cout << timestamp << " " << message << "\n";
    });
    d.SetCurrentLevel(dxrt::RuntimeEventDispatcher::LEVEL::WARNING);
    ```

| Enum | Values |
|---|---|
| `LEVEL` | `INFO` (1), `WARNING` (2), `ERROR` (3), `CRITICAL` (4) |
| `TYPE` | `DEVICE_CORE` (1000), `DEVICE_STATUS` (1001), `DEVICE_IO` (1002), `DEVICE_MEMORY` (1003), `UNKNOWN` (1004) |
| `CODE` | `WRITE_INPUT` (2000), `READ_OUTPUT` (2001), `MEMORY_OVERFLOW` (2002), `MEMORY_ALLOCATION` (2003), `DEVICE_EVENT` (2004), `RECOVERY_OCCURRED` (2005), `TIMEOUT_OCCURRED` (2006), `THROTTLING_NOTICE` (2007), `THROTTLING_EMERGENCY` (2008), `UNKNOWN` (2009) |

You can also send your own events with `DispatchEvent(level, type, code, message)` (`dispatch_event` in Python).

## Next steps

* [Command line tools](cli.md)
* [DX-Fit](dx-fit.md)
* [Python API](python-api.md)
* [C++ API](cpp-api.md)
