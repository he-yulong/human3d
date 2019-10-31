"""
Usage:

python demo_pc_webcam.py

Demo of HMR.

Note that HMR requires the bounding box of the person in the image. The best performance is obtained when max length of the person in the image is roughly 150px.

When only the image path is supplied, it assumes that the image is centered on a person whose length is roughly 150px.
Alternatively, you can supply output of the openpose to figure out the bbox and the right scale factor.

Sample usage:

# On images on a tightly cropped image around the person
python -m demo --img_path data/im1963.jpg
python -m demo --img_path data/coco1.png

# On images, with openpose output
python -m demo --img_path data/random.jpg --json_path data/random_keypoints.json
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
from absl import flags
import numpy as np

import skimage.io as io
import tensorflow as tf

from hmr.util import renderer as vis_util
from hmr.util import image as img_util
from hmr.util import openpose as op_util
import hmr.config
from hmr.RunModel import RunModel

flags.DEFINE_string('img_path', 'data/im1963.jpg', 'Image to run')
flags.DEFINE_string(
    'json_path', None,
    'If specified, uses the openpose output to crop the image.')


def visualize_joints(img, proc_param, joints, verts, cam):
    cam_for_render, vert_shifted, joints_orig = vis_util.get_original(
        proc_param, verts, cam, joints, img_size=img.shape[:2])
    # Render results
    # skel_img = vis_util.draw_skeleton(img, joints_orig)
    rend_img_overlay = renderer(
        vert_shifted, cam=cam_for_render, img=img, do_alpha=True)
    return rend_img_overlay


def preprocess_frame(frame, json_path=None):
    if frame.shape[2] == 4:
        frame = frame[:, :, :3]

    if json_path is None:
        if np.max(frame.shape[:2]) != config.img_size:
            print('Resizing so the max image size is %d..' % config.img_size)
            scale = (float(config.img_size) / np.max(frame.shape[:2]))
        else:
            scale = 1.
        center = np.round(np.array(frame.shape[:2]) / 2).astype(int)
        # image center in (x,y)
        center = center[::-1]
    else:
        scale, center = op_util.get_bbox(json_path)

    crop, proc_param = img_util.scale_and_crop(frame, scale, center,
                                               config.img_size)

    # Normalize image to [-1, 1]
    crop = 2 * ((crop / 255.) - 0.5)

    return crop, proc_param, frame


def main(img_path, json_path=None):
    sess = tf.Session()
    model = RunModel(config, sess=sess)

    # Video capture
    import socket
    import json
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # import argparse
    import cv2
    # parser = argparse.ArgumentParser()
    # parser.add_argument('v', 'video_path', help='file path.')
    # args = parser.parse_args()

    capture = cv2.VideoCapture('data/demo2.mov')
    # capture.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
    # capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)
    # capture.set(cv2.CAP_PROP_FPS, 0.1)

    if capture.isOpened() is False:
        print('Error openning the video')

    import time

    while capture.isOpened():

        ret, frame = capture.read()
        # time.sleep(0.1)
        if ret:
            # cv2.imshow('Original frame from the video file', frame)
            t0 = time.time()
            input_img, proc_param, img = preprocess_frame(frame, json_path)
            # Add batch dimension: 1 x D x D x 3
            input_img = np.expand_dims(input_img, 0)

            t1 = time.time()

            # Theta is the 85D vector holding [camera, pose, shape]
            # where camera is 3D [s, tx, ty]
            # pose is 72D vector holding the rotation of 24 joints of SMPL in axis angle format
            # shape is 10D shape coefficients of SMPL
            joints, verts, cams, joints3d, theta = model.predict(
                input_img, get_theta=True)
            t2 = time.time()
            client.sendto(str.encode(json.dumps(theta.tolist())), ('127.0.0.1', 8889))

            skel_img = visualize_joints(img, proc_param, joints[0], verts[0], cams[0])

            t3 = time.time()
            cv2.imshow('render_SMPL', skel_img)

            t4 = time.time()

            # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # cv2.imshow('Grayscale frame', gray_frame)
            if (cv2.waitKey(10) & 0xFF) == ord('q'):
                client.sendto(str.encode(json.dumps('#STOP#')), ('127.0.0.1', 8889))
                break

            print(t1 - t0)
            print(t2 - t1)
            print(t3 - t2)
            print(t4 - t3)
            print('-' * 20)
        else:
            client.sendto(str.encode(json.dumps('#STOP#')), ('127.0.0.1', 8889))
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    config = flags.FLAGS
    config(sys.argv)
    # Using pre-trained model, change this to use your own.
    config.load_path = hmr.config.PRETRAINED_MODEL

    config.batch_size = 1

    renderer = vis_util.SMPLRenderer(face_path=config.smpl_face_path)
    main(config.img_path, config.json_path)
