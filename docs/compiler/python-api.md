---
title: DX-COM Python API
description: Reference for dx_com.compile(), calibration with a PyTorch DataLoader, PPUConfig and QMasterConfig.
---

# DX-COM Python API

This page lets you compile models from Python code with `dx_com.compile()`, including multi input models and non image data.

## Before you start

* Install DX-COM: see [Install](../get-started/install.md). The pip package `dx-com` installs the `dx_com` module and the `dxcom` command.
* Check it with `python3 -c "import dx_com; print(dx_com.__version__)"`.

## When to use Python instead of the CLI

| Need | CLI (`dxcom`) | Python (`dx_com.compile()`) |
|---|---|---|
| Single input image model | Yes | Yes |
| Multi input model | No | Yes, with a `DataLoader` |
| Non image data (audio, time series, point clouds) | No | Yes, with a `DataLoader` |
| Model already loaded as `onnx.ModelProto` | No | Yes |
| Run `dx_com.pre_optimize()` before compiling | No (use the JSON `pre_optimize` block) | Yes |

## Quick example

```python
import dx_com

dx_com.compile(
    model="model.onnx",
    output_dir="./compiled",
    config="config.json",
)
```

`compile()` returns `None` and writes its results to `output_dir`. Always call it with keyword arguments.

## dx_com.compile()

```python
def compile(
    model: Union[str, onnx.ModelProto],
    output_dir: str,
    config: Optional[str] = None,
    dataloader: Optional[DataLoader] = None,
    calibration_method: str = "ema",
    calibration_num: int = 100,
    use_gpu: bool = True,
    opt_level: int = 1,
    aggressive_partitioning: bool = False,
    input_nodes: Optional[List[str]] = None,
    output_nodes: Optional[List[str]] = None,
    use_q_pro: bool = False,
    enhanced_scheme: Optional[Dict] = None,
    ppu_config: Optional[PPUConfig] = None,
    qmaster: Optional[QMasterConfig] = None,
    gen_log: bool = False,
    float64_calibration: bool = False,
    export_html: bool = False,
    verbose: bool = False,
    **kwargs,
) -> None
```

