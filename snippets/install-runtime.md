<!-- Single source of truth for the quick runtime install.
     Included in docs/get-started/install.md and docs/runtime/index.md.
     Edit only here. -->

## Install the runtime

**Supported systems:** Ubuntu 20.04 to 26.04, Debian 12 and 13 · x86_64 and arm64 · requires a DEEPX DX-M1, DX-M1M or DX-H1 NPU.

First, check that the device sees the NPU on the PCIe bus:

```bash
lspci -d 1ff4: # (1)!
```

1. `1ff4` is the DEEPX PCI vendor ID. If this prints nothing, the card is not detected: check the slot and BIOS settings before you install.

### Install

=== "APT repository (recommended)"

    ```bash
    wget -O deepx-archive-keyring.asc https://apt.releases.deepx.ai/gpg # (1)!
    gpg --show-keys deepx-archive-keyring.asc # (2)!
    sudo gpg --dearmor -o /usr/share/keyrings/deepx-archive-keyring.gpg deepx-archive-keyring.asc # (3)!
    rm deepx-archive-keyring.asc # (4)!

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/deepx-archive-keyring.gpg] \
      https://apt.releases.deepx.ai $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") main" \
      | sudo tee /etc/apt/sources.list.d/deepx.list # (5)!

    sudo apt update # (6)!
    sudo apt install dxrt-driver-dkms libdxrt-bin # (7)!
    ```

    1. Downloads the DEEPX APT repository signing key.
    2. Displays the key fingerprint. It must be exactly `3A20CC853C64AE328D0F58CFD816AAC6689DBDEA`. Do not continue if it differs.
    3. Converts the key to binary format and places it in the system keyring.
    4. Removes the downloaded key file; it is now stored in the keyring.
    5. Adds the DEEPX repository for your OS release (detected from `/etc/os-release`).
    6. Refreshes the package list to include the new repository.
    7. `dxrt-driver-dkms` is the NPU kernel driver; DKMS rebuilds it on every kernel update. `libdxrt-bin` is the DX-RT library, CLI tools and the `dxrtd` service.

    The APT repository does not ship firmware. See [Update the firmware](../get-started/install.md#update-the-firmware).

=== "One-line script"

    ```bash
    curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-runtime/main/oneline-install.sh | sh # (1)!
    ```

    1. Installs the NPU driver, DX-RT and firmware in one step. Does not install DX-APP or DX-Stream.

    To pin exact versions, see [Option B: one line script](../get-started/install.md#option-b-one-line-script).

=== "Clone"

    ```bash
    git clone --recurse-submodules https://github.com/DEEPX-AI/dx-runtime.git # (1)!
    cd dx-runtime
    ./install.sh --all # (2)!
    ```

    1. Clones the repository and its submodules (driver, firmware, DX-RT, DX-APP, DX-Stream).
    2. Runs the full installer. Use `--runtime-only` to install only the driver, DX-RT and firmware.

??? tip "Install the Python package (dx_engine), required for Python"

    `libdxrt-bin` ships one wheel per Python version (3.8 to 3.14) in `/usr/share/libdxrt-bin/python`. Install it into a virtual environment:

    ```bash
    sudo apt install python3-venv # (1)!
    python3 -m venv ~/dx-venv # (2)!
    source ~/dx-venv/bin/activate # (3)!
    PYTAG=cp$(python -c 'import sys; print(f"{sys.version_info[0]}{sys.version_info[1]}")') # (4)!
    pip install /usr/share/libdxrt-bin/python/dx_engine-*-${PYTAG}-${PYTAG}-*.whl # (5)!
    ```

    1. Installs the `venv` module if it is not already available.
    2. Creates an isolated Python environment at `~/dx-venv`.
    3. Activates the environment.
    4. Builds the CPython tag for your Python version, for example `cp312` for Python 3.12, to select the matching wheel.
    5. Installs the `dx_engine` wheel that matches your Python version.

    Do not use `pip install dx-engine`: the PyPI release is yanked and does not match the installed DX-RT.

### Restart and verify

Restart once after the install. If the firmware was updated, do a **cold boot**: shut down, remove power for 10 to 30 seconds, then power on.

```bash
sudo reboot # (1)!
```

1. Enough when only the driver or DX-RT changed. A plain reboot may not reset the NPU after a firmware update.

Verify the installation:

```bash
dxcli -s # (1)!
python3 -c "import dx_engine; print(dx_engine.__version__)" # (2)!
```

1. Prints the device, driver and firmware versions. You should see `Device 0` with real version numbers.
2. Checks that the Python package imports and prints its version.

??? tip "Uninstall"

    ```bash
    curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-runtime/main/oneline-uninstall.sh | sh # (1)!
    ```

    1. Removes the driver, DX-RT and their packages. Or run `sudo apt purge libdxrt-bin dxrt-driver-dkms`.
