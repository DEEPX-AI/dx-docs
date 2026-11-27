---
title: Python API
description: Reference for dx_engine, the DX-RT Python package, with every public class and method.
---

# Python API

This page lists the public classes and methods of `dx_engine` 3.5.0, the DX-RT Python package.

## Before you start

* `dx_engine` comes with DX-RT. See [Install](../get-started/install.md). It supports Python 3.8 to 3.14.
* For worked examples, see [Run inference](run-inference.md) and [DX-RT examples](tutorials.md).

## Package contents

```python
from dx_engine import (
    InferenceEngine, InferenceOption, Configuration, DeviceStatus,
    RuntimeEventDispatcher, Profiler, JobMetrics, TaskMetrics, NpuDeviceMetrics,
    DeviceRemovedError, __version__,
)
```

### Version check on import

When you import `dx_engine`, it compares its major and minor version with the loaded `libdxrt.so`. If they differ, the import fails:

```text
RuntimeError: dx_engine and DX-RT versions do not match.
  - dx_engine (python package) : 3.5.0
  - libdxrt.so (runtime)       : <version>
Please install matching versions of dx_engine and libdxrt-bin.
...
To skip this check, set DX_ENGINE_SKIP_VERSION_CHECK=1.
```

Install matching versions. Set `DX_ENGINE_SKIP_VERSION_CHECK=1` only if you know the versions work together.

## InferenceEngine

```python
InferenceEngine(model_path: str, inference_option: InferenceOption | None = None)
InferenceEngine.from_buffer(memory_buffer: np.ndarray, inference_option: InferenceOption | None = None)
```

`from_buffer` takes the model file contents as a C contiguous `uint8` array. The engine is a context manager. Leaving the `with` block calls `dispose()`.

### Run methods

| Method | Returns | Notes |
|---|---|---|
| `run(input_data, output_buffers=None, user_args=None)` | `List[np.ndarray]` or `List[List[np.ndarray]]` | Synchronous. Handles single, multi input and batch input |
| `run_multi_input(input_tensors: Dict[str, np.ndarray], output_buffers=None, user_arg=None)` | `List[np.ndarray]` | Inputs by tensor name |
| `run_async(input_data, user_arg=None, output_buffer=None)` | `int` job ID | No batch input |
| `run_async_multi_input(input_tensors, user_arg=None, output_buffer=None)` | `int` job ID | Inputs by tensor name |
| `wait(job_id)` | `List[np.ndarray]` | Blocks until the job is done |
| `register_callback(callback)` | | `callback(outputs, user_arg) -> int`. Pass `None` to remove it |
| `run_benchmark(num_loops, input_data=None)` | `float` FPS | Built in throughput test |
| `validate_device(input_data, device_id=0)` | `List[np.ndarray]` | Device check. Works only with models compiled in debug mode |
| `validate_device_multi_input(input_tensors, device_id=0)` | `List[np.ndarray]` | The same, with inputs by name |
| `dispose()` | | Release the engine |

How `run` reads `input_data`:

| Input | Meaning |
|---|---|
| `np.ndarray` | One inference. For a multi input model, an array of the total input size is split into the inputs |
| `List[np.ndarray]` whose first element has the total input size | One inference, split automatically. Other elements are ignored |
| `List[np.ndarray]`, multi input model | Length equal to the input count: one inference. Length N times the input count: a batch of N |
| `List[np.ndarray]`, single input model | Length 1: one inference. Length above 1: a batch |
| `List[List[np.ndarray]]` | An explicit batch, one inner list per sample |

A batch needs `output_buffers`, one per sample. Each input array must have the model's data type. Errors:

| Error | When |
|---|---|
| `ValueError: Input data list cannot be empty.` | Empty list |
| `TypeError: Input data must be np.ndarray, List[np.ndarray], or List[List[np.ndarray]].` | Wrong type |
| `ValueError: Multi-input model requires N input tensors [...] per sample. Got M inputs, which is not a valid multiple.` | Bad flat list length |
| `ValueError: Batch inference is not supported in run_async. ...` | Batch passed to `run_async` |
| `ValueError: Input dtype mismatch for '<name>': expected <type>, got <type>` | Wrong data type |

### Model and tensor info

| Method | Returns |
|---|---|
| `get_input_size()` | Total input size in bytes |
| `get_input_tensor_sizes()` | Size of each input in bytes |
| `get_output_size()` | Total output size in bytes |
| `get_output_tensor_sizes()` | Size of each output in bytes |
| `has_dynamic_output()` | `True` if an output shape is known only after inference |
| `get_input_tensors_info()`, `get_output_tensors_info()` | List of dicts with `name`, `shape`, `dtype` and `elem_size` |
| `get_input_tensor_count()`, `get_output_tensor_count()` | Number of tensors |
| `get_input_tensor_names()`, `get_output_tensor_names()` | Tensor names in order |
| `get_input_tensor_to_task_mapping()` | Dict from input name to task name |
| `is_multi_input_model()` | `True` for more than one input |
| `get_all_task_outputs()` | Outputs of every task of the last run |
| `get_task_order()` | Task names in run order |
| `get_num_tail_tasks()` | Number of tail tasks |
| `get_compile_type()`, `get_model_version()` | Compile type and model file version |
| `is_ppu()` | `True` if the model uses the post processing unit |
| `get_bitmatch_mask(index=0)` | Bit match mask |

`get_input_data_type()` and `get_output_data_type()` are deprecated. Read `dtype` from `get_input_tensors_info()` instead.

### Timing

All values are in microseconds.

