---
title: DX EdgeGuide
description: Use DX EdgeGuide to pick a DEEPX NPU board and host for your vision workload from real benchmark results.
---

# DX EdgeGuide

DX EdgeGuide lets you pick the DEEPX NPU board and host that fit your computer vision workload, based on real YOLO26 benchmark measurements.

## Before you start

* A running studio. See [Install and launch](install-and-launch.md). No NPU is needed: EdgeGuide reads stored results.

## How it works

The tool is one page with a four step strip: **Scenario → Pick → Evidence → Buy**. Panels open as you go.

### 1. Describe the workload

* Optionally click a **Quick scenario** chip (**4-ch CCTV OD**, **8-ch retail cls**, **2-ch pose 30FPS**).
* **AI task:** Object Detection, Pose Estimation, Segmentation, OBB or Classification.
* **Model size:** n (fastest) to x (most accurate).
* **Operating requirements:** number of cameras (channels), target FPS, runtime (ONNX Runtime or Native) and max latency.
* Click **Next: choose ranking** and pick a ranking priority: **Most channels**, **Best Performance** (camera pipeline FPS) or **Lowest Power** (NPU TDP only, host power not included). Then click **Get Recommendations**. After the first run, any change refreshes the results; **Start over** clears everything.

### 2. Read the recommendations

A verdict line names the **Top pick** and whether your channel and FPS target is met. Each card has a **Measured** or **Estimated** badge and one line saying why, for example `12 ch held 30.4 FPS each ≥ 30 FPS target (measured)` or `534 FPS ÷ 60 FPS = 8.9 → 8 ch (estimated from the measured total; tested up to 18 ch)`.

How the channel count is worked out:

| Case | Result |
|---|---|
| A measured stream count meets your target and the next one misses it | That count (**Measured**) |
| Every measured count meets the target | The larger of that count and `floor(T_sat / target)` |
| No measured count meets the target | `floor(T_sat / target)` (**Estimated**) |

`T_sat` is the lowest measured total FPS; near saturation the total stays almost flat as streams are added. An estimate never exceeds twice the highest tested count. **Estimated+** means the estimate hit that cap, so the real capacity may be higher.

The notes on each card also say:

* when the NPU throttled during the measurement (the result is kept but ranks after an equal cool result);
* the **limit**: **NPU** when the NPU was at least 85 % busy at the most loaded measured count, otherwise **host** (CPU, decode, PCIe), with the measured NPU load. A faster host helps in the host case, a bigger NPU in the NPU case;
* when latency was not measured. With a latency budget set, an unmeasured latency never counts as a pass.

**How ranking works** shows every formula with its meaning and a summary of your session.

### 3. Explore and compare

Click a card or a throughput bar to open **Details**: key facts, platform specs, a performance radar, a sortable benchmark table and a per model size chart. **Task tabs** show the same platform for other tasks. Click a size bar or row to rerun at that size. **Compare with** lines up a second platform, with a count of Meets and Insufficient.

### 4. Buy

Pricing is by quote. **Product info** and **Request quote** in the Buy panel go to DEEPX.

## Example: check a four camera target

1. Choose **4-ch CCTV OD**. Keep Object Detection, one model size, **30 FPS** and one runtime setting.
1. Request recommendations, open the top card and its **Evidence**.
1. Compare a second platform without changing the inputs, and read the badge and arithmetic.

If nothing meets the target, look at the channel or latency shortfall, try a smaller model or fewer channels, and rerun. Recommendations are not a production guarantee for a different camera, decoder or host; contact us for production sizing.

The current selection is kept in the URL (a link from DX Benchmark reproduces the inputs) and your last inputs are restored on reload. EdgeGuide does not create cloud resources; for AWS see [DX Cloud on AWS](cloud-aws.md).

## Next steps

* [Compare stored results in DX Benchmark](monitor-and-benchmark.md#dx-benchmark)
* [Benchmark your own hardware with DX-Benchmark](../benchmark.md)
