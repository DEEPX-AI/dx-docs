---
title: DX-Stream release notes
description: Changes in each DX-Stream release, newest first, from 3.2.0 back to 1.7.0.
---

# DX-Stream release notes

This page lists what changed in each DX-Stream release, newest first.

## 3.2.0 (2026-10-23)

Part of DEEPX SDK 2.5.0.

**Changed**

* Sample models now come from DX-COM 2.5.0 builds (`model_list.json` version `2_5_0`).
* Removed the SCRFD500M PPU face detection and YOLOv5Pose PPU pose demos and their Linux and Windows launchers. Update scripts that call them.
* EfficientNet-Lite0 256x256 is replaced by the 224x224 model in the secondary pipelines and tests.
* V3 DSP and RGA transform kernels moved into optional backend plugins (`gstdxstream-v3`, `gstdxstream-rga`). The core keeps the libyuv software path and loads installed backends. Build with `./build.sh --dxv3` to keep V3 DSP; RGA is built when `librga` is installed (or force it with `--rkrga`).

**Fixed**

* OC-SORT: observation history, assignment, association and GIoU handling, momentum weights, invalid or unmatched predictions, and recovery from an invalid tracker config.
* Documentation errors and typos.

**Added**

* Optional OpenGL ES backend `gstdxstream-gles`: crop, resize, letterbox and color conversion on EGL and GLES 3.0 GPUs with zero copy DMA-BUF import; secondary preprocessing sends all objects of a frame in one GPU submission. Built automatically on ARM hosts with EGL and GLESv2 (validated on Raspberry Pi 5); other hosts need `-Dwith_gles=enabled`.
* YOLO26 depth estimation demo with `DXFrameMeta` depth data and depth map drawing in `dxosd`.
* Raspberry Pi camera demos with `libcamerasrc` for YOLO26 detection, pose, segmentation and depth.
* DX-H1 V-NPU support: hardware decode, encode, transform, preprocessing and inference through `dxvnpudec`, `dxvnpuenc` and `dxinfer`. Build with `./build.sh --dxvnpu` (needs the DX-H1 V-NPU SDK). The V-NPU plugin in 3.2.0 registers `dxvnpudec` and `dxvnpuenc` only.

## 3.1.0 (2026-07-22)

**Changed**

* Multi stream domain: new `application/x-dxvideoraw` caps let one chain process streams with different sizes and formats. Per stream events keep each stream's own timeline. `dxinputselector` and `dxoutputselector` are the domain boundaries.
* `dxinputselector` and `dxgather` now use `GstAggregator`.
* Transform kernel pool with automatic backend choice by source format and libyuv fallback, used by `dxscale`, `dxconvert`, `dxpreprocess` and `dxmsgconv`.
* `dxinfer` uses an inference backend layer with asynchronous put and get and the `backend` property (`auto`, `dxrt`, `dxvnpu`).
* Custom library API: every custom function gets `GstBuffer *buf` first; `frame_meta->_buf` was removed; create objects with `dx_acquire_obj_meta_from_pool()`.
* Sample models from DX-COM 2.4.0.

**Fixed**

* All processing elements report their own processing time in `LATENCY` queries.
* Queues, threads and per stream state reset on FLUSH, fixing hangs on seek and replay.
* Push thread cleanup at EOS, FLUSH and state changes, fixing single frame hangs.
* Tighter pad template caps, so wrong links fail at negotiation.
* `abort()` and uncaught exceptions replaced by GStreamer errors, also for errors in custom libraries.

**Added**

* Windows (MSVC) build, demo launcher, tests and `pydxs`.
* Agent driven development (beta).
* Reorganized test suite with 73 new test binaries.
* `include-frame` property on `dxmsgconv` (base64 JPEG frame in the message).

## 3.0.1 (2026-05-06)

* Fixed manual typos.
* Fixed uninstall leaving app build folders and the pydxs build cache.
* Added the third party sample model license notice.

## 3.0.0 (2026-04-10)

**Changed**

* Breaking: models now come from DX-ModelZoo, one at a time through `model_list.json` and `setup_sample_models.sh` (needs `jq`). Demo models moved from YOLOv5s to YOLO26n, YOLOv5Pose to YOLO26n pose, DeepLabV3 MobileNetV2 to YOLO26n seg.
* Breaking: no more `/etc/profile.d/gstdxstream.sh`; environment variables go to `~/.bashrc`.
* Breaking: C++14.
* New transform kernel layer (RGA, libyuv, V3 DSP) with automatic backend choice.
* `dxosd` draws in place on YUV without extra conversion or copies.
* New build dependency `gstreamer1.0-dev`; default prefix `/usr/local`.

**Fixed**

* NV12 stride and offset for CPU input in `dxconvert` and `dxscale`.
* DMA-BUF zero copy in the RGA preprocessor and `dxosd`.
* Orange Pi 5 Plus (Debian 12) display corruption (the I420 workaround ships commented out in the demo scripts; see [Debugging](../stream/debugging.md#orange-pi-5-plus-with-debian-12-shows-corrupted-video)).
* RGA build errors, multi stream software rendering, tensor memory handling, meson install in a Python venv.

**Added**

* `dxscale` and `dxconvert` elements.
* RGA accelerated conversion and scaling with software fallback.
* V3 DSP preprocessor and OSD for DEEPX V3.
* YOLO26 examples, cleanup of files from older major versions, debugging guide.

## 2.2.1 (2026-02-26)

* Sample models updated from DX-COM 2.2.0 to 2.2.1.

## 2.2.0 (2026-01-16)

**Changed**

* `dxpreprocess` deep copies shared buffers (for example after `tee`).
* Metadata split into frame, object and user metadata files.
* Debian added to the OS requirements.

**Fixed**

* Race condition and crashes in secondary mode with several streams.

**Added**

* `pydxs` Python binding with `writable_buffer` and the `usermeta_app.py` example.
* User metadata API and its test suite and guide.

## 2.1.0 (2025-11-28)

**Changed**

* Default YOLOv5 model updated; sync disabled in secondary mode sinks; simpler message conversion config and JSON payload.
* Better Debian 12 dependency install (meson version checks, libdrm conflicts).

**Fixed**

* Setup script retries, `dxinfer` shutdown, `dxinputselector` event timing that froze compositor pipelines, `librga-dev` install on Rockchip, MQTT connection timeout.

**Added**

* PPU support for YOLOv5s, SCRFD500M and YOLOv5Pose (box decoding and NMS on the NPU).
* Orange Pi 5 Plus guide, GstShark integration, preprocess skip, V3 build configuration.

## 2.0.0 (2025-09-08)

* Compatible with DX-RT 3.0.0. Only DXNN v7 models from DX-COM 2.0.0 or newer run.
* Postprocess examples split per model.
* Fixed `dxinputselector` delays, SCRFD secondary postprocessing and multi tail models.
* Added `uninstall.sh`.

## 1.7.0 (2025-07-23)

* `dxinfer` buffer queue uses request IDs and a wait function instead of locking on queue size.
* Fixed video corruption in `dxpreprocess` and `dxosd` from wrong stride and offset.
* Demo scripts run setup automatically when files are missing.

## Next steps

* [DX-Stream overview](../stream/index.md)
* [All release notes](index.md)
