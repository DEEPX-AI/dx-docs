---
title: Datasets
description: Folder layouts, download links, licenses and dataset classes for the evaluation datasets that DX-ModelZoo uses.
---

# Datasets

This page shows where to put each evaluation dataset so `dxmz eval` and `dxmz compile` can find it, and lists every registered dataset class.

## Before you start

* Datasets are not included. Download them yourself and follow each dataset's license.
* Set `DATA_ROOT` to the folder that holds them, or link the default folder:

```bash
export DATA_ROOT=/your/datasets/folder
# or
ln -s /your/datasets/folder ./download/datasets
```

Model YAMLs point to `${DATA_ROOT}/<folder>`. Use `--data-root <path>` to override `DATA_ROOT` for one command. Run `dxmz info <model>` to see the exact `eval_path` a model expects.

!!! note "Datasets are checked before evaluation"
    Each dataset class validates its folder, files and labels when it loads. A missing folder stops with `Dataset not found` and the expected path.

## Dataset summary

| Dataset | Registry key | Task | Path under `DATA_ROOT` | License |
|---|---|---|---|---|
| [ImageNet ILSVRC2012](https://image-net.org/download-images.php) | `ILSVRC2012` | Image classification | `ILSVRC2012/val` | Academic and research use only |
| [DOTA v1](https://captain-whu.github.io/DOTA/dataset.html) | `DOTAv1` | Oriented object detection | `DOTAv1` | Research use only |
| [Pascal VOC 2007 and 2012](http://host.robots.ox.ac.uk/pascal/VOC/voc2007/) | `PascalVOC2007`, `PascalVOC2012` | Detection (2007), segmentation (2012) | `PascalVOC/VOCdevkit/VOC2007`, `PascalVOC/VOCdevkit/VOC2012` | VOC challenge data |
| [COCO 2017](https://cocodataset.org/#download) | `COCO`, `COCOPose`, `COCOPoseTopDown`, `COCOPersonSeg` | Detection, instance segmentation, pose | `COCO` | Annotations CC BY 4.0, images under their owners' rights ([terms](https://cocodataset.org/#termsofuse)) |
| [Oxford-IIIT Pet](https://www.robots.ox.ac.uk/~vgg/data/pets/) | `OxfordIIITPet` | Semantic segmentation | `Oxford-IIIT_Pet` | CC BY-SA 4.0 |
| [Cityscapes](https://www.cityscapes-dataset.com/register/) | `Cityscapes` | Semantic segmentation | `cityscapes` | Academic and research use only |
| [AFLW2000-3D](http://www.cbsr.ia.ac.cn/users/xiangyuzhu/projects/3DDFA/main.htm) | `AFLW20003D` | 3D face landmark | `AFLW20003D` | Research use only |
| Hand Keypoints | `HandKeypoints`, `HandKeypointsDetection` | Hand landmark, hand detection | `hand-keypoints` | Custom dataset |
| [CelebA](https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html) | `CelebA` | Face attribute | `CelebA` | Non commercial research only |
| [LFW](http://vis-www.cs.umass.edu/lfw/) | `LFW` | Face recognition | `LFW` | Research use only |
| [WiderFace](http://shuoyang1213.me/WIDERFACE/) | `WiderFace` | Face detection | `widerface` | Non commercial research only |
| [PETA](https://mmlab.ie.cuhk.edu.hk/projects/PETA.html) | `PETA` | Pedestrian attribute | `PETA` | Research use only |
| [BSD100](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/) | `BSD100` | Super resolution | `BSD100/bicubic_4x` | BSD license |
| [BSD68](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/) | `BSD68` | Image denoising | `BSD68` | BSD license |
| [CBSD68](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/) | `CBSD68` | Image denoising (color) | `CBSD68` | BSD license |
| [LOL](https://daooshee.github.io/BMVC2018website/) | `LOL` | Low light enhancement | `LOL` | Research use only |
| [NYU Depth v2](https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html) | `NYUDepthv2` | Depth estimation | `nyudepthv2` | Research use only |
| [Market-1501](https://zheng-lab.cecs.anu.edu.au/Project/project_reid.html) | `Market1501` | Person re identification | `Market1501` | Research use only |
| [KITTI 3D](https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d) | `KITTI` | 3D object detection | see model YAML | Research use only |
| [CamVid](http://mi.eng.cam.ac.uk/research/projects/VideoRec/CamVid/) | `CamVid` | Semantic segmentation | see model YAML | Research and non commercial use only |
| [Distinctions-646](https://github.com/PaddlePaddle/PaddleSeg) | `Distinctions646` | Image matting | see model YAML | Distinctions-646 and Pascal VOC 2012 terms |
| [MVTec AD](https://www.mvtec.com/company/research/datasets/mvtec-ad) | `MVTecAD` | Anomaly detection | see model YAML | Non commercial research and education only |
| ADE20K (SceneParse150) | `ADE20K` | Semantic segmentation | see model YAML | see dataset site |
| BDD100K | `BDD100K` | Panoptic driving perception | see model YAML | see dataset site |
| HOPE | `HOPE` | Object pose estimation | see model YAML | see dataset site |
| HPatches | `HPatches` | Keypoint detection | see model YAML | see dataset site |
| Objectron | `Objectron` | 3D object detection and pose | see model YAML | see dataset site |
| ImageNet text prompts | `ImageNetText` | Image retrieval (CLIP text queries) | see model YAML | uses ImageNet |

## Folder layouts

Only the files that evaluation reads are shown.

=== "ImageNet"

    ```text
    ILSVRC2012/
    └── val/
        ├── n01440764/      # 1000 class folders, 50 JPEG images each
        ├── n01443537/
        └── ...
    ```

=== "COCO"

    ```text
    COCO/
    ├── annotations/
    │   ├── instances_val2017.json
    │   └── person_keypoints_val2017.json
    └── val2017/            # 5000 .jpg
    ```

=== "Pascal VOC"

    ```text
    PascalVOC/
    └── VOCdevkit/
        ├── VOC2007/
        │   ├── Annotations/
        │   ├── ImageSets/
        │   ├── JPEGImages/
        │   ├── SegmentationClass/
        │   └── SegmentationObject/
        └── VOC2012/        # same folders as VOC2007
    ```

=== "DOTA v1"

    ```text
    DOTAv1/
    ├── images/
    │   └── val/            # 458 .jpg
    └── labels/
        ├── val/            # 458 .txt
        └── val_original/   # 458 .txt
    ```

=== "Cityscapes"

    ```text
    cityscapes/
    ├── gtFine/val/{frankfurt,lindau,munster}/
    └── leftImg8bit/val/{frankfurt,lindau,munster}/
    ```

=== "Faces"

    ```text
    widerface/
    ├── eval_tools/ground_truth/   # .mat files
    ├── wider_face_split/
    └── WIDER_val/images/          # 61 event folders
    LFW/
    ├── lfw-deepfunneled/          # one folder per person
    └── *.csv
    CelebA/
    ├── img_align_celeba/          # .jpg
    └── *.csv
    AFLW20003D/
    ├── Code/
    └── *.jpg, *.mat               # 2000 of each
    ```

=== "Restoration"

    ```text
    BSD100/
    ├── bicubic_2x/{HR,LR}/
    ├── bicubic_3x/{HR,LR}/
    └── bicubic_4x/{HR,LR}/        # 100 .png each
    BSD68/                         # 68 .png
    CBSD68/                        # 68 .png
    LOL/
    ├── eval15/{high,low}/         # 15 .png each
    └── our485/{high,low}/
    ```

=== "Other"

    ```text
    Oxford-IIIT_Pet/
    ├── annotations/{trimaps,xmls}/
    └── images/
    hand-keypoints/
    ├── images/{train,val}/
    └── labels/{train,val}/
    PETA/
    └── images/                    # .png, plus one .mat file
    nyudepthv2/
    └── val/official/              # 654 .h5
    Market1501/
    ├── bounding_box_test/
    └── query/
    ```

## Dataset classes

All datasets inherit from `DatasetBase` and are registered in `DATASET_REGISTRY` (module `dx_modelzoo.dataset`). Every constructor takes `data_dir` first. The `__getitem__` return format must match what the evaluator expects.

| Registry key | Extra constructor parameters | `__getitem__` returns |
|---|---|---|
| `ILSVRC2012` | none | `(img, label)` |
| `DOTAv1` | `split="val"` | `(img, origin_shape, image_id)` |
| `PascalVOC2007` | none | `(img, image_shape, idx)` |
| `PascalVOC2012` | none | `(img, label)`, 21 classes |
| `COCO` | none | `(img, origin_shape, image_id)` |
| `COCOPose` | none | `(img, origin_shape, image_id)` |
| `COCOPoseTopDown` | `bbox_pad_ratio=0.25`, `square_crop=False`, `model_input_w=192`, `model_input_h=256` | `(crop, gt_bbox, crop_params, kpts_crop, visibility, img_id, ann_id)` |
| `COCOPersonSeg` | `inputs=None`, `ann_file=None`, `person_only=True` | `(image, binary_mask)`, 2 classes |
| `Cityscapes` | none | `(img, label)`, 19 classes |
| `OxfordIIITPet` | none | `(img, label)`, 3 classes |
| `CamVid` | `split="val"` | `(img, label)`, 11 classes |
| `ADE20K` | `eval_size=512` | `(img, label)`, 150 classes |
| `AFLW20003D` | none | `(face_crop, gt_landmarks, bbox_size, yaw_deg, idx)`, 68 keypoints |
| `HandKeypoints` | none | `(crop, gt_kpts, idx)`, 21 keypoints |
| `HandKeypointsDetection` | none | `(image, boxes_xyxy_normalized, (h, w), img_path)` |
| `CelebA` | none | `(img, labels, idx)`, 40 attributes |
| `LFW` | none | `(img1, img2, label)` |
| `WiderFace` | none | `(img, image_shape, file_path)` |
| `PETA` | none | `(img, labels, idx)` |
| `BSD100` | none | `(lr_image, hr_image)` |
| `BSD68`, `CBSD68` | none | `(noisy_input, origin_img)` |
| `LOL` | none | `(low_img, high_img)` |
| `NYUDepthv2` | none | `(rgb, depth)` |
| `Market1501` | none | `(img, idx)` |
| `KITTI` | `split="val"` | `(bev, bev_shape, sample_id)` |
| `Distinctions646` | `split="val"`, `background_dir=None` | `(composite, alpha)` |
| `MVTecAD` (class `MVTecADDataset`) | `category=None`, `max_train_images=0` | `(img, label, category, mask_path)` |
| `BDD100K`, `HOPE`, `HPatches`, `Objectron`, `ImageNetText` | see source | task specific |

Notes:

* `Distinctions646` builds composites in memory on Pascal VOC 2012 backgrounds. When `background_dir` is not set, it uses the Pascal VOC folder next to `data_dir`.
* `MVTecAD` labels are `0` (good) and `1` (anomalous). `category=None` uses all categories.
* `COCOPoseTopDown` crops one person per sample from the ground truth box with 25% padding.

## Next steps

* [Evaluate models](evaluate.md)
* [Custom models and datasets](custom-models.md#add-a-custom-dataset)
* [YAML configuration](yaml-config.md#dataset)
