---
title: Install and launch DX AI Studio
description: Requirements, launch options, remote access, security settings and troubleshooting for DX AI Studio.
---

# Install and launch DX AI Studio

This page shows you how to start DX AI Studio, open it from another computer and fix common start problems.

## Before you start

* Linux: Debian 12 or 13, or Ubuntu 20.04 to 26.04.
* Python 3.8 or newer. The base studio uses only the Python standard library (`dependencies = []`), so there is no `pip install` step.
* The DEEPX SDK checkout (`dx-all-suite`) with `dx-ai-studio` next to `dx-runtime` and `dx-compiler`. See [Install the DEEPX SDK](../../get-started/install.md).

### What each feature needs

The studio opens without any of these. A tool that misses something tells you what, and it never replaces a missing part with a fake result.

| Feature | Extra requirement |
|---|---|
| Local compilation (DX Compiler) | The DX-COM compiler SDK. DX Compiler **Setup** can install it. |
| Real NPU inference (DX App, DX Stream, DX Monitor) | A DEEPX NPU, the NPU driver, DX-RT (`dx_engine`) and prepared models and examples in `dx-runtime/dx_app` |
| Running DX Stream pipelines | System GStreamer and PyGObject (`python3-gi`, `gstreamer1.0-*`) |
| Live DX App runs (camera, RTSP, Continuous, Run Demo video, Graph Live) | `xvfb`, `libxcb1` and Pillow (`python3-pil`). Not needed for plain image or batch video runs. |
| Graph Composer | A dx_app build with `multi_model_graph_sync` / `multi_model_graph_async` (build with dx_app `./build.sh`) and the graph's models |
| Graph Composer zone editor | Pillow; reading a video frame also needs `ffmpeg` |
| Camera discovery and preview | A separate media Python with compatible NumPy and OpenCV. The web server itself does not import `cv2`. |
| DX Cloud AWS operations | The optional `boto3` extra (see [DX Cloud on AWS](cloud-aws.md)) |

!!! note "How the studio finds the SDK"
    `./launcher.sh` creates `.venv` with `--system-site-packages`, so it sees the installed `dx_engine` (DX-RT) and `gi` (GStreamer bindings). If `dx_engine` is missing, DX Monitor shows *NPU telemetry unavailable* and live inference is off. If `gi` is missing, DX Stream can build pipelines but not run them.

Check the NPU from the command line:

```bash
dxcli -s
```

`dxcli` lists each NPU with its driver and firmware versions. The old name `dxrt-cli` still works as an alias.

## Launch

From the `dx-ai-studio` folder:

```bash
./launcher.sh
```

The launcher installs the package on first run, starts the hub and every tool server, and opens your browser at the hub address. Wait for the boot screen to finish, then click a tool card. The launcher uses `.venv/bin/python` if it exists, otherwise your system `python3`.

### Launcher options

| Option | Effect |
|---|---|
| `--port <PORT>`, `-p <PORT>` | Preferred hub port (default **8890**). If the port is busy, the next free port is used and saved in `.launcher-port`. Open the address the launcher prints. |
| `--no-browser` | Start the servers without opening a browser |
| `--no-kill` | Keep a studio that is already running. By default a new launch stops your previous one. |
| `--fast` | Skip the boot animation in the terminal |
| `--debug[=PATH]` | Log user actions to `var/log/studio-debug.log` (or to `PATH`) |
| `--help`, `-h` | Print the options |

You only ever open the hub port. The hub proxies every tool.

### Stop the studio

Press `Ctrl+C` in the terminal that runs `./launcher.sh`. Running `./launcher.sh` again replaces your previous studio. With `--no-kill` the old one keeps running and the new one takes the next free port.

## Remote access and security

By default the hub listens on all network interfaces, so you can open a studio that runs on a headless board from another computer. The tool servers behind the hub listen only on `127.0.0.1`.

| Who | What they need |
|---|---|
| You, on the board (or through an SSH or VS Code tunnel) | Nothing |
| A browser on another computer | The 6 digit code printed in the board's `./launcher.sh` terminal, once per browser |
| A script or API client | `DX_API_TOKEN`, sent as `Authorization: Bearer <token>` or `X-DX-Api-Token` |

### Pair a browser

1. On the board, run `./launcher.sh`. Next to the address it prints `Remote access code: 123456`.
1. On your laptop, open the address printed under **other computers:** (for example `http://192.168.0.42:8890`). The top bar button **Connected browsers** on the board shows it too.
1. Type the code in **Connect this browser**.

The browser stays paired for 30 days (`DX_SESSION_DAYS`). Each code works once; a new one is printed after each use. After 5 wrong tries the studio pauses for a minute and prints a new code.

**Connected browsers** in the top bar lists every paired browser (browser and OS, IP, last active, paired date) with **Disconnect**. On the board you see all of them; a paired browser sees only itself. Scripts can use `GET /api/auth/sessions`, `POST /api/auth/sessions/revoke` (board only) and `POST /api/auth/logout`.

!!! tip "DX Stream from another computer"
    Choose **Playback: Remote (MJPEG)** in DX Stream. **Local (WebRTC)** works on the board or the same LAN segment and does not cross an SSH tunnel.

### Private access through an SSH tunnel

This keeps the studio hidden from the network. No pairing code is needed because the tunnel arrives on the board's `localhost`.

1. On the board, bind to localhost only:

    ```bash
    DX_BIND_LOCAL=1 ./launcher.sh
    ```

1. On your laptop, forward the port:

    ```bash
    ssh -L 8890:localhost:8890 <user>@<board-ip>
    ```

