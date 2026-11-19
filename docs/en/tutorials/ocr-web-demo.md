---
title: PP-OCR web demo
description: Run a PaddleOCR server with NPU acceleration and a Gradio web demo for OCR on images and PDFs.
---

# PP-OCR web demo

This demo lets you run OCR on images and PDF files in your browser, with the OCR running on our NPU.

It has two parts. The OCR server is the FastAPI server in [PaddleOCR-deepx](https://github.com/DEEPX-AI/PaddleOCR-deepx), our PaddleOCR fork with NPU support (branch `deepx-v6`, which serves PP-OCRv5 and PP-OCRv6). The web UI is the Gradio app in [PP-OCR_Online_demo-deepx](https://github.com/DEEPX-AI/PP-OCR_Online_demo-deepx). The web UI does no OCR itself, it only calls the server.

## Before you start

* DX-RT installed and the NPU visible, see [Install](../get-started/install.md).
* Python 3.10 or newer, 2 GB RAM and about 500 MB of disk for the web demo.
* `git-lfs` for the example images (optional: without it the app works but some examples do not show).

## Steps

1. Get the server and set it up for the NPU. Point `--dx_rt` at your DX-RT source folder:

    ```bash
    git clone https://github.com/DEEPX-AI/PaddleOCR-deepx.git
    cd PaddleOCR-deepx
    git checkout deepx-v6
    cd deploy/fastapi
    ./local_deepx_setup.sh --dx_rt ~/dx-all-suite/dx-runtime/dx_rt
    ```

    The script rebuilds DX-RT from that folder and asks for your `sudo` password. It downloads all NPU model sets (v5 server, v5 mobile and v6). For a CPU only server use `./local_setup.sh` (or `./local_setup.sh --gpu`).

1. Start the server. Both options are required:

    ```bash
    ./run.sh --ocr-version v6 --model-size medium
    curl http://localhost:8080/health
    ```

    ```text
    {"status": "healthy"}
    ```

    | `--ocr-version` | `--model-size` values |
    |---|---|
    | `v6` | `medium`, `small`, `tiny` |
    | `v5` | `server`, `mobile` |

1. In a second terminal, install and start the web demo:

    ```bash
    sudo apt-get install git-lfs
    git lfs install
    git clone https://github.com/DEEPX-AI/PP-OCR_Online_demo-deepx.git
    cd PP-OCR_Online_demo-deepx
    git lfs pull
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    python app.py
    ```

    For a server on another host or port, set `export API_URL="http://<host>:<port>/api/v1/ocr"` before `python app.py`. The app reads only the real environment variable, not a `.env` file.

1. Open `http://localhost:7860`, upload a PDF, JPG or PNG (or click an example) and pick **DEEPX NPU** or **CPU** as the inference device.

## Expected result

The page shows the image with text boxes, the JSON result and a Performance tab. On the NPU the Performance tab also shows the time per OCR stage. Measured end to end demo latency for one page on DX-M1:

| Server started with | NPU (image) | CPU (image) | NPU (PDF) |
|---|---|---|---|
| `--ocr-version v5 --model-size server` | 1.94 s | 11.95 s | 0.98 s |
| `--ocr-version v5 --model-size mobile` | 0.94 s | 3.75 s | 0.59 s |
| `--ocr-version v6 --model-size medium` | 1.51 s | 9.84 s | 0.86 s |
| `--ocr-version v6 --model-size small` | 0.96 s | 4.00 s | 0.62 s |
| `--ocr-version v6 --model-size tiny` | 0.81 s | 1.78 s | 0.54 s |

## Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| `API request failed` | Server not running or wrong URL | `curl http://localhost:8080/health`; start `./run.sh`; set `API_URL` |
| `Address already in use` | Port 7860 is taken | `lsof -i :7860`; change `server_port` at the end of `app.py` |
| Server slow or out of memory at start | Model too large | Restart with `--model-size tiny` or `small` (v6) or `mobile` (v5) |
| `Failed to load CPU models: No available model hosting platforms detected` | A proxy re-signs TLS, so the CPU model download fails | `export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt` and restart the server |

## Next steps

* [PP-OCRv6 camera OCR](ocr-camera.md)
* [RapidDoc document parsing](rapiddoc.md)
* [Tutorials](index.md)
