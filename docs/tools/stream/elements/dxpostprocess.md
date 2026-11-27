---
title: DxPostprocess
description: Reference for the dxpostprocess element and the postprocess libraries that ship with DX-Stream.
---

# DxPostprocess

`dxpostprocess` calls a model specific function that turns the output tensors of [DxInfer](dxinfer.md) (stored under `inference-id`) into results in the metadata: new `DXObjectMeta` objects, or frame level maps such as segmentation and depth.

## Example

```bash
gst-launch-1.0 urisourcebin uri=file://$PWD/dx_stream/samples/videos/boat.mp4 ! decodebin ! queue ! \
  dxpreprocess preprocess-id=1 resize-width=640 resize-height=640 ! queue ! \
  dxinfer preprocess-id=1 inference-id=1 model-path=$PWD/dx_stream/samples/models/yolo26-n_640x640.dxnn ! queue ! \
  dxpostprocess inference-id=1 library-file-path=/usr/local/share/gstdxstream/lib/libpostprocess_yolo26od.so function-name=PostProcess ! queue ! \
  dxosd ! videoconvert ! autovideosink
```

## Behavior

* **Primary mode**: the function creates new objects and adds them to `DXFrameMeta`.
* **Secondary mode** (`secondary-mode=true`): the function is called per object and updates the existing `DXObjectMeta`. Do not remove or reallocate it.
* The element is stateless and works the same inside and outside the multi stream domain.
* An exception thrown by the library becomes a GStreamer error on the bus.

The function signature:

```cpp
extern "C" void PostProcess(GstBuffer *buf,
                            std::vector<dxs::DXTensor> network_output,
                            DXFrameMeta *frame_meta,
                            DXObjectMeta *object_meta);
```

See [Write an application](../write-an-application.md#custom-postprocess-library) to write your own.

## Shipped postprocess libraries

`./build.sh` installs these to `<prefix>/share/gstdxstream/lib/` (default `/usr/local/share/gstdxstream/lib/`). Source: `dx_stream/custom_library/postprocess_library/`.

| Library file | Functions |
|---|---|
| `libpostprocess_yolo26od.so` | `PostProcess` |
| `libpostprocess_yolo26pose.so` | `PostProcess` |
| `libpostprocess_yolo26seg.so` | `PostProcess` |
| `libpostprocess_yolo26depth.so` | `PostProcess` |
| `libpostprocess_yolo26obb.so` | `PostProcess` |
| `libpostprocess_yolo26cls.so` | `PostProcess` |
| `libpostprocess_ppu.so` | `YOLOV5S_PPU`, `YOLOV5Pose_PPU`, `SCRFD500M_PPU`, `SCRFD500M_PPU_SECOND` |
| `libpostprocess_yolov5s_face.so` | `PostProcess`, `PostProcess_Secondary` |
| `libpostprocess_scrfd500m.so` | `PostProcess` |
| `libpostprocess_object_class.so` | `PostProcess` |
| `libpostprocess_yolov5s_6.so` | `PostProcess` |
| `libpostprocess_yolov7.so` | `PostProcess` |
| `libpostprocess_yolov8n.so` | `PostProcess` |
| `libpostprocess_yolov8m_pose.so` | `PostProcess` |
| `libpostprocess_yolov9s.so` | `PostProcess` |
| `libpostprocess_yoloxs.so` | `PostProcess` |
| `libpostprocess_yolov11.so` | `PostProcess` |

## Pads

| Pad | Caps |
|---|---|
| sink | `video/x-raw`; `application/x-dxvideoraw` |
| src | `video/x-raw`; `application/x-dxvideoraw` |

## Properties

| Name | Type | Default | Range | Description |
|---|---|---|---|---|
| `config-file-path` | string | none | | JSON file with any of the properties below. |
| `inference-id` | uint | `0` | 0 to 1000 | Output tensors to read. Must match `dxinfer inference-id`. |
| `secondary-mode` | bool | `false` | | Update existing objects instead of creating new ones. |
| `library-file-path` | string | none | | Postprocess library (`.so`). |
| `function-name` | string | none | | Function to call in that library. |

JSON example (`dx_stream/configs/YoloV5S_PPU/postprocess_config.json`):

```json
{
    "inference_id": 1,
    "library_file_path": "/usr/local/share/gstdxstream/lib/libpostprocess_ppu.so",
    "function_name": "YOLOV5S_PPU"
}
```

## Next steps

* [DxTracker](dxtracker.md)
* [DxOsd](dxosd.md)
* [Write an application](../write-an-application.md)