1. Open `http://localhost:8890` in your laptop browser.

### What the studio refuses

* Requests whose `Host` is not `localhost`, the machine's host name, an IP address or a name in `DX_ALLOWED_HOSTS`. This blocks DNS rebinding.
* Cross site requests: there is no `Access-Control-Allow-Origin: *`, and a POST, PUT, PATCH or DELETE that carries another site's `Origin` or `Referer` is refused.
* Compile paths outside the allowed folders: the suite folder, the studio's `var/`, your home folder, `/media` and `/mnt`. Add more with `DX_COMPILER_ALLOWED_ROOTS`.
* For HTTPS or access from outside the LAN, put the hub behind a reverse proxy that terminates TLS. Requests that arrive through a proxy (`X-Forwarded-For`) count as remote and must be paired.

### Several people on one board

* **Different machines:** fully separate studios. On an open LAN anyone can reach each one by its IP; use SSH tunnels to keep them private.
* **Same board, same Linux account:** a new `./launcher.sh` stops the previous studio. Two people on one login interrupt each other.
* **Same board, separate Linux accounts:** studios do not stop each other and the port moves up (8890, 8891 and so on). Give each user their own copy of `dx-ai-studio` so they do not share `outputs/`, sessions and downloads.

### Access settings

| Variable | Effect |
|---|---|
| `DX_BIND_LOCAL=1` | Bind the hub to `127.0.0.1` only (use with an SSH tunnel) |
| `DX_BIND_HOST=<host>` | Bind the hub to one interface or address |
| `DX_API_TOKEN=<secret>` | Let scripts call the studio from another machine. Also required to run a single tool server beyond `127.0.0.1`. |
| `DX_PAIRING=off` | Turn browser pairing off; remote access works only with `DX_API_TOKEN` |
| `DX_SESSION_DAYS=<n>` | How long a paired browser stays connected (default 30) |
| `DX_ALLOWED_HOSTS=<a,b>` | Extra host names the studio answers to |
| `DX_COMPILER_ALLOWED_ROOTS=<dir:dir>` | Extra folders the compiler may read and write |

All other variables are on the [Reference](reference.md#environment-variables) page.

## Managed runtime profiles

DX AI Studio treats DX-RT and the NPU driver as an external, versioned dependency and never changes the `dx-runtime` sources. The file `config/runtime_profiles.json` lists the supported runtime and driver package pairs with fixed download URLs and SHA-256 digests.

* **Target profile:** SDK 2.5.0 (DX-RT 3.5.0, NPU driver 2.7.0, firmware 2.7.6) on `x86_64` and `aarch64`. The 2.3.0, 2.4.1 and 2.4.2 profiles are kept only as sources to upgrade from and as rollback targets.
* **Unknown runtime:** a runtime that is not in the file (for example a newer pre release) is never replaced. Setup stops with "No verified rollback profile".
* **Checked packages:** packages are cached under `var/runtime/artifacts/` only after their SHA-256 digest matches. A mismatch never reaches a privileged command.
* **Explicit approval:** installing packages needs an explicit **Runtime Setup** action. Only then does the studio run a privileged `dpkg` command.
* **Launch gate:** DX App and DX Stream start inference only when an active profile passed validation, or when the tool's own launch checks pass live on this board. A failure returns a check ID and a fix instead of starting the job.
* **Clean environment:** inference jobs get the studio's own Python, virtual environment, library paths, GStreamer plugin folder and postprocess path. `PYTHONPATH`, `VIRTUAL_ENV`, `LD_LIBRARY_PATH` and `GST_PLUGIN_PATH` from your shell are not passed on.
* **Rollback:** if a new profile fails validation, the studio reinstalls and validates the previous declared profile. Studio outputs and the artifact cache are kept.

!!! warning "Reboot after a driver change"
    Installing or changing the DKMS driver can need a reboot before the NPU device nodes appear. After the reboot, run **DX-Runtime Dependencies** and **NPU Linux Driver** in DX Stream **Setup** again to validate the profile before you start inference.

## Troubleshooting

| Symptom | What to do |
|---|---|
| DX Monitor says *NPU telemetry unavailable*, or a tool says the SDK is missing | Check the driver with `lsmod \| grep dx` (expect `dxrt_driver` and `dx_dma`) and the device with `dxcli -s`. The DX Monitor version panel shows what the studio sees. |
| A tool stays on the splash screen or says "not ready" | The tool servers may still be starting. Wait and reload. If it persists, read the errors in the `./launcher.sh` terminal. The hub retries for about 30 seconds, then shows **Module unavailable** with **Retry**. |
| "Port already in use" | Port 8890 moves to the next free port automatically. Pin one with `-p`, or use `--no-kill` to leave the running studio alone. |
| The UI works but compile or inference fails | Read the error. Open **Setup** in DX Compiler for the compiler, or in DX App or DX Stream for runtime, driver, example binaries and models. |
| DX Stream refuses to launch after a runtime change | Open **Setup**, then **DX-Runtime Dependencies** and **NPU Linux Driver**, read the failed check and follow its fix. Run the checks again after an approved install or a reboot. |
| Graph validation or **Run once** is unavailable | Make sure the studio uses a dx_app checkout with the graph runners, build them there and prepare the graph's models. |

Tool servers write their error logs to `~/.local/state/dx-ai-studio/logs/`.

## Next steps

* [Tour the hub](hub.md)
* [Compile a model in DX Compiler](workflow.md#dx-compiler)
* [Run your first inference in DX App](app.md)
