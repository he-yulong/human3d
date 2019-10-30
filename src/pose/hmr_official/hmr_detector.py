import sys
import tensorflow as tf
from src.RunModel import RunModel
import src.config
from absl import flags


sess = tf.Session()
config = flags.FLAGS
config(sys.argv)
# Using pre-trained model, change this to use your own.
config.load_path = src.config.PRETRAINED_MODEL
config.batch_size = 2
model = RunModel(config, sess=sess)

# input_img
input_img = None

# Theta is the 85D vector holding [camera, pose, shape]
# where camera is 3D [s, tx, ty]
# pose is 72D vector holding the rotation of 24 joints of SMPL in axis angle format
# shape is 10D shape coefficients of SMPL
joints, verts, cams, joints3d, theta = model.predict(input_img, get_theta=True)