`compile()` also takes the diagnosis and resume arguments `quant_diagnosis`, `checkpoint`, `recalibration_method` and `dataset_path`. Run `help(dx_com.compile)` for the docstring.

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `model` | `str` or `onnx.ModelProto` | required | Path to the ONNX file, or a loaded model. Not needed with `checkpoint`. |
| `output_dir` | `str` | required | Directory for the `.dxnn` file and other outputs. |
| `config` | `str` | `None` | Path to the JSON config. Give `config` or `dataloader`, never both. |
| `dataloader` | `torch.utils.data.DataLoader` | `None` | Calibration data from your own code. `batch_size` must be 1 (the model input batch). Give `config` or `dataloader`, never both. |
| `calibration_method` | `str` | `"ema"` | `"ema"`, `"minmax"` or `"iqr"`. See [Calibration](quantization.md#calibration). |
| `calibration_num` | `int` | `100` | Number of calibration samples. |
| `use_gpu` | `bool` | `True` | New in 2.5.0. `True` quantizes on GPU when available, else CPU. `False` forces CPU. Pass only `True` or `False`: any other value, including `None`, makes DX-COM fall back to its legacy compile path, which skips a JSON `pre_optimize` block and ignores `verbose`. |
| `opt_level` | `int` | `1` | `0` fast compile, `1` full optimization. |
| `aggressive_partitioning` | `bool` | `False` | Experimental. Puts as many operations as possible on the NPU. |
| `input_nodes` | `List[str]` | `None` | ONNX node names where compilation starts (partial compile). Node names, not tensor names. |
| `output_nodes` | `List[str]` | `None` | ONNX node names where compilation ends (partial compile). Node names, not tensor names. |
| `use_q_pro` | `bool` | `False` | Automatic Q-PRO. Do not combine with `enhanced_scheme` or `qmaster`. ONNX compile path only. |
| `enhanced_scheme` | `dict` | `None` | Manual DXQ scheme, for example `{"DXQ-P3": {"num_samples": 1024}}`. Not supported for multi input models. See [DXQ schemes](quantization.md#dxq-schemes). |
| `ppu_config` | `PPUConfig` | `None` | PPU settings for YOLO detection models. See [PPUConfig](#ppuconfig). |
| `qmaster` | `QMasterConfig` | `None` | New in 2.5.0. Runs Q-Master (QAT). See [QMasterConfig](#qmasterconfig). |
| `gen_log` | `bool` | `False` | Writes `compiler.log` in `output_dir`. |
| `float64_calibration` | `bool` | `False` | float64 precision in calibration for the same result on different CPUs. |
| `export_html` | `bool` | `False` | Writes `<model_name>_summary.html`. See [Summary report](summary-report.md). |
| `verbose` | `bool` | `False` | New in 2.5.0. Expands masked error messages. |
| `quant_diagnosis` | `bool` | `False` | Writes `quant_diagnosis/diagnosis_report.html` and `quant_diagnosis/<model>.qxnn`. |
| `checkpoint` | `str` | `None` | Path to a `.qxnn` file from `quant_diagnosis`. Selects resume mode. `model` and `config` are not needed. |
| `recalibration_method` | `str` | `None` | Resume mode only. `"minmax"`, `"ema"` or `"iqr"`. |
| `dataset_path` | `str` | `None` | Resume mode only. Replaces the calibration dataset path stored in the checkpoint. |

!!! warning "Removed in 2.5.0"
    * `quantization_device` is deprecated and ignored with a `UserWarning`. Use `use_gpu` and `CUDA_VISIBLE_DEVICES`.
    * `quantization_mode`, `qat_config`, `qat_skip_training` and `qat_resume_from_checkpoint` are replaced by `qmaster`. `quantization_mode` and `qat_skip_training` raise `InvalidValueError`. `qat_config` and `qat_resume_from_checkpoint` are ignored without an error, so their settings are not applied.
    * Unknown keyword arguments are ignored without an error. Check the spelling of every argument.

### Rules for combining arguments

| Do not combine | Why |
|---|---|
| `config` and `dataloader` | Give exactly one. Neither raises `ConfigFileError: Either CONFIG (config file path) or DATALOADER (PyTorch DataLoader) must be provided`. DX-COM 2.5.0 does not reject both, so the result is not defined: pass only one. |
| `use_q_pro` and `enhanced_scheme` | Automatic and manual Q-PRO: pick one. |
| `qmaster` and `use_q_pro` or `enhanced_scheme` | Raises `EnhancementSchemeError`: QAT and Q-PRO are mutually exclusive. |
| `checkpoint` and `model` | Resume mode works from the checkpoint only. |
| JSON `ppu` and JSON `pre_optimize` | Both rewrite detection post processing. See [Pre Optimize API](pre-optimize.md). |

### Output files

| File | When |
|---|---|
| `<model_name>.dxnn` | Always. The compiled model. |
| `compiler.log` | With `gen_log=True`. |
| `<model_name>_summary.html` | With `export_html=True`. |
| `quant_diagnosis/diagnosis_report.html`, `quant_diagnosis/<model>.qxnn` | With `quant_diagnosis=True`. |
| `qat_checkpoint/qat_checkpoint.qxnn` | With Q-Master. |

## Calibrate with a DataLoader

Use a `DataLoader` for multi input models, non image data, or preprocessing that the JSON operations cannot express. With a `DataLoader`, DX-COM does not read the JSON `default_loader`, so do all preprocessing inside your Dataset.

```python
import glob

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset

import dx_com


class NpyDataset(Dataset):
    """Each .npy file holds one preprocessed sample shaped like the model input without the batch axis, for example (3, 224, 224)."""

    def __init__(self, folder):
        self.files = sorted(glob.glob(f"{folder}/*.npy"))

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        return torch.from_numpy(np.load(self.files[idx]).astype(np.float32))


loader = DataLoader(NpyDataset("./calib_npy"), batch_size=1, shuffle=True)

dx_com.compile(
    model="model.onnx",
    output_dir="./output",
    dataloader=loader,
    calibration_method="ema",
    calibration_num=100,
)
```

Rules for the samples:

* DX-COM checks `next(iter(dataloader))`. The batched sample must match the ONNX input shape exactly, including the batch axis. So each `__getitem__` item is the input shape without the batch axis (`[3, 224, 224]` for an input `[1, 3, 224, 224]`), and `batch_size` equals the model batch (normally 1).
* Use `float32` tensors.
* Single input: return one `torch.Tensor`.
* Multi input: return a `dict[str, torch.Tensor]` keyed by ONNX input name (recommended). A list or tuple also works, but DX-COM maps it by the model's internal input order, which can differ from your order.
* The preprocessing must match what your application does at inference time. A mismatch (other mean and std, wrong channel order, missing `/255`) lowers accuracy without an error.

### Preprocessing in the Dataset

With `torchvision` (PIL, RGB):

```python
from PIL import Image
from torchvision import transforms

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),  # HWC uint8 to CHW float in [0, 1]
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def __getitem__(self, idx):
    image = Image.open(self.image_files[idx]).convert("RGB")
    return transform(image)  # shape [3, 224, 224]
```

With OpenCV and NumPy, which matches the JSON `default_loader` step by step:

```python
import cv2
import numpy as np
import torch


def __getitem__(self, idx):
    img = cv2.imread(self.image_files[idx])        # BGR, HWC, uint8
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)     # convertColor BGR2RGB
    img = cv2.resize(img, (224, 224))              # resize
    img = img.astype(np.float32) / 255.0           # div x=255
    mean = np.array([0.485, 0.456, 0.406], np.float32)
    std = np.array([0.229, 0.224, 0.225], np.float32)
    img = (img - mean) / std                       # normalize
    img = np.transpose(img, (2, 0, 1))             # transpose [2, 0, 1]
    return torch.from_numpy(img)                   # shape [3, 224, 224]
```

### JSON operations and their DataLoader equivalents

| JSON operation | Arguments | DataLoader equivalent |
|---|---|---|
| `resize` | `width`, `height` (or `size`), `mode`, `interpolation` | `cv2.resize(...)` or `transforms.Resize(...)` |
| `resize2`, `resize3`, `resize_tv` | Resize variants (`mlcommons`, `scale`, `torchvision` mode). `resize2` and `resize3` also need `scale`. Prefer `resize`. | Matching resize logic |
| `centercrop`, `centercrop2` | `width`, `height` | `img[top:top+h, left:left+w]` or `transforms.CenterCrop(...)` |
| `convertColor` | `form`, for example `BGR2RGB` | `cv2.cvtColor(...)` or `Image.convert("RGB")` |
| `div` | `x` (scalar or per channel list) | `img / x` (`div` 255 is what `transforms.ToTensor()` does) |
| `mul` | `x` | `img * x` |
| `subtract` | `x` | `img - x` |
| `add` | `x` | `img + x` |
| `normalize` | `mean`, `std` (lists) | `(img - mean) / std` or `transforms.Normalize(...)` |
| `transpose` | `axis`, for example `[2, 0, 1]` | `np.transpose(img, axis)` or `tensor.permute(...)` |
| `expandDim` | `axis` | `np.expand_dims(...)` or `tensor.unsqueeze(axis)` |
| `squeeze` | `axis` | `np.squeeze(...)` or `tensor.squeeze(axis)` |
| `slice` | `channel` | `img[..., channel]` |
| `dtype` | `t` (NumPy dtype) | `img.astype(t)` |
| `pil_2_cv` | none | PIL to NumPy BGR conversion |

## PPUConfig

`PPUConfig` is the Python form of the JSON `ppu` block. It turns on the NPU Post Processing Unit for YOLO detection models. See [PPU for YOLO models](ppu.md) for which type fits your model and how to find the node names.

```python
from dx_com import PPUConfig, PPUTypes
```

| `PPUTypes` | JSON `type` | Models |
|---|---|---|
| `PPUTypes.YOLO_BASE` | 0 | Anchor based: YOLOv3, YOLOv4, YOLOv5, YOLOv7 |
| `PPUTypes.YOLO_ANCHORFREE` | 1 | Anchor free: YOLOX, YOLOv8, YOLOv9, YOLOv10, YOLOv11, YOLOv12 |
| `PPUTypes.YOLOV8` | 2 | Deprecated since 2.4.0. DFL based CPU TopK for YOLOv8, YOLOv9, YOLOv11, YOLOv12. Use [Pre Optimize API](pre-optimize.md) instead. |

Build it in one call or step by step:

```python
from dx_com import PPUConfig, PPUTypes

# Type 0, anchor based, in one call
cfg = PPUConfig(
    type=PPUTypes.YOLO_BASE,
    conf_thres=0.25,
    activation="Sigmoid",
    num_classes=80,
    layer={
        "Conv_245": {"num_anchors": 3},
        "Conv_294": {"num_anchors": 3},
        "Conv_343": {"num_anchors": 3},
    },
)

# Type 1, anchor free (YOLOv8 to v12), step by step
cfg = (
    PPUConfig()
    .set_type(PPUTypes.YOLO_ANCHORFREE)
    .set_num_classes(80)
    .set_conf_thres(0.25)
)
cfg.add_layer(bbox="Mul_441", cls_conf="Sigmoid_442")
```

| Method | Purpose |
|---|---|
| `set_type(PPUTypes.*)` | Sets the PPU type. Resets `layer`. |
| `set_num_classes(int)` | Number of detection classes. |
| `set_conf_thres(float)` | Confidence threshold (type 0 and 1). |
| `set_activation(str)` | Activation, for example `"Sigmoid"` (type 0). |
| `set_topk(int)` | Number of TopK candidates (type 2). |
| `add_layer(...)` | Adds a detection head. Type 0: `add_layer("Conv_245", num_anchors=3)`. Type 1 and 2: `add_layer(bbox="...", cls_conf="...")` with optional `obj_conf=`. |
| `validate()` | Checks the required fields. `compile()` calls it and raises if a field is missing. |

How often to call `add_layer`:

* Type 1, YOLOX: once per detection scale, with `obj_conf=`.
* Type 1, YOLOv8 to v12: once, with the two nodes that feed the final output `Concat`: `bbox` (decoded boxes, usually a `Mul`) and `cls_conf` (a `Sigmoid`).
* Type 2: once per detection scale.

Pass it with a config that has no `ppu` block, or with a `dataloader`:

```python
dx_com.compile(
    model="yolov8.onnx",
    output_dir="output/yolov8",
    config="yolov8_base_config.json",  # no ppu block
    ppu_config=cfg,
)
```

## QMasterConfig

`QMasterConfig` runs Q-Master (quantization aware training) from Python. New in 2.5.0. See [Q-Master (QAT)](q-master.md) for the workflow and all training keys.

```python
from dx_com import QMasterConfig
```

| Field | Type | Default | Description |
|---|---|---|---|
| `config` | `dict` | `None` | Training settings: the same keys as the JSON `qmaster` block. Always set `batch_size` here. |
| `skip_training` | `bool` | `False` | Skips training and only compiles. Use with `resume_from_checkpoint`. |
| `resume_from_checkpoint` | `str` | `None` | Path to a `qat_checkpoint.qxnn` with trained weights. |

```python
import dx_com
from dx_com import QMasterConfig

# Train and compile
dx_com.compile(
    model="model.onnx",
    config="config.json",
    output_dir="output/",
    qmaster=QMasterConfig(config={"batch_size": 16, "train_limit": 2000, "epochs": 10}),
)

# Compile only, from a trained checkpoint
dx_com.compile(
    model="model.onnx",
    config="config.json",
    output_dir="output/",
    qmaster=QMasterConfig(
        skip_training=True,
        resume_from_checkpoint="output/qat_checkpoint/qat_checkpoint.qxnn",
    ),
)
```

A JSON config with a `qmaster` block also starts Q-Master, without the `qmaster` argument.

## Next steps

* [Use cases](use-cases.md)
* [Pre Optimize API](pre-optimize.md)
* [Quantization](quantization.md)
* [DX-RT Python API](../runtime/python-api.md)
