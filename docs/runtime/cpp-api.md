---
title: C++ API
description: Reference for the DX-RT C++ API in the dxrt_cxx_api.h header, with every public class and method.
---

# C++ API

This page lists the public C++ API of DX-RT 3.5.0. Everything is in the `dxrt` namespace.

## Before you start

* Install DX-RT. See [Install](../get-started/install.md).
* For worked examples, see [Run inference](run-inference.md) and [DX-RT examples](tutorials.md).

## Headers and linking

Include one header:

```cpp
#include <dxrt/dxrt_cxx_api.h>
```

`dxrt_cxx_api.h` is a C++14 header only wrapper over the stable C ABI in `dxrt_c_api.h`. `libdxrt` exports only `dxrt_*` C symbols, so you can update the library without rebuilding against new C++ internals.

The older header `<dxrt/dxrt_api.h>` still works but prints a note at compile time. Define `DXRT_LEGACY_HEADER_OK` to hide the note.

!!! warning "Use one header per source file"
    Do not include `dxrt_api.h` and `dxrt_cxx_api.h` in the same translation unit.

Link with CMake:

```cmake
cmake_minimum_required(VERSION 3.14)
project(my_app CXX)
set(CMAKE_CXX_STANDARD 14)

find_package(dxrt REQUIRED)
add_executable(my_app main.cpp)
target_link_libraries(my_app PRIVATE dxrt::dxrt)
```

The package files install to `lib/cmake/dxrt` under the install prefix. If DX-RT is not in a standard location, pass `-DCMAKE_PREFIX_PATH=<prefix>` to CMake.

## InferenceEngine

```cpp
explicit InferenceEngine(const std::string& modelPath,
                         InferenceOption& option = detail::default_option());
InferenceEngine(const uint8_t* data, size_t size,
                InferenceOption& option = detail::default_option());
```

The second form loads a model from memory. You cannot copy or move an engine. Hold it in `std::unique_ptr` to pass it around. Call `Dispose()` to release it early.

### Run methods

| Method | Meaning |
|---|---|
| `TensorPtrs Run(void* input, void* userArg = nullptr, void* output = nullptr)` | Synchronous inference |
| `std::vector<TensorPtrs> Run(const std::vector<void*>& inputBuffers, const std::vector<void*>& outputBuffers, const std::vector<void*>& userArgs = {})` | Batch inference. `outputBuffers` must match `inputBuffers` in size. A `nullptr` element lets the engine allocate |
| `RunMultiInput(const std::map<std::string, void*>&, void* userArg = nullptr, void* output = nullptr)` | Multi input by name |
| `RunMultiInput(const std::vector<void*>&, void* userArg = nullptr, void* output = nullptr)` | Multi input in `GetInputTensorNames()` order |
| `int RunAsync(void* input, void* userArg = nullptr, void* output = nullptr)` | Async inference. Returns a job ID |
| `int RunAsync(const std::vector<void*>&, void* userArg = nullptr, void* output = nullptr)` | Async multi input. A vector that does not match the input count uses only its first element |
| `RunAsyncMultiInput(map or vector, void* userArg = nullptr, void* output = nullptr)` | Async multi input. Throws for a single input model |
| `TensorPtrs Wait(int jobId) const` | Wait for a job and get its outputs |
| `TensorPtrs Wait(int jobId, void* output) const` | Wait and copy the outputs into your buffer |
| `void RegisterCallback(std::function<int(TensorPtrs&, void*)> cb)` | Called when each async job finishes |
| `float RunBenchmark(int num, void* inputPtr = nullptr)` | Built in benchmark. Returns FPS |
| `ValidateDevice(void* input, int deviceId = 0)` | Device check with a model compiled in debug mode. Also takes a vector |
| `ValidateDeviceMultiInput(map or vector, int deviceId = 0)` | The same for multi input models |
| `void RegisterUserInputReleaseCallback(std::function<void(void* userArg, int jobId)>)` | Called when the runtime no longer needs an input buffer. Internal: built only with `USE_VNPU` |

