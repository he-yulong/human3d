"""
Recording the realsense data
Usage:
python recorder.py

test: .ovB4c=En*0r

Stream Profiles supported by Stereo Module
Supported modes:
stream resolution fps format
Depth	1280x720	@ 6Hz	Z16
Depth	640x480	    @ 30Hz	Z16
Depth	640x480	    @ 15Hz	Z16
Depth	640x480	    @ 6Hz	Z16
Depth	480x270	    @ 60Hz	Z16
Depth	480x270	    @ 30Hz	Z16
Depth	480x270	    @ 15Hz	Z16
Depth	480x270	    @ 6Hz	Z16
Depth	256x144	    @ 90Hz	Z16

Depth	  1280x720	@ 30Hz	   Z16
    Depth	  1280x720	@ 15Hz	   Z16
    Depth	  1280x720	@ 6Hz	   Z16
    Depth	  848x480	@ 90Hz	   Z16
    Depth	  848x480	@ 60Hz	   Z16
    Depth	  848x480	@ 30Hz	   Z16
    Depth	  848x480	@ 15Hz	   Z16
    Depth	  848x480	@ 6Hz	   Z16
    Depth	  848x100	@ 100Hz	   Z16
    Depth	  640x480	@ 90Hz	   Z16
    Depth	  640x480	@ 60Hz	   Z16
    Depth	  640x480	@ 30Hz	   Z16
    Depth	  640x480	@ 15Hz	   Z16
    Depth	  640x480	@ 6Hz	   Z16
    Depth	  640x360	@ 90Hz	   Z16
    Depth	  640x360	@ 60Hz	   Z16
    Depth	  640x360	@ 30Hz	   Z16
    Depth	  640x360	@ 15Hz	   Z16
    Depth	  640x360	@ 6Hz	   Z16
    Depth	  480x270	@ 90Hz	   Z16
    Depth	  480x270	@ 60Hz	   Z16
    Depth	  480x270	@ 30Hz	   Z16
    Depth	  480x270	@ 15Hz	   Z16
    Depth	  480x270	@ 6Hz	   Z16
    Depth	  424x240	@ 90Hz	   Z16
    Depth	  424x240	@ 60Hz	   Z16
    Depth	  424x240	@ 30Hz	   Z16
    Depth	  424x240	@ 15Hz	   Z16
    Depth	  424x240	@ 6Hz	   Z16

Stream Profiles supported by RGB Camera
 Supported modes:
    stream       resolution      fps       format
    Color	  1920x1080	@ 30Hz	   RGB8
    Color	  1920x1080	@ 30Hz	   RAW16
    Color	  1920x1080	@ 30Hz	   Y16
    Color	  1920x1080	@ 30Hz	   BGRA8
    Color	  1920x1080	@ 30Hz	   RGBA8
    Color	  1920x1080	@ 30Hz	   BGR8
    Color	  1920x1080	@ 30Hz	   YUYV
    Color	  1920x1080	@ 15Hz	   RGB8
    Color	  1920x1080	@ 15Hz	   Y16
    Color	  1920x1080	@ 15Hz	   BGRA8
    Color	  1920x1080	@ 15Hz	   RGBA8
    Color	  1920x1080	@ 15Hz	   BGR8
    Color	  1920x1080	@ 15Hz	   YUYV
    Color	  1920x1080	@ 6Hz	   RGB8
    Color	  1920x1080	@ 6Hz	   Y16
    Color	  1920x1080	@ 6Hz	   BGRA8
    Color	  1920x1080	@ 6Hz	   RGBA8
    Color	  1920x1080	@ 6Hz	   BGR8
    Color	  1920x1080	@ 6Hz	   YUYV
    Color	  1280x720	@ 30Hz	   RGB8
    Color	  1280x720	@ 30Hz	   Y16
    Color	  1280x720	@ 30Hz	   BGRA8
    Color	  1280x720	@ 30Hz	   RGBA8
    Color	  1280x720	@ 30Hz	   BGR8
    Color	  1280x720	@ 30Hz	   YUYV
    Color	  1280x720	@ 15Hz	   RGB8
    Color	  1280x720	@ 15Hz	   Y16
    Color	  1280x720	@ 15Hz	   BGRA8
    Color	  1280x720	@ 15Hz	   RGBA8
    Color	  1280x720	@ 15Hz	   BGR8
    Color	  1280x720	@ 15Hz	   YUYV
    Color	  1280x720	@ 6Hz	   RGB8
    Color	  1280x720	@ 6Hz	   Y16
    Color	  1280x720	@ 6Hz	   BGRA8
    Color	  1280x720	@ 6Hz	   RGBA8
    Color	  1280x720	@ 6Hz	   BGR8
    Color	  1280x720	@ 6Hz	   YUYV
    Color	  960x540	@ 60Hz	   RGB8
    Color	  960x540	@ 60Hz	   Y16
    Color	  960x540	@ 60Hz	   BGRA8
    Color	  960x540	@ 60Hz	   RGBA8
    Color	  960x540	@ 60Hz	   BGR8
    Color	  960x540	@ 60Hz	   YUYV
    Color	  960x540	@ 30Hz	   RGB8
    Color	  960x540	@ 30Hz	   Y16
    Color	  960x540	@ 30Hz	   BGRA8
    Color	  960x540	@ 30Hz	   RGBA8
    Color	  960x540	@ 30Hz	   BGR8
    Color	  960x540	@ 30Hz	   YUYV
    Color	  960x540	@ 15Hz	   RGB8
    Color	  960x540	@ 15Hz	   Y16
    Color	  960x540	@ 15Hz	   BGRA8
    Color	  960x540	@ 15Hz	   RGBA8
    Color	  960x540	@ 15Hz	   BGR8
    Color	  960x540	@ 15Hz	   YUYV
    Color	  960x540	@ 6Hz	   RGB8
    Color	  960x540	@ 6Hz	   Y16
    Color	  960x540	@ 6Hz	   BGRA8
    Color	  960x540	@ 6Hz	   RGBA8
    Color	  960x540	@ 6Hz	   BGR8
    Color	  960x540	@ 6Hz	   YUYV
    Color	  848x480	@ 60Hz	   RGB8
    Color	  848x480	@ 60Hz	   Y16
    Color	  848x480	@ 60Hz	   BGRA8
    Color	  848x480	@ 60Hz	   RGBA8
    Color	  848x480	@ 60Hz	   BGR8
    Color	  848x480	@ 60Hz	   YUYV
    Color	  848x480	@ 30Hz	   RGB8
    Color	  848x480	@ 30Hz	   Y16
    Color	  848x480	@ 30Hz	   BGRA8
    Color	  848x480	@ 30Hz	   RGBA8
    Color	  848x480	@ 30Hz	   BGR8
    Color	  848x480	@ 30Hz	   YUYV
    Color	  848x480	@ 15Hz	   RGB8
    Color	  848x480	@ 15Hz	   Y16
    Color	  848x480	@ 15Hz	   BGRA8
    Color	  848x480	@ 15Hz	   RGBA8
    Color	  848x480	@ 15Hz	   BGR8
    Color	  848x480	@ 15Hz	   YUYV
    Color	  848x480	@ 6Hz	   RGB8
    Color	  848x480	@ 6Hz	   Y16
    Color	  848x480	@ 6Hz	   BGRA8
    Color	  848x480	@ 6Hz	   RGBA8
    Color	  848x480	@ 6Hz	   BGR8
    Color	  848x480	@ 6Hz	   YUYV
    Color	  640x480	@ 60Hz	   RGB8
    Color	  640x480	@ 60Hz	   Y16
    Color	  640x480	@ 60Hz	   BGRA8
    Color	  640x480	@ 60Hz	   RGBA8
    Color	  640x480	@ 60Hz	   BGR8
    Color	  640x480	@ 60Hz	   YUYV
    Color	  640x480	@ 30Hz	   RGB8
    Color	  640x480	@ 30Hz	   Y16
    Color	  640x480	@ 30Hz	   BGRA8
    Color	  640x480	@ 30Hz	   RGBA8
    Color	  640x480	@ 30Hz	   BGR8
    Color	  640x480	@ 30Hz	   YUYV
    Color	  640x480	@ 15Hz	   RGB8
    Color	  640x480	@ 15Hz	   Y16
    Color	  640x480	@ 15Hz	   BGRA8
    Color	  640x480	@ 15Hz	   RGBA8
    Color	  640x480	@ 15Hz	   BGR8
    Color	  640x480	@ 15Hz	   YUYV
    Color	  640x480	@ 6Hz	   RGB8
    Color	  640x480	@ 6Hz	   Y16
    Color	  640x480	@ 6Hz	   BGRA8
    Color	  640x480	@ 6Hz	   RGBA8
    Color	  640x480	@ 6Hz	   BGR8
    Color	  640x480	@ 6Hz	   YUYV
    Color	  640x360	@ 60Hz	   RGB8
    Color	  640x360	@ 60Hz	   Y16
    Color	  640x360	@ 60Hz	   BGRA8
    Color	  640x360	@ 60Hz	   RGBA8
    Color	  640x360	@ 60Hz	   BGR8
    Color	  640x360	@ 60Hz	   YUYV
    Color	  640x360	@ 30Hz	   RGB8
    Color	  640x360	@ 30Hz	   Y16
    Color	  640x360	@ 30Hz	   BGRA8
    Color	  640x360	@ 30Hz	   RGBA8
    Color	  640x360	@ 30Hz	   BGR8
    Color	  640x360	@ 30Hz	   YUYV
    Color	  640x360	@ 15Hz	   RGB8
    Color	  640x360	@ 15Hz	   Y16
    Color	  640x360	@ 15Hz	   BGRA8
    Color	  640x360	@ 15Hz	   RGBA8
    Color	  640x360	@ 15Hz	   BGR8
    Color	  640x360	@ 15Hz	   YUYV
    Color	  640x360	@ 6Hz	   RGB8
    Color	  640x360	@ 6Hz	   Y16
    Color	  640x360	@ 6Hz	   BGRA8
    Color	  640x360	@ 6Hz	   RGBA8
    Color	  640x360	@ 6Hz	   BGR8
    Color	  640x360	@ 6Hz	   YUYV
    Color	  424x240	@ 60Hz	   RGB8
    Color	  424x240	@ 60Hz	   Y16
    Color	  424x240	@ 60Hz	   BGRA8
    Color	  424x240	@ 60Hz	   RGBA8
    Color	  424x240	@ 60Hz	   BGR8
    Color	  424x240	@ 60Hz	   YUYV
    Color	  424x240	@ 30Hz	   RGB8
    Color	  424x240	@ 30Hz	   Y16
    Color	  424x240	@ 30Hz	   BGRA8
    Color	  424x240	@ 30Hz	   RGBA8
    Color	  424x240	@ 30Hz	   BGR8
    Color	  424x240	@ 30Hz	   YUYV
    Color	  424x240	@ 15Hz	   RGB8
    Color	  424x240	@ 15Hz	   Y16
    Color	  424x240	@ 15Hz	   BGRA8
    Color	  424x240	@ 15Hz	   RGBA8
    Color	  424x240	@ 15Hz	   BGR8
    Color	  424x240	@ 15Hz	   YUYV
    Color	  424x240	@ 6Hz	   RGB8
    Color	  424x240	@ 6Hz	   Y16
    Color	  424x240	@ 6Hz	   BGRA8
    Color	  424x240	@ 6Hz	   RGBA8
    Color	  424x240	@ 6Hz	   BGR8
    Color	  424x240	@ 6Hz	   YUYV
    Color	  320x240	@ 60Hz	   RGB8
    Color	  320x240	@ 60Hz	   Y16
    Color	  320x240	@ 60Hz	   BGRA8
    Color	  320x240	@ 60Hz	   RGBA8
    Color	  320x240	@ 60Hz	   BGR8
    Color	  320x240	@ 60Hz	   YUYV
    Color	  320x240	@ 30Hz	   RGB8
    Color	  320x240	@ 30Hz	   Y16
    Color	  320x240	@ 30Hz	   BGRA8
    Color	  320x240	@ 30Hz	   RGBA8
    Color	  320x240	@ 30Hz	   BGR8
    Color	  320x240	@ 30Hz	   YUYV
    Color	  320x240	@ 6Hz	   RGB8
    Color	  320x240	@ 6Hz	   Y16
    Color	  320x240	@ 6Hz	   BGRA8
    Color	  320x240	@ 6Hz	   RGBA8
    Color	  320x240	@ 6Hz	   BGR8
    Color	  320x240	@ 6Hz	   YUYV
    Color	  320x180	@ 60Hz	   RGB8
    Color	  320x180	@ 60Hz	   Y16
    Color	  320x180	@ 60Hz	   BGRA8
    Color	  320x180	@ 60Hz	   RGBA8
    Color	  320x180	@ 60Hz	   BGR8
    Color	  320x180	@ 60Hz	   YUYV
    Color	  320x180	@ 30Hz	   RGB8
    Color	  320x180	@ 30Hz	   Y16
    Color	  320x180	@ 30Hz	   BGRA8
    Color	  320x180	@ 30Hz	   RGBA8
    Color	  320x180	@ 30Hz	   BGR8
    Color	  320x180	@ 30Hz	   YUYV
    Color	  320x180	@ 6Hz	   RGB8
    Color	  320x180	@ 6Hz	   Y16
    Color	  320x180	@ 6Hz	   BGRA8
    Color	  320x180	@ 6Hz	   RGBA8
    Color	  320x180	@ 6Hz	   BGR8
    Color	  320x180	@ 6Hz	   YUYV
————————————————
版权声明：本文为CSDN博主「古路」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/fb_941219/article/details/102534405
inference:
https://blog.csdn.net/NiYintang/article/details/86116591
https://github.com/IntelRealSense/librealsense/issues/3537
https://github.com/IntelRealSense/librealsense/issues/4962
http://docs.ros.org/kinetic/api/diagnostic_msgs/html/msg/DiagnosticStatus.html
http://wiki.ros.org/diagnostics/Tutorials
https://pyrosbag.readthedocs.io/en/latest/index.html
"""
import os, sys, select, tty, termios
import time
import multiprocessing
import pyrealsense2 as rs

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--c_width', type=int, help='color frame width', default=640)
parser.add_argument('--c_height', type=int, help='color frame height', default=480)
parser.add_argument('--d_width', type=int, help='depth frame width', default=640)
parser.add_argument('--d_height', type=int, help='depth frame height', default=480)
# 6/15/30
parser.add_argument('-f', '--fps', type=int, help='frames per second', default=15)
parser.add_argument('-d', '--dir', type=str, help='data directory', default='data/')
args = parser.parse_args()


