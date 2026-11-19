---
title: Third party licenses
description: License terms of the third party sample models and sample data that ship with DX-APP, with the license of every upstream project.
---

# Third party licenses

This page lists the licenses of the third party models and sample data that DX-APP uses, so you can check them before you use any of them in a product.

## Sample models

The sample models (`.dxnn` files) that DX-APP downloads are for **evaluation and development only** and are **not licensed for commercial deployment**.

Each model is compiled from a third party open source project with its own license. Many of these licenses restrict commercial use, for example with copyleft source disclosure obligations, a ban on commercial use, or required attribution. For commercial use, you must either get a license from the original model authors, or use your own commercially licensed models.

### Licenses by count

The license of each model comes from its model card (the `README.md` in each example folder). The [model catalog](models.md) shows the license of every variant.

| License | Models | What it usually means |
|---|---:|---|
| AGPL-3.0 | 145 | Copyleft: source disclosure obligations, also for network use |
| Apache-2.0 | 142 | Permissive: keep the license and notices |
| GPL-3.0 | 78 | Copyleft: source disclosure obligations |
| MIT | 64 | Permissive: keep the copyright notice |
| BSD-3-Clause | 53 | Permissive: keep the copyright notice |
| Public Domain | 6 | No restrictions stated upstream |
| CC BY-NC 4.0 | 3 | Non commercial use only |
| Apple Sample Code License | 3 | Read the Apple license terms |
| Non-commercial | 2 | Non commercial use only |
| No License | 1 | No license published upstream: no rights are granted |

The last column is a short reminder, not legal advice. Always read the upstream license itself.

### Licenses by upstream project

