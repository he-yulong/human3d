"""
Sets default args

Note all data format is NHWC because slim resnet wants NHWC.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path as osp
from os import makedirs
from glob import glob
from datetime import datetime
import json
import ipdb
import numpy as np

curr_path = osp.dirname(osp.abspath(__file__))
model_dir = osp.join(curr_path, '..', 'models')
if not osp.exists(model_dir):
    print('Fix path to models/')
    ipdb.set_trace()

SMPL_MODEL_PATH = osp.join(model_dir,
                           'neutral_smpl_with_cocoplustoesankles_reg.pkl')
SMPL_FACE_PATH = osp.join(curr_path, '../src/tf_smpl', 'smpl_faces.npy')

# Default pred-trained model path for the demo.
PRETRAINED_MODEL = osp.join(model_dir, 'hmr_noS5.ckpt-642561')

# Pre-trained HMMR model:
HMMR_MODEL = osp.join(model_dir, 'hmmr_model.ckpt-1119816')


def get_config(parser):
    # Pre-trained HMMR model:
    parser.add_argument('--smpl_model_path', default=SMPL_MODEL_PATH, help='path to the neutral smpl model.')
    parser.add_argument('--smpl_face_path', default=SMPL_FACE_PATH,
                        help='path to smpl mesh faces (for easy rendering).')

    parser.add_argument('--load_path', default=None, help='path to trained model dir.')
    parser.add_argument('--batch_size', type=int, default=8, help='Size of mini-batch.')
    parser.add_argument('--T', type=int, default=20, help='Length of sequence.')
    parser.add_argument('--num_kps', type=int, default=25, help='Number of keypoints.')
    parser.add_argument('--num_conv_layers', type=int, default=3, help='Number of layers for convolutional.')
    parser.add_argument('--delta_t_values', nargs='+', default=['-5', '5'], help='Amount of time to jump by.')
    # For training.
    parser.add_argument('--data_dir', default=None, help='Where tfrecords are saved.')
    parser.add_argument('--log_dir', default='logs', help='Where to save training models.')
    parser.add_argument('--model_dir', default=None, help='Where model will be saved -- filled automatically.')
    parser.add_argument('--datasets', nargs='+', default=['h36m', 'penn_action', 'insta_variety'],
                        help='datasets to use for training.')
    parser.add_argument('--mocap_datasets', nargs='+', default=['CMU', 'H3.6', 'jointLim'],
                        help='Where to save training models.')
    parser.add_argument('--pretrained_model_path', nargs='+', default=[PRETRAINED_MODEL],
                        help='if not None, fine-tunes from this ckpt.')
    parser.add_argument('--image_encoder_model_type', default='resnet', help='Specifies which image encoder to use.')
    parser.add_argument('--temporal_encoder_type', default='AZ_FC2GN',
                        help='Specifies which network to use for temporal encoding.')
    parser.add_argument('--hallucinator_model_type', default='fc2_res',
                        help='Specifies network to convert phi to moviestrip.')
    parser.add_argument('--img_size', type=int, default=224,
                        help='Input image size to the network after preprocessing.')
    parser.add_argument('--data_format', default='NHWC', help='Data format.')
    parser.add_argument('--num_stage', type=int, default=3,
                        help='Number of times to iterate IEF regressor.')
    parser.add_argument('--max_iteration', type=int, default=5000000,
                        help='Number of max iteration to train.')
    parser.add_argument('--log_img_count', type=int, default=10,
                        help='Number of images in sequence to visualize.')
    parser.add_argument('--log_img_step', type=int, default=5000,
                        help='How often to visualize img during training.')
    parser.add_argument('--log_vid_step', type=int, default=100000,
                        help='How often to visualize video during training.')
    # Loss weights.
    parser.add_argument('--e_lw_smpl', type=int, default=60, help='Weight on loss_e_smpl.')
    parser.add_argument('--e_lw_joints', type=int, default=60, help='Weight on loss_e_joints.')
    parser.add_argument('--e_lw_const', type=int, default=1, help='Weight on loss_e_const.')
    parser.add_argument('--e_lw_kp', type=int, default=60, help='Weight on loss_e_kp.')
    parser.add_argument('--e_lw_pose', type=int, default=1, help='Weight on loss_e_pose.')
    parser.add_argument('--e_lw_shape', type=int, default=1, help='Weight on loss_e_shape.')
    parser.add_argument('--d_lw_pose', type=int, default=1, help='Weight on loss_d_pose.')

    # Hyper parameters:
    parser.add_argument('--e_lr', type=float, default=1e-5, help='Encoder learning rate.')
    parser.add_argument('--d_lr', type=float, default=1e-4, help='Adversarial prior learning rate.')
    parser.add_argument('--e_wd', type=float, default=1e-4, help='Encoder weight decay.')
    parser.add_argument('--d_wd', type=float, default=1e-4, help='Adversarial prior weight decay.')

    # Training setup.
    parser.add_argument('--use_3d_label', type=bool, default=True, help='Uses 3D labels if on.')
    parser.add_argument('--freeze_phi', type=bool, default=True, help='Fixes ResNet weights.')
    parser.add_argument('--use_hmr_ief_init', type=bool, default=True,
                        help='If True, uses HMR regressor as initialization to HMMR regressor.')
    parser.add_argument('--predict_delta', type=bool, default=True, help='If True, predicts future and past as well.')
    parser.add_argument('--precomputed_phi', type=bool, default=True,
                        help='If True, uses tfrecord with precomputed phi.')
    parser.add_argument('--use_3d_label', type=bool, default=True, help='Uses 3D labels if on.')
    parser.add_argument('--use_delta_from_pred', type=bool, default=True,
                        help='If True, initializes delta regressor from current prediction.')
    parser.add_argument('--use_hmr_only', type=bool, default=False, help='If true, uses HMR model.')
    # Equal split
    parser.add_argument('--split_balanced', type=bool, default=True,
                        help='default true, the queue is forced, '
                             'so its half 3D data (H36M) and half 2D in-the-wild data.')
    # Hallucinating
    parser.add_argument('--do_hallucinate', type=bool, default=False,
                        help='If true trained hallucinator.')
    parser.add_argument('--do_hallucinate_preds', type=bool, default=False,
                        help='if True, compute losses on predictions from hallucinator.')
    parser.add_argument('--e_lw_hallucinate', type=float, default=1.0,
                        help='Weight on ||pred movie_strip - movie_strip||.')

    # Data augmentation
    parser.add_argument('--trans_max', type=int, default=20, help='Max value of translation jitter.')
    parser.add_argument('--delta_trans_max', type=int, default=20, help='Max consecutive translation jitter.')
    parser.add_argument('--scale_max', type=float, default=0.3, help='Max value of scale jitter (power of 2).')
    parser.add_argument('--delta_scale_max', type=float, default=0.3, help='Max consecutive scale jitter.')
    parser.add_argument('--rotate_max', type=float, default=0, help='Max value to rotate jitter.')
    parser.add_argument('--delta_rotate_max', type=float, default=5, help='Max consecutive rotate jitter.')

    # Random seed
    parser.add_argument('--seed', type=int, default=1, help='Graph-level random seed.')
    parser.add_argument('--mosh_ignore', type=bool, default=False,
                        help='if true sets has_gt (smpl) off.')
    config = parser.parse_args()
    # Actually the rest of the code really assumes NHWC
    if config.data_format == 'NCHW':
        print('dont use NCHW')
        exit(1)

    return config


# ----- For training ----- #


def prepare_dirs(config, prefix=[]):
    # Continue training from a load_path
    if config.load_path:
        if not osp.exists(config.load_path):
            print("load_path: %s doesnt exist..!!!" % config.load_path)
            import ipdb
            ipdb.set_trace()
        print('continuing from %s!' % config.load_path)

        # Check for changed training parameter:
        # Load prev config param path
        param_path = glob(osp.join(config.load_path, '*.json'))[0]

        with open(param_path, 'r') as fp:
            prev_config = json.load(fp)
        dict_here = config.__dict__
        ignore_keys = ['load_path', 'log_img_step', 'pretrained_model_path']
        diff_keys = [
            k for k in dict_here
            if k not in ignore_keys and k in prev_config.keys()
               and prev_config[k] != dict_here[k]
        ]

        for k in diff_keys:
            if k == 'load_path' or k == 'log_img_step':
                continue
            if prev_config[k] is None and dict_here[k] is not None:
                print("%s is different!! before: None after: %g" %
                      (k, dict_here[k]))
            elif prev_config[k] is not None and dict_here[k] is None:
                print("%s is different!! before: %g after: None" %
                      (k, prev_config[k]))
            else:
                print("%s is different!! before: " % k)
                print(prev_config[k])
                print("now:")
                print(dict_here[k])

        if len(diff_keys) > 0:
            print("really continue??")
            import ipdb
            ipdb.set_trace()

        config.model_dir = config.load_path

    else:
        postfix = []

        # If config.dataset is not the same as default, add that to name.
        default_dataset = [
            'lsp', 'lsp_ext', 'mpii', 'h36m', 'coco', 'mpi_inf_3dhp'
        ]
        default_static_datasets = sorted(['lsp', 'coco'])
        default_mocap = ['CMU', 'H3.6', 'jointLim']

        if sorted(config.datasets) != sorted(default_dataset):
            has_all_default = np.all(
                [name in config.datasets for name in default_dataset])
            if has_all_default:
                new_names = [
                    name for name in sorted(config.datasets)
                    if name not in default_dataset
                ]
                postfix.append('default+' + '-'.join(sorted(new_names)))
            else:
                postfix.append('-'.join(sorted(config.datasets)))
        if sorted(config.mocap_datasets) != sorted(default_mocap):
            postfix.append('-'.join(config.mocap_datasets))

        if config.e_lr != 1e-5:
            postfix.append('Elr{:g}'.format(config.e_lr))

        # Weights:
        if config.e_lw_smpl != 60:
            postfix.append('lwsmpl-{}'.format(config.e_lw_smpl))
        if config.e_lw_joints != 60:
            postfix.append('lw3djoints-{}'.format(config.e_lw_joints))
        if config.e_lw_kp != 60:
            postfix.append('lw-kp{:g}'.format(config.e_lw_kp))
        if config.e_lw_shape != 1:
            postfix.append('lw-shape{:g}'.format(config.e_lw_shape))
        if config.e_lw_pose != 1:
            postfix.append('lw-pose{:g}'.format(config.e_lw_pose))
        if config.e_lw_hallucinate != 1:
            postfix.append('lw-hall{:g}'.format(config.e_lw_pose))

        if config.d_lr != 1e-4:
            postfix.append('Dlr{:g}' % config.d_lr)

        postfix.append('const{}'.format(config.e_lw_const))

        postfix.append('l2-shape-{}'.format(config.e_lw_shape))

        if config.use_hmr_ief_init:
            if config.temporal_encoder_type != 'AZ_FC2GN':
                print(
                    'HMR ief init is only implemented for AZ_FC2GN, implement'
                    ' it and update this warning!')
                import ipdb
                ipdb.set_trace()
            postfix.append('hmr-ief-init')

        # Model
        if not config.use_hmr_only:
            prefix.append(config.temporal_encoder_type)
            if config.temporal_encoder_type[0:5] == 'AZ_FC':
                prefix.append('{}'.format(config.num_conv_layers))
        else:
            prefix.append('HMR')

        if config.predict_delta:
            pref = 'pred-delta'
            if config.use_delta_from_pred:
                pref += '-from-pred'
            pref += '_'.join(config.delta_t_values)
            prefix.append(pref)

        if config.do_hallucinate:
            assert config.predict_delta
            pref = 'hal'
            if config.do_hallucinate_preds:
                # Prob. depreciated
                pref += '-preds'
            prefix.append(pref)

        if config.num_stage != 3:
            prefix += ["ief-stages%d" % config.num_stage]

        prefix.append('B{}'.format(config.batch_size))
        prefix.append('T{}'.format(config.T))

        if config.precomputed_phi:
            prefix.append('precomputed-phi')
        elif config.freeze_phi:
            prefix.append('freeze-phi')

        # Add pretrained (dont worry about load_path,
        # bc if it was specified id never get here):
        if config.pretrained_model_path is not None:
            if 'resnet_v2_50' in config.pretrained_model_path:
                postfix.append('from_resnet')
            elif 'hmr_noS5.ckpt-642561' == osp.basename(
                    config.pretrained_model_path[0]):
                postfix.append('from_{}'.format(
                    osp.basename(config.pretrained_model_path[0])))
            else:
                # We are finetuning from HMR/HMMR! include date.
                date = osp.basename(
                    osp.dirname(config.pretrained_model_path[0]))[-10:]
                model_ckpt = osp.basename(config.pretrained_model_path[0])
                postfix.append('from_{}_{}'.format(date, model_ckpt))

        # Data:
        # Jitter amount:
        if config.trans_max != 20 or config.delta_trans_max != 20:
            postfix.append('transmax-{}:{}'.format(config.trans_max,
                                                   config.delta_trans_max))
        if config.scale_max != 0.3 or config.delta_scale_max != 0.3:
            postfix.append('scmax-{}:{}'.format(config.scale_max,
                                                config.delta_scale_max))

        if not config.split_balanced:
            postfix.append('no-split-balance')

        if config.mosh_ignore:
            postfix.append('mosh_ignore')

        if not postfix:
            postfix.append('')

        prefix = '_'.join(prefix)
        postfix = '_'.join(postfix)

        time_str = datetime.now().strftime("%b%d_%H%M")

        save_name = "%s_%s_%s" % (prefix, postfix, time_str)
        config.model_dir = osp.join(config.log_dir, save_name)

    for path in [config.log_dir, config.model_dir]:
        if not osp.exists(path):
            print('making %s' % path)
            makedirs(path)


def save_config(config):
    param_path = osp.join(config.model_dir, "params.json")

    print("[*] MODEL dir: %s" % config.model_dir)
    print("[*] PARAM path: %s" % param_path)

    config_dict = {}
    for k in dir(config):
        config_dict[k] = config.__getattr__(k)

    with open(param_path, 'w') as fp:
        json.dump(config_dict, fp, indent=4, sort_keys=True)