class Recorder:
    def __init__(self, c_width, c_height, d_width, d_height, fps, filename):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(stream_type=rs.stream.depth, width=d_width, height=d_height, format=rs.format.z16,
                                  framerate=fps)
        self.config.enable_stream(stream_type=rs.stream.color, width=c_width, height=c_height, format=rs.format.rgb8,
                                  framerate=fps)
        self.config.enable_record_to_file(filename)
        self.recorder = self.pipeline.start(self.config).get_device().as_recorder()
        self.recorder.resume()

    def run(self):
        self.pipeline.wait_for_frames()

    def pause(self):
        self.recorder.pause()

    def close(self):
        self.pipeline.stop()


def recording_process(shared):
    if not os.path.exists(args.dir):
        os.makedirs(args.dir)
    filename = args.dir + time.strftime("%Y%m%d_%H_%M_%S", time.localtime(
        time.time())) + '_cw{}_ch{}_dw{}_dh{}_fps{}'.format(args.c_width, args.c_height, args.d_width, args.d_height,
                                                            args.fps)
    bagname = filename + '.bag'

    if os.path.exists(bagname):
        print('Error: already have this file.')
        exit(1)
    recorder = Recorder(args.c_width, args.c_height, args.d_width, args.d_height, args.fps, bagname)
    print('Start recording...')
    while shared['is_recording']:
        print('.', end='')
        recorder.run()
    recorder.close()
    print('Recording ended.')
    # print('Compressing...')
    # new_zip = zipfile.ZipFile(filename + '.zip', 'w', zipfile.ZIP_DEFLATED)
    # new_zip.write(bagname, compress_type=zipfile.ZIP_DEFLATED)
    # new_zip.close()
    # print('Compression completed.')


if __name__ == '__main__':

    old_attr = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    print('Please input keys, press Ctrl + C to quit')

    # set shared variable
    manager = multiprocessing.Manager()
    shared = manager.dict()
    shared['is_recording'] = False

    # check the keyborad
    p = None
    try:
        while True:
            if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
                key = sys.stdin.read(1)
                if key == ' ':
                    # toggle
                    shared['is_recording'] = not shared['is_recording']

                    if shared['is_recording']:
                        p = multiprocessing.Process(target=recording_process, args=(shared,))
                        p.start()
                    else:
                        # stop recording
                        p and p.join()
                elif key == 'q':
                    print('Quit the program.')
                    break
                else:
                    print('You just pressed the button {}: no any influence.'.format(key))
    except Exception as e:
        print(e)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)
        p and p.join()

    print('Program exit.')
