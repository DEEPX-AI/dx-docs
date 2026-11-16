---
title: C# through the C API
description: How to call DX-RT from C# with P/Invoke on the stable C API.
---

# C# through the C API

We do not ship a C# package. Your C# program calls the `dxrt_*` functions of the stable C API directly with P/Invoke.

## Before you start

* Install DX-RT on Windows. See [Install](../get-started/install.md). The Windows build uses the `dxrtd` service.
* Build for **x64** only (`<PlatformTarget>x64</PlatformTarget>`).
* Put `dxrt.dll`, `onnxruntime.dll` and `onnxruntime_providers_shared.dll` from the install `bin` folder next to your program or on `PATH`. A source build with `build.bat install` puts them in `out\install\x64-Release\bin\`.

!!! note "The C# package was removed in DX-RT 3.5.0"
    The old C++/CLI `csharp_package` depended on the C++ ABI. Move existing code to the C API as shown here.

## Source of truth

Take every signature, struct, ownership and lifetime rule from `include/dxrt/dxrt_c_api.h`. Do not copy declarations from older C# code. Do not bind declarations marked `@internal`, such as `dxrt_engine_register_release_callback`.

## Binding rules

### Calls and errors

* Use `CallingConvention.Cdecl` and the library name `"dxrt"`.
* Most functions return `dxrt_status_t` (`int`, `0` is `DXRT_OK`).
* On failure, call `dxrt_last_error_message()` on the same thread before any other `dxrt_*` call, and copy the string. The message is per thread, and the next call invalidates it. Do not use `SetLastError` or `Marshal.GetLastWin32Error`.

### Inline helpers

`dxrt_options_init()`, `dxrt_tensor_slice_init()` and `dxrt_npu_timing_init()` are `static inline` in the header, so `dxrt.dll` does not export them. Calling them through P/Invoke throws `EntryPointNotFoundException`. Write them in C#: zero the struct, set `struct_size`, then apply the defaults from the header.

### Struct layout

Use `[StructLayout(LayoutKind.Sequential)]` with the default packing. Do not set `Pack = 1`, because the C layout has padding. Set `struct_size` from `Marshal.SizeOf<T>()` and check it against these sizes (MSVC x64):

| C struct | Size | Notes |
|---|---|---|
| `dxrt_options_t` | 44 | Fixed by `static_assert` |
| `dxrt_tensor_info_t` | 344 | `name[256]` at 0, `type` at 256, 4 bytes padding, `shape[8]` at 272, `size_in_bytes` at 336 |
| `dxrt_tensor_slice_t` | 384 | `data` at 8 (4 bytes padding after `struct_size`), `info` at 24, `reserved` at 368 |
| `dxrt_npu_timing_t` | 88 | Size is negotiated through `struct_size` |

### Strings

* Paths are UTF-8. Marshal them with `[MarshalAs(UnmanagedType.LPUTF8Str)]`.
* The library owns returned `const char*` strings. Receive them as `IntPtr`, copy them with `Marshal.PtrToStringUTF8`, and never free them.
* Functions that fill your buffer, such as `dxrt_engine_get_model_name`, take a `byte[]` and its length.

### Handles and buffers

* Wrap `dxrt_engine_t` in a `SafeHandle` whose `ReleaseHandle` calls `dxrt_engine_destroy`.
* Get buffer sizes with `dxrt_engine_get_input_size` and `dxrt_engine_get_output_size`.
* For sync calls, blittable arrays such as `byte[]` stay pinned during the call.
* For `dxrt_engine_run_async`, keep the input and output buffers pinned (`GCHandle.Alloc(..., GCHandleType.Pinned)` or native memory) until the job finishes through `dxrt_engine_wait` or the callback.

### Callbacks

These rules apply to `dxrt_engine_register_callback` and `dxrt_event_register_handler`:

* Keep the delegate referenced while the runtime can call it: until `dxrt_engine_destroy` returns for engine callbacks, and for the life of the process for event handlers. Registering `NULL` does not wait for a handler call already running. A collected delegate crashes the process.
* Declare the delegate with `[UnmanagedFunctionPointer(CallingConvention.Cdecl)]`.
* `dxrt_tensor_slice_t.data` is valid only during the callback. Copy the data before you return.
* Never let an exception leave a callback. Catch everything inside it.
* Callbacks run on runtime worker threads and can run at the same time. An event handler also runs on the thread that calls `dxrt_event_dispatch`. Lock shared state, and move UI work to the UI thread, for example with `SynchronizationContext` or `Control.BeginInvoke`.
* The runtime ignores the `int` that `dxrt_callback_fn` returns. Return 0.
* `dxrt_engine_register_callback` has no unregister function and rejects a `null` delegate with `DXRT_ERR_INVALID_ARG`.
* A failed job also calls `dxrt_callback_fn`, with `tensor_count` 0.
* Do not call `dxrt_engine_wait` for the same job or `dxrt_engine_destroy` inside the callback. Both wait for the callback to return, so they deadlock.

## Minimal example

This program loads a model, runs one inference on a zero input and prints the buffer sizes. The `Options` defaults mirror `dxrt_options_init()`: `BufferCount` 0, `DeviceId` -1, `BoundOption` 0, `UseOrt` -1 and `ShowModelInfo` -1.

```csharp
using System;
using System.Runtime.InteropServices;

