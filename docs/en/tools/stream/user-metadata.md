---
title: User metadata
description: Attach your own data to DX-Stream frames and objects with DXUserMeta in C++ and Python.
---

# User metadata

This page shows you how to attach your own data to a frame or an object, so later elements or your app can read it. Use frame metadata for scene level results (crowd count, timing) and object metadata for per object results (features, attributes).

## The API

```cpp
enum class DXUserMetaType {
    DX_USER_META_FRAME = 0x1000,   // frame level
    DX_USER_META_OBJECT = 0x2000,  // object level
};

struct _DXUserMeta {
    gpointer user_meta_data;        // your data
    gsize user_meta_size;           // its size
    DXUserMetaType user_meta_type;  // FRAME or OBJECT
    GDestroyNotify release_func;    // required: frees your data
    GBoxedCopyFunc copy_func;       // required: deep copies your data
};
```

| Function | Purpose |
|---|---|
| `DXUserMeta *dx_acquire_user_meta_from_pool(void)` | Allocate a new `DXUserMeta`. The name is historical; no pooling happens. |
| `void dx_release_user_meta(DXUserMeta*)` | Free a user meta that was not attached. |
| `gboolean dx_user_meta_set_data(DXUserMeta*, gpointer data, gsize size, DXUserMetaType type, GDestroyNotify release_func, GBoxedCopyFunc copy_func)` | Store your data. Both functions are required. |
| `gboolean dx_add_user_meta_to_frame(DXFrameMeta*, DXUserMeta*)` | Attach to a frame. |
| `gboolean dx_add_user_meta_to_obj(DXObjectMeta*, DXUserMeta*)` | Attach to an object. |
| `std::vector<DXUserMeta*> *dx_get_frame_user_metas(DXFrameMeta*)` | All user metas of a frame. |
| `std::vector<DXUserMeta*> *dx_get_object_user_metas(DXObjectMeta*)` | All user metas of an object. |

Who frees what:

* After `dx_user_meta_set_data()` succeeds, the user meta owns your data and frees it with `release_func`.
* If `dx_user_meta_set_data()` fails, you still own the data: free it, then call `dx_release_user_meta()`.
* If attaching fails, call `dx_release_user_meta()`; it frees the data through `release_func`.

## Add and read user metadata

The C++ example defines a structure with heap pointers, its copy and free functions, attaches it to a frame and reads it back. The Python binding stores any Python object, so it needs no copy or free functions.

=== "C++"
    ```cpp
    #include <gstdxstream/gst-dxframemeta.hpp>
    #include <gstdxstream/gst-dxusermeta.hpp>

    typedef struct {
        gint total_objects;
        gfloat scene_confidence;
        gchar *scene_type;
        guint64 processing_time_us;
    } SceneAnalytics;

    static gpointer scene_analytics_copy(gconstpointer src) {
        const SceneAnalytics *s = (const SceneAnalytics *)src;
        SceneAnalytics *d = g_new0(SceneAnalytics, 1);
        d->total_objects = s->total_objects;
        d->scene_confidence = s->scene_confidence;
        d->scene_type = g_strdup(s->scene_type);   // deep copy
        d->processing_time_us = s->processing_time_us;
        return d;
    }

    static void scene_analytics_free(gpointer data) {
        SceneAnalytics *a = (SceneAnalytics *)data;
        g_free(a->scene_type);
        g_free(a);
    }

    void add_scene_analytics(DXFrameMeta *frame_meta, gint count, const gchar *scene, guint64 time_us) {
        DXUserMeta *user_meta = dx_acquire_user_meta_from_pool();
        SceneAnalytics *a = g_new0(SceneAnalytics, 1);
        a->total_objects = count;
        a->scene_confidence = 0.89f;
        a->scene_type = g_strdup(scene);
        a->processing_time_us = time_us;

        if (!dx_user_meta_set_data(user_meta, a, sizeof(SceneAnalytics),
                                   DXUserMetaType::DX_USER_META_FRAME,
                                   scene_analytics_free, scene_analytics_copy)) {
            g_warning("Failed to set user metadata");
            scene_analytics_free(a);           // still owned by us
            dx_release_user_meta(user_meta);
            return;
        }
        if (!dx_add_user_meta_to_frame(frame_meta, user_meta)) {
            g_warning("Failed to attach user metadata to frame");
            dx_release_user_meta(user_meta);   // frees a through release_func
        }
    }

    void print_scene_analytics(DXFrameMeta *frame_meta) {
        for (DXUserMeta *user_meta : *dx_get_frame_user_metas(frame_meta)) {
            if (user_meta->user_meta_type == DXUserMetaType::DX_USER_META_FRAME) {
                SceneAnalytics *a = (SceneAnalytics *)user_meta->user_meta_data;
                g_print("Objects: %d, scene: %s (%.2f), time: %" G_GUINT64_FORMAT " us\n",
                        a->total_objects, a->scene_type, a->scene_confidence, a->processing_time_us);
            }
        }
    }
    ```
