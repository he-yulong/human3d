# Video capture
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

import time





while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
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
    # print('joints:', joints[0], joints[0].shape)
    # print('verts:', verts[0], verts[0].shape)
    # print('cams:', cams[0], cams[0].shape)
    skel_img = visualize_joints(img, proc_param, joints[0], verts[0], cams[0])
    t3 = time.time()
    cv2.imshow('render_SMPL', skel_img)

    t4 = time.time()
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break

    print(t1 - t0)
    print(t2 - t1)
    print(t3 - t2)
    print(t4 - t3)
    print('-' * 20)
