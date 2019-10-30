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
server.bind(('0.0.0.0', 8888))

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

# theta = np.array([[0.65375429, -0.12651032, 0.69847161, 1.20795631, -0.68683738, 3.06554484,
#                    -0.2044993, 0.05865749, 0.31660637, -0.33618885, -0.312289, -0.3469328,
#                    0.35565928, 0.06655198, -0.02633067, 0.60488713, -0.21113533, -0.17966062,
#                    0.66467255, -0.12848833, 0.13370527, 0.13724093, -0.07187334, -0.0362551,
#                    -0.16843867, -0.09506486, -0.03108483, -0.14844014, -0.20193914, 0.18179893,
#                    -0.11232163, -0.01554313, -0.0188742, -0.19961238, 0.36859128, -0.07566048,
#                    -0.0170522, -0.04483943, -0.14284033, 0.03346763, -0.07012553, -0.09445562,
#                    -0.1719825, -0.46976602, -0.11803561, -0.11201438, 0.51989555, 0.03870144,
#                    -0.20713428, -0.13355994, 0.06921966, -0.19867136, -0.42817655, -0.37556809,
#                    -0.29381952, 0.56291795, 0.33206582, -0.08018727, -1.6725651, 1.09471381,
#                    0.30702329, 1.81851137, -1.26697814, 0.06094411, -0.16671088, 0.37845773,
#                    1.04654193, 0.04094768, -0.63187224, -0.07983252, -0.08654476, -0.12918299,
#                    0.01232874, 0.29337054, 0.26530373, -1.14819586, 0.94468343, 0.6564284,
#                    0.7488265, -1.15599048, 1.71598029, -0.47796577, -0.10777956, 0.06191299,
#                    1.85676169]])
import time
frame_id = 0
while True:

    data = server.recv(1024 * 2)
    data = json.loads(data.decode())
    if data == '#STOP#' or frame_id >= 50:
        break
    frame_id += 1
    print 'frame_id' + str(frame_id)
    t0 = time.time()
    theta = np.array(data)
    # camera = theta[:3]
    # betas = theta[75:]
    # real_theta = theta[3:75]
    pose = theta[:, 3:75]  # This is the 1 x 72 pose vector of SMPL, which is the rotation of 24 joints in axis angle format
    pose[0, :] = rectify_pose(pose[0, :])
    t1 = time.time()
    rotations = [cv2.Rodrigues(aa)[0] for aa in pose.reshape(-1, 3)]
    t2 = time.time()
    cmds.currentTime(0)
    for idx, item in enumerate(rotations):
        x, y, z = Rotation.from_dcm(item).as_euler('xyz', degrees=True)
        # print (x, y, z)
        key = 'm_avg_' + j_names[idx]
        cmds.setAttr('{}.rx'.format(key), x)
        cmds.setKeyframe('{}.rx'.format(key))
        cmds.setAttr('{}.ry'.format(key), y)
        cmds.setKeyframe('{}.ry'.format(key))
        cmds.setAttr('{}.rz'.format(key), z)
        cmds.setKeyframe('{}.rz'.format(key))
    t3 = time.time()
    print('t1: ', t1 - t0)
    print('t2: ', t2 - t1)
    print('t3: ', t3 - t2)
    print('-' * 20)
    # print rotations

    # for i in range(10):
    #     cmds.currentTime(i)
    #     cmds.setAttr('m_avg_root.rx', i * 10, )
    #     cmds.setKeyframe('m_avg_root.rx')
