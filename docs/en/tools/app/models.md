---
title: Model catalog
description: Every model that DX-APP ships a C++ and a Python example for, grouped by task, with input size, dataset and license.
---

# Model catalog

This page lists every model that DX-APP ships a ready to run example for, grouped by AI task.

## At a glance

* DX-APP 3.3.0 registers **497 model variants** in **29 task folders**.
* Every variant has **both** a C++ example (sync and async) and a Python example (sync, async, and the two `*_cpp_postprocess` variants).
* That is 994 C++ entry files and 1988 Python entry scripts, built from one `config/model_registry.json`.
* All 497 variants have a downloadable `.dxnn` file. 492 of them can also run inside a [multi model graph](multi-model-graph.md).

The table on each row gives the **variant**: the `.dxnn` file stem. The variant names everything else, so you can build and run any row without looking anything up.

## How to run any example

Replace `<task>`, `<family>` and `<variant>` with the values from a row below (the task folder is in each section title, the family in the table).

1. Download the model. The variant name works as a model name:

    ```bash
    ./setup.sh --models <variant>
    ```

1. Run it.

    === "Python"

        ```bash
        python3 src/python_example/<task>/<family>/<variant>/<variant>_sync.py
        ```

    === "C++"

        ```bash
        ./build.sh --target <variant>_sync <variant>_async
        ./bin/<variant>_sync
        ```

Without an input option, an example uses the default sample image of its task, and without `-m` it uses `assets/models/<variant>.dxnn` (downloaded if it is missing). Add `-i <image>`, `-v <video>`, `-c <camera index>` or `-r <rtsp url>` to choose the input. All options are on [Run the examples](run-examples.md).

For example, the YOLOv9-S detector is in the task folder `object_detection`, family `yolov9`, variant `yolov9-s_640x640`:

```bash
./setup.sh --models yolov9-s_640x640
python3 src/python_example/object_detection/yolov9/yolov9-s_640x640/yolov9-s_640x640_sync.py --image sample/img/sample_street.jpg
```

!!! note "Licenses"
    Each model comes from a third party project with its own license (AGPL-3.0, GPL-3.0, Apache-2.0 and others). The sample models are for evaluation only. Check [Third party licenses](licenses.md) before any commercial use.

## Tasks

| Task | Folder | Variants |
|---|---|---:|

