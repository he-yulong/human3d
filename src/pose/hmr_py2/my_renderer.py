from hyl_utils.network.udp_decorator import process_udp_server
import time
import cv2
from hmr.util import renderer as vis_util
import hmr.config
from absl import flags
import sys


def visualize_joints(img, proc_param, joints, verts, cam):
    cam_for_render, vert_shifted, joints_orig = vis_util.get_original(
        proc_param, verts, cam, joints, img_size=img.shape[:2])
    # Render results
    # skel_img = vis_util.draw_skeleton(img, joints_orig)

    rend_img_overlay = renderer(
        vert_shifted, cam=cam_for_render, img=img, do_alpha=False)

    return rend_img_overlay


if __name__ == '__main__':
    config = flags.FLAGS
    config(sys.argv)
    # Using pre-trained model, change this to use your own.
    config.load_path = hmr.config.PRETRAINED_MODEL
    renderer = vis_util.SMPLRenderer(face_path=config.smpl_face_path)


    @process_udp_server('0.0.0.0', 4399, 1024 * 1024)
    def multiply(x):
        img, proc_param, joint, vert, cam = x
        t1 = time.time()
        skel_img = visualize_joints(img, proc_param, joint, vert, cam)
        t2 = time.time()
        cv2.imshow('render_SMPL', skel_img)
        t3 = time.time()
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            exit(0)


    multiply()
