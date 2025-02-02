'''SEGMENTOR_CFG for LRASPPNet'''
SEGMENTOR_CFG = {
    'type': 'LRASPPNet',
    'num_classes': -1,
    'benchmark': True,
    'align_corners': False,
    'backend': 'nccl',
    'work_dir': 'ckpts',
    'logfilepath': '',
    'log_interval_iterations': 50,
    'eval_interval_epochs': 10,
    'save_interval_epochs': 1,
    'resultsavepath': '',
    'norm_cfg': {'type': 'SyncBatchNorm', 'eps': 0.001},
    'act_cfg': {'type': 'ReLU', 'inplace': True},
    'backbone': {
        'type': 'MobileNetV3', 'structure_type': 'mobilenetv3_large', 'pretrained': True,
        'outstride': 8, 'arch_type': 'large', 'selected_indices': (0, 1, 2),
    },
    'head': {
        'in_channels_list': [16, 24, 960], 'branch_channels_list': [32, 64], 'feats_channels': 128, 'dropout': 0.1,
    },
    'losses': {
        'loss_cls': {'type': 'CrossEntropyLoss', 'scale_factor': 1.0, 'ignore_index': 255, 'reduction': 'mean'},
    },
    'inference': {
        'mode': 'whole',
        'opts': {}, 
        'tricks': {
            'multiscale': [1], 'flip': False, 'use_probs_before_resize': False,
        }
    },
    'scheduler': {
        'type': 'PolyScheduler', 'max_epochs': 0, 'power': 0.9,
        'optimizer': {
            'type': 'SGD', 'lr': 0.01, 'momentum': 0.9, 'weight_decay': 5e-4, 'params_rules': {},
        }
    },
    'dataset': None,
    'dataloader': None,
}