internal sealed class DxrtEngineHandle : SafeHandle
{
    public DxrtEngineHandle() : base(IntPtr.Zero, ownsHandle: true) { }
    public override bool IsInvalid => handle == IntPtr.Zero;
    protected override bool ReleaseHandle()
    {
        Dxrt.dxrt_engine_destroy(handle);
        return true;
    }
}

internal static class Dxrt
{
    private const string Lib = "dxrt";

    [StructLayout(LayoutKind.Sequential)]
    public struct Options
    {
        public uint StructSize;
        public int BufferCount;
        public int DeviceId;
        public uint BoundOption;
        public int UseOrt;
        public int ShowModelInfo;
        public uint Reserved0, Reserved1, Reserved2, Reserved3, Reserved4;

        // Must match sizeof(dxrt_options_t), which the header pins with static_assert.
        public const int NativeSize = 44;

        // Mirrors the header-only dxrt_options_init().
        public static Options CreateDefault()
        {
            int size = Marshal.SizeOf<Options>();
            if (size != NativeSize)
                throw new InvalidOperationException(
                    $"Options layout mismatch: {size} bytes, expected {NativeSize}");

            return new Options
            {
                StructSize = (uint)size,
                BufferCount = 0,
                DeviceId = -1,
                BoundOption = 0,
                UseOrt = -1,
                ShowModelInfo = -1,
            };
        }
    }

    [DllImport(Lib, CallingConvention = CallingConvention.Cdecl)]
    private static extern IntPtr dxrt_last_error_message();

    [DllImport(Lib, CallingConvention = CallingConvention.Cdecl)]
    public static extern int dxrt_engine_create(
        [MarshalAs(UnmanagedType.LPUTF8Str)] string modelPath,
        in Options options,
        out DxrtEngineHandle engine);

    [DllImport(Lib, CallingConvention = CallingConvention.Cdecl)]
    public static extern void dxrt_engine_destroy(IntPtr engine);

    [DllImport(Lib, CallingConvention = CallingConvention.Cdecl)]
    public static extern int dxrt_engine_get_input_size(DxrtEngineHandle engine, out ulong size);

    [DllImport(Lib, CallingConvention = CallingConvention.Cdecl)]
    public static extern int dxrt_engine_get_output_size(DxrtEngineHandle engine, out ulong size);

    [DllImport(Lib, CallingConvention = CallingConvention.Cdecl)]
    public static extern int dxrt_engine_run(DxrtEngineHandle engine, byte[] input, [Out] byte[] output);

    public static void Check(int status)
    {
        if (status != 0)
        {
            string message = Marshal.PtrToStringUTF8(dxrt_last_error_message()) ?? string.Empty;
            throw new InvalidOperationException($"DX-RT error {status}: {message}");
        }
    }
}

internal static class Program
{
    private static void Main(string[] args)
    {
        var options = Dxrt.Options.CreateDefault();
        Dxrt.Check(Dxrt.dxrt_engine_create(args[0], options, out var engine));
        using (engine)
        {
            Dxrt.Check(Dxrt.dxrt_engine_get_input_size(engine, out ulong inputSize));
            Dxrt.Check(Dxrt.dxrt_engine_get_output_size(engine, out ulong outputSize));

            var input = new byte[inputSize];
            var output = new byte[outputSize];
            Dxrt.Check(Dxrt.dxrt_engine_run(engine, input, output));

            Console.WriteLine($"input={inputSize} bytes, output={outputSize} bytes");
        }
    }
}
```

## Next steps

* [C++ API](cpp-api.md#c-api-reference)
* [Run inference](run-inference.md)
* [Troubleshooting](troubleshooting.md)
