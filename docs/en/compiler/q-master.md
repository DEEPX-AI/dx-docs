---
title: Q-Master (QAT)
description: Fine tune a model with quantization aware training in DX-COM when post training quantization is not accurate enough.
---

# Q-Master (QAT)

This page lets you recover accuracy with Q-Master, our quantization aware training (QAT): DX-COM fine tunes the model while it simulates INT8 quantization.

In short: add a `qmaster` block to the JSON config you already use, run `dxcom` as usual, and you get a fine tuned `.dxnn`. You need no labels, no training script and no extra command line flag. Q-Master is available from DX-COM 2.4.0. DX-COM 2.5.0 adds the Python `QMasterConfig` and segmentation models.

## Before you start

* The model already compiles with PTQ using the same JSON config, and you tried the steps on [Quantization](quantization.md).
* A CUDA GPU that PyTorch can use. This must print `True`:

    ```bash
    python3 -c "import torch; print(torch.cuda.is_available())"
    ```

* A folder of representative images in `default_loader.dataset_path` (searched recursively by `file_extensions`). Use images like your real input, not the test set you report accuracy on.
* A way to compare accuracy of the PTQ `.dxnn` and the Q-Master `.dxnn` on the same evaluation set.

## PTQ or Q-Master

| | PTQ | Q-Master (QAT) |
|---|---|---|
| Data | Calibration images only (about 100) | Training images (hundreds to thousands) |
| GPU | Not needed | Needed (CUDA, default `cuda:0`) |
| Compile time | Minutes | Minutes to hours, depending on model and data size |
| Changes the weights | No | Yes, fine tuned |
| Typical use | First attempt | Accuracy still below target after PTQ tuning |

## Quick start

1. Add a `qmaster` block to your PTQ config. Example for an ImageNet classifier:

    ```json
    {
      "inputs": {"input": [1, 3, 224, 224]},
      "calibration_num": 100,
      "calibration_method": "ema",
      "default_loader": {
        "dataset_path": "/datasets/ILSVRC2012/train",
        "file_extensions": ["jpeg", "jpg", "png", "JPEG"],
        "preprocessings": [
          {"resize": {"mode": "default", "size": 256}},
          {"centercrop": {"width": 224, "height": 224}},
          {"convertColor": {"form": "BGR2RGB"}},
          {"div": {"x": 255}},
          {"normalize": {"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}},
          {"transpose": {"axis": [2, 0, 1]}},
          {"expandDim": {"axis": 0}}
        ]
      },
      "qmaster": {
        "batch_size": 16,
        "train_limit": 2000,
        "val_limit": 200,
        "epochs": 10
      }
    }
    ```

    `default_loader.preprocessings` is used for both calibration and training. Do not repeat it inside `qmaster`.

1. Run a smoke test first: add `"fast_run": true` to the `qmaster` block. It trains 1 epoch on 1 batch (100 training and 10 validation images) to prove that the pipeline works. The accuracy is not meaningful. Remove `fast_run` for the real run.

1. Compile:

    ```bash
    dxcom -m model.onnx -c config_with_qmaster.json -o output/ --gen_log
    ```

1. Check the result:

    | File | Description |
    |---|---|
    | `output/<model>.dxnn` | The compiled model. Same format and runtime as a PTQ model. |
    | `output/qat_checkpoint/qat_checkpoint.qxnn` | The best checkpoint (lowest validation loss). |
    | `output/compiler.log` | Starts with a **Q-MASTER CONFIG** box with the values actually used, then the metrics of each epoch. |

1. Compare accuracy with your PTQ result. Q-Master does not guarantee a gain. The original ONNX file is never changed.

!!! warning "Apply convertColor again at inference"
    `convertColor` never moves into the NPU graph. Your inference code must apply the same `BGR2RGB` conversion, or accuracy drops without an error.

## How it works

1. **Calibration**: estimates the first quantization parameters, the same as PTQ.
1. **Training (stage 1)**: fine tunes the model with simulated quantization at your `batch_size`. Saves the checkpoint with the lowest validation loss to `qat_checkpoint/qat_checkpoint.qxnn`.
1. **Compilation (stage 2)**: turns the trained weights into the `.dxnn`, always at batch size 1.

