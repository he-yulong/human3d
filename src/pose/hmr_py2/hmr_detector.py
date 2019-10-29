import sys
import time

import tensorflow as tf
import numpy as np

from hmr.RunModel import RunModel
import hmr.config
from absl import flags
from hyl_utils.realsense.color_client_decorator import start_client
from hmr.util import openpose as op_util
from hmr.util import image as img_util

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


@start_client
def inference(input_img):
    # Theta is the 85D vector holding [camera, pose, shape]
    # where camera is 3D [s, tx, ty]
    # pose is 72D vector holding the rotation of 24 joints of SMPL in axis angle format
    # shape is 10D shape coefficients of SMPL
    t0 = time.time()
    input_img, proc_param, img = preprocess_frame(input_img, None)
    # Add batch dimension: 1 x D x D x 3
    input_img = np.expand_dims(input_img, 0)
    joints, verts, cams, joints3d, theta = model.predict(input_img, get_theta=True)
    t1 = time.time()
    print(joints)
    print(t1 - t0)
    print('-' * 20)


inference()
