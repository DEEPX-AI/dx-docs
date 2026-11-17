---
title: Run inference
description: How to run synchronous, asynchronous, batch and multi input inference with DX-RT in Python and C++.
---

# Run inference

This page shows the main ways to run a compiled `.dxnn` model with DX-RT, in Python and C++.

## Before you start

* Install DX-RT, the NPU driver and the firmware. See [Install](../get-started/install.md).
* Compile your model to a `.dxnn` file with DX-COM, or take one from DX-ModelZoo.
* Check that `dxcli -s` lists your device. See [Command line tools](cli.md#dxcli).

## The basic flow

Every program follows the same steps:

1. Create an `InferenceEngine` with the model path. Optionally pass an `InferenceOption`.
1. Prepare input buffers in the model's input format (NHWC, the model's data type).
1. Run inference with `run` (sync) or `run_async` (async).
1. Read the output tensors and post process them.

Create the engine once and reuse it. Loading a model is slow compared to one inference.

=== "Python"

    ```python
    import numpy as np
    from dx_engine import InferenceEngine

    with InferenceEngine("model.dxnn") as ie:
        info = ie.get_input_tensors_info()[0]
        print(info["name"], info["shape"], info["dtype"])

        buf = np.empty(ie.get_input_size(), dtype=np.uint8)
        buf.fill(0)

        outputs = ie.run([buf])
        for out in outputs:
            print(out.shape, out.dtype)
    ```

=== "C++"

    ```cpp
    #include <dxrt/dxrt_cxx_api.h>
    #include <iostream>
    #include <vector>

    int main()
    {
        try {
            dxrt::InferenceEngine ie("model.dxnn");
            std::vector<uint8_t> input(ie.GetInputSize(), 0);

            auto outputs = ie.Run(input.data());
            for (auto& t : outputs) {
                std::cout << t->name() << " " << t->size_in_bytes() << " bytes\n";
            }
        } catch (const dxrt::Exception& e) {
            std::cerr << "dxrt error: " << e.what() << "\n";
            return -1;
        }
        return 0;
    }
    ```

The Python engine is a context manager. It releases the NPU when the `with` block ends. You can also call `dispose()`. In C++, the engine releases its resources in its destructor. You cannot copy or move a C++ `InferenceEngine`. Use `std::unique_ptr<dxrt::InferenceEngine>` if you need to pass it around.

!!! warning "Do not use np.zeros for input buffers"
    `np.zeros()` maps every page to one shared zero page. The PCIe DMA driver then sees duplicate physical pages and the transfer fails with `EFAULT`. Use `np.empty()` and then `fill()`, as in the examples on this page.

Python checks that each input array has the model's data type. A mismatch raises `ValueError: Input dtype mismatch for '<name>': expected <type>, got <type>`.

## Synchronous inference

`run` blocks until the outputs are ready. It uses one request at a time, so it does not keep all NPU cores busy. Use it for simple programs and for latency tests.

=== "Python"

    ```python
    outputs = ie.run([input_array])        # list of np.ndarray
    ```

=== "C++"

    ```cpp
    dxrt::TensorPtrs outputs = ie.Run(input.data());
    ```

You can pass your own output buffer. It must hold at least `GetOutputSize()` bytes.

=== "Python"

    ```python
    out_buf = np.empty(ie.get_output_size(), dtype=np.uint8)
    outputs = ie.run([input_array], output_buffers=[out_buf])
    ```

=== "C++"

    ```cpp
    std::vector<uint8_t> output(ie.GetOutputSize());
    auto outputs = ie.Run(input.data(), nullptr, output.data());
    ```

When you pass an output buffer, the returned tensors point into it. Keep the buffer alive while you use them.

## Asynchronous inference

`run_async` queues a request and returns a job ID at once. Several requests run at the same time on different NPU cores, so async gives the best throughput. You get the result in one of two ways.

### With a callback

Register a callback once. DX-RT calls it from a runtime thread when each job finishes. The callback gets the outputs and the user argument you passed to `run_async`. Return 0.

=== "Python"

    ```python
    import threading

    done = threading.Event()
    count = 0
    loops = 100

    def on_done(outputs, user_arg):
        global count
        count += 1
        if count == loops:
            done.set()
        return 0

    ie.register_callback(on_done)
    for i in range(loops):
        ie.run_async([input_array], user_arg=i)
    done.wait()
    ```

