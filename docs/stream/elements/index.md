---
title: DX-Stream elements
description: List of all DX-Stream GStreamer elements, how to set their properties, and where each may be placed.
---

# DX-Stream elements

This page lists every DX-Stream element and the rules that apply to all of them. Each element has its own reference page with pads and properties.

## Element list

| Element | Factory name | Base class | What it does |
|---|---|---|---|
| [DxPreprocess](dxpreprocess.md) | `dxpreprocess` | GstBaseTransform | Turns a frame or object region into an input tensor (color conversion, crop, resize, padding). |
| [DxInfer](dxinfer.md) | `dxinfer` | GstElement | Runs a `.dxnn` model on the NPU. |
| [DxPostprocess](dxpostprocess.md) | `dxpostprocess` | GstBaseTransform | Turns output tensors into objects with a model specific library. |
| [DxTracker](dxtracker.md) | `dxtracker` | GstBaseTransform | Tracks objects across frames (OC_SORT). |
| [DxOsd](dxosd.md) | `dxosd` | GstBaseTransform | Draws boxes, labels, masks, depth, poses and landmarks on the frame. |
| [DxGather](dxgather.md) | `dxgather` | GstAggregator | Merges `tee` branches of one source back into one stream. |
| [DxInputSelector](dxinputselector.md) | `dxinputselector` | GstAggregator | Merges N streams into one, ordered by PTS. Entry of the multi stream domain. |
| [DxOutputSelector](dxoutputselector.md) | `dxoutputselector` | GstElement | Splits the merged stream back into N streams by `stream_id`. Exit of the domain. |
| [DxRate](dxrate.md) | `dxrate` | GstBaseTransform | Sets the output frame rate by dropping or duplicating frames. |
| [DxMsgConv](dxmsgconv.md) | `dxmsgconv` | GstBaseTransform | Converts inference metadata into message payloads (for example JSON). |
| [DxMsgBroker](dxmsgbroker.md) | `dxmsgbroker` | GstBaseSink | Publishes payloads to MQTT or Kafka. |
| [DxScale](dxscale.md) | `dxscale` | GstBaseTransform | Scales frames (NV12, I420, RGB, BGR). |
| [DxConvert](dxconvert.md) | `dxconvert` | GstBaseTransform | Converts between NV12, I420, RGB and BGR. |
| [DxVnpuDec](dxvnpudec.md) | `dxvnpudec` | GstVideoDecoder | Decodes H.264 and H.265 on the DX-H1 V-NPU. Needs `--dxvnpu`. |
| [DxVnpuEnc](dxvnpuenc.md) | `dxvnpuenc` | GstVideoEncoder | Encodes NV12 to H.264 or H.265 on the DX-H1 V-NPU. Needs `--dxvnpu`. |

Check what your build contains:

```bash
gst-inspect-1.0 dxstream
gst-inspect-1.0 dxinfer
```

The V-NPU elements live in a separate plugin file (`libgstdxstream-vnpu.so`) that `./build.sh --dxvnpu` adds.

## Setting properties

You set properties on the command line (`dxinfer model-path=model.dxnn`) or in a JSON file passed with `config-file-path`. `dxpreprocess`, `dxinfer`, `dxpostprocess`, `dxtracker` and `dxmsgconv` accept a JSON file.

In JSON the key is the property name with `_` instead of `-`: `preprocess-id` becomes `preprocess_id`, `library-file-path` becomes `library_file_path`.

```json
{
    "preprocess_id": 1,
    "inference_id": 1,
    "model_path": "./dx_stream/samples/models/yolov5-s_640x640_ppu.dxnn",
    "use_ort": false
}
```

!!! note "Relative paths"
    Relative paths in a JSON file (such as `model_path` above) are resolved from the current working directory, not from the JSON file. The shipped configs in `dx_stream/configs/` work only when you start the pipeline from the repository root. A property on the command line overrides the value from the file, so you can pass `model-path=` with an absolute path instead.

## Where elements may be placed

| Element | Single stream (`video/x-raw`) | Between DxInputSelector and DxOutputSelector |
|---|:-:|:-:|
| `dxpreprocess`, `dxinfer`, `dxpostprocess`, `dxtracker`, `dxosd`, `dxrate` | Yes | Yes |
| `dxmsgconv`, `dxmsgbroker` | Yes | Yes |
| `dxscale`, `dxconvert` | Yes | No |
| `dxgather` | Yes | No |
| `dxinputselector`, `dxoutputselector` | Not used | Boundary only |

[Multi stream domain](multi-stream-domain.md) explains why.

## Hardware backends for transforms

`dxpreprocess`, `dxscale` and `dxconvert` pick a transform backend at run time, in this order:

1. DEEPX V3 DSP, when the V3 backend plugin is installed (`--dxv3`).
1. DX-H1 V-NPU, when the V-NPU plugin is installed (`--dxvnpu`).
1. Rockchip RGA, when the RGA backend plugin is installed (built automatically with `librga`).
1. libyuv on the CPU, always available.

An OpenGL ES 3.0 backend (`gstdxstream-gles`) also exists. It is built automatically on ARM hosts with EGL and GLESv2 (validated on Raspberry Pi 5); other hosts need the Meson option `-Dwith_gles=enabled`. No configuration is needed at run time.

## Next steps

* [Multi stream domain](multi-stream-domain.md)
* [DxPreprocess](dxpreprocess.md)
* [Pipelines](../pipelines.md)
