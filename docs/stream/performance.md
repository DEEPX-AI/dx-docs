---
title: Performance with GstShark
description: Install GstShark and measure CPU use, processing time, frame rate and queue levels of each DX-Stream element.
---

# Performance with GstShark

This page shows you how to measure where time goes in a DX-Stream pipeline with GstShark, a set of GStreamer tracers from RidgeRun.

## Before you start

* DX-Stream built, sample models and videos downloaded, terminal in the repository root.
* sudo rights (GStreamer tracers install into `/usr`).

## Install GstShark

!!! warning "install_gstshark.sh fails in 3.2.0"
    The repository script clones into `gst-shark` and then changes into `gstshark`, so it stops before building. Use the steps below instead.

```bash
sudo apt-get install -y graphviz libgraphviz-dev octave epstool babeltrace autoconf automake libtool
mkdir -p util && cd util
git clone https://github.com/RidgeRun/gst-shark.git gst-shark
cd gst-shark
./autogen.sh --prefix /usr --libdir /usr/lib/$(uname -m)-linux-gnu
make
sudo make install
sudo ldconfig
echo "export PATH=\"\$PATH:$PWD/scripts/graphics\"" >> ~/.bashrc
source ~/.bashrc
cd ../..
```

The last lines put `gstshark-plot` on your `PATH`. Check that GStreamer sees the tracers:

```bash
rm -rf ~/.cache/gstreamer-1.0/registry.*.bin
gst-inspect-1.0 | grep shark
```

## Environment variables

| Variable | Purpose |
|---|---|
| `GST_TRACERS` | Tracers to use, separated by `;` |
| `GST_SHARK_LOCATION` | Folder for the result files |
| `GST_DEBUG` | Set `GST_TRACER:7` to print tracer output to the console |

| Tracer | Measures |
|---|---|
| `cpuusage` | CPU use |
| `proctime` | Processing time inside each element |
| `framerate` | Frame rate reached at each pad |
| `bitrate` | Data rate of the stream |
| `interlatency` | Latency between elements |
| `queuelevel` | Fill level of `queue` elements, to find backpressure |
| `buffer` | Buffer flow and timestamps |

## Measure a DX-Stream pipeline

`queuelevel` only measures `queue` elements, so put one between every stage:

```bash
S=$PWD/dx_stream
mkdir -p /tmp/gst-shark-results
GST_DEBUG="GST_TRACER:7" \
GST_TRACERS="cpuusage;proctime;framerate;queuelevel" \
GST_SHARK_LOCATION=/tmp/gst-shark-results \
gst-launch-1.0 urisourcebin uri=file://$S/samples/videos/boat.mp4 ! decodebin ! queue max-size-buffers=1 ! \
  dxpreprocess config-file-path=$S/configs/YoloV5S_PPU/preprocess_config.json ! queue max-size-buffers=1 ! \
  dxinfer config-file-path=$S/configs/YoloV5S_PPU/inference_config.json ! queue max-size-buffers=1 ! \
  dxpostprocess config-file-path=$S/configs/YoloV5S_PPU/postprocess_config.json ! queue max-size-buffers=1 ! \
  dxosd ! fakesink
```

Make graphs from the results:

```bash
ls -la /tmp/gst-shark-results/
gstshark-plot /tmp/gst-shark-results/ -s pdf
```

## Read the results

| Sign | Means | Look at |
|---|---|---|
| High processing time | Slow element (complex preprocessing, slow model) | Elements with high `proctime` |
| CPU hot spot | One element loads the host CPU (for example software decoding) | `cpuusage` |
| Full queue before an element | That element is slower than its input | `queuelevel` |
| Low frame rate | The pipeline cannot keep up | `framerate` against the input rate |

Ways to improve:

* Run secondary models less often with `interval` on `dxpreprocess`, or lower the rate with [DxRate](elements/dxrate.md).
* Tune queue sizes: larger queues drop fewer frames but add latency.
* Use hardware decode and the hardware transform backends where the platform has them.
* Use PPU models: box decoding runs on the NPU instead of the CPU.

Measure a baseline first, keep the system state the same between runs, and average several runs.

## Troubleshooting

| Problem | Fix |
|---|---|
| No tracer output | Set `GST_SHARK_LOCATION` and create that folder. |
| `gstshark-plot` not found | Add `util/gst-shark/scripts/graphics` to `PATH` as above. |
| Cannot write results | Fix the folder rights with `chmod` or pick a folder you own. |
| Tracers not found | Delete `~/.cache/gstreamer-1.0/registry.*.bin` and run `gst-inspect-1.0 > /dev/null` to rebuild the registry. |

## Next steps

* [Debugging and troubleshooting](debugging.md)
* [Pipelines](pipelines.md)
