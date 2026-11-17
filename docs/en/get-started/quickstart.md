---
title: Quickstart
description: Compile one sample model with DX-COM and run it on the NPU with DX-RT from Python or C++.
---

# Quickstart

This page takes you from an installed SDK to a first result: you compile one sample model on the host and run it on the NPU from Python or C++.

## Before you start

* DX-COM is installed on an x86_64 host and `dxcom -v` works. See [Install](install.md#host-dx-com).
* The NPU driver, firmware and DX-RT are installed on the device, the device was restarted, and `dxcli -s` shows `Device 0`. See [Install](install.md#device-driver-runtime-and-firmware).
* `dx_engine` is installed in the Python environment you use on the device.
* `git` and `curl` are installed on the host.

Host and device can be the same machine.

## 1. Compile a sample model (host)

We publish three small sample models with their JSON configs: `MobileNetV2-1` (classification), `YOLOV5S-1` (object detection) and `YOLOV5S_Face-1` (face detection). The helper scripts in the `dx-compiler` repository download them and a calibration image set.

```bash
git clone https://github.com/DEEPX-AI/dx-compiler.git
cd dx-compiler
./example/1-download_sample_models.sh
./example/2-download_sample_calibration_dataset.sh
```

The files land in `dx_com/sample_models/onnx/`, `dx_com/sample_models/json/` and `dx_com/calibration_dataset/`. Run `dxcom` from `dx_com/`, because the configs point to `./calibration_dataset`:

```bash
cd dx_com
dxcom -m sample_models/onnx/MobileNetV2-1.onnx \
      -c sample_models/json/MobileNetV2-1.json \
      -o output/
ls output/
```

`-o` is an output directory. When the compile succeeds it holds `MobileNetV2-1.dxnn`. Add `--export_html` to also get `MobileNetV2-1_summary.html`, a report that shows which parts of the graph run on the NPU and which on the CPU.

The same compile from Python:

```python
import dx_com

dx_com.compile(
    model="sample_models/onnx/MobileNetV2-1.onnx",
    config="sample_models/json/MobileNetV2-1.json",
    output_dir="output/",
)
```

To compile all three samples at once, run `./example/3-compile_sample_models.sh` from the repository root.

!!! note "`.dxnn` files from DX-COM 2.5.0 need DX-RT 3.5.0"
    DX-COM 2.5.0 writes `.dxnn` format v9. DX-RT 3.4.2 and older cannot load it.

## 2. Copy the model to the device

Skip this step if host and device are the same machine.

```bash
scp output/MobileNetV2-1.dxnn user@device:~/
```

## 3. Check the model with the CLI (device)

```bash
dxparse -m MobileNetV2-1.dxnn
dxrun -m MobileNetV2-1.dxnn -l 100
```

`dxparse` prints the model inputs and outputs. `dxrun` runs 100 inferences and prints the latency and FPS. If both work, the whole stack is fine.

## 4. Run the model from your code (device)

Both programs load the model, feed one input buffer of the right size, run one synchronous inference and print the output tensors. Replace the zero buffer with your preprocessed image data in the model's input layout (`get_input_tensors_info()` in Python shows the shape and type).

=== "Python"

    Save as `first_inference.py`:

    ```python
    import numpy as np
    from dx_engine import InferenceEngine

    with InferenceEngine("MobileNetV2-1.dxnn") as ie:
        print("inputs:", ie.get_input_tensors_info())

        # np.empty plus fill gives each page its own memory, which the NPU DMA needs.
        buf = np.empty(ie.get_input_size(), dtype=np.uint8)
        buf.fill(0)

        outputs = ie.run([buf])
        for out in outputs:
            print("output:", out.shape, out.dtype)
    ```

    Run it in the environment that has `dx_engine`:

    ```bash
    python3 first_inference.py
    ```

=== "C++"

    Save as `main.cpp`:

    ```cpp
    #include "dxrt/dxrt_cxx_api.h"
    #include <cstdint>
    #include <iostream>
    #include <string>
    #include <vector>

    int main(int argc, char* argv[])
    {
        std::string model = argc > 1 ? argv[1] : "MobileNetV2-1.dxnn";
        try
        {
            dxrt::InferenceEngine ie(model);

            std::vector<uint8_t> input(ie.GetInputSize(), 0);
            auto outputs = ie.Run(input.data());

            for (auto& t : outputs)
            {
                std::cout << "output: " << t->name() << " shape:";
                for (auto d : t->shape()) std::cout << ' ' << d;
                std::cout << '\n';
            }
        }
        catch (const std::exception& e)
        {
            std::cerr << "error: " << e.what() << '\n';
            return 1;
        }
        return 0;
    }
    ```

    Save as `CMakeLists.txt` next to it. The `libdxrt-bin` package installs the CMake package under `/usr/local/lib/cmake/dxrt`:

    ```cmake
    cmake_minimum_required(VERSION 3.14)
    project(first_inference CXX)
    set(CMAKE_CXX_STANDARD 14)
    find_package(dxrt REQUIRED)
    add_executable(first_inference main.cpp)
    target_link_libraries(first_inference PRIVATE dxrt::dxrt)
    ```

    Build and run:

    ```bash
    cmake -S . -B build
    cmake --build build
    ./build/first_inference MobileNetV2-1.dxnn
    ```

The same model also runs asynchronously, in batches and on several NPU cores. See the [Python API](../runtime/python-api.md) and the [C++ API](../runtime/cpp-api.md).

## Shortcut: the getting started scripts

The full suite clone (`dx-all-suite`, see [Install](install.md#option-c-full-suite-clone)) has scripts that do all of the above and run three DX-APP demos. Run them from the `dx-all-suite` folder, in this order:

```bash
./getting-started/compiler-0_install_dx-compiler.sh
./getting-started/compiler-1_download_onnx.sh
./getting-started/compiler-2_setup_calibration_dataset.sh
./getting-started/compiler-3_setup_output_path.sh
./getting-started/compiler-4_model_compile.sh
./getting-started/runtime-0_install_dx-runtime.sh
```

`runtime-0` runs `./dx-runtime/install.sh --all` unless the sanity check already passes (`--exclude-fw` and `--exclude-driver` skip parts, `--force` reinstalls). If it installed the driver or firmware, restart now as described in [The restart rule](install.md#the-restart-rule) and check `dxcli -s`. Then continue:

```bash
./getting-started/runtime-1_setup_input_path.sh
./getting-started/runtime-2_setup_assets.sh
./getting-started/runtime-3_run_example_using_dxrt.sh
```

| Script | What it does |
|---|---|
| `compiler-0_install_dx-compiler.sh` | Runs `dx-compiler/install.sh` unless `dxcom -v` already works (`--force` reinstalls) |
| `compiler-1_download_onnx.sh` | Downloads `YOLOV5S-1`, `YOLOV5S_Face-1` and `MobileNetV2-1` and links them to `getting-started/sample_models` |
| `compiler-2_setup_calibration_dataset.sh` | Downloads the calibration images and links them to `getting-started/calibration_dataset` |
| `compiler-3_setup_output_path.sh` | Links `getting-started/dxnn` to the output folder (`workspace/dxnn` locally) |
| `compiler-4_model_compile.sh` | Compiles the three models into `.dxnn` files |
| `runtime-0_install_dx-runtime.sh` | Installs driver, firmware, DX-RT, DX-APP and DX-Stream |
| `runtime-1_setup_input_path.sh` | Points the runtime examples at `getting-started/dxnn` |
| `runtime-2_setup_assets.sh` | Runs `setup.sh` of DX-APP and DX-Stream to download demo assets |
| `runtime-3_run_example_using_dxrt.sh` | Runs the three demos and prints FPS and latency (`--no-display` for headless machines) |

`runtime-3` runs these DX-APP binaries from `getting-started/forked_dx_app_example/`:

| Model | Binary | Input | Task | Loops |
|---|---|---|---|---|
| `YOLOV5S_Face-1` | `yolov5-s-face_640x640_async` | `sample/sample_face.jpg` | Face detection | 30 |
| `YOLOV5S-1` | `yolov5-s_640x640_async` | `sample/sample_kitchen.jpg` | Object detection | 300 |
| `MobileNetV2-1` | `mobilenetv2_224x224_async` | `sample/ILSVRC2012/1.jpeg` | Image classification | 300 |

All three models must compile in `compiler-4`, otherwise `runtime-3` stops with a file not found error. In Docker, run the scripts inside the containers from `/deepx/getting-started`.

To evaluate a DX-ModelZoo model instead (ONNX baseline, compile, NPU evaluation), use `modelzoo-0_install_dx-modelzoo.sh`, `modelzoo-1_prepare_assets.sh` and `modelzoo-2_run_first_npu_model.sh`. The fastest check of the NPU path downloads a precompiled `.dxnn` and skips the rest:

```bash
./getting-started/modelzoo-2_run_first_npu_model.sh --skip-onnx --skip-compile
```

The default model `resnet50_224x224` needs the full ImageNet validation set (50,000 images) in `getting-started/modelzoo/datasets/ILSVRC2012/val`. See [DX-ModelZoo](../tools/model-zoo/index.md).

## Next steps

* [Learn the DX-COM options and config file](../compiler/index.md)
* [Write a full application with the Python API](../runtime/python-api.md)
* [Run ready made demos with DX-APP](../tools/app/index.md)
* [Build video pipelines with DX-Stream](../tools/stream/index.md)
