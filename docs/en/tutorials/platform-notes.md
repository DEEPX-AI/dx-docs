---
title: Platform notes
description: Extra setup for Raspberry Pi 5, Orange Pi 5 Plus, Intel GPUs and GStreamer version conflicts.
---

# Platform notes

This page lets you prepare a Raspberry Pi 5, an Orange Pi 5 Plus or an Intel GPU host before you run the tutorials.

## Raspberry Pi 5: PCIe Gen3

The Raspberry Pi 5 PCIe port runs at Gen2 (5 GT/s) by default. Gen3 (8 GT/s) roughly doubles the bandwidth to the DX-M1. Raspberry Pi does not certify Gen3, but it works with good FPC cables and boards.

1. Add these lines to the end of `/boot/firmware/config.txt`:

    ```text
    # Enable PCIe Gen3 x1
    dtparam=pciex1_gen=3
    ```

    For the Seeed Studio dual HAT case use:

    ```text
    dtparam=pciex1
    dtparam=pciex1_gen=3
    dtoverlay=pciex1-compat-pi5,no-mip,mmio-hi
    ```

1. Reboot and check the link (install `pciutils` if `lspci` is missing):

    ```bash
    sudo reboot
    sudo lspci -vvv | grep -iA 33 accelerators | grep -E "LnkCap|LnkSta"
    ```

    ```text
    LnkCap: Port #0, Speed 8GT/s, Width x4, ASPM L1, Exit Latency L1 <16us
    LnkSta: Speed 8GT/s, Width x1 (downgraded)
    ```

    `Speed 8GT/s` in `LnkSta` means Gen3 is active. The DX-M1 shows as `Processing accelerators: DEEPX Co., Ltd. DX_M1`. Width x1 is expected: the Pi has one lane.

| PCIe generation | Rate | Max bandwidth (x1) |
|---|---|---|
| Gen1 | 2.5 GT/s | about 250 MB/s |
| Gen2 (Pi 5 default) | 5.0 GT/s | about 500 MB/s |
| Gen3 | 8.0 GT/s | about 985 MB/s |

## Orange Pi 5 Plus: kernel headers

The official Orange Pi image may lack the kernel headers that the NPU driver build needs. Install them before the SDK:

```bash
ls /opt/linux-headers-current-rockchip-rk3588_*.deb
sudo apt install /opt/linux-headers-current-rockchip-rk3588_*.deb
```

If there is no package under `/opt`, build it with `orangepi-build`:

```bash
sudo apt update
sudo apt install git build-essential bison flex libssl-dev dwarves
git clone https://github.com/orangepi-xunlong/orangepi-build.git
cd orangepi-build
./build.sh
```

In the menu choose Kernel package, Do not change the kernel configuration, orangepi5plus, Current Recommended. Then install the package from `output/debs`, for example `sudo dpkg -i output/debs/linux-headers-current-rockchip-rk3588_1.2.0_arm64.deb`.

## Intel GPU for DX-Stream

On Ubuntu 24.04, 25.10 or 26.04 you can use the Intel GPU for video decode in DX-Stream:

```bash
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:kobuk-team/intel-graphics
sudo apt-get install -y libze-intel-gpu1 libze1 intel-metrics-discovery intel-opencl-icd clinfo intel-gsc
sudo apt-get install -y intel-media-va-driver-non-free libmfx-gen1.2 libvpl2 libvpl-tools libva-glx2 va-driver-all vainfo gstreamer1.0-vaapi
sudo apt-get install -y intel-gpu-tools
```

Check it:

```bash
vainfo
clinfo | grep "Device Name"
sudo intel_gpu_top
```

If no device shows, add yourself to the `render` group:

```bash
sudo gpasswd -a ${USER} render
newgrp render
```

## GStreamer version conflicts (Ubuntu 22.04)

Use this only when DX-Stream fails because of held or mismatched GStreamer packages.

1. Show and release held packages:

    ```bash
    apt-mark showhold
    sudo apt-mark unhold gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
      gstreamer1.0-plugins-bad gstreamer1.0-plugins-bad-apps gstreamer1.0-plugins-ugly \
      gstreamer1.0-libav gstreamer1.0-opencv gstreamer1.0-wpe \
      libgstreamer1.0-0 libgstreamer1.0-dev gir1.2-gstreamer-1.0 \
      libgstreamer-plugins-base1.0-0 libgstreamer-plugins-base1.0-dev \
      libgstreamer-plugins-good1.0-0 libgstreamer-plugins-good1.0-dev \
      libgstreamer-plugins-bad1.0-0 libgstreamer-plugins-bad1.0-dev \
      libgstreamer-opencv1.0-0 gir1.2-gst-plugins-bad-1.0 2>/dev/null || true
    ```

1. Remove the packages that pin strict versions:

    ```bash
    sudo apt purge -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
      libgstreamer-plugins-good1.0-dev libgstreamer-plugins-bad1.0-dev \
      gstreamer1.0-opencv libgstreamer-opencv1.0-0 gstreamer1.0-wpe gir1.2-gst-plugins-bad-1.0
    sudo apt autoremove -y
    ```

1. Update the base libraries from `jammy-updates`:

    ```bash
    sudo apt update
    sudo apt -t jammy-updates install -y --allow-downgrades --allow-change-held-packages \
      gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-ugly gstreamer1.0-libav \
      gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-bad-apps \
      libgstreamer1.0-0 libgstreamer-plugins-base1.0-0 \
      libgstreamer-plugins-good1.0-0 libgstreamer-plugins-bad1.0-0
    ```

1. Reinstall the development and optional packages:

    ```bash
    sudo apt -t jammy-updates install -y --allow-downgrades \
      libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
      libgstreamer-plugins-good1.0-dev libgstreamer-plugins-bad1.0-dev \
      gstreamer1.0-opencv libgstreamer-opencv1.0-0 gstreamer1.0-wpe gir1.2-gst-plugins-bad-1.0
    ```

## Next steps

* [Set up the tutorials](setup.md)
* [Driver and firmware](../runtime/driver-firmware.md)
* [Troubleshooting](../get-started/troubleshooting.md)