| [3D Object Detection](#3d-object-detection) | `3d_object_detection` | 1 |
| [Anomaly Detection](#anomaly-detection) | `anomaly_detection` | 4 |
| [Attribute Recognition](#person-attribute) | `person_attribute` | 2 |
| [Classification](#image-classification) | `image_classification` | 136 |
| [Depth Estimation](#depth-estimation) | `depth_estimation` | 10 |
| [Embedding](#face-recognition) | `face_recognition` | 4 |
| [Face Alignment](#face-landmark) | `face_landmark` | 2 |
| [Face Attribute](#face-attribute) | `face_attribute` | 1 |
| [Face Detection](#face-detection) | `face_detection` | 18 |
| [Hand Detection](#hand-detection) | `hand_detection` | 1 |
| [Hand Landmark](#hand-landmark) | `hand_landmark` | 1 |
| [Image Denoising](#image-denoising) | `image_denoising` | 5 |
| [Image Enhancement](#low-light-enhancement) | `low_light_enhancement` | 2 |
| [Image Matting](#image-matting) | `image_matting` | 2 |
| [Image Retrieval](#image-retrieval) | `image_retrieval` | 2 |
| [Instance Segmentation](#instance-segmentation) | `instance_segmentation` | 53 |
| [Keypoint Detection](#keypoint-detection) | `keypoint_detection` | 1 |
| [Main-body Detection](#mainbody-detection) | `mainbody_detection` | 2 |
| [OBB Detection](#oriented-object-detection) | `oriented_object_detection` | 5 |
| [Object Detection](#object-detection) | `object_detection` | 167 |
| [Object Pose Estimation](#object-pose-estimation) | `object_pose_estimation` | 1 |
| [Panoptic Driving Perception](#panoptic-driving-perception) | `panoptic_driving_perception` | 1 |
| [Pose Estimation](#pose-estimation) | `pose_estimation` | 36 |
| [Re-Identification](#person-reid) | `person_reid` | 1 |
| [Semantic Segmentation](#semantic-segmentation) | `semantic_segmentation` | 24 |
| [Super Resolution](#super-resolution) | `super_resolution` | 6 |
| [Visual Place Recognition](#visual-place-recognition) | `visual_place_recognition` | 3 |
| [Zero-Shot Classification](#zero-shot-image-classification) | `zero_shot_image_classification` | 5 |
| [Zero-Shot Segmentation](#zero-shot-instance-segmentation) | `zero_shot_instance_segmentation` | 1 |

## 3D Object Detection { #3d-object-detection }

Task folder `3d_object_detection`, 1 variants.

SFA3D reads a KITTI LiDAR point cloud (`.bin`), not an image. Pass one `.bin` file or a `velodyne/` folder with `--image`; the default sample is `sample/kitti/velodyne/000049.bin`. Video, camera and RTSP input are refused.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| SFA3D | `sfa3d_608x608` | `sfa3d` | 608x608x3 | KITTI | MIT |

## Anomaly Detection { #anomaly-detection }

Task folder `anomaly_detection`, 4 variants.

The anomaly detection models cannot run in a multi model graph in this release.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| EfficientAD-M Autoencoder | `efficientad-m-autoencoder_256x256` | `efficientad` | 256x256x3 | MVTecAD | Apache-2.0 |
| EfficientAD-M Student | `efficientad-m-student_256x256` | `efficientad` | 256x256x3 | MVTecAD | Apache-2.0 |
| EfficientAD-M Teacher | `efficientad-m-teacher_256x256` | `efficientad` | 256x256x3 | MVTecAD | Apache-2.0 |
| PatchCore 224x224 | `patchcore_224x224` | `patchcore` | 224x224x3 | MVTecAD | Apache-2.0 |

## Attribute Recognition { #person-attribute }

Task folder `person_attribute`, 2 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| DeepMAR ResNet-18 | `deepmar_resnet18_224x224` | `deepmar` | 224x224x3 | PETA | MIT |
| DeepMAR ResNet-50 | `deepmar_resnet50_224x224` | `deepmar` | 224x224x3 | PETA | MIT |

## Classification { #image-classification }

Task folder `image_classification`, 136 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| AlexNet | `alexnet_224x224` | `alexnet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| BEiT-Large/16 | `beit-l-p16_224x224` | `beit` | 224x224x3 | ILSVRC2012 | MIT |
| BEiT-Large/16 (384x384) | `beit-l-p16_384x384` | `beit` | 384x384x3 | ImageNet | MIT |
| CAS-ViT-M | `casvit-m_224x224` | `casvit` | 224x224x3 | ImageNet | MIT |
| CAS-ViT-T | `casvit-t_224x224` | `casvit` | 224x224x3 | ImageNet | MIT |
| DeiT-Base (224x224) | `deit-b_224x224` | `deit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| DeiT-Base (distilled, 224x224) | `deit-b_224x224_distilled` | `deit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| DeiT-Base (384x384) | `deit-b_384x384` | `deit` | 384x384x3 | ILSVRC2012 | Apache-2.0 |
| DeiT-Base (distilled, 384x384) | `deit-b_384x384_distilled` | `deit` | 384x384x3 | ILSVRC2012 | Apache-2.0 |
| DeiT-Small | `deit-s_224x224` | `deit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| DeiT-Small (distilled) | `deit-s_224x224_distilled` | `deit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| DeiT-Tiny | `deit-t_224x224` | `deit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| DeiT-Tiny (distilled) | `deit-t_224x224_distilled` | `deit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| DenseNet-121 | `densenet121_224x224` | `densenet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| DenseNet-161 | `densenet161_224x224` | `densenet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| DenseNet-169 | `densenet169_224x224` | `densenet` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| DenseNet-201 | `densenet201_224x224` | `densenet` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| EfficientFormer-L3 | `efficientformer-l3_224x224` | `efficientformer` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| EfficientFormer-L7 | `efficientformer-l7_224x224` | `efficientformer` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| EfficientFormerV2-L | `efficientformerv2-l_224x224` | `efficientformer` | 224x224x3 | ImageNet | Apache-2.0 |
| EfficientNet-B2 | `efficientnet-b2_288x288` | `efficientnet` | 288x288x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| EfficientNet-B3 | `efficientnet-b3_300x300` | `efficientnet` | 300x300x3 | ILSVRC2012 | BSD-3-Clause |
| EfficientNet-B4 | `efficientnet-b4_380x380` | `efficientnet` | 380x380x3 | ILSVRC2012 | BSD-3-Clause |
| EfficientNet-B5 | `efficientnet-b5_456x456` | `efficientnet` | 456x456x3 | ILSVRC2012 | BSD-3-Clause |
| EfficientNet-B6 | `efficientnet-b6_528x528` | `efficientnet` | 528x528x3 | ILSVRC2012 | BSD-3-Clause |
| EfficientNet-B7 | `efficientnet-b7_600x600` | `efficientnet` | 600x600x3 | ILSVRC2012 | Apache-2.0 |
| EfficientNet-Lite0 | `efficientnet-lite0_224x224` | `efficientnet` | 256x256x3 | ILSVRC2012 | Apache-2.0 |
| EfficientNet-Lite1 | `efficientnet-lite1_240x240` | `efficientnet` | 240x240x3 | ImageNet (ILSVRC2012) | Apache-2.0 |
| EfficientNet-Lite2 | `efficientnet-lite2_260x260` | `efficientnet` | 260x260x3 | ImageNet (ILSVRC2012) | Apache-2.0 |
| EfficientNet-Lite3 | `efficientnet-lite3_300x300` | `efficientnet` | 300x300x3 | ImageNet (ILSVRC2012) | Apache-2.0 |
| EfficientNet-Lite4 | `efficientnet-lite4_380x380` | `efficientnet` | 380x380x3 | ImageNet (ILSVRC2012) | Apache-2.0 |
| EfficientNetV2-L | `efficientnetv2-l_480x480` | `efficientnet` | 480x480x3 | ILSVRC2012 | BSD-3-Clause |
| EfficientNetV2-M | `efficientnetv2-m_480x480` | `efficientnet` | 480x480x3 | ILSVRC2012 | Apache-2.0 |
| EfficientNetV2-S | `efficientnetv2-s_384x384` | `efficientnet` | 384x384x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| FastViT-MA36 | `fastvit-ma36_256x256` | `fastvit` | 256x256x3 | ILSVRC2012 | Apple Sample Code License |
| FastViT-SA24 | `fastvit-sa24_256x256` | `fastvit` | 256x256x3 | ILSVRC2012 | Apple Sample Code License |
| FastViT-SA36 | `fastvit-sa36_256x256` | `fastvit` | 256x256x3 | ILSVRC2012 | Apple Sample Code License |
| GhostNet | `ghostnet_224x224` | `ghostnet` | 224x224x3 | ILSVRC2012 | No License |
| HarDNet-39DS | `hardnet39ds_224x224` | `hardnet` | 224x224x3 | ImageNet (ILSVRC2012) | MIT |
| HarDNet-68 | `hardnet68_224x224` | `hardnet` | 224x224x3 | ImageNet (ILSVRC2012) | MIT |
| GoogLeNet (Inception v1) | `inceptionv1_224x224` | `inception` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| LeViT-128 | `levit-128_224x224` | `levit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| LeViT-128S | `levit-128s_224x224` | `levit` | 224x224x3 | ImageNet | Apache-2.0 |
| LeViT-192 | `levit-192_224x224` | `levit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| LeViT-256 | `levit-256_224x224` | `levit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| LeViT-384 | `levit-384_224x224` | `levit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| MnasNet-0.5 | `mnasnet-0.5_224x224` | `mnasnet` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| MnasNet-0.75 | `mnasnet-0.75_224x224` | `mnasnet` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| MnasNet-1.0 | `mnasnet-1.0_224x224` | `mnasnet` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| MnasNet-1.3 | `mnasnet-1.3_224x224` | `mnasnet` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| MobileNetV1 | `mobilenetv1_224x224` | `mobilenet` | 224x224x3 | ImageNet (ILSVRC2012) | Apache-2.0 |
| MobileNetV2 | `mobilenetv2_224x224` | `mobilenet` | 224x224x3 | ImageNet (ILSVRC2012) | Apache-2.0 |
| MobileNetV3-Large | `mobilenetv3-large_224x224` | `mobilenet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| PPHGNet_base | `pphgnet-base_224x224` | `pphgnet` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| PPHGNet_small | `pphgnet-small_224x224` | `pphgnet` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| PPHGNet_tiny | `pphgnet-tiny_224x224` | `pphgnet` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| PPHGNetV2_B0 | `pphgnetv2-b0_224x224` | `pphgnetv2` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| PPHGNetV2_B1 | `pphgnetv2-b1_224x224` | `pphgnetv2` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| PPHGNetV2_B2 | `pphgnetv2-b2_224x224` | `pphgnetv2` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| PPHGNetV2_B3 | `pphgnetv2-b3_224x224` | `pphgnetv2` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| PPHGNetV2_B4 | `pphgnetv2-b4_224x224` | `pphgnetv2` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| PPHGNetV2_B5 | `pphgnetv2-b5_224x224` | `pphgnetv2` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| PPHGNetV2_B6 | `pphgnetv2-b6_224x224` | `pphgnetv2` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| PPLCNetV2_base | `pplcnetv2-base_224x224` | `pplcnetv2` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| PPLCNetV2_large | `pplcnetv2-large_224x224` | `pplcnetv2` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| PPLCNetV2_small | `pplcnetv2-small_224x224` | `pplcnetv2` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| RegNetX-1.6GF (v1) | `regnet-x1.6gf_224x224_v1` | `regnet` | 224x224x3 | ImageNet (ILSVRC2012) | Apache-2.0 |
| RegNetX-1.6GF (v2) | `regnet-x1.6gf_224x224_v2` | `regnet` | 224x224x3 | ImageNet | BSD-3-Clause |
| RegNetX-16GF | `regnet-x16gf_224x224` | `regnet` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| RegNetX-3.2GF | `regnet-x3.2gf_224x224` | `regnet` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| RegNetX-32GF | `regnet-x32gf_224x224` | `regnet` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| RegNetX-400MF | `regnet-x400mf_224x224` | `regnet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| RegNetX-800MF | `regnet-x800mf_224x224` | `regnet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| RegNetX-8GF | `regnet-x8gf_224x224` | `regnet` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| RegNetY-1.6GF | `regnet-y1.6gf_224x224` | `regnet` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| RegNetY-16GF | `regnet-y16gf_384x384` | `regnet` | 384x384x3 | ILSVRC2012 | Apache-2.0 |
| RegNetY-200MF | `regnet-y200mf_224x224` | `regnet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| RegNetY-3.2GF | `regnet-y3.2gf_224x224` | `regnet` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| RegNetY-32GF | `regnet-y32gf_384x384` | `regnet` | 384x384x3 | ILSVRC2012 | Apache-2.0 |
| RegNetY-400MF | `regnet-y400mf_224x224` | `regnet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| RegNetY-800MF | `regnet-y800mf_224x224` | `regnet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| RegNetY-8GF | `regnet-y8gf_224x224` | `regnet` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| RepGhost-2.0x | `repghost-2.0x_224x224` | `repghost` | 224x224x3 | ILSVRC2012 | MIT |
| RepVGG-A0 | `repvgg-a0_320x320` | `repvgg` | 320x320x3 | ILSVRC2012 | MIT |
| RepVGG-A1 | `repvgg-a1_320x320` | `repvgg` | 320x320x3 | ILSVRC2012 | MIT |
| RepVGG-A2 | `repvgg-a2_320x320` | `repvgg` | 320x320x3 | ILSVRC2012 | MIT |
| RepVGG-B0 | `repvgg-b0_320x320` | `repvgg` | 320x320x3 | ILSVRC2012 | MIT |
| RepVGG-B1 | `repvgg-b1_320x320` | `repvgg` | 320x320x3 | ILSVRC2012 | MIT |
| ResMLP-24 | `resmlp24_224x224` | `resmlp` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| ResNet-101 | `resnet101_224x224` | `resnet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| ResNet-152 | `resnet152_224x224` | `resnet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| ResNet-18 | `resnet18_224x224` | `resnet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| ResNet-18 (BRECQ) | `resnet18_224x224_brecq` | `resnet` | 224x224 | ILSVRC2012 | Apache-2.0 |
| ResNet-34 | `resnet34_224x224` | `resnet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| ResNet-50 | `resnet50_224x224` | `resnet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| ResNeXt-101 (32x8d) | `resnext101-32x8d_224x224` | `resnext` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| ResNeXt-101 (64x4d) | `resnext101-64x4d_224x224` | `resnext` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| ResNeXt-26 (32x4d) | `resnext26-32x4d_224x224` | `resnext` | 224x224x3 | ImageNet (ILSVRC2012) | Apache-2.0 |
| ResNeXt-50 (32x4d) | `resnext50-32x4d_224x224` | `resnext` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| ResNeXt-50 (32x4d, imgclsmob) | `resnext50-32x4d_224x224_imgclsmob` | `resnext` | 224x224 | ILSVRC2012 | MIT |
| ShuffleNetV1-x1.0 | `shufflenetv1-x1.0_224x224` | `shufflenetv1` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| ShuffleNetV2-x0.5 | `shufflenetv2-x0.5_224x224` | `shufflenetv2` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| ShuffleNetV2-x1.0 | `shufflenetv2-x1.0_224x224` | `shufflenetv2` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| ShuffleNetV2-x1.5 | `shufflenetv2-x1.5_224x224` | `shufflenetv2` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| ShuffleNetV2-x2.0 | `shufflenetv2-x2.0_224x224` | `shufflenetv2` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| SqueezeNet-1.0 | `squeezenet-1.0_224x224` | `squeezenet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| SqueezeNet-1.1 | `squeezenet-1.1_224x224` | `squeezenet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| Swin-B 224x224 | `swin-b_224x224` | `swin` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| VGG-11 (BN) | `vgg11-bn_224x224` | `vgg` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| VGG-11 | `vgg11_224x224` | `vgg` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| VGG-13 (BN) | `vgg13-bn_224x224` | `vgg` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| VGG-13 | `vgg13_224x224` | `vgg` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| VGG-16 (BN) | `vgg16-bn_224x224` | `vgg` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| VGG-16 | `vgg16_224x224` | `vgg` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| VGG-19 (BN) | `vgg19-bn_224x224` | `vgg` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| VGG-19 | `vgg19_224x224` | `vgg` | 224x224x3 | ILSVRC2012 | BSD-3-Clause |
| ViT-Base/16 | `vit-b-p16_224x224` | `vit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| ViT-Base/16 (BN) | `vit-b-p16_224x224_bn` | `vit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| ViT-Base/16 (384x384) | `vit-b-p16_384x384` | `vit` | 384x384x3 | ImageNet | Apache-2.0 |
| ViT-Base/32 | `vit-b-p32_224x224` | `vit` | 224x224x3 | ImageNet | BSD-3-Clause |
| vit-l-p16_512x512_swag | `vit-l-p16_512x512_swag` | `vit` | 512x512x3 | ILSVRC2012 | BSD-3-Clause |
| ViT-Large/32 | `vit-l-p32_224x224` | `vit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| ViT-Small/16 | `vit-s-p16_224x224` | `vit` | 224x224x3 | ILSVRC2012 | Apache-2.0 |
| ViT-Tiny/16 | `vit-t-p16_224x224` | `vit` | 224x224x3 | ImageNet | Apache-2.0 |
| Wide-ResNet-101-2 | `wide-resnet101-2_224x224` | `wide_resnet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| Wide-ResNet-50-2 | `wide-resnet50-2_224x224` | `wide_resnet` | 224x224x3 | ImageNet (ILSVRC2012) | BSD-3-Clause |
| Ultralytics YOLO26-l-cls | `yolo26-cls-l_224x224` | `yolo26_cls` | 224x224x3 | ILSVRC2012 | AGPL-3.0 |
| Ultralytics YOLO26-m-cls | `yolo26-cls-m_224x224` | `yolo26_cls` | 224x224x3 | ILSVRC2012 | AGPL-3.0 |
| Ultralytics YOLO26-n-cls | `yolo26-cls-n_224x224` | `yolo26_cls` | 224x224x3 | ILSVRC2012 | AGPL-3.0 |
| Ultralytics YOLO26-s-cls | `yolo26-cls-s_224x224` | `yolo26_cls` | 224x224x3 | ILSVRC2012 | AGPL-3.0 |
| Ultralytics YOLO26-x-cls | `yolo26-cls-x_224x224` | `yolo26_cls` | 224x224x3 | ILSVRC2012 | AGPL-3.0 |
| YOLOv12-l-cls | `yolov12-cls-l_224x224` | `yolov12_cls` | 224x224x3 | ILSVRC2012 | AGPL-3.0 |
| YOLOv12-m-cls | `yolov12-cls-m_224x224` | `yolov12_cls` | 224x224x3 | ILSVRC2012 | AGPL-3.0 |
| YOLOv12-n-cls | `yolov12-cls-n_224x224` | `yolov12_cls` | 224x224x3 | ILSVRC2012 | AGPL-3.0 |
| YOLOv12-s-cls | `yolov12-cls-s_224x224` | `yolov12_cls` | 224x224x3 | ILSVRC2012 | AGPL-3.0 |
| YOLOv12-x-cls | `yolov12-cls-x_224x224` | `yolov12_cls` | 224x224x3 | ILSVRC2012 | AGPL-3.0 |

## Depth Estimation { #depth-estimation }

Task folder `depth_estimation`, 10 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| Depth-Anything-V2-ViT-B | `depthanythingv2-vitb_224x224` | `depthanythingv2` | 224x224x3 | NYUDepthv2 | CC BY-NC 4.0 |
| Depth-Anything-V2-ViT-L | `depthanythingv2-vitl_224x224` | `depthanythingv2` | 224x224x3 | NYUDepthv2 | CC BY-NC 4.0 |
| Depth-Anything-V2-ViT-S | `depthanythingv2-vits_224x224` | `depthanythingv2` | 224x224x3 | NYUDepthv2 | Apache-2.0 |
| FastDepth | `fastdepth_224x224` | `fastdepth` | 224x224x3 | NYU Depth V2 | MIT |
| SC-DepthV3 | `scdepthv3_256x320` | `scdepthv3` | 320x256x3 | NYUDepthv2 | GPL-3.0 |
| Ultralytics YOLO26-l-depth | `yolo26-depth-l_768x768` | `yolo26_depth` | 768x768 | NYUDepthv2 | AGPL-3.0 |
| Ultralytics YOLO26-m-depth | `yolo26-depth-m_768x768` | `yolo26_depth` | 768x768 | NYUDepthv2 | AGPL-3.0 |
| Ultralytics YOLO26-n-depth | `yolo26-depth-n_768x768` | `yolo26_depth` | 768x768 | NYUDepthv2 | AGPL-3.0 |
| Ultralytics YOLO26-s-depth | `yolo26-depth-s_768x768` | `yolo26_depth` | 768x768 | NYUDepthv2 | AGPL-3.0 |
| Ultralytics YOLO26-x-depth | `yolo26-depth-x_768x768` | `yolo26_depth` | 768x768 | NYUDepthv2 | AGPL-3.0 |

## Embedding { #face-recognition }

Task folder `face_recognition`, 4 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| ArcFace IResNet-100 (MS1M) | `arcface_iresnet100_112x112_ms1m` | `arcface` | 112x112x3 | LFW | MIT |
| ArcFace IResNet-50 (MS1M) | `arcface_iresnet50_112x112_ms1m` | `arcface` | 112x112x3 | LFW | MIT |
| ArcFace MobileFaceNet | `arcface_mobilefacenet_112x112` | `arcface` | 112x112x3 | LFW | MIT |
| ArcFace ResNet-50 | `arcface_resnet50_112x112` | `arcface` | 112x112x3 | LFW | MIT |

## Face Alignment { #face-landmark }

Task folder `face_landmark`, 2 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| 3DDFA-V2 (MobileNet-0.5) | `3ddfa-v2_mobilenet-0.5_120x120` | `3ddfa_v2` | 120x120x3 | AFLW20003D | MIT |
| 3DDFA-V2 (MobileNetV1) | `3ddfa-v2_mobilenetv1_120x120` | `3ddfa_v2` | 120x120x3 | AFLW20003D | MIT |

## Face Attribute { #face-attribute }

Task folder `face_attribute`, 1 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| FaceAttr ResNet-18 | `faceattr_resnetv1-18_218x178` | `faceattr` | 178x218x3 | CelebA | MIT |

## Face Detection { #face-detection }

Task folder `face_detection`, 18 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| RetinaFace (MobileNet-0.25) | `retinaface_mobilenet-0.25_640x640` | `retinaface` | 640x640x3 | WiderFace | MIT |
| RetinaFace (MobileNetV1) | `retinaface_mobilenetv1_736x1280` | `retinaface` | 736x1280x3 | WiderFace | MIT |
| SCRFD-10G | `scrfd-10g_640x640` | `scrfd` | 640x640x3 | WiderFace | MIT |
| SCRFD-2.5G | `scrfd-2.5g_640x640` | `scrfd` | 640x640x3 | WiderFace | MIT |
| SCRFD-500M | `scrfd-500m_640x640` | `scrfd` | 640x640x3 | WiderFace | MIT |
| ULFGFD-RFB (240x320) | `ulfgfd-rfb_240x320` | `ulfgfd` | 320x240x3 | WiderFace | MIT |
| ULFGFD-RFB (no-PP) | `ulfgfd-rfb_240x320_nopp` | `ulfgfd` | 320x240x3 | WiderFace | MIT |
| ULFGFD-RFB (480x640) | `ulfgfd-rfb_480x640` | `ulfgfd` | 640x480x3 | WiderFace | MIT |
| ULFGFD-Slim | `ulfgfd-slim_240x320` | `ulfgfd` | 320x240x3 | WiderFace | MIT |
| ULFGFD-Slim (no-PP) | `ulfgfd-slim_240x320_nopp` | `ulfgfd` | 320x240x3 | WiderFace | MIT |
| YOLOv5-m-face | `yolov5-m-face_640x640` | `yolov5_face` | 640x640x3 | WiderFace | GPL-3.0 |
| YOLOv5-n-face | `yolov5-n-face_640x640` | `yolov5_face` | 640x640x3 | WiderFace | GPL-3.0 |
| YOLOv5-s-face | `yolov5-s-face_640x640` | `yolov5_face` | 640x640x3 | WiderFace | GPL-3.0 |
| YOLOv7-face | `yolov7-face_640x640` | `yolov7_face` | 640x640x3 | WiderFace | GPL-3.0 |
| YOLOv7-lite-t-face | `yolov7-lite-t-face_640x640` | `yolov7_face` | 640x640x3 | WiderFace | GPL-3.0 |
| YOLOv7-s-face | `yolov7-s-face_640x640` | `yolov7_face` | 640x640x3 | WiderFace | GPL-3.0 |
| YOLOv7-w6-face (TTA) | `yolov7-w6-face_1280x1280_tta` | `yolov7_face` | 1280x1280x3 | WiderFace | GPL-3.0 |
| YOLOv7-w6-face | `yolov7-w6-face_960x960` | `yolov7_face` | 960x960x3 | WiderFace | GPL-3.0 |

## Hand Detection { #hand-detection }

Task folder `hand_detection`, 1 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| MediaPipe Hand (Palm) Detector | `mediapipe-hand-detector_192x192` | `mediapipe_hand_detector` | 192x192x3 | HandKeypointsDetection | Apache-2.0 |

## Hand Landmark { #hand-landmark }

Task folder `hand_landmark`, 1 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| MediaPipe Hands (Lite) | `mediapipe-hands-lite_224x224` | `mediapipe_hands_lite` | 224x224x3 | HandKeypoints | Apache-2.0 |

## Image Denoising { #image-denoising }

Task folder `image_denoising`, 5 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| DnCNN-15 | `dncnn-15_512x512` | `dncnn` | 512x512x1 | BSD68 | Apache-2.0 |
| DnCNN-25 | `dncnn-25_512x512` | `dncnn` | 512x512x1 | BSD68 | Apache-2.0 |
| DnCNN-50 | `dncnn-50_512x512` | `dncnn` | 512x512x1 | BSD68 | Apache-2.0 |
| DnCNN-color | `dncnn-color_512x512` | `dncnn` | 512x512x3 | CBSD68 | MIT |
| DnCNN-gray | `dncnn-gray_512x512` | `dncnn` | 512x512x1 | BSD68 | MIT |

## Image Enhancement { #low-light-enhancement }

Task folder `low_light_enhancement`, 2 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| Zero-DCE++ | `zerodce-pp_400x600` | `zerodce` | 400x600x3 | LOL | Non-commercial |
| Zero-DCE | `zerodce_400x600` | `zerodce` | 400x600x3 | LOL | CC BY-NC 4.0 |

## Image Matting { #image-matting }

Task folder `image_matting`, 2 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| ppmatting-hrnet_w48-composition | `ppmatting-hrnet-w48-composition_512x512` | `ppmatting` | 512x512x3 | Distinctions646 | Apache-2.0 |
| ppmatting-hrnet_w48-distinctions | `ppmatting-hrnet-w48-distinctions_512x512` | `ppmatting` | 512x512x3 | Distinctions646 | Apache-2.0 |

## Image Retrieval { #image-retrieval }

Task folder `image_retrieval`, 2 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| CLIP ResNet-50 (OpenAI) | `clip-img_resnet50_224x224_openai` | `clip_rn50` | 224x224x3 | ILSVRC2012 | MIT |
| CLIP ResNet-50 Text Encoder (OpenAI) | `clip-text_resnet50_77x512_openai` | `clip_rn50` | 77x512 | ImageNetText | MIT |

## Instance Segmentation { #instance-segmentation }

Task folder `instance_segmentation`, 53 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| mask_rtdetr_hgnetv2_h_6x_coco | `mask-rtdetr-hgnetv2-h-6x_640x640` | `mask_rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| mask_rtdetr_hgnetv2_l_6x_coco | `mask-rtdetr-hgnetv2-l-6x_640x640` | `mask_rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| mask_rtdetr_hgnetv2_m_6x_coco | `mask-rtdetr-hgnetv2-m-6x_640x640` | `mask_rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| mask_rtdetr_hgnetv2_s_6x_coco | `mask-rtdetr-hgnetv2-s-6x_640x640` | `mask_rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| mask_rtdetr_hgnetv2_x_6x_coco | `mask-rtdetr-hgnetv2-x-6x_640x640` | `mask_rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| YOLACT (RegNetX-1.6GF) | `yolact_regnet-x1.6gf_512x512` | `yolact` | 512x512x3 | COCO | MIT |
| YOLACT (RegNetX-800MF) | `yolact_regnet-x800mf_512x512` | `yolact` | 512x512x3 | COCO | MIT |
| Ultralytics YOLO11-l-seg | `yolo11-l-seg_640x640` | `yolo11_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-l-seg (Pre-Optimized) | `yolo11-l-seg_640x640_pre-optimized` | `yolo11_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-m-seg | `yolo11-m-seg_640x640` | `yolo11_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-m-seg (Pre-Optimized) | `yolo11-m-seg_640x640_pre-optimized` | `yolo11_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-n-seg | `yolo11-n-seg_640x640` | `yolo11_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-n-seg (Pre-Optimized) | `yolo11-n-seg_640x640_pre-optimized` | `yolo11_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-s-seg | `yolo11-s-seg_640x640` | `yolo11_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-s-seg (Pre-Optimized) | `yolo11-s-seg_640x640_pre-optimized` | `yolo11_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-x-seg | `yolo11-x-seg_640x640` | `yolo11_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-x-seg (Pre-Optimized) | `yolo11-x-seg_640x640_pre-optimized` | `yolo11_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-l-seg | `yolo26-l-seg_640x640` | `yolo26_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-m-seg | `yolo26-m-seg_640x640` | `yolo26_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-n-seg | `yolo26-n-seg_640x640` | `yolo26_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-s-seg | `yolo26-s-seg_640x640` | `yolo26_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-x-seg | `yolo26-x-seg_640x640` | `yolo26_seg` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-l-seg | `yolov12-seg-l_640x640` | `yolov12_seg` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-l-seg (Pre-Optimized) | `yolov12-seg-l_640x640_pre-optimized` | `yolov12_seg` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-m-seg | `yolov12-seg-m_640x640` | `yolov12_seg` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-m-seg (Pre-Optimized) | `yolov12-seg-m_640x640_pre-optimized` | `yolov12_seg` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-n-seg | `yolov12-seg-n_640x640` | `yolov12_seg` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-n-seg (Pre-Optimized) | `yolov12-seg-n_640x640_pre-optimized` | `yolov12_seg` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-s-seg | `yolov12-seg-s_640x640` | `yolov12_seg` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-s-seg (Pre-Optimized) | `yolov12-seg-s_640x640_pre-optimized` | `yolov12_seg` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-x-seg | `yolov12-seg-x_640x640` | `yolov12_seg` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-x-seg (Pre-Optimized) | `yolov12-seg-x_640x640_pre-optimized` | `yolov12_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv5-l-seg | `yolov5-l-seg_640x640` | `yolov5_seg` | 640x640x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-m-seg | `yolov5-m-seg_640x640` | `yolov5_seg` | 640x640x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-n-seg | `yolov5-n-seg_640x640` | `yolov5_seg` | 640x640x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-s-seg | `yolov5-s-seg_640x640` | `yolov5_seg` | 640x640x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-x-seg | `yolov5-x-seg_640x640` | `yolov5_seg` | 640x640x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv8-l-seg | `yolov8-l-seg_640x640` | `yolov8_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-l-seg (Pre-Optimized) | `yolov8-l-seg_640x640_pre-optimized` | `yolov8_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-m-seg | `yolov8-m-seg_640x640` | `yolov8_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-m-seg (Pre-Optimized) | `yolov8-m-seg_640x640_pre-optimized` | `yolov8_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-n-seg | `yolov8-n-seg_640x640` | `yolov8_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-n-seg (Pre-Optimized) | `yolov8-n-seg_640x640_pre-optimized` | `yolov8_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-s-seg | `yolov8-s-seg_640x640` | `yolov8_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-s-seg (Pre-Optimized) | `yolov8-s-seg_640x640_pre-optimized` | `yolov8_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-x-seg | `yolov8-x-seg_640x640` | `yolov8_seg` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-x-seg (Pre-Optimized) | `yolov8-x-seg_640x640_pre-optimized` | `yolov8_seg` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv9-c-seg | `yolov9-seg-c_640x640` | `yolov9_seg` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv9-c-seg (Pre-Optimized) | `yolov9-seg-c_640x640_pre-optimized` | `yolov9_seg` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv9-e-seg | `yolov9-seg-e_640x640` | `yolov9_seg` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv9-e-seg (Pre-Optimized) | `yolov9-seg-e_640x640_pre-optimized` | `yolov9_seg` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv9-gelan-c-seg | `yolov9-seg-gelan-c_640x640` | `yolov9_seg` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv9-gelan-c-seg (Pre-Optimized) | `yolov9-seg-gelan-c_640x640_pre-optimized` | `yolov9_seg` | 640x640x3 | COCO | GPL-3.0 |

## Keypoint Detection { #keypoint-detection }

Task folder `keypoint_detection`, 1 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| SuperPoint | `superpoint_480x640` | `superpoint` | 480x640x3 | HPatches | Non-commercial |

## Main-body Detection { #mainbody-detection }

Task folder `mainbody_detection`, 2 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| PP-ShiTuV1_mainbody_detection | `pp-shituv1-mainbody-detection_640x640` | `pp_shitu` | 640x640x3 | COCO | Apache-2.0 |
| PP-ShiTuV2_mainbody_detection | `pp-shituv2-mainbody-detection_640x640` | `pp_shitu` | 640x640x3 | COCO | Apache-2.0 |

## OBB Detection { #oriented-object-detection }

Task folder `oriented_object_detection`, 5 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| Ultralytics YOLO26-l-obb | `yolo26-l-obb_1024x1024` | `yolo26_obb` | 1024x1024x3 | DOTAv1 | AGPL-3.0 |
| Ultralytics YOLO26-m-obb | `yolo26-m-obb_1024x1024` | `yolo26_obb` | 1024x1024x3 | DOTAv1 | AGPL-3.0 |
| Ultralytics YOLO26-n-obb | `yolo26-n-obb_1024x1024` | `yolo26_obb` | 1024x1024x3 | DOTAv1 | AGPL-3.0 |
| Ultralytics YOLO26-s-obb | `yolo26-s-obb_1024x1024` | `yolo26_obb` | 1024x1024x3 | DOTAv1 | AGPL-3.0 |
| Ultralytics YOLO26-x-obb | `yolo26-x-obb_1024x1024` | `yolo26_obb` | 1024x1024x3 | DOTAv1 | AGPL-3.0 |

## Object Detection { #object-detection }

Task folder `object_detection`, 167 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| DAMO-YOLO-L | `damoyolo-l_640x640` | `damoyolo` | 640x640x3 | COCO | Apache-2.0 |
| DAMO-YOLO-M | `damoyolo-m_640x640` | `damoyolo` | 640x640x3 | COCO 2017 | Apache-2.0 |
| DAMO-YOLO-S | `damoyolo-s_640x640` | `damoyolo` | 640x640x3 | COCO | Apache-2.0 |
| DAMO-YOLO-T | `damoyolo-t_640x640` | `damoyolo` | 640x640x3 | COCO | Apache-2.0 |
| DAMO-YOLO TinyNAS-L20M | `damoyolo-tinynas-l20m_640x640` | `damoyolo` | 640x640x3 | COCO | Apache-2.0 |
| DAMO-YOLO TinyNAS-L20T | `damoyolo-tinynas-l20t_640x640` | `damoyolo` | 640x640x3 | COCO | Apache-2.0 |
| DAMO-YOLO TinyNAS-L25S | `damoyolo-tinynas-l25s_640x640` | `damoyolo` | 640x640x3 | COCO | Apache-2.0 |
| EfficientDet-D1 | `efficientdet-d1_640x640` | `efficientdet` | 640x640x3 | COCO | Apache-2.0 |
| EfficientDet-D2 | `efficientdet-d2_768x768` | `efficientdet` | 768x768x3 | COCO | Apache-2.0 |
| EfficientDet-D4 | `efficientdet-d4_1024x1024` | `efficientdet` | 1024x1024x3 | COCO | Apache-2.0 |
| NanoDet-Plus-1.5x | `nanodet-plus-1.5x_224x224` | `nanodet` | 416x416x3 | COCO | Apache-2.0 |
| NanoDet-Plus | `nanodet-plus_416x416` | `nanodet` | 416x416x3 | COCO | Apache-2.0 |
| NanoDet-RepVGG-A12 | `nanodet-repvgg-a12_224x224` | `nanodet` | 640x640x3 | COCO | Apache-2.0 |
| NanoDet-RepVGG-A | `nanodet-repvgg-a_224x224` | `nanodet` | 640x640x3 | COCO 2017 | Apache-2.0 |
| NanoDet | `nanodet_224x224` | `nanodet` | 416x416x3 | COCO 2017 | Apache-2.0 |
| rtdetr_hgnetv2_h_6x_coco | `rtdetr-hgnetv2-h-6x_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetr_hgnetv2_l_6x_coco | `rtdetr-hgnetv2-l-6x_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetr_hgnetv2_x_6x_coco | `rtdetr-hgnetv2-x-6x_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetr_r101vd_6x_coco | `rtdetr-r101vd-6x_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetr_r18vd_6x_coco | `rtdetr-r18vd-6x_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetr_r34vd_6x_coco | `rtdetr-r34vd-6x_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetr_r50vd_6x_coco | `rtdetr-r50vd-6x_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetr_r50vd_m_6x_coco | `rtdetr-r50vd-m-6x_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetrv2_r101vd_6x_coco | `rtdetrv2-r101vd-6x_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetrv2_r18vd_120e_coco | `rtdetrv2-r18vd-120e_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetrv2_r34vd_120e_coco | `rtdetrv2-r34vd-120e_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetrv2_r50vd_6x_coco | `rtdetrv2-r50vd-6x_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetrv2_r50vd_m_7x_coco | `rtdetrv2-r50vd-m-7x_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetrv3_r18vd_6x_coco | `rtdetrv3-r18vd-6x_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| rtdetrv3_r50vd_6x_coco | `rtdetrv3-r50vd-6x_640x640` | `rtdetr` | 640x640x3 | COCO | Apache-2.0 |
| SSD (MobileNetV1) | `ssd-mobilenetv1_300x300` | `ssd` | 300x300x3 | Pascal VOC 2007 | MIT |
| SSD (MobileNetV2-Lite) | `ssd-mobilenetv2-lite_300x300` | `ssd` | 300x300x3 | Pascal VOC 2007 | MIT |
| SSD (VGG-16) | `ssd-vgg16_300x300` | `ssd` | 300x300x3 | PascalVOC2007 | MIT |
| Ultralytics YOLO11-l | `yolo11-l_640x640` | `yolo11` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-l (Pre-Optimized) | `yolo11-l_640x640_pre-optimized` | `yolo11` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-m | `yolo11-m_640x640` | `yolo11` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-m (Pre-Optimized) | `yolo11-m_640x640_pre-optimized` | `yolo11` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-n | `yolo11-n_640x640` | `yolo11` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-n (Pre-Optimized) | `yolo11-n_640x640_pre-optimized` | `yolo11` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-s | `yolo11-s_640x640` | `yolo11` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-s (Pre-Optimized) | `yolo11-s_640x640_pre-optimized` | `yolo11` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-x | `yolo11-x_640x640` | `yolo11` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-x (Pre-Optimized) | `yolo11-x_640x640_pre-optimized` | `yolo11` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-l | `yolo26-l_640x640` | `yolo26` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-m | `yolo26-m_640x640` | `yolo26` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-n | `yolo26-n_640x640` | `yolo26` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-s | `yolo26-s_640x640` | `yolo26` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-x | `yolo26-x_640x640` | `yolo26` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO11-n (PPU) | `yolo11-n_640x640_ppu` | `yolo_ppu` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv10-n (PPU) | `yolov10-n_640x640_ppu` | `yolo_ppu` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-n (PPU) | `yolov12-n_640x640_ppu` | `yolo_ppu` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv3-tiny (PPU) | `yolov3-tiny_416x416_ppu` | `yolo_ppu` | 416x416x3 | COCO | GPL-3.0 |
| YOLOv3 (PPU, 416x416) | `yolov3_416x416_ppu` | `yolo_ppu` | 416x416x3 | COCO | Public Domain |
| YOLOv3 (PPU, 608x608) | `yolov3_608x608_ppu` | `yolo_ppu` | 608x608x3 | COCO | Public Domain |
| YOLOv4 (PPU) | `yolov4_512x512_ppu` | `yolo_ppu` | 512x512x3 | COCO | Public Domain |
| Ultralytics YOLOv5-s (PPU) | `yolov5-s_640x640_ppu` | `yolo_ppu` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv7-x (PPU) | `yolov7-x_640x640_ppu` | `yolo_ppu` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv7 (PPU) | `yolov7_640x640_ppu` | `yolo_ppu` | 640x640x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv8-n (PPU) | `yolov8-n_640x640_ppu` | `yolo_ppu` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-s (PPU) | `yolov8-s_640x640_ppu` | `yolo_ppu` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv9-t (PPU) | `yolov9-t_640x640_ppu` | `yolo_ppu` | 640x640x3 | COCO | GPL-3.0 |
| YOLOX-s (PPU) | `yolox-s_640x640_ppu` | `yolo_ppu` | 640x640x3 | COCO | Apache-2.0 |
| Ultralytics YOLO26-l (Pre-Optimized) | `yolo26-l_640x640_pre-optimized` | `yolo_preopt` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-m (Pre-Optimized) | `yolo26-m_640x640_pre-optimized` | `yolo_preopt` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-n (Pre-Optimized) | `yolo26-n_640x640_pre-optimized` | `yolo_preopt` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-s (Pre-Optimized) | `yolo26-s_640x640_pre-optimized` | `yolo_preopt` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLO26-x (Pre-Optimized) | `yolo26-x_640x640_pre-optimized` | `yolo_preopt` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv10-b | `yolov10-b_640x640` | `yolov10` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv10-l | `yolov10-l_640x640` | `yolov10` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv10-m | `yolov10-m_640x640` | `yolov10` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv10-n | `yolov10-n_640x640` | `yolov10` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv10-s | `yolov10-s_640x640` | `yolov10` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv10-x | `yolov10-x_640x640` | `yolov10` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-l | `yolov12-l_640x640` | `yolov12` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-l (Pre-Optimized) | `yolov12-l_640x640_pre-optimized` | `yolov12` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-m | `yolov12-m_640x640` | `yolov12` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-m (Pre-Optimized) | `yolov12-m_640x640_pre-optimized` | `yolov12` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-n | `yolov12-n_640x640` | `yolov12` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-n (Pre-Optimized) | `yolov12-n_640x640_pre-optimized` | `yolov12` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-s | `yolov12-s_640x640` | `yolov12` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-s (Pre-Optimized) | `yolov12-s_640x640_pre-optimized` | `yolov12` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-x | `yolov12-x_640x640` | `yolov12` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv12-x (Pre-Optimized) | `yolov12-x_640x640_pre-optimized` | `yolov12` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv13-l | `yolov13-l_640x640` | `yolov13` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv13-l (Pre-Optimized) | `yolov13-l_640x640_pre-optimized` | `yolov13` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv13-n | `yolov13-n_640x640` | `yolov13` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv13-n (Pre-Optimized) | `yolov13-n_640x640_pre-optimized` | `yolov13` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv13-s | `yolov13-s_640x640` | `yolov13` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv13-s (Pre-Optimized) | `yolov13-s_640x640_pre-optimized` | `yolov13` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv13-x | `yolov13-x_640x640` | `yolov13` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv13-x (Pre-Optimized) | `yolov13-x_640x640_pre-optimized` | `yolov13` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv3 GluonCV (416x416) | `yolov3-gluon_416x416` | `yolov3` | 416x416x3 | COCO | Apache-2.0 |
| YOLOv3 GluonCV (608x608) | `yolov3-gluon_608x608` | `yolov3` | 608x608x3 | COCO | Apache-2.0 |
| YOLOv3-tiny | `yolov3-tiny_416x416` | `yolov3` | 416x416x3 | COCO | GPL-3.0 |
| YOLOv3 Darknet (416x416) | `yolov3_416x416` | `yolov3` | 416x416x3 | COCO | GPL-3.0 |
| YOLOv3 Darknet (640x640) | `yolov3_640x640` | `yolov3` | 640x640x3 | COCO 2017 | Public Domain |
| YOLOv4-leaky | `yolov4-leaky_512x512` | `yolov4` | 512x512x3 | COCO | Public Domain |
| YOLOv4-t | `yolov4-t_416x416` | `yolov4` | 416x416x3 | COCO | Public Domain |
| Ultralytics YOLOv5-l6 | `yolov5-l6_1280x1280` | `yolov5` | 1280x1280x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-l | `yolov5-l_640x640` | `yolov5` | 640x640x3 | COCO 2017 | GPL-3.0 |
| Ultralytics YOLOv5-m6 (1280x1280) | `yolov5-m6_1280x1280` | `yolov5` | 1280x1280 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-m6 (v6.1) | `yolov5-m6_1280x1280_v6.1` | `yolov5` | 1280x1280x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-m6 (640x640) | `yolov5-m6_640x640` | `yolov5` | 640x640x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-m | `yolov5-m_640x640` | `yolov5` | 640x640x3 | COCO 2017 | GPL-3.0 |
| Ultralytics YOLOv5-m (no-SPP) | `yolov5-m_640x640_nospp` | `yolov5` | 640x640x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-n6 | `yolov5-n6_1280x1280` | `yolov5` | 1280x1280x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-n6 (v6.1) | `yolov5-n6_1280x1280_v6.1` | `yolov5` | 1280x1280x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-n | `yolov5-n_640x640` | `yolov5` | 640x640x3 | COCO 2017 | GPL-3.0 |
| Ultralytics YOLOv5-s6 | `yolov5-s6_1280x1280` | `yolov5` | 1280x1280x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-s6 (v6.1) | `yolov5-s6_1280x1280_v6.1` | `yolov5` | 1280x1280x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-s (320x320) | `yolov5-s_320x320` | `yolov5` | 320x320x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-s (640x640) | `yolov5-s_640x640` | `yolov5` | 640x640x3 | COCO 2017 | GPL-3.0 |
| Ultralytics YOLOv5-s (C3TR) | `yolov5-s_640x640_c3tr` | `yolov5` | 640x640x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-s (decode) | `yolov5-s_640x640_decode` | `yolov5` | 640x640x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-s (no-SPP) | `yolov5-s_640x640_nospp` | `yolov5` | 640x640x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-x6 | `yolov5-x6_1280x1280` | `yolov5` | 1280x1280x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-x | `yolov5-x_640x640` | `yolov5` | 640x640x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv5-xs (no-SPP) | `yolov5-xs_512x512_nospp` | `yolov5` | 512x512x3 | COCO | GPL-3.0 |
| YOLOv6-l6 | `yolov6-l6_1280x1280` | `yolov6` | 1280x1280x3 | COCO | GPL-3.0 |
| YOLOv6-l | `yolov6-l_640x640` | `yolov6` | 640x640x3 | COCO | GPL-3.0 |
| yolov6-m6_1280x1280 | `yolov6-m6_1280x1280` | `yolov6` | 1280x1280x3 | COCO | GPL-3.0 |
| YOLOv6-m | `yolov6-m_640x640` | `yolov6` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv6-n0 (v0.1.0) | `yolov6-n0_640x640_v0.1.0` | `yolov6` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv6-n0 (v0.2.1) | `yolov6-n0_640x640_v0.2.1` | `yolov6` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv6-n | `yolov6-n_640x640` | `yolov6` | 640x640x3 | COCO 2017 | GPL-3.0 |
| YOLOv6-n (NMS-score) | `yolov6-n_640x640_nmscore` | `yolov6` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv6-s | `yolov6-s_640x640` | `yolov6` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv7-d6 | `yolov7-d6_1280x1280` | `yolov7` | 1280x1280x3 | COCO | GPL-3.0 |
| YOLOv7-e6 | `yolov7-e6_1280x1280` | `yolov7` | 1280x1280x3 | COCO 2017 | GPL-3.0 |
| YOLOv7-e6e | `yolov7-e6e_1280x1280` | `yolov7` | 1280x1280x3 | COCO | GPL-3.0 |
| YOLOv7-tiny | `yolov7-tiny_640x640` | `yolov7` | 640x640x3 | COCO 2017 | GPL-3.0 |
| YOLOv7-w6 | `yolov7-w6_1280x1280` | `yolov7` | 1280x1280x3 | COCO | GPL-3.0 |
| YOLOv7-w6 (no-decode) | `yolov7-w6_1280x1280_nodecode` | `yolov7` | 1280x1280x3 | COCO | GPL-3.0 |
| YOLOv7-x | `yolov7-x_640x640` | `yolov7` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv7 | `yolov7_640x640` | `yolov7` | 640x640x3 | COCO 2017 | GPL-3.0 |
| YOLOv7 (no-decode) | `yolov7_640x640_nodecode` | `yolov7` | 640x640x3 | COCO | GPL-3.0 |
| Ultralytics YOLOv8-l | `yolov8-l_640x640` | `yolov8` | 640x640x3 | COCO 2017 | AGPL-3.0 |
| Ultralytics YOLOv8-l (Pre-Optimized) | `yolov8-l_640x640_pre-optimized` | `yolov8` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-m | `yolov8-m_640x640` | `yolov8` | 640x640x3 | COCO 2017 | AGPL-3.0 |
| Ultralytics YOLOv8-m (Pre-Optimized) | `yolov8-m_640x640_pre-optimized` | `yolov8` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-n | `yolov8-n_640x640` | `yolov8` | 640x640x3 | COCO 2017 | AGPL-3.0 |
| Ultralytics YOLOv8-n (Pre-Optimized) | `yolov8-n_640x640_pre-optimized` | `yolov8` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-s | `yolov8-s_640x640` | `yolov8` | 640x640x3 | COCO 2017 | AGPL-3.0 |
| Ultralytics YOLOv8-s (decode) | `yolov8-s_640x640_decode` | `yolov8` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-s (Pre-Optimized) | `yolov8-s_640x640_pre-optimized` | `yolov8` | 640x640x3 | COCO | AGPL-3.0 |
| Ultralytics YOLOv8-x | `yolov8-x_640x640` | `yolov8` | 640x640x3 | COCO 2017 | AGPL-3.0 |
| Ultralytics YOLOv8-x (Pre-Optimized) | `yolov8-x_640x640_pre-optimized` | `yolov8` | 640x640x3 | COCO | AGPL-3.0 |
| YOLOv9-c | `yolov9-c_640x640` | `yolov9` | 640x640x3 | COCO 2017 | GPL-3.0 |
| YOLOv9-c (Pre-Optimized) | `yolov9-c_640x640_pre-optimized` | `yolov9` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv9-e | `yolov9-e_640x640` | `yolov9` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv9-e (Pre-Optimized) | `yolov9-e_640x640_pre-optimized` | `yolov9` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv9-gelan-c | `yolov9-gelan-c_640x640` | `yolov9` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv9-gelan-c (Pre-Optimized) | `yolov9-gelan-c_640x640_pre-optimized` | `yolov9` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv9-m | `yolov9-m_640x640` | `yolov9` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv9-m (Pre-Optimized) | `yolov9-m_640x640_pre-optimized` | `yolov9` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv9-s | `yolov9-s_640x640` | `yolov9` | 640x640x3 | COCO 2017 | GPL-3.0 |
| YOLOv9-s (Pre-Optimized) | `yolov9-s_640x640_pre-optimized` | `yolov9` | 640x640x3 | COCO | GPL-3.0 |
| YOLOv9-t | `yolov9-t_640x640` | `yolov9` | 640x640x3 | COCO 2017 | GPL-3.0 |
| YOLOv9-t (Pre-Optimized) | `yolov9-t_640x640_pre-optimized` | `yolov9` | 640x640x3 | COCO | GPL-3.0 |
| YOLOX-l-leaky | `yolox-l-leaky_640x640` | `yolox` | 640x640x3 | COCO 2017 | Apache-2.0 |
| YOLOX-l | `yolox-l_640x640` | `yolox` | 640x640x3 | COCO | Apache-2.0 |
| YOLOX-m | `yolox-m_640x640` | `yolox` | 640x640x3 | COCO | Apache-2.0 |
| YOLOX-s-leaky | `yolox-s-leaky_640x640` | `yolox` | 640x640x3 | COCO 2017 | Apache-2.0 |
| YOLOX-s-wide-leaky | `yolox-s-wide-leaky_640x640` | `yolox` | 640x640x3 | COCO 2017 | Apache-2.0 |
| YOLOX-s | `yolox-s_640x640` | `yolox` | 640x640x3 | COCO 2017 | Apache-2.0 |
| YOLOX-t | `yolox-t_416x416` | `yolox` | 416x416x3 | COCO 2017 | Apache-2.0 |
| YOLOX-x | `yolox-x_640x640` | `yolox` | 640x640x3 | COCO | Apache-2.0 |

## Object Pose Estimation { #object-pose-estimation }

Task folder `object_pose_estimation`, 1 variants.

DOPE is a visualization demo for one object (a ketchup bottle) in a still image. It estimates the camera focal length from the image width, so the drawn cuboid looks right but the pose is not metric. Set `object_size_cm` and `focal_length` in its `config.json` for another object or a calibrated camera.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| DOPE (HOPE Ketchup) | `dope-hope-ketchup_480x640` | `dope` | 480x640x3 | HOPE | Apache-2.0 |

## Panoptic Driving Perception { #panoptic-driving-perception }

Task folder `panoptic_driving_perception`, 1 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| YOLOPv2 | `yolopv2_384x640` | `yolopv2` | 384x640x3 | BDD100K | MIT |

## Pose Estimation { #pose-estimation }

Task folder `pose_estimation`, 36 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| CenterPose-FPN (RegNetX-1.6GF) | `centerpose-fpn_regnet-x1.6gf_512x512` | `centerpose` | 512x512x3 | COCOPose | Apache-2.0 |
| CenterPose (RegNetX-800MF) | `centerpose_regnet-x800mf_640x640` | `centerpose` | 640x640x3 | COCOPose | MIT |
| CenterPose (RepVGG-A0) | `centerpose_repvgg-a0_416x416` | `centerpose` | 416x416x3 | COCOPose | MIT |
| dark_hrnet_w32_256x192 | `dark-hrnet-w32_256x192` | `dark_hrnet` | 192x256x3 | COCOPoseTopDown | Apache-2.0 |
| ViTPose-S | `vitpose-s_256x192` | `vitpose` | 256x192x3 | COCOPoseTopDown | Apache-2.0 |
| Ultralytics YOLO11-l-pose | `yolo11-l-pose_640x640` | `yolo11_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO11-l-pose (Pre-Optimized) | `yolo11-l-pose_640x640_pre-optimized` | `yolo11_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO11-m-pose | `yolo11-m-pose_640x640` | `yolo11_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO11-m-pose (Pre-Optimized) | `yolo11-m-pose_640x640_pre-optimized` | `yolo11_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO11-n-pose | `yolo11-n-pose_640x640` | `yolo11_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO11-n-pose (Pre-Optimized) | `yolo11-n-pose_640x640_pre-optimized` | `yolo11_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO11-s-pose | `yolo11-s-pose_640x640` | `yolo11_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO11-s-pose (Pre-Optimized) | `yolo11-s-pose_640x640_pre-optimized` | `yolo11_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO11-x-pose | `yolo11-x-pose_640x640` | `yolo11_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO11-x-pose (Pre-Optimized) | `yolo11-x-pose_640x640_pre-optimized` | `yolo11_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO26-l-pose | `yolo26-l-pose_640x640` | `yolo26_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO26-m-pose | `yolo26-m-pose_640x640` | `yolo26_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO26-n-pose | `yolo26-n-pose_640x640` | `yolo26_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO26-s-pose | `yolo26-s-pose_640x640` | `yolo26_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO26-x-pose | `yolo26-x-pose_640x640` | `yolo26_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO26-l-pose (Pre-Optimized) | `yolo26-l-pose_640x640_pre-optimized` | `yolo_preopt_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO26-m-pose (Pre-Optimized) | `yolo26-m-pose_640x640_pre-optimized` | `yolo_preopt_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO26-n-pose (Pre-Optimized) | `yolo26-n-pose_640x640_pre-optimized` | `yolo_preopt_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO26-s-pose (Pre-Optimized) | `yolo26-s-pose_640x640_pre-optimized` | `yolo_preopt_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLO26-x-pose (Pre-Optimized) | `yolo26-x-pose_640x640_pre-optimized` | `yolo_preopt_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLOv5-s6-pose | `yolov5-s6-pose_640x640` | `yolov5_pose` | 640x640x3 | COCOPose | GPL-3.0 |
| Ultralytics YOLOv8-l-pose | `yolov8-l-pose_640x640` | `yolov8_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLOv8-l-pose (Pre-Optimized) | `yolov8-l-pose_640x640_pre-optimized` | `yolov8_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLOv8-m-pose | `yolov8-m-pose_640x640` | `yolov8_pose` | 640x640x3 | COCO Keypoints 2017 | AGPL-3.0 |
| Ultralytics YOLOv8-m-pose (Pre-Optimized) | `yolov8-m-pose_640x640_pre-optimized` | `yolov8_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLOv8-n-pose | `yolov8-n-pose_640x640` | `yolov8_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLOv8-n-pose (Pre-Optimized) | `yolov8-n-pose_640x640_pre-optimized` | `yolov8_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLOv8-s-pose | `yolov8-s-pose_640x640` | `yolov8_pose` | 640x640x3 | COCO Keypoints 2017 | AGPL-3.0 |
| Ultralytics YOLOv8-s-pose (Pre-Optimized) | `yolov8-s-pose_640x640_pre-optimized` | `yolov8_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLOv8-x-pose | `yolov8-x-pose_640x640` | `yolov8_pose` | 640x640x3 | COCOPose | AGPL-3.0 |
| Ultralytics YOLOv8-x-pose (Pre-Optimized) | `yolov8-x-pose_640x640_pre-optimized` | `yolov8_pose` | 640x640x3 | COCOPose | AGPL-3.0 |

## Re-Identification { #person-reid }

Task folder `person_reid`, 1 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| RepVGG-A0 Person ReID | `repvgg-a0-reid_256x128` | `repvgg_reid` | 256x128x3 | Market1501 | MIT |

## Semantic Segmentation { #semantic-segmentation }

Task folder `semantic_segmentation`, 24 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| BiSeNetV1 | `bisenetv1_1024x2048` | `bisenet` | 1024x2048x3 | Cityscapes | Apache-2.0 |
| BiSeNetV2 | `bisenetv2_1024x2048` | `bisenet` | 1024x2048x3 | Cityscapes | Apache-2.0 |
| CAS-ViT-T FPN (ResNet-50) | `casvit-t-fpn-resnet50_512x512` | `casvit_seg` | 512x512x3 | ADE20K | MIT |
| DDRNet23-Slim | `ddrnet23-slim_1024x2048` | `ddrnet` | 1024x2048x3 | Cityscapes | MIT |
| DDRNet23 | `ddrnet23_1024x2048` | `ddrnet` | 1024x2048x3 | Cityscapes | MIT |
| DeepLabV3 (ResNet-101) | `deeplabv3-resnet101_512x512` | `deeplabv3` | 512x512x3 | PascalVOC2012 | Apache-2.0 |
| DeepLabV3 (ResNet-50) | `deeplabv3-resnet50_512x512` | `deeplabv3` | 512x512x3 | PascalVOC2012 | Apache-2.0 |
| DeepLabV3 (MobileNetV2) | `deeplabv3_mobilenetv2_512x512` | `deeplabv3` | 512x512x3 | Pascal VOC 2012 | Apache-2.0 |
| DeepLabV3 (MobileNetV2, no-dilation) | `deeplabv3_mobilenetv2_513x513_nodilation` | `deeplabv3` | 513x513x3 | PascalVOC2012 | Apache-2.0 |
| DeepLabV3+ (DRN) | `deeplabv3plus-drn_512x512` | `deeplabv3` | 512x512x3 | PascalVOC2012 | Apache-2.0 |
| DeepLabV3+ (ResNet-101) | `deeplabv3plus-resnet101_512x512` | `deeplabv3` | 512x512x3 | PascalVOC2012 | MIT |
| DeepLabV3+ (ResNet-50) | `deeplabv3plus-resnet50_512x512` | `deeplabv3` | 512x512x3 | PascalVOC2012 | MIT |
| DeepLabV3+ (MobileNetV1) | `deeplabv3plus_mobilenetv1_512x512` | `deeplabv3` | 512x512x3 | Pascal VOC 2012 | Apache-2.0 |
| DeepLabV3+ (MobileNetV2) | `deeplabv3plus_mobilenetv2_512x512` | `deeplabv3` | 512x512x3 | Pascal VOC 2012 | Apache-2.0 |
| FCN-8s (ResNet-18) | `fcn8_resnet18_1024x1920` | `fcn` | 1024x1920x3 | Cityscapes | Apache-2.0 |
| FCN-8s (ResNet-50) | `fcn8_resnet50_512x512` | `fcn` | 512x512x3 | PascalVOC2012 | Apache-2.0 |
| PIDNet-S | `pidnet-s_1024x2048` | `pidnet` | 1024x2048x3 | Cityscapes | MIT |
| pp_liteseg_stdc1_camvid_960x720_10k | `pp-liteseg-stdc1-camvid-10k_960x720` | `pp_liteseg` | 720x960x3 | CamVid | Apache-2.0 |
| SegFormer (MiT-B0) | `segformer_mit-b0_512x1024` | `segformer` | 1024x512x3 | Cityscapes | Apache-2.0 |
| STDC1-Seg50 | `stdc1-seg50_512x1024` | `stdc_seg` | 512x1024x3 | Cityscapes | MIT |
| STDC1-Seg75 | `stdc1-seg75_768x1536` | `stdc_seg` | 768x1536x3 | Cityscapes | MIT |
| STDC2-Seg50 | `stdc2-seg50_512x1024` | `stdc_seg` | 512x1024x3 | Cityscapes | MIT |
| STDC2-Seg75 | `stdc2-seg75_768x1536` | `stdc_seg` | 768x1536x3 | Cityscapes | MIT |
| U-Net (MobileNetV2) | `unet_mobilenetv2_256x256` | `unet` | 256x256x3 | OxfordIIITPet | Apache-2.0 |

## Super Resolution { #super-resolution }

Task folder `super_resolution`, 6 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| ESPCN-x2 | `espcn-x2_17x17` | `espcn` | 17x17x1 | BSD100 | Apache-2.0 |
| ESPCN-x3 | `espcn-x3_17x17` | `espcn` | 17x17x1 | BSD100 | Apache-2.0 |
| ESPCN-x4 | `espcn-x4_17x17` | `espcn` | 17x17x1 | BSD100 | Apache-2.0 |
| Real-ESRGAN-x2 | `realesrgan-x2_192x192` | `realesrgan` | 192x192x3 | BSD100 | BSD-3-Clause |
| Real-ESRGAN-x4 | `realesrgan-x4_192x192` | `realesrgan` | 192x192x3 | BSD100 | BSD-3-Clause |
| Real-ESRGAN-x8 | `realesrgan-x8_192x192` | `realesrgan` | 192x192x3 | BSD100 | BSD-3-Clause |

## Visual Place Recognition { #visual-place-recognition }

Task folder `visual_place_recognition`, 3 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| EigenPlaces ResNet-18 | `eigenplaces-resnet18_512x512` | `eigenplaces` | 512x512x3 | HPatches | MIT |
| EigenPlaces ResNet-50 | `eigenplaces-resnet50_512x512` | `eigenplaces` | 512x512x3 | HPatches | MIT |
| PP-ShiTuV2_feature_extraction | `pp-shituv2-feature-extraction_224x224` | `pp_shitu_rec` | 224x224x3 | HPatches | Apache-2.0 |

## Zero-Shot Classification { #zero-shot-image-classification }

Task folder `zero_shot_image_classification`, 5 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| CLIP ResNet-50x16 (OpenAI WIT) | `clip-img_resnet50x16_384x384_openai-wit` | `clip` | 384x384x3 | ILSVRC2012 | MIT |
| CLIP ViT-B/16 QuickGELU (MetaCLIP FullCC) | `clip-img_vit-b16-quickgelu_224x224_metaclip-fullcc` | `clip` | 224x224x3 | ILSVRC2012 | MIT |
| CLIP ViT-B/32 (DataComp) | `clip-img_vit-b32_256x256_datacomp-s34b-b86k` | `clip` | 256x256x3 | ILSVRC2012 | MIT |
| CLIP ViT-L/14 QuickGELU (DFN-2B) | `clip-img_vit-l14-quickgelu_224x224_dfn2b` | `clip` | 224x224x3 | ILSVRC2012 | MIT |
| CLIP ViT-L/14 (DataComp-XL) | `clip-img_vit-l14_224x224_datacomp-xl-s13b-b90k` | `clip` | 224x224x3 | ILSVRC2012 | MIT |

## Zero-Shot Segmentation { #zero-shot-instance-segmentation }

Task folder `zero_shot_instance_segmentation`, 1 variants.

| Model | Variant | Family | Input | Dataset | License |
|---|---|---|---|---|---|
| FastSAM-s | `fastsam-s_1024x1024` | `fastsam` | 1024x1024x3 | COCO | Apache-2.0 |

## Next steps

* [Run the examples](run-examples.md): every command line option and environment variable.
* [Multi model graph](multi-model-graph.md): run several of these models on one input.
* [Third party licenses](licenses.md): the license of each upstream project.
