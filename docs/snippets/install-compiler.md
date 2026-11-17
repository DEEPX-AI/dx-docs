## Install the compiler

```bash
pip install dx-com # (1)!
```

1. Installs DX-COM and all its dependencies (PyTorch, ONNX Runtime, OpenCV and others). The first install downloads around 8 GB.

Works on x86_64 Linux and Windows. With [uv](https://docs.astral.sh/uv/): `uv pip install dx-com`.

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
