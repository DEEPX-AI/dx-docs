<!-- Single source of truth for compiler install instructions.
     This file is included via pymdownx.snippets in:
       - en/get-started/install.md
       - en/compiler/index.md
     Edit ONLY here — never edit the included content in those pages. -->

## Install the compiler

### Pre-installation requirements

Install the system libraries that `dx-com` depends on before installing the Python package.

=== "Debian / Ubuntu"

    ```bash
    sudo apt-get install -y --no-install-recommends libgl1 libglib2.0-0 make # (1)!
    ```

    1. `libgl1` and `libglib2.0-0` are required by OpenCV which is bundled with `dx-com`. `make` is used by some build steps.

=== "Fedora"

    ```bash
    sudo dnf install -y mesa-libGL glib2 make
    ```

=== "RHEL / CentOS 9–10"

    ```bash
    sudo dnf install -y dnf-plugins-core
    sudo dnf config-manager --set-enabled crb # (1)!
    sudo dnf install -y mesa-libGL glib2 make
    ```

    1. `mesa-libGL` lives in the CodeReady Builder (CRB) repository on RHEL/CentOS — enable it first.

### Install

=== "PyPI (recommended)"

    ```bash
    pip install dx-com # (1)!
    ```

    1. Installs DX-COM and all its dependencies (PyTorch, ONNX Runtime, OpenCV and others). The first install downloads around 8 GB.

=== "One-line script"

    ```bash
    curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-compiler/main/oneline-install.sh | sh # (1)!
    ```

    1. Creates a dedicated virtualenv at `~/deepx/venv-dx-compiler`, installs `dx-com` and links the `dxcom` launcher to `~/.local/bin`. No repository clone required.

    Available environment variables to customise the install:

    | Variable | Default | Description |
    |---|---|---|
    | `DX_VERSION` | latest on PyPI | Pin a specific `dx-com` release, e.g. `DX_VERSION=2.5.0` |
    | `DX_INSTALL_DIR` | `~/deepx` | Root directory for the virtualenv |
    | `DX_BIN_DIR` | `~/.local/bin` | Where the `dxcom` launcher is linked |
    | `DX_NO_UV` | — | Set to `1` to force pip instead of uv |
    | `UV_PIN` | pinned by default | Bootstrap a specific uv release |

    **System-wide install** (shared machine):

    ```bash
    curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-compiler/main/oneline-install.sh \
      | sudo DX_INSTALL_DIR=/opt/deepx DX_BIN_DIR=/usr/local/bin sh
    ```

=== "uv"

    ```bash
    uv pip install dx-com # (1)!
    ```

    1. Uses [uv](https://docs.astral.sh/uv/)'s faster resolver — significantly quicker than plain pip for large dependency sets like PyTorch and ONNX Runtime.

=== "Local wheel"

    Download the wheel matching your Python version from the DEEPX release and install it directly:

    ```bash
    pip install dx_com-<VERSION>-cp312-cp312-manylinux_2_31_x86_64.whl # (1)!
    ```

    1. Replace `cp312` with your Python tag (e.g. `cp310` for Python 3.10). Wheels are tagged `manylinux_2_31_x86_64` and require glibc ≥ 2.31 (Ubuntu 20.04+, RHEL/CentOS 9+, Fedora 42+).

Works on x86_64 Linux and Windows.

Verify:

```bash
dxcom -v # (1)!
python3 -c "import dx_com; print(dx_com.__version__)" # (2)!
```

1. Prints the CLI version. Expected output: `dxcom version 2.5.0`.
2. Verifies the Python package is importable and prints its version string.

??? tip "How to set up a virtual environment first (recommended)"

    Installing into a virtual environment keeps `dx-com` and its large dependencies (PyTorch, ONNX Runtime, OpenCV) isolated from your system Python. DX-COM pulls in around 8 GB on first install, so an isolated environment also makes it easy to remove later.

    **With the standard `venv` module**

    ```bash
    python3 -m venv ~/dx-com-venv # (1)!
    source ~/dx-com-venv/bin/activate # (2)!
    pip install dx-com
    ```

    1. Creates an isolated Python environment at `~/dx-com-venv`. The folder can be placed anywhere.
    2. Activates the environment. Must be run again at the start of every new terminal session.

    **With a specific Python version** (e.g. 3.12)

    ```bash
    python3.12 -m venv ~/dx-com-venv # (1)!
    source ~/dx-com-venv/bin/activate
    pip install dx-com
    ```

    1. Replace `3.12` with any supported version from 3.8 to 3.14. Run `python3 --version` to check what is installed on your system.

    **With [uv](https://docs.astral.sh/uv/)** (faster downloads, automatic Python management)

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh # (1)!
    ```

    1. Downloads and installs uv globally. Only needs to be done once per machine.

    ```bash
    uv venv ~/dx-com-venv --python 3.12 # (1)!
    source ~/dx-com-venv/bin/activate # (2)!
    uv pip install dx-com # (3)!
    ```

    1. Creates the environment. If Python 3.12 is not installed, uv downloads it automatically.
    2. Activates the environment.
    3. Installs DX-COM using uv's faster resolver — significantly quicker than plain pip for large packages like PyTorch.

    To deactivate run `deactivate`. To remove entirely: `rm -rf ~/dx-com-venv`.

    !!! note "Activate before every session"
        `dxcom` and `import dx_com` only work while the environment is active. Activate it at the start of each terminal session with `source ~/dx-com-venv/bin/activate`.

??? tip "Uninstall"

    **If installed via the one-line script:**

    ```bash
    curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-compiler/main/oneline-uninstall.sh | sh # (1)!
    ```

    1. Removes the virtualenv and the `dxcom` launcher. Pass the same `DX_INSTALL_DIR` / `DX_BIN_DIR` you used at install time if you changed the defaults.

    For the system-wide install:

    ```bash
    curl -fsSL https://raw.githubusercontent.com/DEEPX-AI/dx-compiler/main/oneline-uninstall.sh \
      | sudo DX_INSTALL_DIR=/opt/deepx DX_BIN_DIR=/usr/local/bin sh
    ```

    **If installed via pip into a virtualenv:**

    ```bash
    pip uninstall dx-com
    # or remove the entire environment:
    rm -rf ~/dx-com-venv
    ```
