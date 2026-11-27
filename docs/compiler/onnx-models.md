---
title: Prepare an ONNX model
description: Export a PyTorch model to ONNX for DX-COM and check it against the list of supported ONNX operators.
---

# Prepare an ONNX model

This page lets you export your model to an ONNX file that DX-COM can compile, and check which ONNX operators run on the NPU.

## Before you start

* Install DX-COM: see [Install](../get-started/install.md). It also installs `torch` and `onnx`.
* A trained PyTorch model (or an ONNX file from another framework).

## Rules for the ONNX file

| Rule | Value |
|---|---|
| ONNX opset | 11 to 21. Opset 22 and newer are not supported. We recommend 17. |
| Batch size | Must be 1. |
| Input shape | Static. Do not use `dynamic_axes`: dynamic shapes are not supported. |
| Inputs | One input for the `dxcom` CLI. Multi input models need the [Python API](python-api.md#calibrate-with-a-dataloader). |
| Operators | Only the [supported operators](#supported-onnx-operators). Unsupported parts run on the host CPU or fail. |

If your model needs several input sizes, export and compile one `.dxnn` per size.

## Export from PyTorch

```python
import torch
import torch.nn as nn


class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 5)

    def forward(self, x):
        return self.linear(x)


model = SimpleModel()
model.eval()  # inference mode: affects Dropout and BatchNorm

# Dummy input with the model input shape. Batch size must be 1.
dummy_input = torch.randn(1, 10)

torch.onnx.export(
    model,
    dummy_input,
    "simple_model.onnx",
    export_params=True,       # store the weights in the ONNX file
    opset_version=17,         # DX-COM supports opset 11 to 21
    input_names=["input"],
    output_names=["output"],
    dynamo=False,             # legacy exporter, see the note below
)
```

| Argument | Description |
|---|---|
| `model` | The PyTorch model, in `eval()` mode. |
| `dummy_input` | An input for `forward()`. Used only to trace the graph. A tuple works for several inputs. |
| `export_params` | `True` stores the weights in the ONNX file. |
| `opset_version` | ONNX opset, 11 to 21. |
| `input_names`, `output_names` | Names of the ONNX input and output tensors. You use the input name in the config `inputs` key. |
| `dynamo` | `False` selects the legacy exporter. |

!!! warning "Set dynamo=False"
    Since PyTorch 2.9, `torch.onnx.export` uses the dynamo exporter by default. It needs the `onnxscript` package, which `pip install dx-com` does not install. Without `dynamo=False` the export fails with `ModuleNotFoundError: No module named 'onnxscript'`. Either pass `dynamo=False` or run `pip install onnxscript`.

For Ultralytics YOLO models, use the Ultralytics exporter (`model.export(format="onnx", ...)`). A manual `torch.onnx.export` of a YOLO model can produce extra outputs.

## Check the exported model

Check the file and print the input name and shape for your config:

```python
import onnx

model = onnx.load("simple_model.onnx")
onnx.checker.check_model(model)
print("opset:", model.opset_import[0].version)
for inp in model.graph.input:
    shape = [d.dim_value for d in inp.type.tensor_type.shape.dim]
    print(f'"{inp.name}": {shape}')
```

```text
opset: 17
"input": [1, 10]
```

Every dimension must be a positive integer. A `0` means a dynamic dimension: export again without `dynamic_axes`. Copy the printed `"name": [shape]` line into the `inputs` key of your [config file](config-reference.md#inputs).

## Supported ONNX operators

These limits apply to every operator:

* Width and height below 8,192.
* Channels below 32,768.
* No dynamic shapes.
* Element wise `Add`, `Div`, `Mul` and `Sub` do not support channel wise broadcasting when the channel size is greater than 1. For example, a 1x24x24x1 (NHWC) tensor cannot be broadcast to 1x24x24x32.

Support can also depend on how operations are combined in a model. Use this list as a guideline.

### Normal operations

| Operator | Supported conditions |
|---|---|
| Add | As bias addition (part of `Gemm` or `Conv`), element wise addition, input normalization, or constant scalar addition. |
| ArgMax | Only when all hold: it is the last operation of the network, the input is 2D or 4D, and it works along the channel axis. |
| AveragePool | `kernel_shape` < 32, `strides` < 32. |
| BatchNormalization | No restrictions. |
| Clip | Only as an activation (for example ReLU6). |
| Concat | No restrictions. |
| Constant | Only numeric constants. |
| ConstantOfShape | No restrictions. |
| Conv | All: `dilations` < 64, `pads` < 64, `strides` < 16.<br>Standard Conv: `kernel_shape` < 16.<br>Depth wise Conv: `kernel_shape` < 16; `dilations` = [1, 1], except a 3×3 kernel with `dilations` = [2, 2]; constant weights only.<br>5D input (3 spatial axes), new in 2.5.0: also `group` = 1, `dilations` = [1, 1, 1], `auto_pad` = `NOTSET`, weight is a compile time constant. Otherwise it runs on CPU. |
| ConvTranspose | `dilations` = [1, 1]; `output_padding` = [0, 0]; `pads` ≤ 14; `strides` in [2, 8] and symmetric (`strides[0]` = `strides[1]`); `kernel_shape` < 16; `group` = 1.<br>5D input (3 spatial axes), new in 2.5.0: also `group` = 1, `dilations` = [1, 1, 1], `output_padding` = [0, 0, 0], `auto_pad` = `NOTSET`, no `output_shape` attribute. Otherwise it runs on CPU. |
| Div | As constant scalar division, input normalization, part of `Softmax`, or part of `LayerNorm`. |
| Dropout | Removed for inference. |
| Einsum | New in 2.5.0. Only two input equations that reduce to a (batched) matrix multiplication: exactly one contracted index shared by both inputs; each input has exactly one free index that is neither batch nor contracted, and it appears in the output; leading indices that are the same in both inputs and the output are batch axes. Examples: `ij,jk->ik`, `bij,bjk->bik`, `bik,bjk->bij`. Single input equations (diagonal, transpose, reduction) and equations with three or more inputs are not supported. |
| Erf | Only as part of `GELU`. |
| Flatten | No restrictions. |
| Gather | `indices` is a 0D, 1D or 2D tensor. Examples: `[0]`, `[0, 2, 5]`, and (new in 2.5.0) `[[0, 2], [1, 3]]`. |
| Gemm | No restrictions. |
| GlobalAveragePool | No restrictions. |
| Identity | No restrictions. |
| LayerNormalization | Only over the last axis: `axis` = -1 (or the last axis index); `Scale` and `B` have shape [D], where D is the last axis size (`B` optional); D < 4080, otherwise CPU. Normalizing over several axes (for example PyTorch `nn.LayerNorm([C, H, W])`) is not supported.<br>A LayerNorm built from `ReduceMean`, `Sub`, `Pow`, `Sqrt`, `Div`, `Mul` and `Add` is also supported when mean and variance use one axis (the last axis, or the channel axis of an NCHW tensor such as ConvNeXt `LayerNorm2d`). Over several axes it runs on CPU. |
| MatMul | No restrictions. |
| MaxPool | `kernel_shape` < 16, `strides` < 16. |
| Mul | As element wise multiplication, constant scalar multiplication, or input normalization. |
| Pad | Only `mode=constant`, and it must come before a `Pool` or `Conv`. |
| ReduceMean | Only along the channel axis, or along width and height. |
| ReduceSum | Only along the channel axis. |
| Reshape | No restrictions. |
| Resize | Only with `coordinate_transformation_mode` = `pytorch_half_pixel` and `mode` = `nearest` or `linear`. See [Resize scale factors](#resize-scale-factors). |
| Shape | Cannot be a model output. |
| Slice | No restrictions. |
| Softmax | Only when the input size along `axis` is < 4080. |
| Split | No restrictions. |
| Squeeze | No restrictions. |
| Sub | As element wise subtraction, constant scalar subtraction, or input normalization. |
| Transpose | No restrictions. |

### Resize scale factors

| Direction | `mode` | Supported scale factor `s` |
|---|---|---|
| Upsampling (`s` > 1) | `linear` | Integers 2 or larger, except primes larger than 8. So 11, 13, 17 are not supported, while 9 and 10 are. |
| Upsampling (`s` > 1) | `nearest` | Powers of two only: 2, 4, 8, 16 and so on. |
| Downsampling (`s` < 1) | `linear` | Only 0.5. |
| Downsampling (`s` < 1) | `nearest` | Not supported. |

### Activation functions

| Operator | Supported conditions |
|---|---|
| Elu | No restrictions. |
| Gelu | No restrictions. |
| HardSigmoid | No restrictions. |
| HardSwish | No restrictions. |
| LeakyRelu | No restrictions. |
| Mish | No restrictions. |
| PRelu | Works, but see the known issue below. |
| Relu | No restrictions. |
| Selu | No restrictions. |
| Sigmoid | No restrictions. |
| Silu (Swish) | No restrictions. |
| Softplus | No restrictions. |
| Tanh | No restrictions. |

!!! warning "Known issue: PRelu"
    Models that use `PRelu` as activation show a large FPS drop on the NPU. Use `LeakyRelu` or `Relu` where you can until a future release fixes this.

### Deprecated operations

ONNX deprecated these operators. We keep them only for older models. Use the newer operator where you can.

| Operator | Supported conditions |
|---|---|
| Upsample | Only when the scale values for the N and C axes are 1. |

## Next steps

* [Config file reference](config-reference.md)
* [Compile a model](compile-a-model.md)
* [Troubleshooting](troubleshooting.md)
