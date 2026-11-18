# Supported ONNX operators

When you build or export models to ONNX format, you **must** use only the operators listed here to ensure successful compilation and optimal NPU performance. Operators not in this list fall back to CPU execution.

## Common constraints

These limits apply to **all** operator types:

**Tensor shape**

- Width and height: < 8,192
- Channels: < 32,768
- Dynamic shapes are **not** supported — all input shapes must be static at compile time

**Broadcasting**

Channel-wise broadcasting is not supported in element-wise ops (Add, Div, Mul, Sub) when the channel dimension is > 1.

!!! example "Broadcasting example"
    A tensor of shape `1×24×24×1` (NHWC) **cannot** be broadcast to `1×24×24×32`.

## Normal operations

| Operator | Supported conditions |
|---|---|
| `Add` | Bias addition (as part of `Gemm` or `Conv`), element-wise addition, input normalization, constant scalar addition |
| `ArgMax` | Only when: it is the final op in the network; the preceding output is 2D or 4D; it operates along the channel dimension |
| `AveragePool` | `kernel_shape` < 32, `strides` < 32 |
| `BatchNormalization` | No restrictions |
| `Clip` | Only as an activation function (e.g. ReLU6) |
| `Concat` | No restrictions |
| `Constant` | Numeric constants only |
| `ConstantOfShape` | No restrictions |
| `Conv` | **Common:** `dilations` < 64, `pads` < 64, `strides` < 16, `kernel_shape` < 16<br>**Depth-wise:** `dilations` = [1,1] except 3×3 with `dilations` = [2,2]; constant weights only<br>**5D input:** `group` = 1, `dilations` = [1,1,1], `auto_pad` = `NOTSET`, constant weight; otherwise CPU |
| `ConvTranspose` | `dilations` = [1,1], `output_padding` = [0,0], `pads` ≤ 14, `strides` ∈ [2,8] and symmetric, `kernel_shape` < 16, `group` = 1<br>**5D input:** `group` = 1, `dilations` = [1,1,1], `output_padding` = [0,0,0], `auto_pad` = `NOTSET`, no `output_shape`; otherwise CPU |
| `Div` | Constant scalar division, input normalization, part of `Softmax`, part of `LayerNorm` |
| `Dropout` | Removed at inference time |
| `Einsum` | Two-input equations that reduce to a (batched) matrix multiply only. Examples: `ij,jk->ik`, `bij,bjk->bik`, `bik,bjk->bij`. Single-input equations and equations with 3+ inputs are not supported. |
| `Erf` | Only as part of `GELU` |
| `Flatten` | No restrictions |
| `Gather` | `indices` must be 0-D, 1-D, or 2-D tensor |
| `Gemm` | No restrictions |
| `GlobalAveragePool` | No restrictions |
| `Identity` | No restrictions |
| `LayerNormalization` | Normalizing over the last dimension only: `axis` = -1, Scale and B have shape [D] where D < 4080; otherwise CPU. Multi-dimension normalization not supported. Fused LayerNorm from primitives supported when reducing over a single dimension. |
| `MatMul` | No restrictions |
| `MaxPool` | `kernel_shape` < 16, `strides` < 16 |
| `Mul` | Element-wise multiplication, constant scalar multiplication, input normalization |
| `Pad` | `mode=constant` only; must precede a `Pool` or `Conv` operation |
| `ReduceMean` | Reducing along the channel dimension or (Width, Height) dimensions |
| `ReduceSum` | Reducing along the channel dimension only |
| `Reshape` | No restrictions |
| `Resize` | `coordinate_transformation_mode` = `pytorch_half_pixel`; `mode` ∈ {`nearest`, `linear`}<br>**Upsampling (linear):** integer scale ≥ 2, non-prime factors only (primes > 8 not supported)<br>**Upsampling (nearest):** powers of two only (2, 4, 8, 16, …)<br>**Downsampling (linear):** scale = 0.5 only<br>**Downsampling (nearest):** not supported |
| `Shape` | Cannot be used as a model output |
| `Slice` | No restrictions |
| `Softmax` | Input size along `axis` must be < 4080 |
| `Split` | No restrictions |
| `Squeeze` | No restrictions |
| `Sub` | Element-wise subtraction, constant scalar subtraction, input normalization |
| `Transpose` | No restrictions |

## Activation functions

