'''
Function:
    Base segmentor for all supported segmentors
Author:
    Zhenchao Jin
'''
import copy
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch.distributed as dist
from ...losses import BuildLoss
from ...backbones import BuildBackbone, BuildActivation, BuildNormalization, NormalizationBuilder


'''BaseSegmentor'''
class BaseSegmentor(nn.Module):
    def __init__(self, cfg, mode):
        super(BaseSegmentor, self).__init__()
        self.cfg = cfg
        self.mode = mode
        assert self.mode in ['TRAIN', 'TEST']
        # parse align_corners, normalization layer and activation layer cfg
        self.align_corners, self.norm_cfg, self.act_cfg = cfg['align_corners'], cfg['norm_cfg'], cfg['act_cfg']
        # build backbone
        backbone_cfg = copy.deepcopy(cfg['backbone'])
        if 'norm_cfg' not in backbone_cfg:
            backbone_cfg.update({'norm_cfg': copy.deepcopy(self.norm_cfg)})
        self.backbone_net = BuildBackbone(backbone_cfg)
    '''forward'''
    def forward(self, x, targets=None):
        raise NotImplementedError('not to be implemented')
    '''customizepredsandlosses'''
    def customizepredsandlosses(self, predictions, targets, backbone_outputs, losses_cfg, img_size, auto_calc_loss=True, map_preds_to_tgts_dict=None):
        predictions = F.interpolate(predictions, size=img_size, mode='bilinear', align_corners=self.align_corners)
        outputs_dict = {'loss_cls': predictions}
        if hasattr(self, 'auxiliary_decoder'):
            backbone_outputs = backbone_outputs[:-1]
            if isinstance(self.auxiliary_decoder, nn.ModuleList):
                assert len(backbone_outputs) >= len(self.auxiliary_decoder)
                backbone_outputs = backbone_outputs[-len(self.auxiliary_decoder):]
                for idx, (out, dec) in enumerate(zip(backbone_outputs, self.auxiliary_decoder)):
                    predictions_aux = dec(out)
                    predictions_aux = F.interpolate(predictions_aux, size=img_size, mode='bilinear', align_corners=self.align_corners)
                    outputs_dict[f'loss_aux{idx+1}'] = predictions_aux
            else:
                predictions_aux = self.auxiliary_decoder(backbone_outputs[-1])
                predictions_aux = F.interpolate(predictions_aux, size=img_size, mode='bilinear', align_corners=self.align_corners)
                outputs_dict = {'loss_cls': predictions, 'loss_aux': predictions_aux}
        if not auto_calc_loss: return outputs_dict
        return self.calculatelosses(predictions=outputs_dict, targets=targets, losses_cfg=losses_cfg, map_preds_to_tgts_dict=map_preds_to_tgts_dict)
    '''inference'''
    def inference(self, images, forward_args=None):
        # assert and initialize
        inference_cfg = self.cfg['inference']
        assert inference_cfg['mode'] in ['whole', 'slide']
        use_probs_before_resize = inference_cfg['tricks']['use_probs_before_resize']
        images = images.type(torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor)
        # inference
        if inference_cfg['mode'] == 'whole':
            if forward_args is None: outputs = self(images)
            else: outputs = self(images, **forward_args)
            if use_probs_before_resize: outputs = F.softmax(outputs, dim=1)
        else:
            opts = inference_cfg['opts']
            stride_h, stride_w = opts['stride']
            cropsize_h, cropsize_w = opts['cropsize']
            batch_size, _, image_h, image_w = images.size()
            num_grids_h = max(image_h - cropsize_h + stride_h - 1, 0) // stride_h + 1
            num_grids_w = max(image_w - cropsize_w + stride_w - 1, 0) // stride_w + 1
            outputs = images.new_zeros((batch_size, self.cfg['num_classes'], image_h, image_w))
            count_mat = images.new_zeros((batch_size, 1, image_h, image_w))
            for h_idx in range(num_grids_h):
                for w_idx in range(num_grids_w):
                    x1, y1 = w_idx * stride_w, h_idx * stride_h
                    x2, y2 = min(x1 + cropsize_w, image_w), min(y1 + cropsize_h, image_h)
                    x1, y1 = max(x2 - cropsize_w, 0), max(y2 - cropsize_h, 0)
                    crop_images = images[:, :, y1:y2, x1:x2]
                    if forward_args is None: outputs_crop = self(crop_images)
                    else: outputs_crop = self(crop_images, **forward_args)
                    outputs_crop = F.interpolate(outputs_crop, size=crop_images.size()[2:], mode='bilinear', align_corners=self.align_corners)
                    if use_probs_before_resize: outputs_crop = F.softmax(outputs_crop, dim=1)
                    outputs += F.pad(outputs_crop, (int(x1), int(outputs.shape[3] - x2), int(y1), int(outputs.shape[2] - y2)))
                    count_mat[:, :, y1:y2, x1:x2] += 1
            assert (count_mat == 0).sum() == 0
            outputs = outputs / count_mat
        # return outputs
        return outputs
    '''auginference'''
    def auginference(self, images, forward_args=None):
        # initialize
        inference_cfg = self.cfg['inference']
        infer_tricks, outputs_list = inference_cfg['tricks'], []
        # iter to inference
        for scale_factor in infer_tricks['multiscale']:
            images_scale = F.interpolate(images, scale_factor=scale_factor, mode='bilinear', align_corners=self.align_corners)
            outputs = self.inference(images=images_scale, forward_args=forward_args).cpu()
            outputs_list.append(outputs)
            if infer_tricks['flip']:
                images_scale_flip = torch.from_numpy(np.flip(images_scale.cpu().numpy(), axis=3).copy())
                outputs_flip = self.inference(images=images_scale_flip, forward_args=forward_args)
                fixed_seg_target_pairs = inference_cfg.get('fixed_seg_target_pairs', None)
                if fixed_seg_target_pairs is None:
                    for data_pipeline in self.cfg['dataset']['train']['data_pipelines']:
                        if 'RandomFlip' in data_pipeline:
                            fixed_seg_target_pairs = data_pipeline[-1].get('fixed_seg_target_pairs', None)
                if fixed_seg_target_pairs is not None:
                    outputs_flip_clone = outputs_flip.data.clone()
                    for (pair_a, pair_b) in fixed_seg_target_pairs:
                        outputs_flip[:, pair_a, :, :] = outputs_flip_clone[:, pair_b, :, :]
                        outputs_flip[:, pair_b, :, :] = outputs_flip_clone[:, pair_a, :, :]
                outputs_flip = torch.from_numpy(np.flip(outputs_flip.cpu().numpy(), axis=3).copy()).type_as(outputs)
                outputs_list.append(outputs_flip)
        # return outputs
        return outputs_list
    '''transforminputs'''
    def transforminputs(self, x_list, selected_indices=None):
        if selected_indices is None:
            if self.cfg['backbone']['type'] in ['HRNet']:
                selected_indices = (0, 0, 0, 0)
            else:
                selected_indices = (0, 1, 2, 3)
        outs = []
        for idx in selected_indices:
            outs.append(x_list[idx])
        return outs
    '''setauxiliarydecoder'''
    def setauxiliarydecoder(self, auxiliary_cfg):
        norm_cfg, act_cfg, num_classes = self.norm_cfg.copy(), self.act_cfg.copy(), self.cfg['num_classes']
        if auxiliary_cfg is None: return
        if isinstance(auxiliary_cfg, dict):
            auxiliary_cfg = [auxiliary_cfg]
        self.auxiliary_decoder = nn.ModuleList()
        for aux_cfg in auxiliary_cfg:
            num_convs = aux_cfg.get('num_convs', 1)
            dec = []
            for idx in range(num_convs):
                if idx == 0:
                    dec += [nn.Conv2d(aux_cfg['in_channels'], aux_cfg['out_channels'], kernel_size=3, stride=1, padding=1, bias=False),]
                else:
                    dec += [nn.Conv2d(aux_cfg['out_channels'], aux_cfg['out_channels'], kernel_size=3, stride=1, padding=1, bias=False),]
                dec += [
                    BuildNormalization(placeholder=aux_cfg['out_channels'], norm_cfg=norm_cfg),
                    BuildActivation(act_cfg)
                ]
                if 'upsample' in aux_cfg:
                    dec += [nn.Upsample(**aux_cfg['upsample'])]
            dec.append(nn.Dropout2d(aux_cfg['dropout']))
            if num_convs > 0:
                dec.append(nn.Conv2d(aux_cfg['out_channels'], num_classes, kernel_size=1, stride=1, padding=0))
            else:
                dec.append(nn.Conv2d(aux_cfg['in_channels'], num_classes, kernel_size=1, stride=1, padding=0))
            dec = nn.Sequential(*dec)
            self.auxiliary_decoder.append(dec)
        if len(self.auxiliary_decoder) == 1:
            self.auxiliary_decoder = self.auxiliary_decoder[0]
    '''freezenormalization'''
    def freezenormalization(self, norm_list=None):
        if norm_list is None:
            norm_list=(nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d, nn.SyncBatchNorm)
        for module in self.modules():
            if NormalizationBuilder.isnorm(module, norm_list):
                module.eval()
                for p in module.parameters():
                    p.requires_grad = False
    '''calculatelosses'''
    def calculatelosses(self, predictions, targets, losses_cfg, map_preds_to_tgts_dict=None):
        assert len(predictions) == len(losses_cfg), 'length of losses_cfg should be equal to the one of predictions'
        # calculate loss according to losses_cfg
        losses_log_dict = {}
        for loss_name, loss_cfg in losses_cfg.items():
            if map_preds_to_tgts_dict is None:
                losses_log_dict[loss_name] = self.calculateloss(
                    prediction=predictions[loss_name], target=targets['seg_target'], loss_cfg=loss_cfg,
                )
            else:
                losses_log_dict[loss_name] = self.calculateloss(
                    prediction=predictions[loss_name], target=targets[map_preds_to_tgts_dict[loss_name]], loss_cfg=loss_cfg,
                )
        # summarize and convert losses_log_dict
        loss = 0
        for loss_key, loss_value in losses_log_dict.items():
            loss_value = loss_value.mean()
            loss = loss + loss_value
            loss_value = loss_value.data.clone()
            dist.all_reduce(loss_value.div_(dist.get_world_size()))
            losses_log_dict[loss_key] = loss_value.item()
        losses_log_dict.update({'loss_total': sum(losses_log_dict.values())})
        # return the loss and losses_log_dict
        return loss, losses_log_dict
    '''calculateloss'''
    def calculateloss(self, prediction, target, loss_cfg):
        assert isinstance(loss_cfg, (dict, list))
        # calculate the loss, dict means single-type loss and list represents multiple-type losses
        if isinstance(loss_cfg, dict):
            loss = BuildLoss(loss_cfg)(prediction, target)
        else:
            loss = 0
            for l_cfg in loss_cfg:
                loss = loss + BuildLoss(l_cfg)(prediction, target)
        # return the loss
        return loss