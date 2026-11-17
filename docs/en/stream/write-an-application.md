---
title: Write an application
description: Run DX-Stream pipelines from Python or C++, read results from metadata, and write custom preprocess, postprocess and message converter libraries.
---

# Write an application

This page shows you how to run a DX-Stream pipeline from your own Python or C++ program, read the results, and plug in your own model logic through custom libraries. It assumes your model is already compiled to `.dxnn` with [DX-COM](../compiler/index.md).

## Before you start

* DX-Stream built and installed ([Build and install](build.md)).
* For Python: the `venv-dx_stream` venv that `build.sh` creates (`source venv-dx_stream/bin/activate`).
* For C++: `pkg-config --exists gstdxstream` succeeds (`PKG_CONFIG_PATH` set as on [Build and install](build.md#environment-variables)).

## Run a pipeline and read results

Both programs build the YOLO26n detection pipeline, read the objects in a pad probe after `dxpostprocess`, and stop on end of stream or error. Run them from the repository root.

=== "Python"
    ```python
    import os
    import gi
    gi.require_version("Gst", "1.0")
    from gi.repository import Gst
    import pydxs

    Gst.init(None)
    root = os.getcwd()
    pipeline = Gst.parse_launch(
        f"urisourcebin uri=file://{root}/dx_stream/samples/videos/boat.mp4 ! decodebin ! queue ! "
        "dxpreprocess preprocess-id=1 resize-width=640 resize-height=640 ! queue ! "
        f"dxinfer preprocess-id=1 inference-id=1 model-path={root}/dx_stream/samples/models/yolo26-n_640x640.dxnn ! queue ! "
        "dxpostprocess name=post inference-id=1 "
        "library-file-path=/usr/local/share/gstdxstream/lib/libpostprocess_yolo26od.so function-name=PostProcess ! queue ! "
        "dxosd ! videoconvert ! fpsdisplaysink sync=false"
    )

    def on_buffer(pad, info):
        frame_meta = pydxs.dx_get_frame_meta(hash(info.get_buffer()))
        if frame_meta:
            for obj in frame_meta:
                print(obj.label_name, round(obj.confidence, 2), obj.box)
        return Gst.PadProbeReturn.OK

    pipeline.get_by_name("post").get_static_pad("src").add_probe(Gst.PadProbeType.BUFFER, on_buffer)
    pipeline.set_state(Gst.State.PLAYING)
    bus = pipeline.get_bus()
    msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS | Gst.MessageType.ERROR)
    if msg.type == Gst.MessageType.ERROR:
        print(msg.parse_error())
    pipeline.set_state(Gst.State.NULL)
    ```
=== "C++"
    ```cpp
    // Build: g++ -std=c++14 app.cpp -o app $(pkg-config --cflags --libs gstreamer-1.0 gstdxstream)
    #include <gst/gst.h>
    #include <string>
    #include <unistd.h>
    #include <gstdxstream/gst-dxframemeta.hpp>
    #include <gstdxstream/gst-dxobjectmeta.hpp>

    static GstPadProbeReturn on_buffer(GstPad *, GstPadProbeInfo *info, gpointer) {
        DXFrameMeta *frame_meta = dx_get_frame_meta(GST_PAD_PROBE_INFO_BUFFER(info));
        if (frame_meta) {
            for (DXObjectMeta *obj : frame_meta->_object_meta_list) {
                g_print("%s %.2f\n", obj->_label_name.c_str(), obj->_confidence);
            }
        }
        return GST_PAD_PROBE_OK;
    }

    int main(int argc, char **argv) {
        gst_init(&argc, &argv);
        char cwd[4096];
        std::string root = getcwd(cwd, sizeof(cwd));
        std::string desc =
            "urisourcebin uri=file://" + root + "/dx_stream/samples/videos/boat.mp4 ! decodebin ! queue ! "
            "dxpreprocess preprocess-id=1 resize-width=640 resize-height=640 ! queue ! "
            "dxinfer preprocess-id=1 inference-id=1 model-path=" + root + "/dx_stream/samples/models/yolo26-n_640x640.dxnn ! queue ! "
            "dxpostprocess name=post inference-id=1 "
            "library-file-path=/usr/local/share/gstdxstream/lib/libpostprocess_yolo26od.so function-name=PostProcess ! queue ! "
            "dxosd ! videoconvert ! fpsdisplaysink sync=false";
        GError *err = nullptr;
        GstElement *pipeline = gst_parse_launch(desc.c_str(), &err);
        if (!pipeline) { g_printerr("%s\n", err->message); return 1; }

        GstElement *post = gst_bin_get_by_name(GST_BIN(pipeline), "post");
        GstPad *pad = gst_element_get_static_pad(post, "src");
        gst_pad_add_probe(pad, GST_PAD_PROBE_TYPE_BUFFER, on_buffer, nullptr, nullptr);

        gst_element_set_state(pipeline, GST_STATE_PLAYING);
        GstBus *bus = gst_element_get_bus(pipeline);
        GstMessage *msg = gst_bus_timed_pop_filtered(bus, GST_CLOCK_TIME_NONE,
            (GstMessageType)(GST_MESSAGE_EOS | GST_MESSAGE_ERROR));
        gst_message_unref(msg);
        gst_element_set_state(pipeline, GST_STATE_NULL);
        gst_object_unref(pad); gst_object_unref(post); gst_object_unref(bus); gst_object_unref(pipeline);
        return 0;
    }
    ```

A complete example that creates and reads metadata in both languages is `dx_stream/apps/usermeta/usermeta_app.py` and `usermeta_app.cpp` (see [User metadata](user-metadata.md)).

## The metadata model

Results travel with each buffer: **GstBuffer → DXFrameMeta → DXObjectMeta → DXUserMeta**.

`DXFrameMeta` (header `gst-dxframemeta.hpp`):

```cpp
struct _DXFrameMeta {
    GstMeta _meta;
    int _stream_id;
    int _width;
    int _height;
    std::string _format;
    std::string _name;
    float _frame_rate;
    int _roi[4];
    std::vector<unsigned char> _seg_data;     // frame level semantic class map
    int _seg_width = 0;
    int _seg_height = 0;
    std::vector<unsigned char> _depth_data;   // row major, 1 channel, 8 bit relative depth
    int _depth_width = 0;
    int _depth_height = 0;
    int _label;                               // classification result (primary mode)
    std::string _label_name;
    float _label_confidence;
    std::vector<DXObjectMeta*> _object_meta_list;
    std::vector<DXUserMeta*> _frame_user_meta_list;
    std::map<int, dxs::DXTensors> _input_tensors;   // preprocess_id to input tensors
    std::map<int, dxs::DXTensors> _output_tensors;  // inference_id to output tensors
};
```

`DXObjectMeta` (header `gst-dxobjectmeta.hpp`):

```cpp
struct _DXObjectMeta {
    int _meta_id;
    int _track_id;
    int _label;
    std::string _label_name;
    float _confidence;
    std::array<float, 4> _box;
    std::vector<float> _keypoints;
    std::vector<float> _body_feature;
    std::vector<float> _obb;                  // oriented box [cx, cy, w, h, angle]
    std::array<float, 4> _face_box;
    float _face_confidence;
    std::vector<float> _face_landmarks;
    std::vector<float> _face_feature;
    std::vector<unsigned char> _seg_data;     // binary mask local to _box
    int _seg_width = 0;
    int _seg_height = 0;
    std::vector<DXUserMeta*> _obj_user_meta_list;
    std::map<int, dxs::DXTensors> _input_tensors;
    std::map<int, dxs::DXTensors> _output_tensors;
};
```

The YOLO26 depth library normalizes each frame to 0 to 255, so depth values are relative and cannot be compared between frames.

Metadata functions:

| Function | Purpose |
|---|---|
| `GstBuffer *dx_create_frame_meta(GstBuffer *buffer)` | Create and attach a `DXFrameMeta`. May return a new, writable buffer. |
| `DXFrameMeta *dx_get_frame_meta(GstBuffer *buffer)` | Get the frame meta, or `nullptr`. |
| `gboolean dx_add_obj_meta_to_frame(DXFrameMeta*, DXObjectMeta*)` | Add an object to a frame. |
| `gboolean dx_remove_obj_meta_from_frame(DXFrameMeta*, DXObjectMeta*)` | Remove an object from a frame. |
| `DXObjectMeta *dx_acquire_obj_meta_from_pool(void)` | Create a new object. |
| `void dx_release_obj_meta(DXObjectMeta*)` | Free an object you did not add to a frame. |
| `void dx_copy_obj_meta(DXObjectMeta *src, DXObjectMeta *dst)` | Copy an object. |

User metadata functions are on [User metadata](user-metadata.md).

## Custom postprocess library

Every model needs a postprocess function that understands its output tensors. Start from a shipped one in `dx_stream/custom_library/postprocess_library/` (list on [DxPostprocess](elements/dxpostprocess.md#shipped-postprocess-libraries)).

1. Look at the output tensors:

    ```bash
    dxparse -m dx_stream/samples/models/yolo26-n_640x640.dxnn
    ```

    The output lists every tensor with name, type and shape, for example `onnx::Reshape_491, FLOAT, [1, 80, 80, 256]` (three NHWC outputs for a YOLOv5 style model).

1. Write the function. In primary mode `object_meta` is `nullptr` and you create objects; in secondary mode you update `object_meta` and must not remove or reallocate it.

    ```cpp
    #include <gst/gst.h>
    #include <gstdxstream/dxcommon.hpp>
    #include <gstdxstream/gst-dxframemeta.hpp>
    #include <gstdxstream/gst-dxobjectmeta.hpp>

    extern "C" void PostProcess(GstBuffer *buf,
                                std::vector<dxs::DXTensor> network_output,
                                DXFrameMeta *frame_meta,
                                DXObjectMeta *object_meta) {
        float *data = (float *)network_output[0]._data;
        auto shape = network_output[0]._shape;   // std::vector<int64_t>
        // decode boxes from data and shape, then for each box:
        DXObjectMeta *obj = dx_acquire_obj_meta_from_pool();
        obj->_label = 0;
        obj->_label_name = "person";
        obj->_confidence = 0.9f;
        obj->_box = {100.f, 100.f, 200.f, 300.f};
        dx_add_obj_meta_to_frame(frame_meta, obj);
    }
    ```

    `dxs::DXTensor` members: `_data` (pointer), `_shape` (`std::vector<int64_t>`), `_type` (`dxs::DataType`), `_elemSize`, `_name`.

1. Build it with Meson:

    ```meson
    project('postprocess_mymodel', 'cpp', version : '1.0.0', default_options: ['cpp_std=c++14'])
    gst_dep = dependency('gstreamer-1.0', version : '>=1.16.3')
    dx_stream_dep = dependency('gstdxstream')
    shared_library('postprocess_mymodel', 'postprocess.cpp',
        dependencies: [gst_dep, dx_stream_dep],
        install: true,
        install_dir: get_option('datadir') / 'gstdxstream' / 'lib')
    ```

    ```bash
    meson setup builddir --prefix=/usr/local
    meson compile -C builddir
    sudo meson install -C builddir
    ```

1. Use it:

    ```json
    {
        "inference_id": 1,
        "library_file_path": "/usr/local/share/gstdxstream/lib/libpostprocess_mymodel.so",
        "function_name": "PostProcess"
    }
    ```

## Custom preprocess library

Use one when the built in resize, pad and color conversion of `dxpreprocess` is not enough.

```cpp
extern "C" bool CustomPreprocessFunc(GstBuffer *buf,
                                     DXFrameMeta *frame_meta,
                                     DXObjectMeta *object_meta,
                                     void *input_tensor) {
    // read pixels from buf, write the model input to input_tensor
    return true;
}
```

* `input_tensor` is allocated by DX-Stream from the size set on `dxpreprocess`. Do not free or reallocate it.
* `object_meta` is the object in secondary mode and `nullptr` in primary mode.
* Return `false` to skip the frame.

Build it like the postprocess library (for example `shared_library('custompreproc', 'preprocess.cpp', ...)`) and set it on `dxpreprocess`:

```json
{
    "library_file_path": "/usr/local/share/gstdxstream/lib/libcustompreproc.so",
    "function_name": "CustomPreprocessFunc"
}
```

## Custom message converter library

`dxmsgconv` needs a library that exports three functions. The shipped one is in `dx_stream/custom_library/message_convert_library/dx_msgconvl/`.

| Function | Purpose |
|---|---|
| `DxMsgContext *dxmsg_create_context()` | Create your conversion context. |
| `void dxmsg_delete_context(DxMsgContext *context)` | Free it. |
| `DxMsgPayload *dxmsg_convert_payload(DxMsgContext *context, GstDxMsgMetaInfo *meta_info)` | Convert one frame's metadata to a payload. |

```cpp
#include "dx_msgconvl_priv.hpp"

extern "C" DxMsgContext *dxmsg_create_context() {
    DxMsgContext *context = g_new0(DxMsgContext, 1);
    context->_priv_data = (void *)dxcontext_create_contextPriv();
    return context;
}

extern "C" void dxmsg_delete_context(DxMsgContext *context) {
    g_return_if_fail(context != nullptr);
    dxcontext_delete_contextPriv((DxMsgContextPriv *)context->_priv_data);
    g_free(context);
}

extern "C" DxMsgPayload *dxmsg_convert_payload(DxMsgContext *context,
                                               GstDxMsgMetaInfo *meta_info) {
    DxMsgPayload *payload = g_new0(DxMsgPayload, 1);
    gchar *json_data = dxpayload_convert_to_json(context, meta_info);
    if (json_data == nullptr) {
        g_warning("dxpayload_convert_to_json returned null");
        g_free(payload);
        return nullptr;
    }
    payload->_size = strlen(json_data);
    payload->_data = json_data;
    return payload;
}
```

`dxpayload_convert_to_json`, `dxcontext_create_contextPriv` and `dxcontext_delete_contextPriv` are helpers of the shipped library, built with json-glib. `dxmsgconv` frees the returned data after sending. When `include-frame=true`, `meta_info->_frame_base64` holds the JPEG frame; check it for `nullptr` first. The library does not parse config files; `dxmsgconv` parses its own `config-file-path`.

Build dependencies of the shipped library: `gstreamer-1.0`, `gstdxstream`, `json-glib-1.0`, `opencv4` and `-ldxrt`. The output format is on [DxMsgConv](elements/dxmsgconv.md#behavior).

## Error rules for custom libraries

`dxpreprocess`, `dxpostprocess` and `dxmsgconv` load your library with `dlopen` and wrap every call in `try`/`catch`. A thrown exception becomes a GStreamer error on the bus, so your application can shut down cleanly.

| Situation | Do this |
|---|---|
| Per frame problem (missing tensor, bad shape for one frame) | `g_warning(...)` and return early: `false` (preprocess), `return` (postprocess), `nullptr` (message convert). The frame is skipped. |
| Permanent problem (model does not match the library, missing resource) | `throw std::runtime_error("message")`. |
| Never | `g_error()`, `g_assert()`, `abort()` or `exit()`. They kill the process with `SIGABRT`, no bus error is sent and nothing is cleaned up. |

```cpp
extern "C" void PostProcess(GstBuffer *buf, std::vector<dxs::DXTensor> network_output,
                            DXFrameMeta *frame_meta, DXObjectMeta *object_meta) {
    if (network_output.empty()) {
        g_warning("PostProcess: no output tensors for this frame, skipping");
        return;
    }
    if (network_output[0]._shape.size() != 4) {
        throw std::runtime_error("PostProcess: unexpected tensor rank, check that model matches the library");
    }
    // normal processing
}
```

## Changes since 3.1.0

If you port a library from DX-Stream before 3.1.0:

* `frame_meta->_buf` is gone. Every custom function now gets `GstBuffer *buf` as the first parameter.
* Create objects with `dx_acquire_obj_meta_from_pool()` and add them with `dx_add_obj_meta_to_frame()` instead of `dx_create_object_meta(buf)`.

## Next steps

* [User metadata](user-metadata.md)
* [Python bindings (pydxs)](python-bindings.md)
* [Pipelines](pipelines.md)
