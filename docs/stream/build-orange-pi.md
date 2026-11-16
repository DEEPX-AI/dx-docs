---
title: Build on Orange Pi 5 Plus
description: Flash an Orange Pi 5 Plus, install the NPU driver and DX-RT, and build and run DX-Stream with a DX-M1 module.
---

# Build on Orange Pi 5 Plus

This how to takes an Orange Pi 5 Plus (RK3588) with a DX-M1 M.2 module from a blank SD card to running DX-Stream demos.

## Before you start

* Orange Pi 5 Plus board, DX-M1 M.2 module, power supply (5 V, 4 A minimum).
* MicroSD card, 32 GB or larger (Class 10 recommended).
* A Linux host to flash the card, with `7z` (`sudo apt install p7zip-full`).

## 1. Flash the SD card

1. Download the Orange Pi 5 Plus Ubuntu 22.04 image (Jammy desktop XFCE, Linux kernel 6.1.43, file `Orangepi5plus_1.2.0_ubuntu_jammy_desktop_xfce_linux6.1.43.7z`, about 4 GB) from the Orange Pi download page for the board.
1. Extract and flash it. Find your card device with `lsblk` first and replace `/dev/sda`.

    ```bash
    7z x Orangepi5plus_1.2.0_ubuntu_jammy_desktop_xfce_linux6.1.43.7z
    sudo umount /dev/sda
    sudo dd if=./Orangepi5plus_1.2.0_ubuntu_jammy_desktop_xfce_linux6.1.43.img of=/dev/sda bs=4M status=progress
    sync
    ```

    !!! warning
        `dd` overwrites the target device completely. Check the device name twice.

    Raspberry Pi Imager, Balena Etcher or Win32DiskImager work too.

1. Insert the card, connect power and peripherals, and boot. The default user and password are `orangepi` and `orangepi`.

Run all following steps on the Orange Pi.

## 2. Install the NPU driver and DX-RT

1. Install the kernel headers that ship in the image:

    ```bash
    cd /opt
    sudo apt install ./linux-headers-current-rockchip-rk3588_1.2.0_arm64.deb
    ```

1. Build and install the NPU driver and DX-RT for aarch64 as described in [Install the DEEPX SDK](../get-started/install.md) and [NPU driver and firmware](../runtime/driver-firmware.md). On this board the source route is:

    ```bash
    mkdir -p ~/dxnn && cd ~/dxnn
    git clone https://github.com/DEEPX-AI/dx_rt_npu_linux_driver.git
    cd dx_rt_npu_linux_driver/modules
    ./build.sh
    sudo ./build.sh -c install
    cd ~/dxnn
    git clone https://github.com/DEEPX-AI/dx_rt.git
    cd dx_rt
    ./install.sh --all
    ./build.sh
    ```

1. Check that the NPU is found (`dxrt-cli` is the old name of `dxcli`):

    ```bash
    dxcli -s
    ```

    ```text
    DXRT <dxrt-version>
    =======================================================
     * Device 0: M1, Accelerator type
    ...
    NPU 0: voltage 750 mV, clock 1000 MHz, temperature 40'C
    ```

    If no device shows up, run `lsmod | grep dx`, `lspci | grep -i deepx` and `dmesg | grep -i deepx`.

## 3. Build DX-Stream

`install.sh` detects the Rockchip board and also installs `librga-dev`, so DX-Stream builds the RGA transform backend for `dxpreprocess`, `dxscale` and `dxconvert`.

```bash
cd ~/dxnn
git clone https://github.com/DEEPX-AI/dx_stream.git
cd dx_stream
./install.sh
./build.sh
source ~/.bashrc
gst-inspect-1.0 dxstream
```

The build takes about 10 to 15 minutes on this board. With the clone at `~/dxnn/dx_stream`, `setup.sh` stores models and videos in `~/workspace/res/`.

## 4. Run the demos

```bash
cd ~/dxnn/dx_stream
./setup.sh
./run_demo.sh
```

The menu is the same as on other Linux hosts (see [Build and install](build.md#run-the-demos)).

## Troubleshooting

| Problem | Fix |
|---|---|
| Plugin not found | `rm -rf ~/.cache/gstreamer-1.0/` then `GST_PLUGIN_PATH=/usr/local/lib/aarch64-linux-gnu/gstreamer-1.0 gst-inspect-1.0 dxstream` |
| Build fails after an update | `./build.sh --clean` |
| Corrupted or distorted video on Debian 12 | Force I420 before the display sink, see [Debugging and troubleshooting](debugging.md#orange-pi-5-plus-with-debian-12-shows-corrupted-video) |
| Slow pipelines | Check the NPU with `dxcli -s` and the CPU with `htop` |

## Next steps

* [Pipelines](pipelines.md)
* [Write an application](write-an-application.md)
* [Elements](elements/index.md)
