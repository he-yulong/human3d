"""
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

from src.util import renderer as vis_util
from src.util import image as img_util
from src.util import openpose as op_util
import src.config
from src.RunModel import RunModel

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


# def visualize(img, proc_param, joints, verts, cam):
#     """
#     Renders the result in original image coordinate frame.
#     """
#     cam_for_render, vert_shifted, joints_orig = vis_util.get_original(
#         proc_param, verts, cam, joints, img_size=img.shape[:2])
#
#     # Render results
#     skel_img = vis_util.draw_skeleton(img, joints_orig)
#     rend_img_overlay = renderer(
#         vert_shifted, cam=cam_for_render, img=img, do_alpha=True)
#     rend_img = renderer(
#         vert_shifted, cam=cam_for_render, img_size=img.shape[:2])
#     rend_img_vp1 = renderer.rotated(
#         vert_shifted, 60, cam=cam_for_render, img_size=img.shape[:2])
#     rend_img_vp2 = renderer.rotated(
#         vert_shifted, -60, cam=cam_for_render, img_size=img.shape[:2])
#
#     import matplotlib.pyplot as plt
#     # plt.ion()
#     plt.figure(1)
#     plt.clf()
#     plt.subplot(231)
#     plt.imshow(img)
#     plt.title('input')
#     plt.axis('off')
#     plt.subplot(232)
#     plt.imshow(skel_img)
#     plt.title('joint projection')
#     plt.axis('off')
#     plt.subplot(233)
#     plt.imshow(rend_img_overlay)
#     plt.title('3D Mesh overlay')
#     plt.axis('off')
#     plt.subplot(234)
#     plt.imshow(rend_img)
#     plt.title('3D mesh')
#     plt.axis('off')
#     plt.subplot(235)
#     plt.imshow(rend_img_vp1)
#     plt.title('diff vp')
#     plt.axis('off')
#     plt.subplot(236)
#     plt.imshow(rend_img_vp2)
#     plt.title('diff vp')
#     plt.axis('off')
#     plt.draw()
#     plt.show()
#     # import ipdb
#     # ipdb.set_trace()


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
    import cv2
    import socket
    import json
    cap = cv2.VideoCapture(0)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    import time
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        t0 = time.time()
        input_img, proc_param, img = preprocess_frame(frame, json_path)
        # Add batch dimension: 1 x D x D x 3
        input_img = np.expand_dims(input_img, 0)
        print(input_img.shape)

        t1 = time.time()

        # Theta is the 85D vector holding [camera, pose, shape]
        # where camera is 3D [s, tx, ty]
        # pose is 72D vector holding the rotation of 24 joints of SMPL in axis angle format
        # shape is 10D shape coefficients of SMPL
        joints, verts, cams, joints3d, theta = model.predict(
            input_img, get_theta=True)
        t2 = time.time()
        # print('joints:', joints, joints.shape)
        # print('joints3d:', joints3d, joints3d.shape)
        # print('theta:', theta, theta.shape)
        # print('verts:', verts[0], verts[0].shape)
        # print('cams:', cams[0], cams[0].shape)

        client.sendto(str.encode(json.dumps(theta.tolist())), ('127.0.0.1', 8888))

        skel_img = visualize_joints(img, proc_param, joints[0], verts[0], cams[0])

        t3 = time.time()
        cv2.imshow('render_SMPL', skel_img)

        t4 = time.time()
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            client.sendto(str.encode(json.dumps('#STOP#')), ('127.0.0.1', 8888))
            break

        print(t1 - t0)
        print(t2 - t1)
        print(t3 - t2)
        print(t4 - t3)
        print('-' * 20)


if __name__ == '__main__':
    config = flags.FLAGS
    config(sys.argv)
    # Using pre-trained model, change this to use your own.
    config.load_path = src.config.PRETRAINED_MODEL

    config.batch_size = 1

    renderer = vis_util.SMPLRenderer(face_path=config.smpl_face_path)
    main(config.img_path, config.json_path)