=== "C++"

    ```cpp
    std::mutex m;
    std::condition_variable cv;
    int count = 0;
    const int loops = 100;

    ie.RegisterCallback([&](dxrt::TensorPtrs& outputs, void* userArg) {
        std::lock_guard<std::mutex> lock(m);
        if (++count == loops) cv.notify_one();
        return 0;
    });

    for (int i = 0; i < loops; ++i) {
        ie.RunAsync(input.data(), reinterpret_cast<void*>(static_cast<intptr_t>(i)));
    }

    std::unique_lock<std::mutex> lock(m);
    cv.wait(lock, [&] { return count == loops; });
    ```

Keep callbacks short. Copy the outputs or hand them to another thread for heavy post processing. In Python, pass `None` to `register_callback` to remove the callback.

### With wait

Without a callback, call `wait(job_id)` to block until that job is done and get its outputs.

=== "Python"

    ```python
    job_id = ie.run_async([input_array])
    outputs = ie.wait(job_id)
    ```

=== "C++"

    ```cpp
    int jobId = ie.RunAsync(input.data());
    auto outputs = ie.Wait(jobId);
    ```

In C++, `Wait(jobId, output)` copies the result into your own buffer.

### How many requests run at once

The number of requests in flight is limited by the buffer count of the engine. The default is 6. Raise it with `InferenceOption` (`buffer_count` in Python, `bufferCount` in C++, range 1 to 100) or `dxrun --buffer-count`. See [Configuration](configuration.md#inference-option).

When you pass your own input buffer to `run_async`, do not change it until the job finishes. The runtime may still be reading it.

## Batch inference

Batch inference runs several inputs in one call. DX-RT runs them asynchronously inside and returns when all are done. You must give one output buffer per sample.

=== "Python"

    ```python
    batch = 8
    inputs, outputs = [], []
    for _ in range(batch):
        buf = np.empty(ie.get_input_size(), dtype=np.uint8)
        buf.fill(0)
        inputs.append([buf])
        outputs.append([np.empty(ie.get_output_size(), dtype=np.uint8)])

    results = ie.run(inputs, output_buffers=outputs)   # list of lists
    ```

=== "C++"

    ```cpp
    const int batch = 8;
    std::vector<std::vector<uint8_t>> in(batch, std::vector<uint8_t>(ie.GetInputSize()));
    std::vector<std::vector<uint8_t>> out(batch, std::vector<uint8_t>(ie.GetOutputSize()));

    std::vector<void*> inputBuffers, outputBuffers;
    for (int i = 0; i < batch; ++i) {
        inputBuffers.push_back(in[i].data());
        outputBuffers.push_back(out[i].data());
    }

    std::vector<dxrt::TensorPtrs> results = ie.Run(inputBuffers, outputBuffers);
    ```

Rules for batch calls:

* In C++, `outputBuffers` must have the same size as `inputBuffers`. Otherwise you get `InvalidArgumentException`. Put `nullptr` in an element to let the engine allocate that output. This is the way to handle models with dynamic output shapes.
* In Python, `run` treats a list of lists as an explicit batch. For a single input model, a flat list with more than one array is also a batch.
* `run_async` does not take a batch. Python raises `ValueError: Batch inference is not supported in run_async. Use multiple run_async calls or use run() for batch processing.`
* In Python, `run` takes `user_args` (one per sample). The other run methods take `user_arg`.

## Multi input models

A model can have more than one input tensor. Get the names, sizes and the task each input feeds:

=== "Python"

    ```python
    names = ie.get_input_tensor_names()
    sizes = ie.get_input_tensor_sizes()
    mapping = ie.get_input_tensor_to_task_mapping()
    print(ie.is_multi_input_model(), ie.get_input_tensor_count())
    ```

=== "C++"

    ```cpp
    auto names = ie.GetInputTensorNames();
    auto sizes = ie.GetInputTensorSizes();
    auto mapping = ie.GetInputTensorToTaskMapping();
    bool multi = ie.IsMultiInputModel();
    ```

You can pass inputs in three ways.

| Form | Python | C++ |
|---|---|---|
| By name | `ie.run_multi_input({"a": arr_a, "b": arr_b})` | `ie.RunMultiInput(std::map<std::string, void*>{...})` |
| As a list in `get_input_tensor_names()` order | `ie.run([arr_a, arr_b])` | `ie.RunMultiInput(std::vector<void*>{a, b})` |
| As one concatenated buffer of `get_input_size()` bytes | `ie.run(concat)` | `ie.Run(concat.data())` |

DX-RT splits a concatenated buffer by the tensor sizes. Async versions exist for each form: `run_async_multi_input` in Python, and `RunAsyncMultiInput` and `RunAsync(std::vector<void*>)` in C++.

=== "Python"

    ```python
    inputs = {}
    for name, size in zip(ie.get_input_tensor_names(), ie.get_input_tensor_sizes()):
        buf = np.empty(size, dtype=np.uint8)
        buf.fill(0)
        inputs[name] = buf
    outputs = ie.run_multi_input(inputs)
    ```

=== "C++"

    ```cpp
    auto names = ie.GetInputTensorNames();
    auto sizes = ie.GetInputTensorSizes();
    std::vector<std::vector<uint8_t>> data;
    std::map<std::string, void*> inputs;
    for (size_t i = 0; i < names.size(); ++i) {
        data.emplace_back(sizes[i], 0);
        inputs[names[i]] = data.back().data();
    }
    auto outputs = ie.RunMultiInput(inputs);
    ```

Multi input rules:

* For a multi input batch in Python, use a list of lists, one inner list per sample. Python also accepts a flat list of N times the input count. C++ needs the vector of vectors form.
* A flat list whose length is not a multiple of the input count raises `ValueError: Multi-input model requires N input tensors [...] per sample. Got M inputs, which is not a valid multiple.`
* In C++, `RunAsync(std::vector<void*>)` with a size that does not match the input count uses only the first element.
* `RunAsyncMultiInput` with a map on a single input model throws an exception.

## Measure performance

Each engine keeps timing statistics, in microseconds:

| Metric | Python | C++ | Meaning |
|---|---|---|---|
| Latency | `get_latency()` | `GetLatency()` | Same as E2E response time since DX-RT 3.5.0 |
| E2E response time | `get_e2e_response_time()` | `GetE2EResponseTime()` | From the request to the result, with buffer and queue waits |
| Core latency | `get_core_latency()` | `GetCoreLatency()` | Per request, without buffer pool and queue wait times |
| NPU inference time | `get_npu_inference_time()` | `GetNpuInferenceTime()` | Time on the NPU core |
| Queue wait time | not available | `GetQueueWaitTime()` | Time a request waited in the queue |

Each metric also has list, mean, standard deviation and count variants, such as `get_core_latency_mean()` or `GetCoreLatencyMean()`. Statistics stop updating after `INT_MAX` samples.

!!! note "Latency changed in DX-RT 3.5.0"
    `GetLatency` now returns the E2E response time. If your code compares against values from older versions, use `GetCoreLatency` instead. See the [compatibility page](../get-started/compatibility.md) for version requirements.

For a quick throughput number, call the built in benchmark. It returns frames per second.

=== "Python"

    ```python
    fps = ie.run_benchmark(100, [input_array])
    ```

=== "C++"

    ```cpp
    float fps = ie.RunBenchmark(100, input.data());
    ```

For full measurement options, use [`dxrun`](cli.md#dxrun) and the [profiler](configuration.md#profiler).

## Load a model from memory

You can create an engine from a model already in memory.

=== "Python"

    ```python
    data = np.fromfile("model.dxnn", dtype=np.uint8)
    ie = InferenceEngine.from_buffer(data)   # uint8, C contiguous
    ```

=== "C++"

    ```cpp
    std::vector<uint8_t> data = /* read model.dxnn */;
    dxrt::InferenceEngine ie(data.data(), data.size());
    ```

## Data layout

DX-RT uses NHWC tensors. The NPU needs aligned data, and DX-RT converts for you:

| Tensor | Layout on the device |
|---|---|
| Input, formatter type | `[N, H, W, C]` |
| Input, IM2COL type | `[N, H, align64(W*C)]` |
| Output | `[N, H, W, align64(C)]` |

Since DX-RT 3.0.0, the runtime adds input padding and removes output padding automatically when ONNX Runtime is off (`USE_ORT=OFF` or `use_ort=False`). You pass and receive plain NHWC data. Your own output buffers must still be at least `GetOutputSize()` bytes.

## Next steps

* [Configuration](configuration.md)
* [Tutorials](tutorials.md)
* [Python API](python-api.md)
* [C++ API](cpp-api.md)
