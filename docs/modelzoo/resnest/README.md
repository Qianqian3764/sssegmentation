## Introduction

<a href="https://github.com/zhanghang1989/ResNeSt">Official Repo</a>

<a href="https://github.com/SegmentationBLWX/sssegmentation/blob/main/ssseg/modules/models/backbones/resnest.py">Code Snippet</a>

<details>
<summary align="left"><a href="https://arxiv.org/pdf/2004.08955.pdf">ResNeSt (ArXiv'2020)</a></summary>

```latex
@article{zhang2020resnest,
    title={ResNeSt: Split-Attention Networks},
    author={Zhang, Hang and Wu, Chongruo and Zhang, Zhongyue and Zhu, Yi and Zhang, Zhi and Lin, Haibin and Sun, Yue and He, Tong and Muller, Jonas and Manmatha, R. and Li, Mu and Smola, Alexander},
    journal={arXiv preprint arXiv:2004.08955},
    year={2020}
}
```

</details>


## Results

#### PASCAL VOC

| Segmentor     | Pretrain               | Backbone  | Crop Size  | Schedule                             | Train/Eval Set  | mIoU   | Download                                                                                                                                                                                                                                                                                                                                                                                                         |
| :-:           | :-:                    | :-:       | :-:        | :-:                                  | :-:             | :-:    | :-:                                                                                                                                                                                                                                                                                                                                                                                                              |
| FCN           | ImageNet-1k-224x224    | S-101-D8  | 512x512    | LR/POLICY/BS/EPOCH: 0.01/poly/16/60  | trainaug/val    | 77.41% | [cfg](https://raw.githubusercontent.com/SegmentationBLWX/sssegmentation/main/ssseg/configs/fcn/fcn_resnest101os8_voc.py) &#124; [model](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/fcn_resnest101os8_voc.pth) &#124; [log](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/fcn_resnest101os8_voc.log)                                         |
| PSPNet        | ImageNet-1k-224x224    | S-101-D8  | 512x512    | LR/POLICY/BS/EPOCH: 0.01/poly/16/60  | trainaug/val    | 79.07% | [cfg](https://raw.githubusercontent.com/SegmentationBLWX/sssegmentation/main/ssseg/configs/pspnet/pspnet_resnest101os8_voc.py) &#124; [model](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/pspnet_resnest101os8_voc.pth) &#124; [log](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/pspnet_resnest101os8_voc.log)                             |
| DeepLabV3     | ImageNet-1k-224x224    | S-101-D8  | 512x512    | LR/POLICY/BS/EPOCH: 0.01/poly/16/60  | trainaug/val    | 78.97% | [cfg](https://raw.githubusercontent.com/SegmentationBLWX/sssegmentation/main/ssseg/configs/deeplabv3/deeplabv3_resnest101os8_voc.py) &#124; [model](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/deeplabv3_resnest101os8_voc.pth) &#124; [log](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/deeplabv3_resnest101os8_voc.log)                 |
| DeepLabV3plus | ImageNet-1k-224x224    | S-101-D8  | 512x512    | LR/POLICY/BS/EPOCH: 0.01/poly/16/60  | trainaug/val    | 79.76% | [cfg](https://raw.githubusercontent.com/SegmentationBLWX/sssegmentation/main/ssseg/configs/deeplabv3plus/deeplabv3plus_resnest101os8_voc.py) &#124; [model](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/deeplabv3plus_resnest101os8_voc.pth) &#124; [log](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/deeplabv3plus_resnest101os8_voc.log) |

#### ADE20k

| Segmentor     | Pretrain               | Backbone  | Crop Size  | Schedule                             | Train/Eval Set  | mIoU   | Download                                                                                                                                                                                                                                                                                                                                                                                                                  |
| :-:           | :-:                    | :-:       | :-:        | :-:                                  | :-:             | :-:    | :-:                                                                                                                                                                                                                                                                                                                                                                                                                       |
| FCN           | ImageNet-1k-224x224    | S-101-D8  | 512x512    | LR/POLICY/BS/EPOCH: 0.01/poly/16/130 | train/val       | 45.74% | [cfg](https://raw.githubusercontent.com/SegmentationBLWX/sssegmentation/main/ssseg/configs/fcn/fcn_resnest101os8_ade20k.py) &#124; [model](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/fcn_resnest101os8_ade20k.pth) &#124; [log](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/fcn_resnest101os8_ade20k.log)                                         |
| PSPNet        | ImageNet-1k-224x224    | S-101-D8  | 512x512    | LR/POLICY/BS/EPOCH: 0.01/poly/16/130 | train/val       | 46.03% | [cfg](https://raw.githubusercontent.com/SegmentationBLWX/sssegmentation/main/ssseg/configs/pspnet/pspnet_resnest101os8_ade20k.py) &#124; [model](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/pspnet_resnest101os8_ade20k.pth) &#124; [log](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/pspnet_resnest101os8_ade20k.log)                             |
| DeepLabV3     | ImageNet-1k-224x224    | S-101-D8  | 512x512    | LR/POLICY/BS/EPOCH: 0.01/poly/16/130 | train/val       | 46.24% | [cfg](https://raw.githubusercontent.com/SegmentationBLWX/sssegmentation/main/ssseg/configs/deeplabv3/deeplabv3_resnest101os8_ade20k.py) &#124; [model](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/deeplabv3_resnest101os8_ade20k.pth) &#124; [log](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/deeplabv3_resnest101os8_ade20k.log)                 |
| DeepLabV3plus | ImageNet-1k-224x224    | S-101-D8  | 512x512    | LR/POLICY/BS/EPOCH: 0.01/poly/16/130 | train/val       | 46.48% | [cfg](https://raw.githubusercontent.com/SegmentationBLWX/sssegmentation/main/ssseg/configs/deeplabv3plus/deeplabv3plus_resnest101os8_ade20k.py) &#124; [model](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/deeplabv3plus_resnest101os8_ade20k.pth) &#124; [log](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/deeplabv3plus_resnest101os8_ade20k.log) |

#### CityScapes

| Segmentor     | Pretrain               | Backbone  | Crop Size  | Schedule                             | Train/Eval Set  | mIoU   | Download                                                                                                                                                                                                                                                                                                                                                                                                                              |
| :-:           | :-:                    | :-:       | :-:        | :-:                                  | :-:             | :-:    | :-:                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| FCN           | ImageNet-1k-224x224    | S-101-D8  | 512x1024   | LR/POLICY/BS/EPOCH: 0.01/poly/8/220  | train/val       | 78.14% | [cfg](https://raw.githubusercontent.com/SegmentationBLWX/sssegmentation/main/ssseg/configs/fcn/fcn_resnest101os8_cityscapes.py) &#124; [model](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/fcn_resnest101os8_cityscapes.pth) &#124; [log](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/fcn_resnest101os8_cityscapes.log)                                         |
| PSPNet        | ImageNet-1k-224x224    | S-101-D8  | 512x1024   | LR/POLICY/BS/EPOCH: 0.01/poly/8/220  | train/val       | 78.70% | [cfg](https://raw.githubusercontent.com/SegmentationBLWX/sssegmentation/main/ssseg/configs/pspnet/pspnet_resnest101os8_cityscapes.py) &#124; [model](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/pspnet_resnest101os8_cityscapes.pth) &#124; [log](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/pspnet_resnest101os8_cityscapes.log)                             |
| DeepLabV3     | ImageNet-1k-224x224    | S-101-D8  | 512x1024   | LR/POLICY/BS/EPOCH: 0.01/poly/8/220  | train/val       | 79.75% | [cfg](https://raw.githubusercontent.com/SegmentationBLWX/sssegmentation/main/ssseg/configs/deeplabv3/deeplabv3_resnest101os8_cityscapes.py) &#124; [model](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/deeplabv3_resnest101os8_cityscapes.pth) &#124; [log](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/deeplabv3_resnest101os8_cityscapes.log)                 |
| DeepLabV3plus | ImageNet-1k-224x224    | S-101-D8  | 512x1024   | LR/POLICY/BS/EPOCH: 0.01/poly/8/220  | train/val       | 80.30% | [cfg](https://raw.githubusercontent.com/SegmentationBLWX/sssegmentation/main/ssseg/configs/deeplabv3plus/deeplabv3plus_resnest101os8_cityscapes.py) &#124; [model](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/deeplabv3plus_resnest101os8_cityscapes.pth) &#124; [log](https://github.com/SegmentationBLWX/modelstore/releases/download/ssseg_resnest/deeplabv3plus_resnest101os8_cityscapes.log) |


## More

You can also download the model weights from following sources:

- BaiduNetdisk: https://pan.baidu.com/s/1gD-NJJWOtaHCtB0qHE79rA with access code **s757**