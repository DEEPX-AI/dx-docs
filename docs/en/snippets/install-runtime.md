## Install the runtime

**Supported systems:** Ubuntu 20.04–26.04, Debian 12–13 · x86_64 and arm64 · requires a DEEPX M1, M1M or H1 NPU.

### Option A: APT repository (recommended)

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
2. Displays the key fingerprint — it must be exactly `3A20CC853C64AE328D0F58CFD816AAC6689DBDEA`. Do not continue if it differs.
3. Converts the key to binary format and places it in the system keyring.
4. Removes the downloaded key file; it is now stored in the keyring.
5. Adds the DEEPX repository for your OS release (auto-detected from `/etc/os-release`).
6. Refreshes the package list to include the new repository.
7. `dxrt-driver-dkms` is the NPU kernel driver — DKMS rebuilds it automatically on every kernel update. `libdxrt-bin` is the DX-RT library, CLI tools and the `dxrtd` service.

??? tip "Install the Python package (dx_engine)"

    `libdxrt-bin` ships one wheel per Python version (3.8–3.14) in `/usr/share/libdxrt-bin/python`. Install it into a virtual environment:

    ```bash
    sudo apt install python3-venv # (1)!
    python3 -m venv ~/dx-venv # (2)!
    source ~/dx-venv/bin/activate # (3)!
    PYTAG=cp$(python -c 'import sys; print(f"{sys.version_info[0]}{sys.version_info[1]}")') # (4)!
    pip install /usr/share/libdxrt-bin/python/dx_engine-*-${PYTAG}-${PYTAG}-*.whl # (5)!
    ```

    1. Installs the `venv` module if it is not already available on your system.
    2. Creates an isolated Python environment at `~/dx-venv`.
    3. Activates the environment.
    4. Builds the CPython tag for your Python version (e.g. `cp312` for Python 3.12) to select the matching wheel.
    5. Installs the `dx_engine` wheel that matches your Python version. The glob expands to a single file.

    Do not use `pip install dx-engine` — the PyPI release is yanked and does not match DX-RT 3.5.0.

### Option B: one-line script

```bash
curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-runtime/main/oneline-install.sh | sh # (1)!
```

1. Downloads and runs the install script directly from the DEEPX GitHub repository. Installs the NPU driver, DX-RT and firmware in one step. Does not install DX-APP or DX-Stream.

Installs the NPU driver, DX-RT and firmware in one step. Pin SDK 2.5.0:

```bash
curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-runtime/main/oneline-install.sh \
  | DX_RT_VERSION=3.5.0 DX_DRIVER_VERSION=2.7.0 DX_FW_VERSION=2.7.6 sh # (1)!
```

1. Environment variables pin each component to a specific version. Remove a variable to track the latest release for that component.

### Option C: clone and install

```bash
git clone --recurse-submodules https://github.com/DEEPX-AI/dx-runtime.git # (1)!
cd dx-runtime
./install.sh --all # (2)!
```

1. Clones the repository and all its submodules (driver, firmware, DX-APP, DX-Stream).
2. Runs the full installer. Use `--runtime-only` to install only the driver and DX-RT without DX-APP and DX-Stream.

### Restart and verify

A reboot is required after the driver installs. For firmware updates, do a **cold boot** (remove power for 10–30 seconds):

```bash
sudo reboot # (1)!
```

1. Use for driver-only changes. For firmware updates, do a cold boot instead: shut the machine down, remove power for 10–30 seconds, then power on. A plain reboot may not reset the NPU.

Verify the installation:

```bash
dxcli -s # (1)!
python3 -c "import dx_engine; print(dx_engine.__version__)" # (2)!
```

1. Prints device info, driver version, firmware version and NPU status. You should see `Device 0` with real version numbers.
2. Verifies the Python package is importable and prints its version string.

### Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-runtime/main/oneline-uninstall.sh | sh # (1)!
```

1. Downloads and runs the uninstall script. Removes the driver, DX-RT and all associated packages. Alternatively run `sudo apt purge libdxrt-bin dxrt-driver-dkms` directly.
