---
title: RapidDoc document parsing
description: Parse PDF documents into text, tables and formulas with RapidDoc, running layout, OCR and table models on the NPU.
---

# RapidDoc document parsing

This demo lets you parse PDFs (digital or scanned) into structured text, tables and formulas with the models running on our NPU.

[RapidDoc](https://github.com/DEEPX-AI/RapidDoc) is our fork of the RapidDoc document parser with DX-RT engines. You do not compile any model: `setup.sh` downloads the compiled ONNX and DXNN models. Only the DEEPX parts are described here; the rest of the repository is upstream documentation.

## Before you start

* DX-RT installed and the NPU visible, see [Install](../get-started/install.md).
* Python 3.10 to 3.13.
* Two or more NPUs only for hybrid mode.

## Steps

1. Get the code and create the environment that the scripts expect (`venv`):

    ```bash
    git clone https://github.com/DEEPX-AI/RapidDoc.git
    cd RapidDoc
    python3 -m venv venv
    source venv/bin/activate
    pip install ~/dx-all-suite/dx-runtime/dx_rt/python_package
    pip install -r requirements.deepx.txt
    pip install -e .
    python -c "from dx_engine import InferenceEngine; print('dx_engine OK')"
    ```

1. Download the models into `dxnn_models/` and `onnx_models/`:

    ```bash
    ./setup.sh
    ```

    Use `./setup.sh --force-remove-models` to download them again, and `./setup.sh --docker_volume_path=/path/to/volume` inside a container.

1. Set the runtime variables. The demos stop unless these are set:

    ```bash
    source ./deepx_scripts/set_env.sh 1 2 1 3 2 4
    ```

    This sets, in order, `CUSTOM_INTER_OP_THREADS_COUNT=1`, `CUSTOM_INTRA_OP_THREADS_COUNT=2`, `DXRT_DYNAMIC_CPU_THREAD=1`, `DXRT_TASK_MAX_LOAD=3`, `NFH_INPUT_WORKER_THREADS=2` and `NFH_OUTPUT_WORKER_THREADS=4`. `DXRT_TASK_MAX_LOAD` may have any value; the others must match. Pass `-1` to unset one.

1. Parse the sample PDFs:

    ```bash
    python demo/demo_offline.py test_files --finegrained
    ```

    The output goes to `demo/output-offline-{mode}/`, with a `performance_summary_YYYYMMDD_HHMMSS.md` file of per stage timing.

## Options for demo_offline.py

| Option | Meaning |
|---|---|
| `PATH` | PDF files or folders; default `test_files/` |
| `--finegrained` | Default. 7 stage streaming pipeline per page (Layout, Plan, Formula, PDF det, OCR det, Table, OCR rec) |
| `--use-async` | Batch pipeline: all pages through each stage in turn |
| `--no-async` | Sequential pipeline, slowest |
| `--parse-method auto` | Default. Text layer where present, OCR only for pages without text |
| `--parse-method txt` | Text layer only, no OCR, fastest |
| `--parse-method ocr` | OCR on every page, for scanned PDFs |
| `--no-formula` | Keep formulas as images instead of LaTeX |
| `--hybrid` | Give each model its own NPU; needs 2 or more NPUs |
| `--output-dir DIR` | Output folder |

```bash
python demo/demo_offline.py test_files/document.pdf --parse-method txt
export DXNN_DEVICES=0,1,2,3
python demo/demo_offline.py test_files --finegrained --hybrid
```

## Environment variables

| Variable | Default | Meaning |
|---|---|---|
| `DXNN_DEVICES` | auto detect | NPU device IDs, for example `0` or `0,1,2,3` |
| `DXRT_TASK_MAX_LOAD` | 3 | NPU I/O buffer depth; higher needs more NPU memory |
| `CUSTOM_INTER_OP_THREADS_COUNT` | 1 | Inter op threads |
| `CUSTOM_INTRA_OP_THREADS_COUNT` | 2 | Intra op threads |

## Other demos

| Command | What it starts |
|---|---|
| `python demo/app_offline.py` | FastAPI server; options `--host`, `--port`, `--pipeline-mode {finegrained,async,sync}`, `--hybrid` or `--no-hybrid`, `--deepx-default` or `--no-deepx-default` |
| `curl http://localhost:8888/health` | Health check of that server |
| `python demo/gradio_app.py` | Web UI at `http://localhost:7860` |
| `python demo/benchmark_pipeline.py --pdf test_files/sample.pdf -n 3` | Benchmark; add `--legacy-async`, `--no-async`, `--hybrid` or `--json-report bench.json` |
| `python run_with_npu_monitor.py python demo/demo_offline.py test_files --finegrained` | Run a command and print NPU utilization from `dxtop` (`--interval 1.0`) |

OCR detection uses four models by aspect ratio (64x640, 160x640, 320x640, 640x640) and recognition uses six width ratio models (3, 5, 10, 15, 25, 35).

## Expected result

For each PDF the output folder holds the parsed document and a performance summary. On a 12 page digital PDF, `--parse-method txt` takes about 5 s and `--parse-method ocr` about 200 s.

## Next steps

* [PP-OCR web demo](ocr-web-demo.md)
* [Python API](../runtime/python-api.md)
* [Tutorials](index.md)
