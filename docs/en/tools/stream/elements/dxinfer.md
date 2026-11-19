---
title: DxInfer
description: Reference for the dxinfer element, which runs a compiled .dxnn model on the DEEPX NPU.
---

# DxInfer

`dxinfer` runs a compiled `.dxnn` model on the NPU. It reads the input tensor that [DxPreprocess](dxpreprocess.md) stored under `preprocess-id` and stores the output tensors under `inference-id` for [DxPostprocess](dxpostprocess.md). Always use the chain `dxpreprocess ! dxinfer ! dxpostprocess`, with the same `secondary-mode` setting on all three.

## Example

```bash
gst-launch-1.0 urisourcebin uri=file://$PWD/dx_stream/samples/videos/boat.mp4 ! decodebin ! queue max-size-buffers=1 ! \
  dxpreprocess preprocess-id=1 resize-width=640 resize-height=640 ! queue max-size-buffers=1 ! \
  dxinfer preprocess-id=1 inference-id=1 model-path=$PWD/dx_stream/samples/models/yolo26-n_640x640.dxnn ! queue max-size-buffers=1 ! \
  dxpostprocess inference-id=1 library-file-path=/usr/local/share/gstdxstream/lib/libpostprocess_yolo26od.so function-name=PostProcess ! queue max-size-buffers=1 ! \
  dxosd ! videoconvert ! fpsdisplaysink sync=false
```

Use `dxparse -m <model>.dxnn` (old name `parse_model`) to see the model's input and output tensors.

## Behavior

* **Backend**: `backend=auto` picks an available backend; `dxrt` uses DX-RT; `dxvnpu` uses the DX-H1 V-NPU (needs the V-NPU plugin from `./build.sh --dxvnpu`).
* **ONNX Runtime**: `use-ort=true` (default) lets DX-RT run parts of the model that are not on the NPU (for example the CPU tail of a model) with ONNX Runtime. The PPU sample config sets `use_ort` to `false`.
* **QoS**: when the sink has `sync=true`, late buffers are dropped.
* **Throttling**: when a downstream `dxrate throttle=true` sends Throttle QoS events, `dxinfer` drops input frames until enough time has passed, so the NPU does not process frames that `dxrate` would drop anyway. The delay comes from the event; it is not a property.
* **Latency**: the element adds its moving average inference time to `LATENCY` queries.
* **Multi stream**: in the domain, the stream comes from `DXFrameMeta._stream_id`; all streams share one NPU.
* **Errors**: a missing model file or an NPU init failure posts a GStreamer error on the bus.

## Pads

| Pad | Caps |
|---|---|
| sink | `video/x-raw`; `application/x-dxvideoraw` |
| src | `video/x-raw`; `application/x-dxvideoraw` |

## Properties

| Name | Type | Default | Range | Description |
|---|---|---|---|---|
| `config-file-path` | string | none | | JSON file with any of the properties below. |
| `model-path` | string | none | | Path to the `.dxnn` model. |
| `preprocess-id` | uint | `0` | 0 to 10000 | Input tensor to use. Must match the upstream `dxpreprocess`. |
| `inference-id` | uint | `0` | 0 to 10000 | ID under which output tensors are stored. |
| `secondary-mode` | bool | `false` | | Run once per object instead of once per frame. |
| `use-ort` | bool | `true` | | Use ONNX Runtime for parts not on the NPU. |
| `backend` | enum | `auto` | `auto`, `dxrt`, `dxvnpu` | Inference backend. |

JSON example (`dx_stream/configs/YoloV5S_PPU/inference_config.json`, path relative to the repository root):

```json
{
    "preprocess_id": 1,
    "inference_id": 1,
    "model_path" : "./dx_stream/samples/models/yolov5-s_640x640_ppu.dxnn",
    "use_ort": false
}
```

## Next steps

* [DxPostprocess](dxpostprocess.md)
* [Write an application](../write-an-application.md)
* [DX-RT overview](../../../runtime/index.md)
