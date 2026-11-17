---
title: Greengrass devices
description: Set up a DX-AIPlayer N97 or a DX-M1 Raspberry Pi 5 kit as an AWS IoT Greengrass core device.
---

# Greengrass devices

This page shows you how to set up a DX-AIPlayer N97 or a DX-M1 Raspberry Pi 5 kit as an AWS IoT Greengrass V2 core device, ready for the DEEPX Greengrass Solution.

Both devices are AWS Qualified Devices for AWS IoT Greengrass. The classic Greengrass nucleus and Greengrass nucleus lite are both supported.

## Devices

| | DX-AIPlayer N97 | DX-M1 Raspberry Pi 5 kit |
|---|---|---|
| Host | Intel N97, quad core up to 3.6 GHz (x86_64) | Raspberry Pi 5 8 GB, Broadcom BCM2712 (aarch64) |
| NPU | DX-M1 M.2 2280, 25 TOPS INT8, 4 GB LPDDR5, up to 5 W (preinstalled) | DX-M1 M.2 2280 on an M.2 HAT over PCIe Gen 3 |
| Memory and storage | 8 GB LPDDR5, 64 GB eMMC | 8 GB LPDDR4X, microSD |
| Network | 2× GbE (optional Wi-Fi through M.2 2230 E-Key) | 1× GbE |
| OS | Ubuntu 24.04 LTS | Raspberry Pi OS 64 bit (Debian 13 "Trixie") |
| Other | 3× USB 3.2, 2× COM, HDMI 2.0b, DP 1.2, TPM 2.0, 12 V 5 A DC, 0 to 60 °C, 95 × 95 × 55 mm | 2× USB 3.0, 2× USB 2.0, 2× micro HDMI, active cooler |

## Before you start

* An AWS account. Follow steps 1 and 2 of the AWS tutorial *Getting started with AWS IoT Greengrass V2* (account and environment setup).
* An Ethernet connection with outbound TCP 443 to AWS.
* A keyboard and monitor for the first boot, or SSH access.

## 1. Prepare the hardware

=== "DX-AIPlayer N97"

    1. Connect Ethernet to **LAN 1** on the right side.
    1. For the first setup, connect a monitor (HDMI or DP) and a USB keyboard, or note the device IP for SSH.
    1. Connect the 12 V adapter and press the power button.
    1. Finish the Ubuntu first boot setup and log in.