=== "Python"
    ```python
    import pydxs

    SCENE_ANALYTICS = 1001

    def add_scene_analytics(pad, info):
        with pydxs.writable_buffer(hash(info)) as frame_meta:
            data = {
                "total_objects": len(list(frame_meta)),
                "scene_confidence": 0.89,
                "scene_type": "indoor_scene",
            }
            frame_meta.dx_add_user_meta_to_frame(data, type_id=SCENE_ANALYTICS)
        return Gst.PadProbeReturn.OK

    def print_scene_analytics(pad, info):
        frame_meta = pydxs.dx_get_frame_meta(hash(info.get_buffer()))
        if frame_meta:
            for user_meta in frame_meta.dx_get_frame_user_metas():
                if user_meta.type == SCENE_ANALYTICS:
                    print(user_meta.get_data())
        return Gst.PadProbeReturn.OK
    ```

Object level metadata works the same with `DX_USER_META_OBJECT`, `dx_add_user_meta_to_obj()` and `dx_get_object_user_metas()` (Python: `obj_meta.dx_add_user_meta_to_obj(data, type_id)` and `obj_meta.dx_get_object_user_metas()`). A structure with a float array needs a deep copy of the array in `copy_func`:

```cpp
typedef struct {
    gfloat custom_score;
    gint feature_dim;
    gfloat *feature_vector;
    gchar *algorithm_name;
} CustomObjectFeature;

static gpointer custom_feature_copy(gconstpointer src) {
    const CustomObjectFeature *s = (const CustomObjectFeature *)src;
    CustomObjectFeature *d = g_new0(CustomObjectFeature, 1);
    d->custom_score = s->custom_score;
    d->feature_dim = s->feature_dim;
    d->feature_vector = g_new(gfloat, s->feature_dim);
    memcpy(d->feature_vector, s->feature_vector, s->feature_dim * sizeof(gfloat));
    d->algorithm_name = g_strdup(s->algorithm_name);
    return d;
}

static void custom_feature_free(gpointer data) {
    CustomObjectFeature *f = (CustomObjectFeature *)data;
    g_free(f->feature_vector);
    g_free(f->algorithm_name);
    g_free(f);
}
```

## Inside a postprocess library

A postprocess function runs once per frame in primary mode (`object_meta == nullptr`) and once per object in secondary mode. Add frame level metadata only in primary mode:

```cpp
extern "C" void custom_analytics_postprocess(GstBuffer *buf,
                                             std::vector<dxs::DXTensor> network_output,
                                             DXFrameMeta *frame_meta,
                                             DXObjectMeta *object_meta) {
    gint64 start_us = g_get_monotonic_time();
    if (object_meta == nullptr) {
        add_scene_analytics(frame_meta, frame_meta->_object_meta_list.size(),
                            "indoor_scene", g_get_monotonic_time() - start_us);
    } else {
        // secondary mode: attach object level metadata to object_meta
    }
}
```

## Rules and pitfalls

| Problem | Cause and fix |
|---|---|
| Crash when reading metadata | Missing deep copy of a pointer in `copy_func`, or use of freed data. Copy every heap field. |
| Memory leak | `release_func` does not free every allocation. Check with valgrind. |
| Metadata not found | Wrong type checked, attach failed, or the wrong list (frame vs object) read. Always check `user_meta_type` (or `type` in Python) before casting. |
| Slow pipeline | Every user meta is a new allocation. Keep the data small and create it only when needed. |

Metadata can be read from several threads. Lists can be empty; check before you use the first entry.

## Next steps

* [Python bindings (pydxs)](python-bindings.md)
* [Write an application](write-an-application.md)
