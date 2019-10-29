#!/usr/bin/python
#-*-coding:utf-8-*-
import pyrealsense2 as rs
import sys, getopt
import asyncore
import numpy as np
import pickle
import socket
import struct

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
mc_ip_address = '0.0.0.0'
port = 1024
chunk_size = 4096


def getColorAndTimestamp(pipeline):
    frames = pipeline.wait_for_frames()
    # take owner ship of the frame for further processing
    frames.keep()
    color = frames.get_color_frame()
    if color:
        color.keep()
        # represent the frame as a numpy array
        colorData = color.as_frame().get_data()
        colorMat = np.asanyarray(colorData)
        ts = frames.get_timestamp()
        return colorMat, ts
    else:
        return None, None


def openPipeline():
    cfg = rs.config()
    cfg.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
    pipeline = rs.pipeline()
    pipeline_profile = pipeline.start(cfg)
    # sensor = pipeline_profile.get_device().first_depth_sensor()
    return pipeline


class DevNullHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        print(self.recv(1024))

    def handle_close(self):
        self.close()


class EtherSenseServer(asyncore.dispatcher):
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        print("Launching Realsense Camera Server")
        try:
            self.pipeline = openPipeline()
        except:
            print("Unexpected error: ", sys.exc_info()[1])
            sys.exit(1)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        print('sending acknowledgement to', address)

        # reduce the resolution of the depth image using post processing
        self.frame_data = ''
        self.connect((address[0], 1024))
        self.packet_id = 0

    def handle_connect(self):
        print("connection received")

    def writable(self):
        return True

    def update_frame(self):
        color, timestamp = getColorAndTimestamp(self.pipeline)
        if color is not None:
            # convert the depth image to a string for broadcast
            data = pickle.dumps(color)
            # capture the length of the data portion of the message
            length = struct.pack('<I', len(data))
            # include the current timestamp for the frame
            ts = struct.pack('<d', timestamp)
            # for the message for transmission
            self.frame_data = length + ts + data 

    def handle_write(self):
        # first time the handle_write is called
        if not hasattr(self, 'frame_data'):
            self.update_frame()
        # the frame has been sent in it entirety so get the latest frame
        if len(self.frame_data) == 0:
            self.update_frame()
        else:
            # send the remainder of the frame_data until there is no data remaining for transmition
            remaining_size = self.send(self.frame_data)
            self.frame_data = self.frame_data[remaining_size:]

    def handle_close(self):
        self.close()


class MulticastServer(asyncore.dispatcher):
    def __init__(self, host=mc_ip_address, port=1024):
        # Asyncore是python的标准库。
        # Asyncore.dispatcher 是这个库中的一个socket的框架，
        # 为socket添加了一些通用的回调方法
        asyncore.dispatcher.__init__(self)

        server_address = (host, port)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(server_address)

    def handle_read(self):
        data, addr = self.socket.recvfrom(42)
        print(addr)
        print('Recived Multicast data bytes from {}'.format(addr))
        # Once the server recives the multicast signal, open the frame server
        EtherSenseServer(addr)
        print(sys.stderr, data)

    def writable(self):
        return False  # don't want write notifies

    def handle_close(self):
        self.close()

    def handle_accept(self):
        channel, addr = self.accept()
        print('received %s bytes from %s' % (data, addr))


if __name__ == '__main__':
    # initalise the multicast receiver
    server = MulticastServer()
    # hand over excicution flow to asyncore
    asyncore.loop()