### Model and tensor info

| Method | Returns |
|---|---|
| `GetInputSize()`, `GetOutputSize()` | Total input or output size in bytes |
| `GetInputTensorSizes()`, `GetOutputTensorSizes()` | Size of each tensor |
| `GetInputTensorCount()` | Number of inputs |
| `GetInputTensorNames()`, `GetOutputTensorNames()` | Tensor names in order |
| `GetInputTensorToTaskMapping()` | Map from input name to task name |
| `GetOutputTensorOffset(name)` | Byte offset of an output in the output buffer |
| `GetInputs(int devId)`, `GetInputs(void* ptr = nullptr, uint64_t phyAddr = 0)` | Input tensor descriptions |
| `GetOutputs(void* ptr = nullptr, uint64_t phyAddr = 0)` | Output tensor descriptions |
| `GetAllTaskOutputs()` | Outputs of every task of the last run |
| `HasDynamicOutput()` | `true` if an output shape is known only after inference |
| `IsMultiInputModel()` | `true` for more than one input |
| `GetModelName()`, `GetModelVersion()`, `GetCompileType()` | Model name, file format version, compile type |
| `GetTaskOrder()`, `GetNumTailTasks()` | Task order and number of tail tasks |
| `IsOrtConfigured()`, `IsPPU()` | ONNX Runtime in use, post processing unit in use |
| `GetBitmatchMask(int index = 0)` | Bit match mask |
| `handle()` | The C API engine handle |

### Timing

All values are in microseconds. Each base method has `Cnt`, `Mean`, `StdDev` and `Vector` variants, such as `GetCoreLatencyMean()`.

| Base method | Meaning |
|---|---|
| `int GetLatency()` | Same as E2E response time since 3.5.0 |
| `int GetE2EResponseTime()` | Request to result, with buffer and queue waits |
| `int GetCoreLatency()` | Without buffer pool and queue waits |
| `uint32_t GetNpuInferenceTime()` | Time on the NPU |
| `int64_t GetQueueWaitTime()` | Time in the NPU and CPU task queues. Never negative |

## InferenceOption

```cpp
class InferenceOption {
public:
    enum BOUND_OPTION { NPU_ALL = 0, NPU_0, NPU_1, NPU_2, NPU_01, NPU_12, NPU_02 };
    int bufferCount = 0;                 // 0 means the library default (6). Range 1 to 100
    uint32_t boundOption = NPU_ALL;
    std::vector<int> devices;            // empty means all devices
    bool useORT;                         // true if built with ONNX Runtime
    bool showModelInfo = true;
};
```

