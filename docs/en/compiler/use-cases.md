---
title: DX-COM use cases
description: Complete, copy ready DX-COM examples for classification, multi input, edge devices, non image data, accuracy tuning and YOLO post processing.
---

# DX-COM use cases

This page gives you complete examples for the most common compile tasks, with the `dxcom` command and the `dx_com` Python module side by side where both work.

## Before you start

* Install DX-COM: see [Install](../get-started/install.md). It already installs `torch`, `torchvision`, `numpy` and `Pillow`, which these examples use.
* Replace the model file names and the dataset paths with your own.

| Use case | CLI | Python |
|---|---|---|
| [Image classification](#image-classification) | Yes | Yes |
| [Multi input model](#multi-input-model) | No | Yes |
| [Edge device with a weak CPU](#edge-device-with-a-weak-cpu) | Yes | Yes |
| [Non image data](#non-image-data) | No | Yes |
| [Better accuracy with DXQ and Q-PRO](#better-accuracy-with-dxq-and-q-pro) | Yes | Yes |
| [Diagnose and re-quantize](#diagnose-and-re-quantize) | Yes | Yes |
| [YOLO post processing on a weak CPU](#yolo-post-processing-on-a-weak-cpu) | Config only | Yes |
| [YOLO with the PPU](#yolo-with-the-ppu) | Yes | Yes |

## Image classification

Compile a ResNet50 or MobileNet classifier with standard ImageNet preprocessing. Both options produce the same calibration tensors: resize the shorter side to 256, center crop 224, RGB, scale to 0 to 1, normalize.

=== "CLI"
    `resnet50_config.json`:

    ```json
    {
      "inputs": {
        "input": [1, 3, 224, 224]
      },
      "calibration_method": "ema",
      "calibration_num": 100,
      "default_loader": {
        "dataset_path": "./calibration_dataset",
        "file_extensions": ["jpeg", "jpg", "png"],
        "preprocessings": [
          {"resize": {"mode": "torchvision", "size": 256, "interpolation": "BILINEAR"}},
          {"centercrop": {"width": 224, "height": 224}},
          {"convertColor": {"form": "BGR2RGB"}},
          {"div": {"x": 255}},
          {"normalize": {"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}},
          {"transpose": {"axis": [2, 0, 1]}},
          {"expandDim": {"axis": 0}}
        ]
      }
    }
    ```

    ```bash
    dxcom -m resnet50.onnx -c resnet50_config.json -o output/resnet50 --opt_level 1
    ```

=== "Python"
    `compile_resnet50.py`:

    ```python
    import os

    from PIL import Image
    from torch.utils.data import DataLoader, Dataset
    from torchvision import transforms

    import dx_com


    class ImageNetDataset(Dataset):
        def __init__(self, image_dir, img_size=224):
            self.image_dir = image_dir
            self.image_files = sorted(
                f for f in os.listdir(image_dir) if f.endswith((".jpg", ".png", ".jpeg"))
            )
            self.transform = transforms.Compose([
                transforms.Resize(256),  # shorter side to 256, same as the CLI config
                transforms.CenterCrop(img_size),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])

        def __len__(self):
            return len(self.image_files)

        def __getitem__(self, idx):
            path = os.path.join(self.image_dir, self.image_files[idx])
            return self.transform(Image.open(path).convert("RGB"))


    dataset = ImageNetDataset("./calibration_dataset")
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

    dx_com.compile(
        model="resnet50.onnx",
        output_dir="output/resnet50",
        dataloader=dataloader,
        calibration_method="ema",
        calibration_num=100,
        opt_level=1,
    )
    print("ResNet50 compilation complete!")
    ```

    ```bash
    python3 compile_resnet50.py
    ```

## Multi input model

A stereo camera model with two image inputs of different sizes. Only the Python API supports more than one input.

```python
import os

from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

import dx_com

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])


class StereoDataset(Dataset):
    def __init__(self, left_dir, right_dir):
        # Keys MUST match the ONNX input names exactly.
        self.dirs = {"left_input": left_dir, "right_input": right_dir}
        self.image_files = sorted(f for f in os.listdir(left_dir) if f.endswith((".jpg", ".png")))
        self.transform = {
            "left_input": transforms.Compose([
                transforms.Resize((128, 128)), transforms.ToTensor(), normalize,
            ]),
            "right_input": transforms.Compose([
                transforms.Resize((256, 256)), transforms.ToTensor(), normalize,
            ]),
        }

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        name = self.image_files[idx]
        sample = {}
        for input_name, folder in self.dirs.items():
            image = Image.open(os.path.join(folder, name)).convert("RGB")
            sample[input_name] = self.transform[input_name](image)
        return sample  # dict keyed by ONNX input name


dataset = StereoDataset(left_dir="./calibration_left", right_dir="./calibration_right")
dataloader = DataLoader(dataset, batch_size=1)

dx_com.compile(
    model="stereo_model.onnx",
    output_dir="output/stereo",
    dataloader=dataloader,
    calibration_method="ema",
    calibration_num=50,
    opt_level=1,
)
```

* Return a `dict[str, torch.Tensor]` keyed by ONNX input name. DX-COM maps a dict by name. A tuple or list also works, but it is mapped by the model's internal input order, which can differ from yours.
* Each tensor has its input shape without the batch axis, as `float32`. `batch_size` is 1.
* Each input can have its own size and preprocessing.
* `enhanced_scheme` is not supported for multi input models.

## Edge device with a weak CPU

On embedded hosts, put as many operations as possible on the NPU with aggressive partitioning (experimental). `opt_level` 0 shortens the compile, but NPU latency can be higher than with 1.

`config.json`:

```json
{
  "inputs": {
    "input": [1, 3, 224, 224]
  },
  "calibration_method": "ema",
  "calibration_num": 50,
  "default_loader": {
    "dataset_path": "./calibration_dataset",
    "file_extensions": ["jpeg", "jpg", "png"],
    "preprocessings": [
      {"resize": {"width": 224, "height": 224}},
      {"convertColor": {"form": "BGR2RGB"}},
      {"div": {"x": 255}},
      {"normalize": {"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}},
      {"transpose": {"axis": [2, 0, 1]}},
      {"expandDim": {"axis": 0}}
    ]
  }
}
```

=== "CLI"
    ```bash
    dxcom -m efficient_model.onnx -c config.json -o output/efficient \
      --aggressive_partitioning --opt_level 0
    ```

=== "Python"
    ```python
    import dx_com

    dx_com.compile(
        model="efficient_model.onnx",
        output_dir="output/efficient",
        config="config.json",
        aggressive_partitioning=True,
        opt_level=0,
    )
    ```

| Pros | Cons |
|---|---|
| More operations run on the NPU, much lower host CPU load. | Compile time and memory use can grow. On a fast host CPU the default partitioning can give better end to end performance. Some models can give unexpected results. |

## Non image data

Audio spectrograms, time series or point clouds need a `DataLoader`. The `dxcom` CLI reads only image files.

```python
import os

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset

import dx_com


class SpectrogramDataset(Dataset):
    """Each .npy file holds one spectrogram of shape (64, 128). The model input is [1, 1, 64, 128]."""

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.data_files = sorted(f for f in os.listdir(data_dir) if f.endswith(".npy"))

    def __len__(self):
        return len(self.data_files)

    def __getitem__(self, idx):
        data = np.load(os.path.join(self.data_dir, self.data_files[idx]))
        data = (data - data.min()) / (data.max() - data.min() + 1e-8)  # scale to [0, 1]
        return torch.from_numpy(data.astype(np.float32)).unsqueeze(0)  # (1, 64, 128)


dataloader = DataLoader(SpectrogramDataset("./spectrogram_data"), batch_size=1)

dx_com.compile(
    model="audio_model.onnx",
    output_dir="output/audio_model",
    dataloader=dataloader,
    calibration_method="minmax",  # minmax often works better for non image data
    calibration_num=100,
)
```

## Better accuracy with DXQ and Q-PRO

When standard quantization loses too much accuracy, try automatic Q-PRO first, then a manual DXQ scheme. Use one of them, not both. See [Quantization](quantization.md).

Automatic Q-PRO:

=== "CLI"
    ```bash
    dxcom -m large_model.onnx -c config.json -o output/large_model_qpro --use_q_pro
    ```

=== "Python"
    ```python
    import dx_com

    dx_com.compile(
        model="large_model.onnx",
        output_dir="output/large_model_qpro",
        config="config.json",
        use_q_pro=True,
    )
    ```

Manual DXQ-P3:

=== "CLI"
    Add to `config.json`:

    ```json
    {
      "enhanced_scheme": {
        "DXQ-P3": {"num_samples": 1024}
      }
    }
    ```

    ```bash
    dxcom -m large_model.onnx -c config.json -o output/large_model_dxq
    ```

=== "Python"
    ```python
    import dx_com

    dx_com.compile(
        model="large_model.onnx",
        output_dir="output/large_model_dxq",
        config="config.json",  # without an enhanced_scheme key
        enhanced_scheme={"DXQ-P3": {"num_samples": 1024}},
    )
    ```

DX-COM uses the GPU when one is available. On a multi GPU host, pick one with `CUDA_VISIBLE_DEVICES=1`.

## Diagnose and re-quantize

Find which regions lose accuracy, then try new settings without compiling from ONNX again.

1. Compile with diagnosis:

    ```bash
    dxcom -m large_model.onnx -c config.json -o output/large_model --quant_diagnosis
    ```

    This writes `output/large_model/quant_diagnosis/large_model.qxnn` and `output/large_model/quant_diagnosis/diagnosis_report.html`.

1. Open the HTML report and read the recommended settings.

1. Re-quantize from the checkpoint, for example with the `iqr` method:

    ```bash
    dxcom \
      --checkpoint output/large_model/quant_diagnosis/large_model.qxnn \
      -o output/large_model_iqr \
      --recalibration_method iqr
    ```

Python versions and all resume options: [Diagnose and re-quantize](quantization.md#diagnose-and-re-quantize).

## YOLO post processing on a weak CPU

On a host such as an ARM Cortex-A53, YOLO CPU post processing over the full anchor grid can be the bottleneck. `pre_optimize` runs TopK first so the expensive steps see only `K` candidates. The tensor names are examples: look up your own with the [script](pre-optimize.md#script-for-yolo).

=== "Python"
    ```python
    import onnx
    import dx_com

    model = onnx.load("yolov8n.onnx")
    optimized = dx_com.pre_optimize(model, passes={
        "yolo_dfl_postprocess": {
            "task": "base",
            "layers": [
                {"bbox": "onnx::Concat_328", "cls_conf": "onnx::Concat_335"},
                {"bbox": "onnx::Concat_343", "cls_conf": "onnx::Concat_350"},
                {"bbox": "onnx::Concat_358", "cls_conf": "onnx::Concat_365"},
            ],
            "num_classes": 80,
            "topk": 300,
        },
    })

    dx_com.compile(model=optimized, config="config.json", output_dir="./optimized")
    ```

=== "Config"
    Add the block to a YOLO config (see [Config file reference](config-reference.md#complete-working-example)):

    ```json
    {
      "pre_optimize": [
        {
          "yolo_dfl_postprocess": {
            "task": "base",
            "layers": [
              {"bbox": "onnx::Concat_328", "cls_conf": "onnx::Concat_335"},
              {"bbox": "onnx::Concat_343", "cls_conf": "onnx::Concat_350"},
              {"bbox": "onnx::Concat_358", "cls_conf": "onnx::Concat_365"}
            ],
            "num_classes": 80,
            "topk": 300
          }
        }
      ]
    }
    ```

    ```python
    import dx_com

    dx_com.compile(model="yolov8n.onnx", config="config.json", output_dir="./optimized")
    ```

Do not combine with `ppu`. All passes and models: [Pre Optimize API](pre-optimize.md).

## YOLO with the PPU

Move confidence filtering and class prediction of a YOLOv8 model onto the NPU Post Processing Unit. NMS still runs on the host CPU. Do not combine with `pre_optimize`.

=== "CLI"
    `yolov8_config.json`:

    ```json
    {
      "inputs": {
        "images": [1, 3, 640, 640]
      },
      "calibration_method": "ema",
      "calibration_num": 100,
      "default_loader": {
        "dataset_path": "./calibration_dataset",
        "file_extensions": ["jpeg", "jpg", "png"],
        "preprocessings": [
          {"convertColor": {"form": "BGR2RGB"}},
          {"resize": {"width": 640, "height": 640}},
          {"div": {"x": 255}},
          {"transpose": {"axis": [2, 0, 1]}},
          {"expandDim": {"axis": 0}}
        ]
      },
      "ppu": {
        "type": 1,
        "conf_thres": 0.25,
        "num_classes": 80,
        "layer": [
          {"bbox": "Mul_441", "cls_conf": "Sigmoid_442"}
        ]
      }
    }
    ```

    ```bash
    dxcom -m yolov8.onnx -c yolov8_config.json -o output/yolov8
    ```

=== "Python"
    Use the same config without the `ppu` block, saved as `yolov8_base_config.json`:

    ```python
    import dx_com
    from dx_com import PPUConfig, PPUTypes

    ppu_config = (
        PPUConfig()
        .set_type(PPUTypes.YOLO_ANCHORFREE)
        .set_num_classes(80)
        .set_conf_thres(0.25)
    )
    ppu_config.add_layer(bbox="Mul_441", cls_conf="Sigmoid_442")

    dx_com.compile(
        model="yolov8.onnx",
        output_dir="output/yolov8",
        config="yolov8_base_config.json",
        ppu_config=ppu_config,
    )
    ```

For anchor based models (YOLOv5, YOLOv7) use type 0 with `activation` and a dict `layer`. See [PPU for YOLO models](ppu.md).

## Next steps

* [Run the model with DX-RT](../runtime/index.md)
* [Summary report](summary-report.md)
* [Troubleshooting](troubleshooting.md)
