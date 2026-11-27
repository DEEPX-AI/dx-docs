---
title: DxMsgConv
description: Reference for the dxmsgconv element, which turns inference metadata into message payloads with a converter library.
---

# DxMsgConv

`dxmsgconv` converts the inference metadata of each frame into a message payload and attaches it to the buffer for [DxMsgBroker](dxmsgbroker.md). A converter library decides the message format. The shipped library `libdx_msgconvl.so` produces JSON.

## Example

Run from the repository root with a broker on `localhost:1883` (see [Message broker pipelines](../pipelines.md#message-broker)):

```bash
gst-launch-1.0 -e urisourcebin uri=file://$PWD/dx_stream/samples/videos/boat.mp4 ! decodebin ! queue ! \
  dxpreprocess config-file-path=dx_stream/configs/YoloV5S_PPU/preprocess_config.json ! queue ! \
  dxinfer config-file-path=dx_stream/configs/YoloV5S_PPU/inference_config.json ! queue ! \
  dxpostprocess config-file-path=dx_stream/configs/YoloV5S_PPU/postprocess_config.json ! queue ! \
  dxosd ! queue ! \
  dxmsgconv config-file-path=dx_stream/configs/msgconv_config.json ! queue ! \
  dxmsgbroker broker-name=mqtt conn-info=localhost:1883 topic=test
```

`dx_stream/configs/msgconv_config.json`:

```json
{
    "library_file_path": "/usr/local/share/gstdxstream/lib/libdx_msgconvl.so",
    "message_interval": 1,
    "include_frame": true
}
```

## Behavior

* The element only reads metadata, never pixels, so it works inside and outside the multi stream domain.
* `message-interval=N` converts every Nth frame.
* `include-frame=true` encodes the frame as base64 JPEG and passes it to the library (`meta_info->_frame_base64`). It can still be `nullptr` when encoding fails.
* An exception thrown by the library becomes a GStreamer error.

The JSON of the shipped library:

```json
{
  "streamId": 0,
  "seqId": 123,
  "width": 1920,
  "height": 1080,
  "objects": [
    {
      "object": {
        "label_id": 1,
        "track_id": 42,
        "confidence": 0.87,
        "name": "person",
        "box": { "startX": 300.0, "startY": 400.0, "endX": 500.0, "endY": 600.0 },
        "body_feature": [0.321, 0.654, 0.987],
        "segment": { "height": 200, "width": 200, "format": "roi-binary-mask", "background_value": 0, "foreground_value": 255, "box": { "startX": 300.0, "startY": 400.0, "endX": 500.0, "endY": 600.0 }, "data": 140712345678912 },
        "pose": { "keypoints": [ {"kx": 100.5, "ky": 200.3, "ks": 0.8} ] },
        "face": { "landmark": [ {"x": 150.2, "y": 180.5} ], "box": { "startX": 100.0, "startY": 150.0, "endX": 200.0, "endY": 250.0 }, "confidence": 0.95, "face_feature": [0.123, 0.456, 0.789] }
      }
    }
  ]
}
```

With `include-frame=true` the payload also has `frameData`. Object `segment` is a binary mask local to `box`, not a full frame class map. `data` is a memory address cast to an integer. To write your own converter, see [Write an application](../write-an-application.md#custom-message-converter-library).

!!! warning "Do not use after GStreamer's input-selector"
    Caps are set once and not renegotiated, so placing `dxmsgconv` after the standard `input-selector` can give a caps mismatch when it switches streams. `dxinputselector` is fine.

## Pads

| Pad | Caps |
|---|---|
| sink | `video/x-raw, format={ NV12, I420, RGB, BGR }`; `application/x-dxvideoraw` |
| src | same as sink |

## Properties

| Name | Type | Default | Range | Description |
|---|---|---|---|---|
| `config-file-path` | string | none | | JSON file with the properties below. |
| `library-file-path` | string | none | | Converter library. Required, directly or in the JSON file. |
| `message-interval` | int | `1` | 1 to 10000 | Convert every Nth frame. |
| `include-frame` | bool | `false` | | Add the frame as base64 JPEG. |

## Next steps

* [DxMsgBroker](dxmsgbroker.md)
* [Message broker pipelines](../pipelines.md#message-broker)