See [Configuration](configuration.md#inference-option).

## Tensor

`TensorPtr` is `std::shared_ptr<Tensor>` and `TensorPtrs` is `std::vector<TensorPtr>`.

| Method | Returns |
|---|---|
| `name()` | Tensor name |
| `type()` | `DataType` |
| `shape()` | `std::vector<int64_t>` |
| `data()` | Pointer to the data |
| `data(h, w, c)` | Pointer to one element |
| `elem_size()` | Bytes per element |
| `size_in_bytes()` | Total size |
| `phy_addr()` | Physical address on the device |

The constructor is `Tensor(std::string name, std::vector<int64_t> shape, int type, void* data = nullptr, int memory_type = 1)`.

`DataType` values: `NONE_TYPE` (0), `FLOAT`, `UINT8`, `INT8`, `UINT16`, `INT16`, `INT32`, `INT64`, `UINT32`, `UINT64`, `BBOX`, `FACE`, `POSE`, `MAX_TYPE`. `DataTypeToString(type)` gives the name.

## Configuration

`static Configuration& GetInstance()` returns the only instance.

| Method | Meaning |
|---|---|
| `SetEnable(ITEM, bool)`, `GetEnable(ITEM)` | Turn an item on or off |
| `LockEnable(ITEM)` | Make an item read only |
| `SetAttribute(ITEM, ATTRIBUTE, const std::string&)`, `GetAttribute(ITEM, ATTRIBUTE)`, `GetIntAttribute(ITEM, ATTRIBUTE)` | String attributes |
| `LoadConfigFile(const std::string&)` | Load a `KEY=VALUE` file |
| `SetFWConfigWithJson(const std::string& json_file)` | Apply firmware settings from JSON |
| `GetVersion()` | DX-RT version |
| `GetDriverVersion()`, `GetPCIeDriverVersion()` | NPU driver versions |
| `GetFirmwareVersions()` | `std::vector<std::pair<int, std::string>>`: device ID and firmware version |
| `GetONNXRuntimeVersion()` | ONNX Runtime version |

`ITEM` values: `DEBUG` (1), `PROFILER`, `SERVICE`, `DYNAMIC_CPU_THREAD`, `TASK_FLOW`, `SHOW_THROTTLING`, `SHOW_PROFILE`, `SHOW_MODEL_INFO`, `CUSTOM_INTRA_OP_THREADS`, `CUSTOM_INTER_OP_THREADS`, `NFH_ASYNC`. `NFH_ACCELERATION` exists only when `DXRT_NFH_ACCELERATION_AVAILABLE` is defined, and `CPU_OP_ACCELERATION` only when `DXRT_CPU_OP_ACCELERATION_AVAILABLE` is defined.

`ATTRIBUTE` values: `PROFILER_SHOW_DATA` (1001), `PROFILER_SAVE_DATA` (1002), `CUSTOM_INTRA_OP_THREADS_NUM` (1003), `CUSTOM_INTER_OP_THREADS_NUM` (1004).

See [Configuration](configuration.md#global-configuration) for what each item does.

## DeviceStatus

| Method | Returns |
|---|---|
| `static int GetDeviceCount()` | Number of devices |
| `static DeviceStatus GetCurrentStatus(int device_id)` | A snapshot of one device |
| `GetInfoString()` | Static info, as `dxcli -i` prints |
| `GetStatusString()` | Live status, as `dxcli -s` prints |
| `GetId()` | Device ID |
| `GetTemperature(ch)`, `Temperature(ch)` | °C. `INT16_MIN` if `ch` is out of range |
| `GetNpuVoltage(ch)`, `Voltage(ch)` | mV |
| `GetNpuClock(ch)`, `NpuClock(ch)` | MHz |
| `GetCoreUtilization(coreId)` | %. `-1.0` if `coreId` is out of range |
| `GetMemoryUsed()`, `GetMemoryFree()` | Bytes |
| `MemorySize()`, `MemoryClock()`, `MemoryFrequency()` | NPU memory size and clock |
| `MemoryTypeStr()`, `MemorySizeStrBinaryPrefix()`, `MemorySizeStrWithComma()`, `AllMemoryInfoStr()` | Memory info as text |
| `GetDeviceType()`, `DeviceTypeStr()`, `DeviceTypeWord()`, `DeviceVariantStr()`, `BoardTypeStr()` | Device and board type |
| `FirmwareVersionStr()`, `DriverVersionStr()` | Versions |
| `PcieInfoStr()` | PCIe link info. The overload with five `int` arguments ignores them |
| `DmaChannel()` | DMA channel count |
| `NpuStatusStr(ch)`, `DdrStatusStr(ch)`, `DdrBitErrStr()` | Status text |
| `IsValid()` | `true` if the data was read |
| `StatusToStream(os)`, `DebugStatusToStream(os)`, `operator<<` | Print the status |

The data refreshes about once a second.

## Profiler

`static Profiler& GetInstance()` returns the shared profiler.

| Method | Meaning |
|---|---|
| `GetJobMetrics(int jobId)` | `JobMetrics` for one job. Call it right after `Wait()` |
| `Start(name)`, `End(name)` | Record a custom event |
| `Show()` | Print statistics of each event |
| `Save(file)` | Save the data as JSON |
| `Clear()`, `UserClear()` | Clear all data, or only custom events |

`GetPerformanceData()` and `GetPerformanceDataByDevice()` are deprecated. The metric structures are described in [Per job metrics](configuration.md#per-job-metrics).

## RuntimeEventDispatcher

| Method | Meaning |
|---|---|
| `static RuntimeEventDispatcher& GetInstance()` | The shared dispatcher |
| `RegisterEventHandler(std::function<void(LEVEL, TYPE, CODE, const std::string& message, const std::string& timestamp)>)` | Set the handler. Replaces any earlier one |
| `DispatchEvent(LEVEL, TYPE, CODE, const std::string& msg)` | Send an event |
| `SetCurrentLevel(LEVEL)`, `GetCurrentLevel()` | Lowest level that reaches the handler |

The enum values are listed in [Runtime events](configuration.md#runtime-events).

## Exceptions

DX-RT throws `dxrt::Exception`, which derives from `std::runtime_error`. Catch it before `std::exception`.

```cpp
try {
    dxrt::InferenceEngine ie("model.dxnn");
} catch (const dxrt::Exception& e) {
    std::cerr << e.what() << " code=" << e.code() << " status=" << e.status() << "\n";
} catch (const std::exception& e) {
    std::cerr << e.what() << "\n";
}
```

`status()` returns the C API status (`dxrt_status_t`). `code()` returns an `ERROR_CODE`:

| `ERROR_CODE` | Value |
|---|---|
| `DEFAULT` | `0x0100` |
| `FILE_NOT_FOUND` | `0x0101` |
| `NULL_POINTER` | `0x0102` |
| `FILE_IO` | `0x0103` |
| `INVALID_ARGUMENT` | `0x0104` |
| `INVALID_OPERATION` | `0x0105` |
| `INVALID_MODEL` | `0x0106` |
| `MODEL_PARSING` | `0x0107` |
| `SERVICE_IO` | `0x0108` |
| `DEVICE_IO` | `0x0109` |
| `INSUFFICIENT_MEMORY` | `0x010A` |
| `DEVICE_REMOVED` | `0x010B` |

`to_string(code)` and `operator<<` give the name. You can compare a code with an `int`.

`DEVICE_REMOVED` (C API `DXRT_ERR_DEVICE_REMOVED`, -10) means the device disappeared. It happens only on Windows. Restart the application to recover.

## Free functions

| Function | Meaning |
|---|---|
| `VersionString()` | DX-RT version text |
| `is_service_running()` | `true` if a `dxrtd` instance is running |
| `get_task_max_load()` | Maximum task load used for NPU scheduling (the default buffer count) |
| `set_skip_inference_io(bool)`, `get_skip_inference_io()` | Skip inference input and output transfers (benchmark mode) |
| `ParseModel(file)`, `ParseModel(file, ParseOptions)` | Print model info, like `dxparse`. `ParseOptions` has `verbose`, `json_extract`, `no_color` and `output_file`. The last two are not yet supported |
| `CheckDevices()` | `std::vector<std::shared_ptr<Device>>&` of the devices found |
| `service_main(argc, argv)` | Entry point of the `dxrtd` service |

The header also keeps helpers from the old `<dxrt/util.h>`, such as `DataFromFile`, `SizeFromFile`, `DataDumpBin`, `GetAlign`, `MemAlloc` and `MemFree`.

## C API { #c-api-reference }

`dxrt_c_api.h` is the stable C interface. All functions start with `dxrt_` and return `dxrt_status_t`. Use it from C or from other languages. See [C# through the C API](csharp.md) for an example.

## Next steps

* [Run inference](run-inference.md)
* [Configuration](configuration.md)
* [Python API](python-api.md)
* [Build from source](build-from-source.md)