By default Q-Master uses knowledge distillation (KD): the original FP32 model is the teacher and the quantized model learns to reproduce its output. With the defaults (`kd_loss` `"mse"`, `kd_alpha` `1.0`) training uses only the teacher output, so unlabeled images work.

## Recipes

Copy the closest recipe and change only what you need.

| Recipe | `qmaster` block | Notes |
|---|---|---|
| A. Default, no labels | `{"batch_size": 16, "train_limit": 2000, "val_limit": 200, "epochs": 10}` | Teacher only MSE distillation. Good first attempt for any model. Any folder layout. |
| B. Classification with labels | `{"batch_size": 16, "train_limit": 5000, "val_limit": 500, "criterion": "cross_entropy", "kd_loss": "kl_div", "kd_temperature": 2.0, "kd_alpha": 0.5}` | Mixes the teacher signal (`kd_alpha`) with the label loss. Needs an ImageFolder layout: `<dataset_path>/<class_name>/<image>`. |
| C. Embedding or encoder model (for example CLIP image encoder) | `{"encoder_mode": true, "kd_alpha": 1.0}` | Tracks cosine similarity instead of accuracy. |
| D. Zero shot classification (for example CLIP) | `{"zeroshot_weights_path": "/path/to/text_embedding.npy", "use_kd": false}` | Cannot be combined with `use_kd` or `encoder_mode`. |
| E. Segmentation (2.5.0 and later) | `{"task_type": "segmentation", "seg_root": "/path/to/dataset_root", "seg_pairs_train": "/path/to/dataset_root/lists/train.txt", "seg_pairs_val": "/path/to/dataset_root/lists/val.txt", "seg_ignore_index": 255, "seg_binary": true, "use_kd": false}` | See [Segmentation](#segmentation). |
| F. Out of GPU memory | `{"batch_size": 4, "gradient_accumulation_steps": 4}` | Effective batch stays 4 × 4 = 16. |
| G. Compile again without training, or keep training | `{"stage1_mode": "skip"}` | See [Reuse a checkpoint](#reuse-a-checkpoint). |

If `train_limit` plus `val_limit` is more than the number of images found, all images are used.

!!! warning "Labels come from folder names"
    In recipe B, class indices are built from the class folders found in the images actually loaded (`train_limit` plus `val_limit`). If a class is missing from that subset, all label indices shift and training learns the wrong classes. Make sure every class is present, or use recipe A.

If CUDA runs out of memory, DX-COM retries stage 1 at batch size 1. That works but is much slower, so lower `batch_size` yourself.

## Parameter reference

Every key is optional. Missing keys use these defaults.

### Data and device

| Key | Default | Description |
|---|---|---|
| `batch_size` | `1` | Training batch size for stage 1. Use more than 1 (for example 16) for faster, more stable training. Models whose input has no batch axis of 1 (for example fixed length text encoders) fall back to 1. |
| `num_workers` | `4` | DataLoader workers. |
| `train_limit` | `500` | Number of training images. The default is small (smoke test scale): raise it to thousands for real training. |
| `val_limit` | `50` | Number of validation images, taken from the same pool before the training images. |
| `train_drop_last` | `true` | Drops the last incomplete training batch. |
| `val_drop_last` | `false` | Drops the last incomplete validation batch. |
| `device` | `"cuda:0"` | Training device. Pick the physical GPU with `CUDA_VISIBLE_DEVICES` and keep `"cuda:0"`. |
| `train_cpu_fp` | `false` | Also trains the parts of the model that run on CPU and writes their weights back into the compiled model. With `false` those weights stay frozen. |

### Training loop

| Key | Default | Description |
|---|---|---|
| `epochs` | `30` | Maximum epochs. |
| `lr` | `1e-5` | Learning rate. Lower it (for example `5e-6`) if accuracy gets worse from the first epoch. |
| `optimizer` | `"adamw"` | `"adamw"` or `"sgd"`. |
| `weight_decay` | `1e-4` | Optimizer weight decay. |
| `scheduler` | `null` | `null`, `"cosine"` or `"step"`. |
| `scheduler_step_size` | `max(1, (epochs - warmup_epochs) // 3)` | Epoch interval, for `"step"` only. |
| `warmup_epochs` | `0` | Linear learning rate warmup epochs. |
| `max_grad_norm` | `1.0` | Gradient clipping. |
| `use_amp` | `true` | Mixed precision training. |
| `gradient_accumulation_steps` | `1` | Effective batch is `batch_size` times this value. |
| `early_stopping_patience` | `5` | Stops after this many epochs without validation loss improvement. `null` turns it off. Needs validation data. |
| `early_stopping_delta` | `1e-3` | Smallest improvement that counts as progress. |
| `save_best_model` | `true` | Saves the checkpoint with the lowest validation loss. |
| `freeze_bn_after` | `null` | From this epoch on, freezes BatchNorm and stops updating activation quantization ranges. See [Pitfalls](#pitfalls). |

### Loss and knowledge distillation

The loss is `kd_alpha * KD_loss + (1 - kd_alpha) * task_loss`.

| Key | Default | Description |
|---|---|---|
| `use_kd` | `true` | Uses the FP32 teacher. |
| `kd_loss` | `"mse"` | `"mse"`, `"kl_div"`, `"cosine"`, `"bce"`, `"smooth_l1"`, `"ciou"`, `"giou"`. |
| `kd_alpha` | `1.0` | KD weight from 0 to 1. At `1.0` the task loss is not computed. |
| `kd_temperature` | `4.0` | Softening temperature. Only for `"kl_div"` and `"bce"`. |
| `kd_box_format` | `"xyxy"` | Box format for `"ciou"` and `"giou"`: `"xyxy"`, `"cxcywh"`, `"xywh"`. |
| `criterion` | `"mse"` | Task loss: `"mse"` or `"cross_entropy"` (`"seg_ce"` for segmentation). Used only when `kd_alpha` is below 1.0 or `use_kd` is `false`. `"cross_entropy"` switches to the labeled ImageFolder loader. |
| `label_smoothing` | `0.0` | Cross entropy only. |

| Goal | Settings |
|---|---|
| No labels | Defaults (`kd_alpha` 1.0, `kd_loss` `"mse"`) |
| Classification with labels | `criterion` `"cross_entropy"`, `kd_loss` `"kl_div"`, `kd_alpha` 0.5 to 0.7 |
| No teacher | `use_kd` `false` plus a `criterion` |

### Mode switches

| Key | Default | Description |
|---|---|---|
| `encoder_mode` | `false` | Tracks cosine similarity instead of accuracy (embedding and encoder models). It does not turn off the task loss: keep `kd_alpha` at 1.0. |
| `zeroshot_weights_path` | none | `.npy` text embedding file for zero shot models. |
| `stage1_mode` | `"fresh"` | `"fresh"`, `"resume"` or `"skip"`. See [Reuse a checkpoint](#reuse-a-checkpoint). Other values raise `ValueError`. |
| `fast_run` | `false` | Smoke test: 1 epoch on 1 batch, 100 training and 10 validation images. Accuracy is not meaningful. |

### Segmentation

| Key | Default | Description |
|---|---|---|
| `task_type` | `"classification"` | Set `"segmentation"` for dense (image, mask) data. |
| `seg_root` | none | Root folder for the pair lists. |
| `seg_pairs_train`, `seg_pairs_val` | none | Text files with one `<image_path> <mask_path>` per line, relative to `seg_root`. |
| `seg_ignore_index` | `255` | Label value left out of loss and metric. |
| `seg_binary` | `true` | Binary (foreground and background) segmentation. Set `false` for multi class. |

With `task_type` `"segmentation"`, `criterion` defaults to `"seg_ce"`. Masks do not go through `preprocessings`; only the image does.

## Reuse a checkpoint

`stage1_mode` sets what happens when `<output_dir>/qat_checkpoint/qat_checkpoint.qxnn` already exists:

| `stage1_mode` | Behavior | Use when |
|---|---|---|
| `"fresh"` (default) | Trains from the start and overwrites the checkpoint. | First run. |
| `"resume"` | Loads the checkpoint weights and keeps training (optimizer and epoch counter restart). Without a checkpoint it trains from scratch with a warning. | Fine tune further with a lower `lr`. |
| `"skip"` | Skips training and only compiles. The checkpoint must exist. | Build the `.dxnn` again, for example after a DX-COM update. |

```json
{
  "qmaster": {"stage1_mode": "skip"}
}
```

To start from a checkpoint made elsewhere, copy it to `<output_dir>/qat_checkpoint/qat_checkpoint.qxnn` first. Without it, `"skip"` fails with `FileNotFoundError: The QAT staged compilation setup is invalid or incomplete`.

## Python

A `qmaster` block in the JSON config starts Q-Master from Python too:

```python
import dx_com

dx_com.compile(model="model.onnx", config="config_with_qmaster.json", output_dir="output/")
```

To set the training keys in code instead, pass `qmaster=QMasterConfig(...)` and always set `batch_size`. See [QMasterConfig](python-api.md#qmasterconfig). `fast_run` and `stage1_mode` are keys of the `qmaster` block, not `compile()` arguments. In Python use `skip_training` and `resume_from_checkpoint`.

!!! warning "Changed in 2.5.0"
    The arguments `quantization_mode`, `qat_config`, `qat_skip_training` and `qat_resume_from_checkpoint` were replaced by `qmaster`. Do not pass them.

## Pitfalls

* **Unknown keys are ignored without an error.** A misspelled key (for example `learning_rate`) silently uses the default. Check the **Q-MASTER CONFIG** box in `compiler.log`.
* **Check that Q-Master ran.** `compiler.log` must show the **Q-MASTER CONFIG** box and training lines per epoch, and no `falling back` message. Otherwise the result is plain PTQ.
* **The dataset path falls back without an error.** If `default_loader.dataset_path` is missing or invalid, DX-COM uses a built in default ImageNet location. Check the dataset path in the log.
* **The best checkpoint is picked by validation loss**, which includes the KD term. It can differ from the checkpoint with the best Top 1 accuracy.
* **`freeze_bn_after` freezes BatchNorm and the activation ranges.** `0` freezes from the first epoch (after one warm up pass), which can make the loss go to `nan`. Leave it `null`, or use a later epoch.
* **Do not combine with Q-PRO.** `qmaster` with `use_q_pro` or `enhanced_scheme` raises `EnhancementSchemeError: use_q_pro/enhanced_scheme (Q-PRO re-quantization) and qmaster (QAT) are mutually exclusive. Set only one.`
* **`train_limit` 500 is for quick checks.** Use thousands of images for a real run.

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| CUDA out of memory | `batch_size` too large for the GPU | Lower `batch_size`, raise `gradient_accumulation_steps`. |
| Loss becomes `nan` | `freeze_bn_after` 0, or `lr` too high | Set `freeze_bn_after` to `null` or a later epoch; lower `lr`. |
| Best epoch is 1 and later epochs get worse | `lr` too high | Lower `lr`, or use `stage1_mode` `"resume"` with a smaller `lr`. |
| Training stops very early | `early_stopping_patience` too small, or noisy validation | Raise `early_stopping_patience` and `val_limit`. |
| Accuracy not better than PTQ | Too little data, or loss not suited | Raise `train_limit`. For classification with labels, use recipe B. |
| Label loss learns the wrong classes | A class is missing from the loaded subset | Check the class folders, raise `train_limit`, or use recipe A. |
| Training used unexpected data | `dataset_path` invalid, silent fallback | Check the dataset path in `compiler.log`. |
| Settings seem to have no effect | Key misspelled or in the wrong block | Check the **Q-MASTER CONFIG** box in `compiler.log`. |
| Training metrics are good but `.dxnn` accuracy dropped | Loss in a compiler step that training cannot see | Compare the `.dxnn` with the original model on the same evaluation set and report the gap to us. |
| `ValueError: Q-Master dispatch could not determine training batch size` | `QMasterConfig(config=...)` without `batch_size` | Set `batch_size` in `config`. |

## FAQ

* **Do I need labeled data?** No. The default recipe learns from the FP32 model and uses images only. Only recipe B needs labels.
* **Can I use my own dataset?** Yes. Point `default_loader.dataset_path` at your images and keep the PTQ preprocessing.
* **Can I train on the calibration images?** Yes, but more varied images usually work better. Never train on the images you report final accuracy on.
* **Is the `.dxnn` different from a PTQ one?** Same format and runtime. Only the weights and quantization parameters differ.
* **I want to try another setting. Do I start over?** Use `stage1_mode` `"resume"` to continue from the checkpoint, or `"fresh"` with a new `output_dir`.
* **I only want to rebuild the `.dxnn`.** Use `stage1_mode` `"skip"` with the existing checkpoint.

## Next steps

* [Quantization](quantization.md)
* [Python API](python-api.md#qmasterconfig)
* [Config file reference](config-reference.md)
