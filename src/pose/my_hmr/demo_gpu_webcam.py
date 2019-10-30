import sys
import time

import tensorflow as tf
import numpy as np

from hmr.RunModel import RunModel
from hmr.util import renderer as vis_util
import hmr.config
from absl import flags
from hmr.util import openpose as op_util
from hmr.util import image as img_util
from hyl_utils.network.color_client import start_color_client
import socket
import json
import cv2
import argparse

sess = tf.Session()

# flags.DEFINE_string('model_path', './', 'model path.')
config = flags.FLAGS
config(sys.argv)
# Using pre-trained model, change this to use your own.
config.load_path = hmr.config.PRETRAINED_MODEL
config.batch_size = 1
model = RunModel(config, sess=sess)

print('---------[model loaded.]------')


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


def visualize_joints(img, proc_param, joints, verts, cam):
    cam_for_render, vert_shifted, joints_orig = vis_util.get_original(
        proc_param, verts, cam, joints, img_size=img.shape[:2])
    # Render results
    # skel_img = vis_util.draw_skeleton(img, joints_orig)

    rend_img_overlay = renderer(
        vert_shifted, cam=cam_for_render, img=img, do_alpha=False)

    return rend_img_overlay


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    renderer = vis_util.SMPLRenderer(face_path=config.smpl_face_path)


    @start_color_client(None, '172.27.15.141', 1024)
    # @start_color_client(None, '172.27.40.106', 1024)
    def process_data(self, data):
        t0 = time.time()
        input_img, proc_param, img = preprocess_frame(data, None)
        # Add batch dimension: 1 x D x D x 3
        input_img = np.expand_dims(input_img, 0)
        print('input_img is ready. Prepared to be predicted...')
	joints, verts, cams, joints3d, theta = model.predict(input_img, get_theta=True)
        client.sendto(str.encode(json.dumps(theta.tolist())), ('172.27.15.141', 8888))
        t1 = time.time()
        if True:
            skel_img = visualize_joints(img, proc_param, joints[0], verts[0], cams[0])
            t2 = time.time()
            cv2.imshow('render_SMPL', skel_img)
        else:
            t2 = time.time()
            cv2.imshow('render_SMPL', img)
        t3 = time.time()
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            client.sendto(str.encode(json.dumps('#STOP#')), ('172.27.15.141', 8888))
            exit(0)

        # client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # print(type(proc_param), proc_param)
        # print(type(joints[0]), joints[0])
        # print(type(verts[0]), verts[0])
        # print(type(cams[0]), cams[0])
        # exit(0)
        # data = {
        #     # 'img': img.tolist(),
        #     'proc_param': proc_param.tolist(),
        #     # 'joint': joints[0].tolist(),
        #     # 'vert': verts[0].tolist(),
        #     # 'cam': cams[0].tolist(),
        # }
        # client.sendto(str.encode(json.dumps(data)), ('172.27.15.189', 4399))

        print('inference: ', t1 - t0)
        print('rendering: ', t2 - t1)
        print('imshow: ', t3 - t2)

        print('-' * 20)


    process_data()