| Upstream project | License | Models | Families |
|---|---|---:|---|
| [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) | AGPL-3.0 | 89 | `yolo11`, `yolo11_pose`, `yolo11_seg`, `yolo26`, `yolo26_cls`, `yolo26_depth`, `yolo26_obb`, `yolo26_pose`, `yolo26_seg`, `yolo_ppu`, `yolo_preopt_pose`, `yolov8`, `yolov8_pose`, `yolov8_seg` |
| [pytorch/vision](https://github.com/pytorch/vision) | BSD-3-Clause | 47 | `alexnet`, `densenet`, `efficientnet`, `inception`, `mnasnet`, `mobilenet`, `regnet`, `resnet`, `resnext`, `shufflenetv2`, `squeezenet`, `vgg`, `wide_resnet` |
| [ultralytics/yolov5](https://github.com/ultralytics/yolov5) | GPL-3.0 | 27 | `yolo_ppu`, `yolov5`, `yolov5_pose`, `yolov5_seg` |
| [sunsmarterjie/yolov12](https://github.com/sunsmarterjie/yolov12) | AGPL-3.0 | 26 | `yolo_ppu`, `yolov12`, `yolov12_cls`, `yolov12_seg` |
| [pytorch/vision](https://github.com/pytorch/vision) | Apache-2.0 | 25 | `deeplabv3`, `efficientnet`, `fcn`, `mobilenet`, `regnet`, `resnext`, `shufflenetv1` |
| Not named in the model card | AGPL-3.0 | 15 | `yolo11`, `yolo_preopt`, `yolov8` |
| [WongKinYiu/yolov9](https://github.com/WongKinYiu/yolov9) | GPL-3.0 | 12 | `yolo_ppu`, `yolov9`, `yolov9_seg` |
| [WongKinYiu/yolov7](https://github.com/WongKinYiu/yolov7) | GPL-3.0 | 11 | `yolo_ppu`, `yolov7` |
| [facebookresearch/deit](https://github.com/facebookresearch/deit) | Apache-2.0 | 9 | `deit`, `resmlp` |
| [Megvii-BaseDetection/YOLOX](https://github.com/Megvii-BaseDetection/YOLOX) | Apache-2.0 | 9 | `yolo_ppu`, `yolox` |
| [meituan/YOLOv6](https://github.com/meituan/YOLOv6) | GPL-3.0 | 9 | `yolov6` |
| [iMoonLab/yolov13](https://github.com/iMoonLab/yolov13) | AGPL-3.0 | 8 | `yolov13` |
| Not named in the model card | Apache-2.0 | 8 | `pphgnetv2`, `pplcnetv2` |
| [THU-MIG/yolov10](https://github.com/THU-MIG/yolov10) | AGPL-3.0 | 7 | `yolo_ppu`, `yolov10` |
| [tinyvision/DAMO-YOLO](https://github.com/tinyvision/DAMO-YOLO) | Apache-2.0 | 7 | `damoyolo` |
| [AlexeyAB/darknet](https://github.com/AlexeyAB/darknet) | Public Domain | 6 | `yolo_ppu`, `yolov3`, `yolov4` |
| [deepinsight/insightface](https://github.com/deepinsight/insightface) | MIT | 6 | `arcface`, `retinaface` |
| [DingXiaoH/RepVGG](https://github.com/DingXiaoH/RepVGG) | MIT | 6 | `repvgg`, `repvgg_reid` |
| [derronqi/yolov7-face](https://github.com/derronqi/yolov7-face) | GPL-3.0 | 5 | `yolov7_face` |
| [huggingface/pytorch-image-models](https://github.com/huggingface/pytorch-image-models) | Apache-2.0 | 5 | `efficientnet` |
| [Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB](https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB) | MIT | 5 | `ulfgfd` |
| [mlfoundations/open_clip](https://github.com/mlfoundations/open_clip) | MIT | 5 | `clip` |
| Not named in the model card | GPL-3.0 | 5 | `yolov9` |
| [RangiLyu/nanodet](https://github.com/RangiLyu/nanodet) | Apache-2.0 | 5 | `nanodet` |
| [google-research/vision_transformer](https://github.com/google-research/vision_transformer) | Apache-2.0 | 4 | `vit` |
| [MichaelFan01/STDC-Seg](https://github.com/MichaelFan01/STDC-Seg) | MIT | 4 | `stdc_seg` |
| [PaddlePaddle/PaddleClas](https://github.com/PaddlePaddle/PaddleClas) | Apache-2.0 | 4 | `pphgnet`, `pphgnetv2` |
| [apple/ml-fastvit](https://github.com/apple/ml-fastvit) | Apple Sample Code License | 3 | `fastvit` |
| [cszn/DnCNN](https://github.com/cszn/DnCNN) | Apache-2.0 | 3 | `dncnn` |
| [deepcam-cn/yolov5-face](https://github.com/deepcam-cn/yolov5-face) | GPL-3.0 | 3 | `yolov5_face` |
| [deepinsight/insightface/tree/master/detection/scrfd](https://github.com/deepinsight/insightface/tree/master/detection/scrfd) | MIT | 3 | `scrfd` |
| [facebookresearch/LeViT](https://github.com/facebookresearch/LeViT) | Apache-2.0 | 3 | `levit` |
| [google/automl/tree/master/efficientdet](https://github.com/google/automl/tree/master/efficientdet) | Apache-2.0 | 3 | `efficientdet` |
| [Lornatang/ESPCN-PyTorch](https://github.com/Lornatang/ESPCN-PyTorch) | Apache-2.0 | 3 | `espcn` |
| [nelson1425/EfficientAD](https://github.com/nelson1425/EfficientAD) | Apache-2.0 | 3 | `efficientad` |
| [qfgaohao/pytorch-ssd](https://github.com/qfgaohao/pytorch-ssd) | MIT | 3 | `ssd` |
| [snap-research/EfficientFormer](https://github.com/snap-research/EfficientFormer) | Apache-2.0 | 3 | `efficientformer` |
| [Tianfang-Zhang/CAS-ViT](https://github.com/Tianfang-Zhang/CAS-ViT) | MIT | 3 | `casvit`, `casvit_seg` |
| [ultralytics/yolov3](https://github.com/ultralytics/yolov3) | GPL-3.0 | 3 | `yolo_ppu`, `yolov3` |
| [xinntao/Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) | BSD-3-Clause | 3 | `realesrgan` |
| [cleardusk/3DDFA_V2](https://github.com/cleardusk/3DDFA_V2) | MIT | 2 | `3ddfa_v2` |
| [CoinCheung/BiSeNet](https://github.com/CoinCheung/BiSeNet) | Apache-2.0 | 2 | `bisenet` |
| [cszn/DnCNN](https://github.com/cszn/DnCNN) | MIT | 2 | `dncnn` |
| [dangweili/pedestrian-attribute-recognition-pytorch](https://github.com/dangweili/pedestrian-attribute-recognition-pytorch) | MIT | 2 | `deepmar` |
| [dbolya/yolact](https://github.com/dbolya/yolact) | MIT | 2 | `yolact` |
| [DepthAnything/Depth-Anything-V2](https://github.com/DepthAnything/Depth-Anything-V2) | CC BY-NC 4.0 | 2 | `depthanythingv2` |
| [dmlc/gluon-cv](https://github.com/dmlc/gluon-cv) | Apache-2.0 | 2 | `yolov3` |
| [gmberton/EigenPlaces](https://github.com/gmberton/EigenPlaces) | MIT | 2 | `eigenplaces` |
| [https://docs.ultralytics.com/models/yolov9#performance-on-ms-coco-dataset](https://docs.ultralytics.com/models/yolov9#performance-on-ms-coco-dataset) | GPL-3.0 | 2 | `yolov9_seg` |
| [https://paddle-imagenet-models-name.bj.bcebos.com/dygraph/rec/models/inference/picodet_PPLCNet_x2_5_mainbody_lite_v1.0_infer.tar](https://paddle-imagenet-models-name.bj.bcebos.com/dygraph/rec/models/inference/picodet_PPLCNet_x2_5_mainbody_lite_v1.0_infer.tar) | Apache-2.0 | 2 | `pp_shitu` |
| [NVlabs/CenterPose](https://github.com/NVlabs/CenterPose) | MIT | 2 | `centerpose` |
| [PingoLH/Pytorch-HarDNet](https://github.com/PingoLH/Pytorch-HarDNet) | MIT | 2 | `hardnet` |
| [VainF/DeepLabV3Plus-Pytorch](https://github.com/VainF/DeepLabV3Plus-Pytorch) | MIT | 2 | `deeplabv3` |
| [ydhongHIT/DDRNet](https://github.com/ydhongHIT/DDRNet) | MIT | 2 | `ddrnet` |
| [amazon-science/patchcore-inspection](https://github.com/amazon-science/patchcore-inspection) | Apache-2.0 | 1 | `patchcore` |
| [CASIA-IVA-Lab/FastSAM](https://github.com/CASIA-IVA-Lab/FastSAM) | Apache-2.0 | 1 | `fastsam` |
| [ChengpengChen/RepGhost](https://github.com/ChengpengChen/RepGhost) | MIT | 1 | `repghost` |
| [d-li14/face-attribute-prediction](https://github.com/d-li14/face-attribute-prediction) | MIT | 1 | `faceattr` |
| [DepthAnything/Depth-Anything-V2](https://github.com/DepthAnything/Depth-Anything-V2) | Apache-2.0 | 1 | `depthanythingv2` |
| [dwofk/fast-depth](https://github.com/dwofk/fast-depth) | MIT | 1 | `fastdepth` |
| [google-ai-edge/mediapipe](https://github.com/google-ai-edge/mediapipe) | Apache-2.0 | 1 | `mediapipe_hands_lite` |
| [https://google.github.io/mediapipe/solutions/hands](https://google.github.io/mediapipe/solutions/hands) | Apache-2.0 | 1 | `mediapipe_hand_detector` |
| [https://huggingface.co/facebook/levit-128S](https://huggingface.co/facebook/levit-128S) | Apache-2.0 | 1 | `levit` |
| [https://huggingface.co/facebook/levit-384](https://huggingface.co/facebook/levit-384) | Apache-2.0 | 1 | `levit` |
| [https://huggingface.co/google/vit-base-patch16-384](https://huggingface.co/google/vit-base-patch16-384) | Apache-2.0 | 1 | `vit` |
| [https://huggingface.co/microsoft/beit-large-patch16-224](https://huggingface.co/microsoft/beit-large-patch16-224) | MIT | 1 | `beit` |
| [https://huggingface.co/timm/resnet50_clip.openai](https://huggingface.co/timm/resnet50_clip.openai) | MIT | 1 | `clip_rn50` |
| [https://huggingface.co/timm/vit_tiny_patch16_224.augreg_in21k_ft_in1k](https://huggingface.co/timm/vit_tiny_patch16_224.augreg_in21k_ft_in1k) | Apache-2.0 | 1 | `vit` |
| [https://paddle-imagenet-models-name.bj.bcebos.com/dygraph/rec/models/inference/PP-ShiTuV2/general_PPLCNetV2_base_pretrained_v1.0_infer.tar](https://paddle-imagenet-models-name.bj.bcebos.com/dygraph/rec/models/inference/PP-ShiTuV2/general_PPLCNetV2_base_pretrained_v1.0_infer.tar) | Apache-2.0 | 1 | `pp_shitu_rec` |
| [https://pytorch.org/vision/stable/models/generated/torchvision.models.swin_b.html#torchvision.models.swin_b](https://pytorch.org/vision/stable/models/generated/torchvision.models.swin_b.html#torchvision.models.swin_b) | BSD-3-Clause | 1 | `swin` |
| [https://pytorch.org/vision/stable/models/generated/torchvision.models.vit_b_32.html](https://pytorch.org/vision/stable/models/generated/torchvision.models.vit_b_32.html) | BSD-3-Clause | 1 | `vit` |
| [https://pytorch.org/vision/stable/models/generated/torchvision.models.vit_l_16.html#torchvision.models.vit_l_16](https://pytorch.org/vision/stable/models/generated/torchvision.models.vit_l_16.html#torchvision.models.vit_l_16) | BSD-3-Clause | 1 | `vit` |
| [huawei-noah/Efficient-AI-Backbones](https://github.com/huawei-noah/Efficient-AI-Backbones) | No License | 1 | `ghostnet` |
| [hustvl/YOLOP](https://github.com/hustvl/YOLOP) | MIT | 1 | `yolopv2` |
| [jfzhang95/pytorch-deeplab-xception](https://github.com/jfzhang95/pytorch-deeplab-xception) | Apache-2.0 | 1 | `deeplabv3` |
| [JiawangBian/sc_depth_pl](https://github.com/JiawangBian/sc_depth_pl) | GPL-3.0 | 1 | `scdepthv3` |
| [Li-Chongyi/Zero-DCE](https://github.com/Li-Chongyi/Zero-DCE) | CC BY-NC 4.0 | 1 | `zerodce` |
| [Li-Chongyi/Zero-DCE_extension](https://github.com/Li-Chongyi/Zero-DCE_extension) | Non-commercial | 1 | `zerodce` |
| [magicleap/SuperPointPretrainedNetwork](https://github.com/magicleap/SuperPointPretrainedNetwork) | Non-commercial | 1 | `superpoint` |
| [maudzung/SFA3D](https://github.com/maudzung/SFA3D) | MIT | 1 | `sfa3d` |
| [microsoft/unilm/tree/master/beit](https://github.com/microsoft/unilm/tree/master/beit) | MIT | 1 | `beit` |
| [NVlabs/CenterPose](https://github.com/NVlabs/CenterPose) | Apache-2.0 | 1 | `centerpose` |
| [NVlabs/Deep_Object_Pose](https://github.com/NVlabs/Deep_Object_Pose) | Apache-2.0 | 1 | `dope` |
| [NVlabs/SegFormer](https://github.com/NVlabs/SegFormer) | Apache-2.0 | 1 | `segformer` |
| [openai/CLIP](https://github.com/openai/CLIP) | MIT | 1 | `clip_rn50` |
| [osmr/imgclsmob](https://github.com/osmr/imgclsmob) | MIT | 1 | `resnext` |
| [PaddlePaddle/PaddleClas/blob/develop/ppcls/arch/backbone/legendary_models/pphgnet.py](https://github.com/PaddlePaddle/PaddleClas/blob/develop/ppcls/arch/backbone/legendary_models/pphgnet.py) | Apache-2.0 | 1 | `pphgnet` |
| [PaddlePaddle/PaddleDetection/blob/release/2.6/configs/pphuman/dark_hrnet_w32_256x192.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.6/configs/pphuman/dark_hrnet_w32_256x192.yml) | Apache-2.0 | 1 | `dark_hrnet` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/mask_rtdetr/mask_rtdetr_hgnetv2_h_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/mask_rtdetr/mask_rtdetr_hgnetv2_h_6x_coco.yml) | Apache-2.0 | 1 | `mask_rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/mask_rtdetr/mask_rtdetr_hgnetv2_l_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/mask_rtdetr/mask_rtdetr_hgnetv2_l_6x_coco.yml) | Apache-2.0 | 1 | `mask_rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/mask_rtdetr/mask_rtdetr_hgnetv2_m_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/mask_rtdetr/mask_rtdetr_hgnetv2_m_6x_coco.yml) | Apache-2.0 | 1 | `mask_rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/mask_rtdetr/mask_rtdetr_hgnetv2_s_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/mask_rtdetr/mask_rtdetr_hgnetv2_s_6x_coco.yml) | Apache-2.0 | 1 | `mask_rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/mask_rtdetr/mask_rtdetr_hgnetv2_x_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/mask_rtdetr/mask_rtdetr_hgnetv2_x_6x_coco.yml) | Apache-2.0 | 1 | `mask_rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_hgnetv2_h_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_hgnetv2_h_6x_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_hgnetv2_l_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_hgnetv2_l_6x_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_hgnetv2_x_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_hgnetv2_x_6x_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_r101vd_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_r101vd_6x_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_r18vd_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_r18vd_6x_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_r34vd_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_r34vd_6x_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_r50vd_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_r50vd_6x_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_r50vd_m_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetr/rtdetr_r50vd_m_6x_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv2/rtdetrv2_r101vd_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv2/rtdetrv2_r101vd_6x_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv2/rtdetrv2_r18vd_120e_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv2/rtdetrv2_r18vd_120e_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv2/rtdetrv2_r34vd_120e_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv2/rtdetrv2_r34vd_120e_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv2/rtdetrv2_r50vd_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv2/rtdetrv2_r50vd_6x_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv2/rtdetrv2_r50vd_m_7x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv2/rtdetrv2_r50vd_m_7x_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv3/rtdetrv3_r18vd_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv3/rtdetrv3_r18vd_6x_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv3/rtdetrv3_r50vd_6x_coco.yml](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.9/configs/rtdetrv3/rtdetrv3_r50vd_6x_coco.yml) | Apache-2.0 | 1 | `rtdetr` |
| [PaddlePaddle/PaddleSeg/blob/release/2.8/configs/pp_liteseg/pp_liteseg_stdc1_camvid_960x720_10k.yml](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.8/configs/pp_liteseg/pp_liteseg_stdc1_camvid_960x720_10k.yml) | Apache-2.0 | 1 | `pp_liteseg` |
| [PaddlePaddle/PaddleSeg/blob/release/2.8/Matting/configs/ppmatting/ppmatting-hrnet_w48-composition.yml](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.8/Matting/configs/ppmatting/ppmatting-hrnet_w48-composition.yml) | Apache-2.0 | 1 | `ppmatting` |
| [PaddlePaddle/PaddleSeg/blob/release/2.8/Matting/configs/ppmatting/ppmatting-hrnet_w48-distinctions.yml](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.8/Matting/configs/ppmatting/ppmatting-hrnet_w48-distinctions.yml) | Apache-2.0 | 1 | `ppmatting` |
| [tensorflow/examples](https://github.com/tensorflow/examples) | Apache-2.0 | 1 | `unet` |
| [ViTAE-Transformer/ViTPose](https://github.com/ViTAE-Transformer/ViTPose) | Apache-2.0 | 1 | `vitpose` |
| [XuJiacong/PIDNet](https://github.com/XuJiacong/PIDNet) | MIT | 1 | `pidnet` |
| [yhhhli/BRECQ](https://github.com/yhhhli/BRECQ) | Apache-2.0 | 1 | `resnet` |

## Sample data

The sample images and videos in DX-APP come from public academic or open source datasets, or are generated by AI. They are for **evaluation and demonstration only**.

* We do not claim ownership of, or grant any commercial rights to, the third party datasets. Many public datasets, such as ImageNet, COCO, Pascal VOC and DOTA, allow only non commercial research and education.
* AI generated sample images contain no third party content and are not subject to an external dataset license. For example, the oriented detection sample image is an AI generated satellite image.
* You are responsible for finding the original source of any sample data and following its license.
* Do not redistribute the sample images or use them in a commercial product or service without permission from the copyright holders.

| Sample | Source | License |
|---|---|---|
| `sample/vpr/` (visual place recognition: 17 database images, 5 query images) | [gmberton/VPR-methods-evaluation](https://github.com/gmberton/VPR-methods-evaluation) toy dataset | MIT |
| `sample/kitti/` (LiDAR point clouds, calibration, camera images) | KITTI | KITTI dataset terms |
| `sample/ILSVRC2012/` (classification images) | ImageNet (ILSVRC2012) | ImageNet terms (non commercial research) |

The VPR toy dataset has no ground truth positions, so it shows top k retrieval but not Recall@k.

## Disclaimer

We provide these third party models and datasets as is, for your convenience. We are not responsible for legal issues or damages from unauthorized or commercial use of these resources. By using the samples, you accept all legal and financial liability for license compliance.

## Next steps

* [Model catalog](models.md)
* [DX-ModelZoo](../model-zoo/index.md)