| Operator | Supported conditions |
|---|---|
| `Elu` | No restrictions |
| `Gelu` | No restrictions |
| `HardSwish` | No restrictions |
| `HardSigmoid` | No restrictions |
| `LeakyRelu` | No restrictions |
| `Mish` | No restrictions |
| `PRelu` | No functional restrictions. **Known issue (v2.4.0):** significant FPS degradation on NPU — use `LeakyRelu` or `Relu` where possible until resolved. |
| `Relu` | No restrictions |
| `Selu` | No restrictions |
| `Sigmoid` | No restrictions |
| `Silu` / `Swish` | No restrictions |
| `Softplus` | No restrictions |
| `Tanh` | No restrictions |

## Deprecated operations

These operators are maintained for backward compatibility only. Avoid them in new models.

| Operator | Supported conditions |
|---|---|
| `Upsample` | Scale values in the N and C dimensions must be 1 |

!!! note
    Operator support may vary depending on how operations are combined within a model. For validation of specific use cases contact DEEPX technical support.

---

## Full ONNX opset 17 reference

**46 of 150** opset 17 operators run on the NPU. The remaining 104 compile and run correctly but execute on the host CPU. Use `--export_html` to inspect the partition split in the [summary report](summary-report.md).

??? note "Show full opset 17 operator table"

    | Operator | Execution |
    |---|---|
    | `Abs` | ⚠️ CPU |
    | `Acos` | ⚠️ CPU |
    | `Acosh` | ⚠️ CPU |
    | `Add` | ✅ NPU |
    | `AffineGrid` | ⚠️ CPU |
    | `And` | ⚠️ CPU |
    | `ArgMax` | ✅ NPU |
    | `ArgMin` | ⚠️ CPU |
    | `Asin` | ⚠️ CPU |
    | `Asinh` | ⚠️ CPU |
    | `Atan` | ⚠️ CPU |
    | `Atanh` | ⚠️ CPU |
    | `AveragePool` | ✅ NPU |
    | `BatchNormalization` | ✅ NPU |
    | `Bernoulli` | ⚠️ CPU |
    | `BitShift` | ⚠️ CPU |
    | `BlackmanWindow` | ⚠️ CPU |
    | `Cast` | ⚠️ CPU |
    | `Ceil` | ⚠️ CPU |
    | `Clip` | ✅ NPU |
    | `Compress` | ⚠️ CPU |
    | `Concat` | ✅ NPU |
    | `Constant` | ✅ NPU |
    | `ConstantOfShape` | ✅ NPU |
    | `Conv` | ✅ NPU |
    | `ConvTranspose` | ✅ NPU |
    | `Cos` | ⚠️ CPU |
    | `Cosh` | ⚠️ CPU |
    | `CumSum` | ⚠️ CPU |
    | `DFT` | ⚠️ CPU |
    | `DepthToSpace` | ⚠️ CPU |
    | `DequantizeLinear` | ⚠️ CPU |
    | `Det` | ⚠️ CPU |
    | `Div` | ✅ NPU |
    | `Dropout` | ✅ NPU |
    | `Einsum` | ✅ NPU |
    | `Elu` | ✅ NPU |
    | `Equal` | ⚠️ CPU |
    | `Erf` | ✅ NPU |
    | `Exp` | ⚠️ CPU |
    | `Expand` | ⚠️ CPU |
    | `EyeLike` | ⚠️ CPU |
    | `Flatten` | ✅ NPU |
    | `Floor` | ⚠️ CPU |
    | `GRU` | ⚠️ CPU |
    | `Gather` | ✅ NPU |
    | `GatherElements` | ⚠️ CPU |
    | `GatherND` | ⚠️ CPU |
    | `Gemm` | ✅ NPU |
    | `GlobalAveragePool` | ✅ NPU |
    | `GlobalLpPool` | ⚠️ CPU |
    | `GlobalMaxPool` | ⚠️ CPU |
    | `Greater` | ⚠️ CPU |
    | `GridSample` | ⚠️ CPU |
    | `GroupNormalization` | ⚠️ CPU |
    | `HammingWindow` | ⚠️ CPU |
    | `HannWindow` | ⚠️ CPU |
    | `HardSigmoid` | ✅ NPU |
    | `HardSwish` | ✅ NPU |
    | `Hardmax` | ⚠️ CPU |
    | `Identity` | ✅ NPU |
    | `If` | ⚠️ CPU |
    | `InstanceNormalization` | ⚠️ CPU |
    | `IsInf` | ⚠️ CPU |
    | `IsNaN` | ⚠️ CPU |
    | `LRN` | ⚠️ CPU |
    | `LSTM` | ⚠️ CPU |
    | `LayerNormalization` | ✅ NPU |
    | `LeakyRelu` | ✅ NPU |
    | `Less` | ⚠️ CPU |
    | `Log` | ⚠️ CPU |
    | `LogSoftmax` | ⚠️ CPU |
    | `Loop` | ⚠️ CPU |
    | `LpNormalization` | ⚠️ CPU |
    | `LpPool` | ⚠️ CPU |
    | `MatMul` | ✅ NPU |
    | `Max` | ⚠️ CPU |
    | `MaxPool` | ✅ NPU |
    | `MaxRoiPool` | ⚠️ CPU |
    | `MaxUnpool` | ⚠️ CPU |
    | `Mean` | ⚠️ CPU |
    | `MelWeightMatrix` | ⚠️ CPU |
    | `Min` | ⚠️ CPU |
    | `Mod` | ⚠️ CPU |
    | `Mul` | ✅ NPU |
    | `Multinomial` | ⚠️ CPU |
    | `Neg` | ⚠️ CPU |
    | `NonMaxSuppression` | ⚠️ CPU |
    | `NonZero` | ⚠️ CPU |
    | `Not` | ⚠️ CPU |
    | `OneHot` | ⚠️ CPU |
    | `Or` | ⚠️ CPU |
    | `PRelu` | ✅ NPU |
    | `Pad` | ✅ NPU |
    | `Pow` | ⚠️ CPU |
    | `QuantizeLinear` | ⚠️ CPU |
    | `RNN` | ⚠️ CPU |
    | `RandomNormal` | ⚠️ CPU |
    | `RandomNormalLike` | ⚠️ CPU |
    | `RandomUniform` | ⚠️ CPU |
    | `RandomUniformLike` | ⚠️ CPU |
    | `Range` | ⚠️ CPU |
    | `Reciprocal` | ⚠️ CPU |
    | `ReduceL1` | ⚠️ CPU |
    | `ReduceL2` | ⚠️ CPU |
    | `ReduceLogSum` | ⚠️ CPU |
    | `ReduceLogSumExp` | ⚠️ CPU |
    | `ReduceMax` | ⚠️ CPU |
    | `ReduceMean` | ✅ NPU |
    | `ReduceMin` | ⚠️ CPU |
    | `ReduceProd` | ⚠️ CPU |
    | `ReduceSum` | ✅ NPU |
    | `ReduceSumSquare` | ⚠️ CPU |
    | `Relu` | ✅ NPU |
    | `Reshape` | ✅ NPU |
    | `Resize` | ✅ NPU |
    | `ReverseSequence` | ⚠️ CPU |
    | `RoiAlign` | ⚠️ CPU |
    | `Round` | ⚠️ CPU |
    | `Scan` | ⚠️ CPU |
    | `Scatter` | ⚠️ CPU |
    | `ScatterElements` | ⚠️ CPU |
    | `ScatterND` | ⚠️ CPU |
    | `Selu` | ✅ NPU |
    | `Shape` | ✅ NPU |
    | `Sigmoid` | ✅ NPU |
    | `Sign` | ⚠️ CPU |
    | `Sin` | ⚠️ CPU |
    | `Sinh` | ⚠️ CPU |
    | `Size` | ⚠️ CPU |
    | `Slice` | ✅ NPU |
    | `Softmax` | ✅ NPU |
    | `Softplus` | ✅ NPU |
    | `Softsign` | ⚠️ CPU |
    | `SpaceToDepth` | ⚠️ CPU |
    | `Split` | ✅ NPU |
    | `Sqrt` | ⚠️ CPU |
    | `Squeeze` | ✅ NPU |
    | `StringNormalizer` | ⚠️ CPU |
    | `Sub` | ✅ NPU |
    | `Sum` | ⚠️ CPU |
    | `Tan` | ⚠️ CPU |
    | `Tanh` | ✅ NPU |
    | `Tile` | ⚠️ CPU |
    | `TopK` | ⚠️ CPU |
    | `Transpose` | ✅ NPU |
    | `Unique` | ⚠️ CPU |
    | `Unsqueeze` | ⚠️ CPU |
    | `Upsample` | ✅ NPU |
    | `Where` | ⚠️ CPU |
    | `Xor` | ⚠️ CPU |
