"""
Runs hmmr on a video.
Extracts tracks using AlphaPose/PoseFlow

Sample Usage:
python -m demo_video --out_dir demo_data/output
python -m demo_video --out_dir demo_data/output270k --load_path models/hmmr_model.ckpt-2699068
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from glob import glob
import json
import os.path
import pickle
import re

import time
import numpy as np

from extract_tracks import compute_tracks
from human_dynamics.config import get_config
from human_dynamics.evaluation.run_video import process_image, render_preds
from human_dynamics.evaluation.tester import Tester
from human_dynamics.util.common import mkdir
from human_dynamics.util.smooth_bbox import get_smooth_bbox_params


def get_labels_poseflow(json_path, num_frames, min_kp_count=20):
    """
    Returns the poses for each person tracklet.

    Each pose has dimension num_kp x 3 (x,y,vis) if the person is visible in the
    current frame. Otherwise, the pose will be None.

    Args:
        json_path (str): Path to the json output from AlphaPose/PoseTrack.
        num_frames (int): Number of frames.
        min_kp_count (int): Minimum threshold length for a tracklet.

    Returns:
        List of length num_people. Each element in the list is another list of
        length num_frames containing the poses for each person.
    """
    with open(json_path, 'r') as f:
        data = json.load(f)
    if len(data.keys()) != num_frames:
        print('Not all frames have people detected in it.')
        frame_ids = [int(re.findall(r'\d+', img_name)[0])
                     for img_name in sorted(data.keys())]
        if frame_ids[0] != 0:
            print('PoseFlow did not find people in the first frame. '
                  'Needs testing.')

    all_kps_dict = {}
    all_kps_count = {}
    for i, key in enumerate(sorted(data.keys())):
        # People who are visible in this frame.
        track_ids = []
        for person in data[key]:
            kps = np.array(person['keypoints']).reshape(-1, 3)
            idx = int(person['idx'])
            if idx not in all_kps_dict.keys():
                # If this is the first time, fill up until now with None
                all_kps_dict[idx] = [None] * i
                all_kps_count[idx] = 0
            # Save these kps.
            all_kps_dict[idx].append(kps)
            track_ids.append(idx)
            all_kps_count[idx] += 1
        # If any person seen in the past is missing in this frame, add None.
        for idx in set(all_kps_dict.keys()).difference(track_ids):
            all_kps_dict[idx].append(None)

    all_kps_list = []
    all_counts_list = []
    for k in all_kps_dict:
        if all_kps_count[k] >= min_kp_count:
            all_kps_list.append(all_kps_dict[k])
            all_counts_list.append(all_kps_count[k])

    # Sort it by the length so longest is first:
    sort_idx = np.argsort(all_counts_list)[::-1]
    all_kps_list_sorted = []
    for sort_id in sort_idx:
        all_kps_list_sorted.append(all_kps_list[sort_id])

    return all_kps_list_sorted


def predict_on_tracks(model, img_dir, poseflow_path, output_path, track_id,
                      trim_length):
    # Get all the images
    im_paths = sorted(glob(os.path.join(img_dir, '*.png')))
    all_kps = get_labels_poseflow(poseflow_path, len(im_paths))

    # Here we set which track to use.
    track_id = min(track_id, len(all_kps) - 1)
    print('Total number of PoseFlow tracks:', len(all_kps))
    print('Processing track_id:', track_id)
    kps = all_kps[track_id]

    bbox_params_smooth, s, e = get_smooth_bbox_params(kps, vis_thresh=0.1)

    images = []
    images_orig = []
    min_f = max(s, 0)
    max_f = min(e, len(kps))

    print('----------')
    print('Preprocessing frames.')
    print('----------')

    for i in range(min_f, max_f):
        proc_params = process_image(
            im_path=im_paths[i],
            bbox_param=bbox_params_smooth[i],
        )
        images.append(proc_params.pop('image'))
        images_orig.append(proc_params)

    if track_id > 0:
        output_path += '_{}'.format(track_id)

    mkdir(output_path)
    pred_path = os.path.join(output_path, 'hmmr_output.pkl')
    if os.path.exists(pred_path):
        print('----------')
        print('Loading pre-computed prediction.')
        print('----------')

        with open(pred_path, 'rb') as f:
            preds = pickle.load(f)
    else:
        print('----------')
        print('Running prediction.')
        print('----------')

        preds = model.predict_all_images(images)

        with open(pred_path, 'wb') as f:
            print('Saving prediction results to', pred_path)
            pickle.dump(preds, f)

    if trim_length > 0:
        output_path += '_trim'

    print('----------')
    print('Rendering results to {}.'.format(output_path))
    print('----------')
    render_preds(
        output_path=output_path,
        config=config,
        preds=preds,
        images=images,
        images_orig=images_orig,
        trim_length=trim_length,
    )


def run_on_video(model, vid_path, trim_length):
    """
    Main driver.
    First extracts alphapose/posetrack in track_dir
    Then runs HMMR.
    """
    print('----------')
    print('Computing tracks on {}.'.format(vid_path))
    print('----------')
    t0 = time.time()

    # See extract_tracks.py
    poseflow_path, img_dir = compute_tracks(vid_path, config.track_dir)

    vid_name = os.path.basename(vid_path).split('.')[0]
    out_dir = os.path.join(config.out_dir, vid_name, 'hmmr_output')

    print(poseflow_path, img_dir, out_dir)
    print(time.time() - t0)
    exit(0)

    predict_on_tracks(
        model=model,
        img_dir=img_dir,
        poseflow_path=poseflow_path,
        output_path=out_dir,
        track_id=config.track_id,
        trim_length=trim_length
    )


if __name__ == '__main__':
    import argparse

    # Demo basic argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--vid_path', default='penn_action-2278.mp4', help='video to run on.')
    parser.add_argument('--track_id',
                        type=int,
                        default=0,
                        help='PoseFlow generates a track for each detected person. This determines which '
                             'track index to use if using vid_path.'
                        )
    parser.add_argument('--vid_dir', default=None, help='If set, runs on all video in directory.')
    parser.add_argument('--out_dir', default='demo_output/', help='Where to save final HMMR results.')

    parser.add_argument('--track_dir', default='demo_output/', help='Where to save intermediate tracking results.')
    parser.add_argument('--pred_mode', default='pred', help='Which prediction track to use (Only pred supported now).')
    parser.add_argument('--mesh_color', default='blue', help='Color of mesh.')
    parser.add_argument('--sequence_length', type=int, default=20,
                        help='Length of sequence during prediction. Larger will be faster for longer '
                             'videos but use more memory.'
                        )
    parser.add_argument('--trim', type=bool, default=False,
                        help='If True, trims the first and last couple of frames for which the temporal'
                             'encoder doesn\'t see full fov.'
                        )

    config = get_config(parser)

    # Set up model:
    model_hmmr = Tester(config, pretrained_resnet_path='models/hmr_noS5.ckpt-642561')

    # Make output directory.
    mkdir(config.out_dir)

    trim_length = model_hmmr.fov // 2 if config.trim else 0

    if config.vid_dir:
        vid_paths = sorted(glob(config.vid_dir + '/*.mp4'))
        for vid_path in vid_paths:
            run_on_video(model_hmmr, vid_path, trim_length)
    else:
        run_on_video(model_hmmr, config.vid_path, trim_length)
