'''upernet_svtbase_ade20k'''
import copy
from .base_cfg import SEGMENTOR_CFG
from .._base_ import DATASET_CFG_ADE20k_512x512, DATALOADER_CFG_BS16


# deepcopy
SEGMENTOR_CFG = copy.deepcopy(SEGMENTOR_CFG)
# modify dataset config
SEGMENTOR_CFG['dataset'] = DATASET_CFG_ADE20k_512x512.copy()
# modify dataloader config
SEGMENTOR_CFG['dataloader'] = DATALOADER_CFG_BS16.copy()
# modify scheduler config
SEGMENTOR_CFG['scheduler']['max_epochs'] = 130
SEGMENTOR_CFG['scheduler']['min_lr'] = 0.0
SEGMENTOR_CFG['scheduler']['power'] = 1.0
SEGMENTOR_CFG['scheduler']['warmup_cfg'] = {'type': 'linear', 'ratio': 1e-6, 'iters': 1500}
SEGMENTOR_CFG['scheduler']['optimizer'] = {
    'type': 'AdamW', 'lr': 0.00006, 'betas': (0.9, 0.999), 'weight_decay': 0.01,
    'params_rules': {
        'norm': dict(wd_multiplier=0.),
        'position_encodings': dict(wd_multiplier=0.),
    },
}
# modify other segmentor configs
SEGMENTOR_CFG['num_classes'] = 150
SEGMENTOR_CFG['backbone'] = {
    'type': 'SVT', 'structure_type': 'svt_base', 'pretrained': True, 'selected_indices': (0, 1, 2, 3), 'norm_cfg': {'type': 'LayerNorm'},
    'embed_dims': [96, 192, 384, 768], 'num_heads': [3, 6, 12, 24], 'mlp_ratios': [4, 4, 4, 4], 'depths': [2, 2, 18, 2], 
    'windiow_sizes': [7, 7, 7, 7], 'norm_after_stage': True, 'drop_path_rate': 0.2
}
SEGMENTOR_CFG['head'] = {
    'in_channels_list': [96, 192, 384, 768], 'feats_channels': 512, 'pool_scales': [1, 2, 3, 6], 'dropout': 0.1,
}
SEGMENTOR_CFG['auxiliary'] = {
    'in_channels': 384, 'out_channels': 512, 'dropout': 0.1,
}
SEGMENTOR_CFG['work_dir'] = 'upernet_svtbase_ade20k'
SEGMENTOR_CFG['logfilepath'] = 'upernet_svtbase_ade20k/upernet_svtbase_ade20k.log'
SEGMENTOR_CFG['resultsavepath'] = 'upernet_svtbase_ade20k/upernet_svtbase_ade20k_results.pkl'