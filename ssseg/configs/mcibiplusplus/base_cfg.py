'''SEGMENTOR_CFG for MCIBI++'''
SEGMENTOR_CFG = {
    'type': 'MCIBIPlusPlus',
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
    'norm_cfg': {'type': 'SyncBatchNorm'},
    'act_cfg': {'type': 'ReLU', 'inplace': True},
    'backbone': {
        'type': 'ResNet', 'depth': 101, 'structure_type': 'resnet101conv3x3stem',
        'pretrained': True, 'outstride': 8, 'use_conv3x3_stem': True, 'selected_indices': (0, 1, 2, 3),
    },
    'head': {
        'context_within_image': {
            'is_on': False, 'type': ['ppm', 'aspp'][1],
            'cfg': {'pool_scales': [1, 2, 3, 6], 'dilations': [1, 12, 24, 36]}
        },
        'warmup_epoch': 0, 'use_hard_aggregate': False, 'downsample_before_sa': False,
        'force_use_preds_pr': False, 'fuse_memory_cwi_before_fpn': True, 'in_channels': 2048,
        'feats_channels': 512, 'transform_channels': 256, 'out_channels': 512,
        'update_cfg': {
            'ignore_index': 255,
            'momentum_cfg': {'base_momentum': 0.1, 'base_lr': None, 'adjust_by_learning_rate': False},
        },
        'decoder': {
            'pr': {'in_channels': 512, 'out_channels': 512, 'dropout': 0.1},
            'cwi': {'in_channels': 512, 'out_channels': 512, 'dropout': 0.1},
            'cls': {'in_channels': 512, 'out_channels': 512, 'dropout': 0.1},
        },
    },
    'auxiliary': {'in_channels': 1024, 'out_channels': 512, 'dropout': 0.1},
    'losses': {
        'loss_aux': {'type': 'CrossEntropyLoss', 'scale_factor': 0.4, 'ignore_index': 255, 'reduction': 'mean'},
        'loss_pr': {'type': 'CrossEntropyLoss', 'scale_factor': 0.4, 'ignore_index': 255, 'reduction': 'mean'},
        'loss_cwi': {'type': 'CrossEntropyLoss', 'scale_factor': 1.0, 'ignore_index': 255, 'reduction': 'mean'},
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