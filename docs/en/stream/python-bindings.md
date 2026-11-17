---
title: Python bindings (pydxs)
description: Install, check and use pydxs, the Python binding for DX-Stream frame, object and user metadata.
---

# Python bindings (pydxs)

`pydxs` lets your Python GStreamer app (PyGObject) read and write DX-Stream metadata: `DXFrameMeta`, `DXObjectMeta` and `DXUserMeta`. You use it in pad probes, next to the `gi` GStreamer binding.

## Install and check

`./build.sh` (Linux) and `build.bat` (Windows) install `pydxs` into the `venv-dx_stream` folder of the repository. `pydxs` is not on PyPI and needs the plugin built first, because it links against `libgstdxstream`.

The venv is created from the system Python with `--system-site-packages`, because the GStreamer binding `gi` (package `python3-gi`) is only installed for the system Python and must come from the same interpreter as `pydxs`. If your GStreamer and `python3-gi` were built for another Python, rebuild `pydxs` with that interpreter.

=== "Linux"
    ```bash
    source venv-dx_stream/bin/activate
    python3 -c "import gi; gi.require_version('Gst', '1.0'); from gi.repository import Gst; print('GStreamer OK')"
    python3 -c "import pydxs; print('pydxs OK')"
    ./test/run_pydxs.sh
    ```
=== "Windows"
    ```bat
    call venv-dx_stream\Scripts\activate.bat
    python -c "import pydxs; print('pydxs OK')"
    test\run_pydxs.bat
    ```

Run the full example (creates frame, object and user metadata and reads it back):

```bash
source venv-dx_stream/bin/activate
python3 dx_stream/apps/usermeta/usermeta_app.py dx_stream/samples/videos/boat.mp4
```

## Frame metadata

Every function takes a GStreamer object's address, which you get with `hash()`.

| Call | Returns | Use |
|---|---|---|
| `pydxs.writable_buffer(hash(info))` | context manager giving a `DXFrameMeta` | Recommended way to change metadata in a probe. Makes the buffer writable and creates the frame meta if it is missing. |
| `pydxs.dx_get_frame_meta(hash(buffer))` | `DXFrameMeta` or `None` | Read existing metadata. |
| `pydxs.dx_create_frame_meta(hash(buffer))` | `DXFrameMeta` | Create frame meta directly. Prefer `writable_buffer`, because this call may attach the meta to a copy when the buffer is not writable. |

```python
def probe(pad, info):
    with pydxs.writable_buffer(hash(info)) as frame_meta:
        frame_meta.dx_add_user_meta_to_frame({"scene": "outdoor"}, type_id=1001)
    return Gst.PadProbeReturn.OK
```

```python
frame_meta = pydxs.dx_get_frame_meta(hash(buffer))
if frame_meta:
    print(f"Frame: {frame_meta.width}x{frame_meta.height}, stream {frame_meta.stream_id}")
    for obj_meta in frame_meta:
        print(obj_meta.label, obj_meta.label_name, obj_meta.confidence, obj_meta.box)
```

`DXFrameMeta` attributes: `stream_id`, `width`, `height`, `format`, `name`, `frame_rate`, `roi`, `label`, `label_name`, `label_confidence`, `object_meta_list`, `seg_data`, `seg_width`, `seg_height`, `seg_format`, `depth_data`, `depth_width`, `depth_height`, `depth_format`, `input_tensors`, `output_tensors`. Iterating over a frame meta yields its objects.

## Object metadata

```python
obj_meta = pydxs.dx_acquire_obj_meta_from_pool()
obj_meta.label = 0
obj_meta.label_name = "dog"
obj_meta.confidence = 0.95
obj_meta.box = [x1, y1, x2, y2]
obj_meta.track_id = 1001
pydxs.dx_add_obj_meta_to_frame(frame_meta, obj_meta)
pydxs.dx_remove_obj_meta_from_frame(frame_meta, obj_meta)
```

`DXObjectMeta` attributes: `meta_id`, `track_id`, `label`, `label_name`, `confidence`, `box`, `keypoints`, `body_feature`, `face_box`, `face_confidence`, `face_landmarks`, `face_feature`, `seg_data`, `seg_width`, `seg_height`, `seg_format`, `input_tensors`, `output_tensors`.

## Segmentation and depth

| Attribute | Content |
|---|---|
| `frame_meta.seg_data` (`bytes`) | Full frame semantic class map, `seg_width` by `seg_height`. `seg_format` is `"full-frame-class-map"` or `"none"`. |
| `obj_meta.seg_data` (`bytes`) | Binary mask local to `obj_meta.box`, `seg_width` by `seg_height`. `seg_format` is `"roi-binary-mask"` or `"none"`. Place it back on the frame with `box`. |
| `frame_meta.depth_data` (`bytes`) | Row major, 1 channel, 8 bit relative depth, normalized per frame to 0 to 255. `depth_format` is `"relative-depth-u8"` or `"none"`. Not an absolute distance. |

```python
if frame_meta.depth_format == "relative-depth-u8":
    print(f"Depth: {frame_meta.depth_width}x{frame_meta.depth_height}, {len(frame_meta.depth_data)} bytes")
for obj_meta in frame_meta:
    if obj_meta.seg_format == "roi-binary-mask":
        print(f"Mask {obj_meta.seg_width}x{obj_meta.seg_height} at {obj_meta.box}")
```

## User metadata

In Python any object can be user metadata. You choose the integer `type_id`.

```python
frame_meta.dx_add_user_meta_to_frame({"scene": "outdoor", "brightness": 0.8}, type_id=1001)
obj_meta.dx_add_user_meta_to_obj({"quality": 0.95}, type_id=2001)

for user_meta in frame_meta.dx_get_frame_user_metas():
    if user_meta.type == 1001:
        print(user_meta.get_data())
for user_meta in obj_meta.dx_get_object_user_metas():
    if user_meta.type == 2001:
        print(user_meta.get_data())
```

## Windows loading

On Windows (Python 3.8 or newer) `pydxs` registers its DLL folders itself before it loads the native module `pydxs._pydxs`; your app does nothing extra. Search order:

| Runtime | Looked up in |
|---|---|
| DX-Stream | `DX_STREAM_ROOT\install`, the venv or checkout `install` folder, then the prefix used at build time |
| GStreamer | `GSTREAMER_1_0_ROOT_MSVC_X86_64`, `GSTREAMER_1_0_ROOT_X86_64`, the SDK used at build time, then the default MSVC x64 folders |
| DX-RT | `DEEPX_SDK_DIR\bin`, the SDK used at build time |
| DX-H1 V-NPU (optional) | `DEEPX_VNPU_DIR\bin` |

Use absolute paths. A wrong `DX_STREAM_ROOT` or SDK path gives an import error instead of loading another checkout. Runtime DLLs are not in the wheel, so these installs must stay in place.

## Next steps

* [User metadata](user-metadata.md)
* [Write an application](write-an-application.md)
