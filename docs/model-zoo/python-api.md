---
title: DX-ModelZoo Python API
description: Reference for ModelBuilder, sessions, runtime configuration, DataLoader, DatasetBase, evaluators and registries in DX-ModelZoo.
---

# DX-ModelZoo Python API

This page documents the Python classes of DX-ModelZoo 1.0.0, so you can run evaluations from your own scripts or extend the zoo.

## Before you start

* DX-ModelZoo installed, see [Install DX-ModelZoo](install.md).
* For NPU sessions: `dx_engine` from DX-RT, see [DX-RT Python API](../runtime/python-api.md).

## Quick example

```python
from dx_modelzoo.loader.model_builder import ModelBuilder

builder = ModelBuilder("src/dx_modelzoo/models/cv/image_classification/resnet/resnet50_224x224.yaml")
result = builder.run_eval("onnx")
print(result["metrics"])
```

## ModelBuilder

Module: `dx_modelzoo.loader.model_builder`. Reads a YAML file and builds everything a profile needs.

```python
ModelBuilder(yaml_path: Union[str, Path], resolve_env: bool = True)
```

| Parameter | Meaning |
|---|---|
| `yaml_path` | Path to the model YAML |
| `resolve_env` | Replace `${VAR}` values with environment variables (default `True`) |

The constructor loads the YAML, replaces variables, imports `custom_ops.py` from the YAML folder and validates the file.

### Properties

| Property | Type | Meaning |
|---|---|---|
| `name` | `str` | YAML `name` |
| `inputs` | `list[dict]` | Input tensor definitions |
| `config` | `dict` | Parsed YAML |
| `yaml_path` | `Path` | YAML file path |
| `model_dir` | `Path` | Folder of the YAML file |
| `appendix` | `dict` | YAML `appendix` block |
| `is_pipeline` | `bool` | `True` for a pipeline YAML |
| `pipeline_stages` | `list[str]` | Stage names of a pipeline YAML |

### Methods

