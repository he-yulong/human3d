"""

"""
import sys

sys.path.append('/Users/mac/.virtualenvs/py2_work/lib/python2.7/site-packages')
import maya.cmds as cmds
import numpy as np
import cv2
from scipy.spatial.transform import Rotation

import socket
import json

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 8889))

"""TODO
cam_s = cam[0]
cam_pos = cam[1:]
flength = 500.
tz = flength / (0.5 * img_size * cam_s)
trans = np.hstack([cam_pos, tz])
"""


def rectify_pose(pose):
    """
    Rectify "upside down" people in global coord

    Args:
        pose (72,): Pose.

    Returns:
        Rotated pose.
    """
    pose = pose.copy()
    R_mod = cv2.Rodrigues(np.array([np.pi, 0, 0]))[0]
    R_root = cv2.Rodrigues(pose[:3])[0]
    new_root = R_root.dot(R_mod)
    pose[:3] = cv2.Rodrigues(new_root)[0].reshape(3)
    return pose


j_names = {0: 'Pelvis', 1: 'L_Hip', 2: 'R_Hip', 3: 'Spine1', 4: 'L_Knee',
           5: 'R_Knee', 6: 'Spine2', 7: 'L_Ankle', 8: 'R_Ankle', 9: 'Spine3',
           10: 'L_Foot', 11: 'R_Foot', 12: 'Neck', 13: 'L_Collar', 14: 'R_Collar',
           15: 'Head', 16: 'L_Shoulder', 17: 'R_Shoulder', 18: 'L_Elbow', 19: 'R_Elbow',
           20: 'L_Wrist', 21: 'R_Wrist', 22: 'L_Hand', 23: 'R_Hand', }

import time

frame_id = 0
while True:
    data = server.recv(1024*2)
    data2 = json.loads(data.decode())
    if data == '#STOP#' or frame_id >= 10000:
        break

    # if frame_id % 2 != 0:
    #     frame_id += 1
    #     continue

    t0 = time.time()
    theta = np.array(data2)

    # camera = theta[:3]
    # print theta.shape
    # betas = theta[0, 75:]
    # idx2 = 0
    # print 'theta:' + str(theta)
    # print 'beta:' + str(betas)
    # for value in betas:
    #     kk = 'm_avg_blendshapes.Shape%03d' % idx2
    #     cmds.setAttr(kk, value)
    #     cmds.setKeyframe(kk)
    #     idx2 += 1

    # This is the 1 x 72 pose vector of SMPL, which is the rotation of 24 joints in axis angle format
    pose = theta[:, 3:75]
    pose[0, :] = rectify_pose(pose[0, :])
    rotations = [cv2.Rodrigues(aa)[0] for aa in pose.reshape(-1, 3)]

    cmds.currentTime(frame_id)
    for idx, item in enumerate(rotations):
        x, y, z = Rotation.from_dcm(item).as_euler('xyz', degrees=True)
        key = 'm_avg_' + j_names[idx]
        cmds.setAttr('{}.rx'.format(key), x)
        cmds.setAttr('{}.ry'.format(key), y)
        cmds.setAttr('{}.rz'.format(key), z)
        cmds.setKeyframe('{}.rx'.format(key))
        cmds.setKeyframe('{}.ry'.format(key))
        cmds.setKeyframe('{}.rz'.format(key))

    print 'frame_id' + str(frame_id)
    frame_id += 1
    t1 = time.time()
    print('t1: ', t1 - t0)
    print('-' * 20)
