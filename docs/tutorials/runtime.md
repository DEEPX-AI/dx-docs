---
title: Run models with DX-RT
description: Three DX-RT tutorials covering the CLI tools, the Python and C++ APIs, async inference and profiling.
---

# Run models with DX-RT

These three tutorials let you run compiled models with DX-RT 3.5.0, first with the CLI tools and then from your own Python or C++ code.

The notebooks are in `notebooks/T06-DX-Runtime/` of [dx-tutorials](https://github.com/DEEPX-AI/dx-tutorials). Everything they create goes to `notebooks/T06-DX-Runtime/workspace/`. No `sudo` is needed. For the example programs in the DX-RT repository, see [DX-RT examples](../runtime/tutorials.md).

## Before you start

* [Set up the tutorials](setup.md) done: DX-RT installed and `/dev/dxrt0` present.
* `uv`, `cmake` and `g++` (from `build-essential`) for 06-2.

## What each part covers

| Part | Notebook | You learn |
|---|---|---|
| 06-1 Beginner | `dx_rt_01_beginner.ipynb` | Check the device, inspect a model, `dxrun` single, benchmark and target FPS modes, `--use-ort`, `dxtop` |
| 06-2 Intermediate | `dx_rt_02_intermediate.ipynb` | Install `dx_engine`, tensor metadata, sync, async with job IDs and callbacks, batch API, `buffer_count`, a minimal C++14 app |
| 06-3 Advanced | `dx_rt_03_advanced.ipynb` | Device and core binding, buffer count tuning, profiler traces, per job metrics, device health, loading from memory, multi input models, runtime events, NFH and CPU op acceleration, release validation |

## Steps

1. Download a sample model and check the device:

    ```bash
    cd ~/dx-all-suite/dx-runtime/dx_app
    bash setup.sh --models resnet50 yolo26s --no-force
    cd ~/dx-all-suite/workspace/res/models
    dxcli -s
    ```

1. Inspect the model and run it in the three `dxrun` modes:

    ```bash
    dxparse -m resnet50_224x224.dxnn -v
    dxrun -m resnet50_224x224.dxnn --single --loops 1 --verbose
    dxrun -m resnet50_224x224.dxnn --benchmark --time 5 --warmup-runs 5 --buffer-count 6
    dxrun -m resnet50_224x224.dxnn --fps 30 --time 5 --warmup-runs 5
    ```

1. Compare NPU only and full pipeline speed for a model with a CPU task. Without `--use-ort`, `dxrun` measures only the NPU part:

    ```bash
    dxrun -m yolo26-s_640x640.dxnn --benchmark --time 5 --warmup-runs 5
    dxrun -m yolo26-s_640x640.dxnn --benchmark --time 5 --warmup-runs 5 --use-ort
    ```

    Add `--profiler` to write `profiler.json` into the current folder. Run `dxtop` in a separate terminal to watch utilization, temperature and memory. `dxbenchmark --dir <folder> -l 5` benchmarks every model in a folder and writes CSV, JSON and HTML reports.

1. Install the `dx_engine` Python package into your environment. The DX-RT package ships wheels per Python version under `/usr/share/libdxrt-bin/python`:

    ```bash
    uv venv ~/venv-dxrt
    uv pip install --python ~/venv-dxrt/bin/python /usr/share/libdxrt-bin/python/dx_engine-*-cp312-*.whl
    ```

    Replace `cp312` with the tag of your Python (`cp310` for 3.10 and so on). See [Python API](../runtime/python-api.md) for other ways.

1. Run one synchronous inference from code:

    === "Python"
        ```python
        import numpy as np
        from dx_engine import InferenceEngine

        with InferenceEngine("resnet50_224x224.dxnn") as ie:
            info = ie.get_input_tensors_info()[0]
            x = np.zeros(info["shape"], dtype=info["dtype"])
            outputs = ie.run([x])
            for i, out in enumerate(outputs):
                print(i, out.shape, out.dtype)
            print("NPU time (ms):", ie.get_npu_inference_time() / 1000)
        ```
    === "C++"
        ```cpp
        #include <dxrt/dxrt_cxx_api.h>
        #include <cstdint>
        #include <iostream>
        #include <vector>

        int main(int argc, char* argv[])
        {
            dxrt::InferenceEngine engine(argv[1]);
            std::vector<std::uint8_t> input(engine.GetInputSize(), 0);
            const auto outputs = engine.Run(input.data());
            for (const auto& out : outputs) {
                std::cout << out->name() << " bytes=" << out->size_in_bytes() << '\n';
            }
            return 0;
        }
        ```

    Build the C++ version with this `CMakeLists.txt`. DX-RT installs the CMake package, so `find_package(dxrt)` is enough:

    ```text
    cmake_minimum_required(VERSION 3.16)
    project(dxrt_sync LANGUAGES CXX)
    find_package(dxrt REQUIRED)
    add_executable(dxrt_sync main.cpp)
    target_compile_features(dxrt_sync PRIVATE cxx_std_14)
    target_link_libraries(dxrt_sync PRIVATE dxrt::dxrt)
    ```

    ```bash
    cmake -S . -B build && cmake --build build
    ./build/dxrt_sync ~/dx-all-suite/workspace/res/models/resnet50_224x224.dxnn
    ```

    Include only `dxrt/dxrt_cxx_api.h`; do not mix it with `dxrt_api.h` in one file.

1. For streaming throughput, submit with `run_async()` and collect with `wait(job_id)`, or register a callback with `register_callback()`. Keep each input array alive until its result arrives. For more C++ patterns, start from the examples in `~/dx-all-suite/dx-runtime/dx_rt/examples/cpp`.

## Expected result

`dxrun` prints latency and FPS, and the code prints one line per output tensor.

## Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| `No dx_engine wheel for cp3XY` | No wheel for your Python version | Create the environment with a supported Python |
| `RuntimeError` about a version mismatch on `import dx_engine` | The wheel is from another DX-RT version | Reinstall the wheel from `/usr/share/libdxrt-bin/python`. `DX_ENGINE_SKIP_VERSION_CHECK=1` skips the check, for diagnosis only |
| Async results look wrong | The input buffer was freed before `wait()` returned | Keep the input alive until `wait()` returns |
| Callbacks never arrive | An exception inside the callback | Keep the callback short and safe; clear it with `register_callback(None)` after the last job |

The old CLI names `dxrt-cli`, `run_model` and `parse_model` still work as links to `dxcli`, `dxrun` and `dxparse`.

## Next steps

* [Python API](../runtime/python-api.md)
* [C++ API](../runtime/cpp-api.md)
* [DX-RT reference](../runtime/index.md)