| Method | Returns | What it does |
|---|---|---|
| `get_profile(profile_name, stage=None)` | `dict` | The profile block |
| `get_stage_config(stage)` | `dict` | One stage of a pipeline YAML |
| `build_preprocessing(profile_name, modal=None, input_dtype=None, stage=None)` | `PreprocessingPipeline` | Preprocessing for the profile. For NPU profiles, `input_dtype="uint8"` skips arithmetic steps. `modal` picks one input of a multi input model. |
| `build_postprocessing(stage=None)` | `PostprocessingPipeline` | Postprocessing (same for every profile) |
| `build_session(profile_name, model_path=None, device=None, stage=None)` | `SessionBase` | `OnnxRuntimeSession` or `DxRuntimeSession`. Downloads a missing model file when `DXMZ_MODEL_URL` is set. `device` overrides `runtime.device`. |
| `build_dataset(data_dir=None)` | `DatasetBase` | Dataset from the YAML. `data_dir` overrides `eval_path`. |
| `build_evaluator(session, dataset, profile_name=None)` | `EvaluatorBase` | Evaluator from `evaluator.type`, else `task`. Applies `appendix` and `evaluator.options`. |
| `run_eval(profile_name, data_dir=None, model_path=None, device=None)` | `dict` | Builds all parts, runs the evaluation and returns the result dict (see [Evaluate models](evaluate.md#read-the-results)) |

### Step by step

```python
from dx_modelzoo.loader.model_builder import ModelBuilder

builder = ModelBuilder("resnet50_224x224.yaml")
session = builder.build_session("onnx")
dataset = builder.build_dataset()

evaluator = builder.build_evaluator(session, dataset, "onnx")
evaluator.set_preprocessing(builder.build_preprocessing("onnx"))
evaluator.set_postprocessing(builder.build_postprocessing())
result = evaluator.eval()

session.close()
```

## Sessions

Module: `dx_modelzoo.session`.

### SessionBase

```python
class SessionBase(ABC):
    def __init__(self, path: str, device_count: int = 1, runtime_config=None)
    def run(self, inputs) -> list[np.ndarray]           # abstract, synchronous
    def run_async(self, inputs, **kwargs) -> int        # returns a job id
    def wait(self, job_id: int) -> list[np.ndarray]
    def close(self) -> None
```

`inputs` is an `np.ndarray`, or a dict of input name to array for multi input models. Sessions are context managers: `with OnnxRuntimeSession("model.onnx") as s:` calls `close()` at the end.

### OnnxRuntimeSession

Module: `dx_modelzoo.session.onnx_session`.

```python
OnnxRuntimeSession(path: str, runtime_config: Optional[RuntimeConfig] = None)
```

* Uses the CUDA provider when `device` is `gpu` (or CUDA device IDs) and CUDA is available, else the CPU.
* `run_async` uses a thread pool. Its size is `ONNX_ASYNC_WORKERS`, or the CPU core count (at least 4).
* Needs `onnxruntime` or `onnxruntime-gpu`.

```python
import numpy as np
from dx_modelzoo.session.onnx_session import OnnxRuntimeSession

session = OnnxRuntimeSession("resnet18.onnx")
outputs = session.run(np.random.randn(1, 3, 224, 224).astype(np.float32))
session.close()
```

### DxRuntimeSession

Module: `dx_modelzoo.session.dx_session`.

```python
DxRuntimeSession(path: str, runtime_config: Optional[RuntimeConfig] = None)
```

* Runs a `.dxnn` file with the DX-RT `InferenceEngine`. Needs `dx_engine`.
* `dtype` attribute: list of model input data types.
* Devices come from `runtime_config.device`. `DXNN_DEVICES` (for example `0,1`) overrides them. With neither, all NPU devices are used.
* Batch size is always 1. Asynchronous inference is the default.

```python
from dx_modelzoo.session.dx_session import DxRuntimeSession
from dx_modelzoo.session.runtime_config import DxnnRuntimeConfig

session = DxRuntimeSession("model.dxnn", runtime_config=DxnnRuntimeConfig(device=[0, 1]))
job_id = session.run_async(input_tensor)
outputs = session.wait(job_id)
session.close()
```

### create_session

Module: `dx_modelzoo.session.factory`.

```python
create_session(model_or_profile: str, *, builder=None, runtime_config=None) -> SessionBase
```

| Argument | Result |
|---|---|
| Existing `.onnx` file path | `OnnxRuntimeSession` |
| Existing `.dxnn` file path | `DxRuntimeSession` |
| Profile name plus `builder` | Session for the profile's `target`. Finds the file from `artifacts.path` and downloads it from `DXMZ_MODEL_URL` when missing. |

A missing file without `DXMZ_MODEL_URL` raises `SessionCreationError: Model file not found`.

### Runtime configuration

Module: `dx_modelzoo.session.runtime_config`. Built from the YAML `runtime` block.

```python
@dataclass
class RuntimeConfig:
    device: Any = None
    batch_size: int = 1
    async_mode: Optional[bool] = None
    start_method: str = "auto"

@dataclass
class OnnxRuntimeConfig(RuntimeConfig):   # async default False
    ...

@dataclass
class DxnnRuntimeConfig(RuntimeConfig):   # async default True
    buffer_count: Optional[int] = None
    use_ort: bool = True
```

| Member | Meaning |
|---|---|
| `RuntimeConfig.from_profile(profile, target=None)` | Returns `DxnnRuntimeConfig` for `target: dxnn`, else `OnnxRuntimeConfig` |
| `use_async` | `async_mode`, or the backend default when it is `None` |
| `with_device_override(device)` | Copy with another device |
| `start_method` | `auto`, `forkserver` or `spawn`. `auto` picks `forkserver` when available, else `spawn`. |

YAML `runtime.async` maps to `async_mode`.

## DatasetBase and DataLoader

Module: `dx_modelzoo.common.dataloader`.

### DatasetBase

```python
class DatasetBase(ABC):
    def __init__(self, data_dir: str)          # calls validate()
    preprocessing                               # property, set by the evaluator
    def __len__(self) -> int                    # abstract
    def __getitem__(self, idx: int) -> tuple    # abstract
    def validate(self) -> None                  # abstract
    def ensure_exists(self, data_dir: str, install_guide: str) -> None
```

* Reading `preprocessing` before it is set raises `ValueError: Dataset's preprocessing is not set.` Inside `__getitem__`, check `self._preprocessing`.
* `ensure_exists` raises `FileNotFoundError` with your install guide text when the folder is missing.
* Errors in `validate` are raised as `DatasetValidationError`.

See [Custom models and datasets](custom-models.md#add-a-custom-dataset) for a full example.

### DataLoader

A NumPy data loader (no PyTorch tensors).

```python
DataLoader(
    dataset: DatasetBase,
    batch_size: int = 1,
    shuffle: bool = False,
    num_workers: int = 0,
    collate_fn: Optional[Callable] = None,
    prefetch_factor: int = 2,
    start_method: str = "auto",
)

make_dataloader(dataset, batch_size=1, shuffle=False, num_workers=0, collate_fn=None, start_method="auto") -> DataLoader
```

| Parameter | Meaning |
|---|---|
| `num_workers` | `0` loads in the main process. More starts worker processes. |
| `collate_fn` | Batch function. Default: see below. |
| `prefetch_factor` | Batches prepared ahead per worker |
| `start_method` | Worker process start method |

`len(loader)` is the number of batches. The default collate merges only mapping (dict) samples into stacked arrays. Tuple samples come back as a list of samples (or the single sample when `batch_size=1`). Pass your own `collate_fn` to get stacked arrays:

```python
def my_collate(batch):
    images = [item[0] for item in batch]
    labels = [item[1] for item in batch]
    return images, labels

loader = DataLoader(dataset, batch_size=4, collate_fn=my_collate)
```

It has no `sampler`, `drop_last` or `pin_memory` options.

## Evaluators

Module: `dx_modelzoo.evaluator`.

### EvaluatorBase

```python
class EvaluatorBase(ABC):
    def __init__(self, session, dataset, workers: int = 12, batch_size: int = 1)
    postprocessing                                    # property
    def set_preprocessing(self, preprocessing) -> None
    def set_postprocessing(self, postprocessing) -> None
    def make_loader(self) -> DataLoader
    def eval(self) -> dict
```

`workers` is capped at the CPU core count. `eval()` runs in async mode when the session's runtime config has `use_async`, else in sync mode. It returns the result dict. On an exception it returns a result with an `error` field instead of raising. `model_name`, `dataset_name` and `profile_name` are set by `ModelBuilder.run_eval`.

Methods a subclass must implement:

| Method | Called | Returns |
|---|---|---|
| `init_metrics()` | once, before the loop | Initial metric state |
| `extract_inputs(batch_data)` | per batch | Model input |
| `process_batch_result(batch_data, output, metrics_state)` | per batch, `output` already postprocessed | Updated state |
| `compute_final_metrics(metrics_state)` | once, after the loop | Final metrics |
| `format_progress_desc(metrics_state, current_fps)` | per batch | Progress bar text |

### Built in evaluators

| Registry key | Task | Main metrics |
|---|---|---|
| `image_classification` | Classification | Top-1, Top-5 |
| `zero_shot_image_classification` | Zero shot classification | Top-1 |
| `image_retrieval` | Image retrieval | Top-1, Top-5 retrieval accuracy |
| `object_detection` | Object detection | COCO mAP |
| `3d_object_detection` | 3D object detection | 3D AP |
| `oriented_object_detection` | Oriented detection | mAP |
| `face_detection` | Face detection | AP |
| `hand_detection` | Hand detection | AP |
| `mainbody_detection` | Main body detection | AP |
| `instance_segmentation` | Instance segmentation | mAP |
| `zero_shot_instance_segmentation` | Zero shot instance segmentation | mAP |
| `semantic_segmentation` | Semantic segmentation | mIoU |
| `person_segmentation` | Person segmentation | mIoU |
| `panoptic_driving_perception` | Driving perception | Detection and segmentation metrics |
| `pose_estimation` | Pose estimation | AP, AR |
| `pose_estimation_topdown` | Top down pose estimation | AP, AR |
| `face_landmark` | Face landmark | NME |
| `hand_landmark` | Hand landmark | NME |
| `keypoint_detection` | Keypoint detection | Matching and repeatability metrics |
| `object_pose_estimation` | 6 DoF object pose | ADD, ADD-S, PnP metrics |
| `face_recognition` | Face recognition | Accuracy |
| `face_attribute` | Face attribute | Accuracy |
| `person_attribute` | Person attribute | mA |
| `person_reid` | Person re identification | Rank-1, mAP |
| `depth_estimation` | Depth estimation | δ < 1.25, RMSE |
| `super_resolution` | Super resolution | PSNR |
| `image_denoising` | Denoising | PSNR |
| `low_light_enhancement` | Low light enhancement | PSNR, SSIM |
| `image_matting` | Matting | SAD, MSE |
| `anomaly_detection` | Anomaly detection | AUROC, F1 |
| `visual_place_recognition` | Place recognition | Retrieval metrics |

## Registry

Module: `dx_modelzoo.common.registry`.

```python
class Registry:
    def __init__(self, name: str)
    def register(self, name_or_cls=None)    # decorator: @R.register("name") or @R.register
    def get(self, name: str) -> type          # KeyError when unknown
    def list(self) -> list[str]
    def __contains__(self, name: str) -> bool
    def __len__(self) -> int
```

| Instance | Import from |
|---|---|
| `PREPROCESSING_REGISTRY` | `dx_modelzoo.preprocessing` |
| `POSTPROCESSING_REGISTRY` | `dx_modelzoo.postprocessing` |
| `DATASET_REGISTRY` | `dx_modelzoo.dataset` |
| `EVALUATOR_REGISTRY` | `dx_modelzoo.evaluator` |

```python
from dx_modelzoo.dataset import DATASET_REGISTRY

dataset_cls = DATASET_REGISTRY.get("ILSVRC2012")
print(DATASET_REGISTRY.list())
```

## Next steps

* [Preprocessing and postprocessing](processing-ops.md)
* [Architecture](architecture.md)
* [Custom models and datasets](custom-models.md)