| Base method | Meaning |
|---|---|
| `get_latency()` | Same as E2E response time since 3.5.0 |
| `get_e2e_response_time()` | Request to result, with waits |
| `get_core_latency()` | Without buffer pool and queue waits |
| `get_npu_inference_time()` | Time on the NPU |

Each has `_list()`, `_mean()`, `_std()` and `_count()` variants, such as `get_core_latency_mean()`.

### Deprecated names

These still work and emit a `DeprecationWarning`:

| Old | New |
|---|---|
| `Run`, `run_batch`, `RunBatch` | `run` |
| `RunAsync` | `run_async` |
| `Wait` | `wait` |
| `RunBenchMark` | `run_benchmark` |
| `ValidateDevice` | `validate_device` |
| `RegisterCallBack` | `register_callback` |
| `input_size`, `output_size` | `get_input_size`, `get_output_size` |
| `input_dtype`, `output_dtype` | `dtype` in `get_input_tensors_info()` and `get_output_tensors_info()` |
| `task_order` | `get_task_order` |
| `latency`, `inference_time` | `get_latency`, `get_npu_inference_time` |
| `get_outputs` | `get_all_task_outputs` |
| `bitmatch_mask`, `get_num_tails`, `is_PPU` | `get_bitmatch_mask`, `get_num_tail_tasks`, `is_ppu` |

## InferenceOption

| Property | Type | Default |
|---|---|---|
| `devices` | `List[int]` | `[]`, all devices |
| `bound_option` | `InferenceOption.BOUND_OPTION` | `NPU_ALL` |
| `buffer_count` | `int` | 0, the library default of 6. Maximum 100 |
| `use_ort` | `bool` | `True` if built with ONNX Runtime |
| `show_model_info` | `bool` | `True` |

Each property also has `set_` and `get_` methods. `BOUND_OPTION` is an `Enum` with `NPU_ALL` (0), `NPU_0`, `NPU_1`, `NPU_2`, `NPU_01`, `NPU_12` and `NPU_02` (6). See [Configuration](configuration.md#inference-option).

## Configuration

`Configuration()` wraps the shared global settings.

| Method | Meaning |
|---|---|
| `set_enable(item, enabled)`, `get_enable(item)` | Turn an item on or off |
| `set_attribute(item, attrib, value)`, `get_attribute(item, attrib)` | Set or read a string attribute |
| `load_config_file(file_name)` | Load a `KEY=VALUE` file |
| `get_version()` | DX-RT library version |
| `get_driver_version()`, `get_pcie_driver_version()` | NPU driver versions |
| `set_fw_config_with_json(json_file)` | Apply firmware settings from JSON |

`Configuration.ITEM` and `Configuration.ATTRIBUTE` are `IntEnum`s with the same values as C++. `NFH_ACCELERATION` (12) and `CPU_OP_ACCELERATION` (13) exist only in accelerated builds. Python has no firmware or ONNX Runtime version getter. Use `dxcli -i` or C++. See [Configuration](configuration.md#global-configuration) for the items.

## DeviceStatus

| Method | Returns |
|---|---|
| `DeviceStatus.get_device_count()` | Number of devices |
| `DeviceStatus.get_current_status(device_id)` | A `DeviceStatus`. Never raises. Check `is_valid()` |
| `get_id()` | Device ID |
| `get_temperature(ch)` | °C |
| `get_npu_voltage(ch)` | mV |
| `get_npu_clock(ch)` | MHz |
| `get_core_utilization(core_id)` | % |
| `get_memory_used()`, `get_memory_free()` | Bytes |
| `get_driver_version()` | Driver version |
| `is_valid()` | `True` if the data was read |

## Profiler

`Profiler.get_instance()` returns the shared profiler.

| Method | Meaning |
|---|---|
| `get_job_metrics(job_id)` | `JobMetrics` for one job |
| `start(name)`, `end(name)` | Record a custom event |
| `show()` | Print min, max, average and CoV of each event |
| `save(filename)` | Save the data as JSON |
| `clear()`, `user_clear()` | Clear all data, or only custom events |

`JobMetrics` has `tasks`, `valid` and `get_task(name)`. `TaskMetrics` has `task_name`, `devices` (dict of `NpuDeviceMetrics`), `cpu_task_us` and `valid`. `NpuDeviceMetrics` has `input_format_us`, `h2d_us`, `inference_core_all_us`, `inference_core_0_us` to `inference_core_2_us`, `d2h_us`, `output_format_us`, `total_us` and `valid`.

## RuntimeEventDispatcher

| Method | Meaning |
|---|---|
| `register_event_handler(handler)` | `handler(level, type, code, message, timestamp)`. Replaces any earlier handler |
| `dispatch_event(level, type, code, event_message)` | Send an event |
| `set_current_level(level)`, `get_current_level()` | Lowest level that reaches the handler |

`LEVEL`, `TYPE` and `CODE` are `IntEnum`s. See [Runtime events](configuration.md#runtime-events) for the values.

## DeviceRemovedError

`DeviceRemovedError` is a subclass of `OSError`. It is raised when a device disappears, which happens only on Windows. Restart the application to recover.

## Functions

| Function | Returns |
|---|---|
| `dx_engine.inference_engine.parse_model(model_path)` | The model description as a string |
| `dx_engine.utils.parse_model(model_path, options=None)` | `int` status. Prints like `dxparse` |

## Not in Python

Some C++ features have no Python version: `GetModelName`, the queue wait time getters, the user input release callback and the firmware and ONNX Runtime version getters. See the [C++ API](cpp-api.md).

## Next steps

* [Run inference](run-inference.md)
* [Configuration](configuration.md)
* [C++ API](cpp-api.md)
* [DX-RT examples](tutorials.md)
