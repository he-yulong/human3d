import time
import cv2
import numpy as np
import sys
import asyncore
import socket
import pickle
import struct

chunk_size = 4096


def get_color_and_timestamp(cap):
    ret, frame = cap.read()
    # take owner ship of the frame for further processing
    if ret:
        return frame, time.time()
    else:
        return None, None


class CameraServer(asyncore.dispatcher):

    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        print("Launching Preposition Camera Server")
        try:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
        except:
            print("Unexpected error: ", sys.exc_info()[1])
            sys.exit(1)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((address[0], 1024))
        print('sending acknowledgement to', address)
        self.frame_data = ''
        self.packet_id = 0

    def handle_connect(self):
        print("connection received")

    def writable(self):
        return True

    def update_frame(self):
        color, timestamp = get_color_and_timestamp(self.cap)
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
    def __init__(self, host='0.0.0.0', port=1024):
        asyncore.dispatcher.__init__(self)
        server_address = (host, port)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(server_address)
        print('MulticastServer listen to {}:{}'.format(host, port))

    def handle_read(self):
        data, addr = self.socket.recvfrom(42)
        print('Recived Multicast data bytes from {}'.format(addr))
        # Once the server recives the multicast signal, open the frame server
        CameraServer(addr)
        print(sys.stderr, data)

    def writable(self):
        return False  # don't want write notifies

    def handle_close(self):
        self.close()

    def handle_accept(self):
        channel, addr = self.accept()
        print('received data from %s' % (addr))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, help='server/client mode', default='server')
    parser.add_argument('-i', '--ip', type=str, help='IP address', default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, help='UDP port', default=1024)
    args = parser.parse_args()

    if args.mode == 'server':
        server = MulticastServer(host=args.ip, port=args.port)
        asyncore.loop()
