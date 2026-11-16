---
title: CLIP in Python
description: Run CLIP text and image matching in Python with the text encoder on ONNX Runtime and the image encoder on the NPU.
---

# CLIP in Python

This demo lets you compute CLIP text and image similarity in Python and match text against a live camera.

The text encoder runs with ONNX Runtime on the CPU and the image encoder runs on the NPU. The code is in [dx-clip-starter](https://github.com/DEEPX-AI/dx-clip-starter).

## Before you start

* DX-RT installed, see [Install](../get-started/install.md).
* A camera for the live scripts. On Raspberry Pi 5 see the note in step 2.
* To compile your own image encoder: DX-COM on an x86_64 host.

## Steps

1. Get the code and create an environment:

    ```bash
    git clone https://github.com/DEEPX-AI/dx-clip-starter
    cd dx-clip-starter
    python3 -m venv .venv-clip
    source .venv-clip/bin/activate
    pip install -r requirements.txt
    pip install ~/dx-all-suite/dx-runtime/dx_rt/python_package
    ```

1. On Raspberry Pi 5, use the system PyQt5 and the Pi requirements instead:

    ```bash
    sudo apt update
    sudo apt install python3-pyqt5
    python3 -m venv --system-site-packages .venv-clip
    source .venv-clip/bin/activate
    pip install -r requirements-rpi5.txt
    pip install ~/dx-all-suite/dx-runtime/dx_rt/python_package
    ```

1. Download the compiled models. This creates `dxnn/` and `onnx/`; the ViT-L-14 image encoder alone is 594 MB:

    ```bash
    wget https://cs.deepx.ai/_deepx_fae_archive/demo_application/clip-models.tar.gz
    tar xzf clip-models.tar.gz
    ```

    The archive has four image encoders (`ViT-B-16-dfn2b`, `ViT-B-16-quickgelu-metaclip_fullcc`, `ViT-B-32-quickgelu-metaclip_fullcc`, `ViT-L-14-quickgelu-dfn2b`) with their text encoders. `ViT-L-14-quickgelu-dfn2b` is the default.

1. Compute the similarity of some texts with an image:

    ```bash
    python3 simple-text-image-similarity.py \
      --texts "a cat" "a dog" "a person" "fine in car" \
      --image assets/img-encoder-sample-1.png
    ```

    ```text
    Text-Image Similarity:
    --------------------------------------------------
    Text                                    Similarity
    --------------------------------------------------
    fine in car                              0.1748
    a person                                 0.0459
    a dog                                    0.0217
    a cat                                    0.0016
    --------------------------------------------------
    ```

1. Try the other scripts:

    | Script | What it does |
    |---|---|
    | `simple-text-encoder.py --onnx-model onnx/ViT-L-14-quickgelu-dfn2b-text.onnx --texts "a photo of a cat" "a dog" --show-similarity` | Text encoder only |
    | `simple-image-encoder.py --model dxnn/ViT-L-14-quickgelu-dfn2b.dxnn --image assets/img-encoder-sample-1.png` | Image encoder only |
    | `camera-text-matcher.py --texts "a person" "thumbs up"` | Top 3 matches on the camera feed |
    | `camera-text-matcher-async.py --texts "a person" "thumbs up"` | Same with async inference, higher FPS |
    | `camera-text-matcher-async-gui.py --texts "A person clapping hands" "A person holding a cup"` | GUI with a score card per text |

    The GUI also takes a video: add `--input assets/CLIP-demo.mp4`. To use another model pair, pass `--text-encoder onnx/ViT-B-16-dfn2b-text.onnx --image-encoder dxnn/ViT-B-16-dfn2b.dxnn`.

    | Option | Default | Meaning |
    |---|---|---|
    | `--camera` | `/dev/video0` | Camera device |
    | `--width`, `--height`, `--fps` | 1280, 720, 30 | Camera mode (MJPEG) |
    | `--skip-frames` | 2 | Encode one frame out of `N + 1` |
    | `--no-normalize` | off | Skip L2 normalization |

## Compile your own encoder

Export the text encoder and the image encoder to ONNX, then compile the image encoder. `export_to_onnx.py` also writes the compiler JSON into `onnx/`:

```bash
python3 export_to_onnx_text_encoder.py --model ViT-L-14-quickgelu --pretrained dfn2b
python3 export_to_onnx.py --model ViT-L-14-quickgelu --pretrained dfn2b
deactivate
source ~/dx-all-suite/dx-compiler/venv-dx-compiler-local/bin/activate
dxcom -m onnx/ViT-L-14-quickgelu-dfn2b.onnx -c onnx/ViT-L-14-quickgelu-dfn2b.json -o dxnn
```

Supported model names: ViT-B-16-dfn2b, ViT-B-16-quickgelu-metaclip_fullcc, ViT-B-32-256-datacomp_s34b_b86k, ViT-B-32-quickgelu-metaclip_fullcc, ViT-L-14-336-openai, ViT-L-14-datacomp_xl_s13b_b90k, ViT-L-14-quickgelu-dfn2b.

## Troubleshooting

| What you see | Cause | Fix |
|---|---|---|
| `Duplicate definition of name (embedding)` | Text encoder exported with an old script | Export it again with the current `export_to_onnx_text_encoder.py` |
| `Failed to open camera: /dev/video0` | Wrong camera path | `ls -la /dev/video*` and pass `--camera` |
| `No module named 'dx_engine'` | `dx_engine` not in the environment | `pip install ~/dx-all-suite/dx-runtime/dx_rt/python_package` |
| `shapes (4,768) and (1,1) not aligned` | Text and image encoder from different models | Use a matching pair |

## Next steps

* [CLIP in C++](clip-cpp.md)
* [CLIP multi channel demo](clip-multi-channel.md)
* [Python API](../runtime/python-api.md)
