'''
Function:
    Implementation of Segformer
Author:
    Zhenchao Jin
'''
import torch
import torch.nn as nn
import torch.nn.functional as F
from ..base import BaseSegmentor
from ...backbones import BuildActivation, BuildNormalization


'''Segformer'''
class Segformer(BaseSegmentor):
    def __init__(self, cfg, mode):
        super(Segformer, self).__init__(cfg, mode)
        align_corners, norm_cfg, act_cfg, head_cfg = self.align_corners, self.norm_cfg, self.act_cfg, cfg['head']
        # build decoder
        self.convs = nn.ModuleList()
        for in_channels in head_cfg['in_channels_list']:
            self.convs.append(nn.Sequential(
                nn.Conv2d(in_channels, head_cfg['feats_channels'], kernel_size=1, stride=1, padding=0, bias=False),
                BuildNormalization(placeholder=head_cfg['feats_channels'], norm_cfg=norm_cfg),
                BuildActivation(act_cfg),
            ))
        self.decoder = nn.Sequential(
            nn.Conv2d(head_cfg['feats_channels'] * len(self.convs), head_cfg['feats_channels'], kernel_size=1, stride=1, padding=0, bias=False),
            BuildNormalization(placeholder=head_cfg['feats_channels'], norm_cfg=norm_cfg),
            BuildActivation(act_cfg),
            nn.Dropout2d(head_cfg['dropout']),
            nn.Conv2d(head_cfg['feats_channels'], cfg['num_classes'], kernel_size=1, stride=1, padding=0),
        )
        # freeze normalization layer if necessary
        if cfg.get('is_freeze_norm', False): self.freezenormalization()
    '''forward'''
    def forward(self, x, targets=None):
        img_size = x.size(2), x.size(3)
        # feed to backbone network
        backbone_outputs = self.transforminputs(self.backbone_net(x), selected_indices=self.cfg['backbone'].get('selected_indices'))
        # feed to decoder
        outs = []
        for idx, feats in enumerate(list(backbone_outputs)):
            outs.append(
                F.interpolate(self.convs[idx](feats), size=backbone_outputs[0].shape[2:], mode='bilinear', align_corners=self.align_corners)
            )
        feats = torch.cat(outs, dim=1)
        predictions = self.decoder(feats)
        # forward according to the mode
        if self.mode == 'TRAIN':
            loss, losses_log_dict = self.customizepredsandlosses(
                predictions=predictions, targets=targets, backbone_outputs=backbone_outputs, losses_cfg=self.cfg['losses'], img_size=img_size,
            )
            return loss, losses_log_dict
        return predictions