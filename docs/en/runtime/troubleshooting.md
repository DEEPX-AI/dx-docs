---
title: Troubleshooting
description: Common DX-RT, NPU driver and firmware errors and how to fix them.
---

# Troubleshooting

This page lists common DX-RT errors, what they mean and how to fix them. For install problems, see [Get started troubleshooting](../get-started/troubleshooting.md).

## First checks

Run these to collect the basic facts:

```bash
lspci -d 1ff4:                      # is the NPU on the PCIe bus?
lsmod | grep dx                     # are dx_dma and dxrt_driver loaded?
dxcli -s                            # does DX-RT see the device?
dxcli -v                            # minimum versions this DX-RT needs
sudo systemctl status dxrt.service  # is dxrtd running?
```

The DX-RT repository also has `SanityCheck.sh all`, and the driver repository has `sudo ./sanity_check.sh`. See [Check the driver](driver-firmware.md#check-the-driver).

## Version errors

| Message | Fix |
|---|---|
| `The current device driver version is X. Please update your device driver to version Y or higher.` | Update the NPU driver. DX-RT 3.5.0 needs 2.7.0 on Linux. See [NPU driver and firmware](driver-firmware.md) |
| The same message for the PCIe driver or firmware | Update that component. DX-RT 3.5.0 needs firmware 2.7.6 |
| `The model's compiler version(X) is not compatible in this RT library. Please use a model file generated with a compiler version Y or higher.` | Compile the model again with a newer DX-COM. DX-RT 3.5.0 needs models from DX-COM 1.18.1 or later |
| `Model file format version N is not supported. Please use model file version between A and B.` | DX-RT 3.5.0 reads format 6 to 9. Update DX-RT for newer models, or recompile older ones |
| `RuntimeError: dx_engine and DX-RT versions do not match.` | Install a `dx_engine` with the same major.minor version as `libdxrt.so` |

## Device and service errors

| Message | Cause and fix |
|---|---|
| `Device not found` | The driver is not loaded or the device is missing. Check `lspci -d 1ff4:` and `lsmod`, then load the modules with `sudo modprobe dx_dma` |
| `All Devices are blocked` | Every device is in a failed state. Reset it with `dxcli -r`, or reboot |
| `dxrt service is not running` | Start it with `sudo systemctl start dxrt.service`. Also check the model path, because a missing model file can show the same message |
| `Firmware Timeout: Device-ID=...` | The firmware stopped responding. Reset with `dxcli -r`. Check `journalctl -u dxrt.service` and the device temperature |
| `Throttling notice: ...` | The NPU is hot and slows down. Improve cooling, or set the fan with `dxcli --fan-ctrl on` |
| `Fail to write input, errno=...`, `Fail to read output, errno=...` | A PCIe transfer failed. See [EFAULT on input](#efault-on-input) and check the link with the driver sanity check |
| `DEVICE_REMOVED` or `DeviceRemovedError` (Windows) | The device was disabled, removed or its driver updated while the program ran. Restart the program |

## Model and inference errors

| Message | Cause and fix |
|---|---|
| `Invalid .dxnn file format` | The file is not a compiled model or is damaged. Check it with `dxparse -m model.dxnn` |
| `Ran out of NPU memory` | The models and buffers do not fit in NPU memory. Lower the buffer count, or load fewer models at once |
| `InferenceEngine::Wait job id N is out of range` | The job ID did not come from `RunAsync` on this engine |
| `ValueError: Input dtype mismatch ...` (Python) | Make the input array the type in `get_input_tensors_info()[i]["dtype"]` |
| `InvalidArgumentException` on batch `Run` (C++) | `outputBuffers` must have as many elements as `inputBuffers`. Use `nullptr` for engine allocated outputs |
| `validate_device` prints that release models are not supported | Device validation works only with models compiled in debug mode |

### EFAULT on input

If a Python input made with `np.zeros()` fails with `EFAULT`, the DMA driver saw the same zero page many times. Make inputs with `np.empty()` and `fill()` instead.

## Performance

| Symptom | What to try |
|---|---|
| Low FPS with `run` | Use `run_async` or batch `run` to keep all cores busy. See [Run inference](run-inference.md#asynchronous-inference) |
| Long Buffer Wait in the profiler | Raise the buffer count, or find the best one with `dxrun --max-throughput` |
| Hint `To improve FPS, set: 'export DXRT_DYNAMIC_CPU_THREAD=ON'` | Set that variable, then measure again |
| Long CPU task or format handler times | Try [acceleration](configuration.md#acceleration) and [DX-Fit](dx-fit.md) |
| FPS drops over time | Check the temperature with `dxtop`. The NPU throttles when hot |
| `dxrun` latency looks different after an update | Since 3.5.0, `GetLatency` is the E2E response time. `dxrun` shows core latency |

## Build and Python errors

| Message | Cause and fix |
|---|---|
| `malloc(): corrupted top size`, `free(): invalid pointer` or `double free or corruption (out)` on `import dx_engine` | The package was built for another Python version. Rebuild with the Python you run. See [Build from source](build-from-source.md) |
| CMake cannot find DX-RT | Use `find_package(dxrt)` and `dxrt::dxrt`, and pass `-DCMAKE_PREFIX_PATH=<prefix>`. See [C++ API](cpp-api.md#headers-and-linking) |
| `add_dxrt` unknown when building `examples/cpp` alone | The examples build only with `build.sh` |
| `NFH_ACCELERATION` not found, or `dxrun` rejects `--accel-nfh` | The build has no acceleration. Turn it on in `cmake/dxrt.cfg.cmake` and do a clean build |

## Windows

| Problem | What to check |
|---|---|
| Device not detected | Device Manager shows the NPU and the driver is 1.8.0 or later (PCIe driver 2.0.1 or later) |
| `dxrtd` does not start | Run `dxrtd --install` and then `dxrtd --start` as administrator |
| C# `EntryPointNotFoundException` | You called a `static inline` helper. See [C# through the C API](csharp.md#inline-helpers) |

## Next steps

* [NPU driver and firmware](driver-firmware.md)
* [Configuration](configuration.md)
* [Get started troubleshooting](../get-started/troubleshooting.md)
