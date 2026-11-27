---
title: Compilation summary report
description: Generate the self contained HTML report of a DX-COM compile, with model details, settings and an NPU and CPU graph viewer.
---

# Compilation summary report

This page lets you create an HTML report of a compiled model, so you can see its inputs, outputs, settings and which parts run on the NPU or the CPU.

The report replaces DX-TRON, which was deprecated in DX-COM 2.4.0 and removed in 2.5.0.

## Before you start

* Install DX-COM: see [Install](../get-started/install.md). The report needs `jinja2`, which `dx-com` installs.
* A model and config that compile. See [Compile a model](compile-a-model.md).

## Generate the report

The report is off by default. Turn it on when you compile:

=== "CLI"
    ```bash
    dxcom -m model.onnx -c config.json -o output/ --export_html
    ```

=== "Python"
    ```python
    import dx_com

    dx_com.compile(
        model="model.onnx",
        output_dir="output/",
        config="config.json",
        export_html=True,
    )
    ```

On success DX-COM prints:

```text
[dx_com] Summary HTML saved to: output/model_summary.html
```

| Item | Detail |
|---|---|
| File name | `<model_name>_summary.html`, from the ONNX file name |
| Location | The compile output directory |
| Format | One self contained HTML file: all styles and scripts are embedded |

Open it in any web browser. You can share the single file without the rest of the output directory.

## What the report shows

| Section | Content |
|---|---|
| Model overview | Model name, original file name, total parameter count, ONNX and `.dxnn` file sizes. |
| Input and output tensors | Names and shapes, from the static shapes of the compiled graph when available. |
| Compilation settings | Optimization level, aggressive partitioning, calibration method and sample count, quantization scheme, target NPU and compiler version. |
| Graph viewer | Pan and zoom view of the compiled graph: which partitions run on the NPU and which on the CPU, with the reason for each CPU fallback, parameter shapes and connections between subgraphs. |

## Troubleshooting

The report is a best effort step after compiling. If it fails, DX-COM prints a warning and the compile still succeeds: the `.dxnn` is not affected.

| Problem | Check |
|---|---|
| No HTML file | You passed `--export_html` (or `export_html=True`). Look for a warning in the compile log that the report was skipped or failed. |
| The report opens but the graph is empty | The compile produced a valid `.dxnn` in the same output directory. The viewer reads the compiled graph. |

## Next steps

* [Compile a model](compile-a-model.md)
* [Troubleshooting](troubleshooting.md)
* [Run the model with DX-RT](../runtime/index.md)
