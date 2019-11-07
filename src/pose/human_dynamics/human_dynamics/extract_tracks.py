"""
Given a directory of videos, extracts 2D pose tracklet using AlphaPose/PoseFlow
for each video.

Make sure you have installed AlphaPose pytorch in src/external.

This script is basically a wrapper around AlphaPose/PoseFlow:
1. Split the video into individual frames since PoseFlow requires that format
2. Run AlphaPose on the produced directory with frames
3. Run PoseFlow on the AlphaPose output.

Therefore, if at any point this script fails, please look into each system cmd
that's printed prior to running them. Make sure you can run those commands on
their own.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
from glob import glob
import os
import subprocess

from human_dynamics.util.common import mkdir


def dump_frames(vid_path, out_dir):
    """
    Extracts all frames from the video at vid_path and saves them inside of
    out_dir.
    """
    print('---Starting to dump frames to {}.---'.format(out_dir))
    if len(glob(os.path.join(out_dir, '*.png'))) > 0:
        print('Writing frames to file: done!')
        return

    print('{} Writing frames to file'.format(vid_path))

    cmd = [
        'ffmpeg',
        '-i', vid_path,
        '-start_number', '0',
        '{temp_dir}/frame%08d.png'.format(temp_dir=out_dir),
    ]
    print(' '.join(cmd))
    subprocess.call(cmd)
    print('---Ending to dump frames to {}.---'.format(out_dir))


def run_alphapose(img_dir, out_dir):
    if os.path.exists(os.path.join(out_dir, 'alphapose-results.json')):
        print('Per-frame detection: already done.')
        return

    print('----------')
    print('Computing per-frame results with AlphaPose')

    # Ex:
    # python3 demo.py --indir demo_data/43139284_2266542610046186_3116128039555373672_n --outdir demo_data/43139284_2266542610046186_3116128039555373672_n/output --sp
    cmd = [
        'python', 'demo.py',
        '--indir', img_dir,
        '--outdir', out_dir,
        '--sp',  # Needed to avoid multi-processing issues.
    ]

    print('Running: {}'.format(' '.join(cmd)))
    curr_dir = os.getcwd()
    os.chdir('src/external/AlphaPose')
    ret = subprocess.call(cmd)
    if ret != 0:
        print('Issue running alphapose. Please make sure you can run the above '
              'command from the commandline.')
        exit(ret)
    os.chdir(curr_dir)
    print('AlphaPose successfully ran!')
    print('----------')


def run_poseflow(img_dir, out_dir):
    alphapose_json = os.path.join(out_dir, 'alphapose-results.json')
    out_json = os.path.join(out_dir, 'alphapose-results-forvis-tracked.json')
    if os.path.exists(out_json):
        print('Tracking: done!')
        return out_json

    print('Computing tracking with PoseFlow')

    # Ex:
    # python PoseFlow/tracker-general.py --imgdir demo_data/43139284_2266542610046186_3116128039555373672_n --in_json demo_data/43139284_2266542610046186_3116128039555373672_n/output/alphapose-results.json --out_json demo_data/43139284_2266542610046186_3116128039555373672_n/output/alphapose-results-forvis-tracked.json --visdir demo_data/43139284_2266542610046186_3116128039555373672_n/output/
    cmd = [
        'python', 'PoseFlow/tracker-general.py',
        '--imgdir', img_dir,
        '--in_json', alphapose_json,
        '--out_json', out_json,
        # '--visdir', out_dir,  # Uncomment this to visualize PoseFlow tracks.
    ]

    print('Running: {}'.format(' '.join(cmd)))
    curr_dir = os.getcwd()
    os.chdir('src/external/AlphaPose')
    ret = subprocess.call(cmd)
    if ret != 0:
        print('Issue running PoseFlow. Please make sure you can run the above '
              'command from the commandline.')
        exit(ret)
    os.chdir(curr_dir)
    print('PoseFlow successfully ran!')
    print('----------')

    return out_json


def compute_tracks(vid_path, out_dir):
    """
    This script basically:
    1. Extracts individual frames from mp4 since PoseFlow requires per frame
       images to be written.
    2. Call AlphaPose on these frames.
    3. Call PoseFlow on the output of 2.
    """
    # To get the first base name splitted by `.`
    # ex:
    # /root/hello.txt.npz -> hello
    vid_name = os.path.basename(vid_path).split('.')[0]

    # Where to save all intermediate outputs in.
    # vid_dir = 'out_dir/vid_base_name'
    # img_dir = 'out_dir/vid_base_name/video_frames'
    # res_dir = 'out_dir/vid_base_name/AlphaPose_output'
    vid_dir = os.path.abspath(os.path.join(out_dir, vid_name))
    img_dir = os.path.abspath(os.path.join(vid_dir, 'video_frames'))
    res_dir = os.path.abspath(os.path.join(vid_dir, 'AlphaPose_output'))

    mkdir(img_dir)
    mkdir(res_dir)

    dump_frames(vid_path, img_dir)

    run_alphapose(img_dir, res_dir)

    exit(0)
    track_json = run_poseflow(img_dir, res_dir)
    return track_json, img_dir


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--vid_dir',
        default='demo_data/',
        help='Directory with demo_data.'
    )
    parser.add_argument(
        '--track_dir',
        default='demo_data/output',
        help='Where to save intermediate tracking results.'
    )
    opts = parser.parse_args()
    # Make output directory.
    mkdir(opts.track_dir)

    # For each video in output directory
    vid_paths = sorted(glob(opts.vid_dir + '/*.mp4'))

    for vid_path in vid_paths:
        compute_tracks(vid_path, opts.track_dir)