=== "Raspberry Pi 5 kit"

    1. Mount the M.2 HAT on the Raspberry Pi 5 with the standoffs and connect the PCIe FPC cable (see the kit's assembly guide).
    1. Insert the DX-M1 module in the HAT's M.2 slot and fix it with the screw. Attach the active cooler.
    1. Flash **Raspberry Pi OS (64-bit)** to the microSD card with Raspberry Pi Imager. Create your user and enable SSH if you work remotely.
    1. Connect Ethernet and power, then boot.
    1. Enable PCIe Gen 3 and reboot:

        ```bash
        echo -e "dtparam=pciex1\ndtparam=pciex1_gen=3" | sudo tee -a /boot/firmware/config.txt
        sudo reboot
        ```

        `sudo raspi-config` (Advanced Options, PCIe Speed) does the same.

    1. Check that the NPU is on the PCIe bus:

        ```bash
        lspci | grep -i deepx
        ```

        ```text
        0001:01:00.0 Processing accelerators: DEEPX Co., Ltd. DX_M1 (rev 01)
        ```

Check internet access on the device:

```bash
ping -c 3 amazon.com
```

## 2. NPU driver and runtime

You have two options:

* Let the [DEEPX Greengrass Solution](dx-edge.md#deploy-the-runtime-with-greengrass) install the NPU driver, firmware, `dx_rt` and `dx_stream` over the air after registration.
* Install them yourself now, following [Install the DEEPX SDK](../get-started/install.md). Then check:

    ```bash
    lsmod | grep -E 'dxrt|dx_'   # expect dxrt_driver and dx_dma
    ls /dev/dxrt0
    dxcli -s
    ```

## 3. Install the Greengrass prerequisites

Greengrass needs Java 8 or newer:

```bash
sudo apt update
sudo apt install -y default-jre curl unzip
java -version
```

On the Raspberry Pi 5, to run Docker application components, install Docker Engine and check that `docker info | grep -i 'storage driver'` shows `overlay2`.

## 4. Install and register Greengrass

1. Give the device temporary AWS credentials. Use long term IAM user keys only for development:

    ```bash
    export AWS_ACCESS_KEY_ID=<access key id>
    export AWS_SECRET_ACCESS_KEY=<secret access key>
    export AWS_REGION=<your console region>
    ```

1. Download the Greengrass Core software:

    ```bash
    cd ~
    curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip -o greengrass-nucleus-latest.zip
    unzip greengrass-nucleus-latest.zip -d GreengrassInstaller
    ```

1. Install with automatic provisioning. Set your own thing name (for example `DX-AIPlayer-N97-Core` or `DX-M1-RPI5-Core`) and thing group:

    ```bash
    sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE \
      -jar ./GreengrassInstaller/lib/Greengrass.jar \
      --aws-region "$AWS_REGION" \
      --thing-name DX-AIPlayer-N97-Core \
      --thing-group-name DXGreengrassGroup \
      --thing-policy-name GreengrassV2IoTThingPolicy \
      --tes-role-name GreengrassV2TokenExchangeRole \
      --tes-role-alias-name GreengrassCoreTokenExchangeRoleAlias \
      --component-default-user ggc_user:ggc_group \
      --provision true \
      --setup-system-service true
    ```

1. Remove the keys from the shell, and deactivate or delete the access key in the IAM console:

    ```bash
    unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY
    ```

1. Check the service:

    ```bash
    sudo systemctl status greengrass.service
    ```

    In the AWS IoT console, **Greengrass devices, Core devices** shows the device as **Healthy**.

To try a first component, follow the AWS tutorial sections *Develop and test a component on your device*, *Create your component in the AWS IoT Greengrass service* and *Deploy your component*. A local Hello World component logs to `/greengrass/v2/logs/com.example.HelloWorld.log`.

## 5. Deploy the DEEPX runtime

With the device in a thing group, deploy the DEEPX runtime with the [DEEPX Greengrass Solution](dx-edge.md#deploy-the-runtime-with-greengrass). Then run `dxcli -s` and the test pipeline on that page to check the NPU.

## Debugging

* Greengrass Core log: `/greengrass/v2/logs/greengrass.log`. Component logs: `/greengrass/v2/logs/<component-name>.log`.
* Service messages: `journalctl -u greengrass.service -f`.

| Symptom | Fix |
|---|---|
| `java: command not found` | `sudo apt install -y default-jre`, then rerun the installer |
| `lspci` does not show the DX_M1 (Raspberry Pi) | Enable PCIe Gen 3, reseat the module and the FPC cable, reboot |
| `dxcli` not found | Install the NPU driver and DX-RT (step 2) and check `dxrt_driver` with `lsmod` |
| The device does not appear in the AWS IoT console | Check internet, outbound TCP 443 and that the region matches the console |
| `greengrass.service` fails to start | Read `/greengrass/v2/logs/greengrass.log`; make sure you installed with `sudo` and `/tmp` is mounted with `exec` |
| Component deployment stuck | Check that the token exchange role was created (`--provision true` output) and the deployment status |
| Docker component fails (Raspberry Pi) | Check Docker Engine and the `overlay2` storage driver |

For device support, contact tech_support@deepx.ai.

## Next steps

* [Deploy the runtime with the DEEPX Greengrass Solution](dx-edge.md#deploy-the-runtime-with-greengrass)
* [NPU driver and firmware](../runtime/driver-firmware.md)
