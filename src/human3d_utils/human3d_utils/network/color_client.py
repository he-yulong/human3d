#!/usr/bin/python
import sys
import asyncore
import pickle
import socket
import struct
import cv2
import functools


def start_color_client(initialize, mc_ip_address, port, message='hello!'):
    def decorator(func):
        @functools.wraps(func)
        def processing(*args, **kwargs):
            class ImageClient(asyncore.dispatcher):
                """
                UDP client for each camera server
                """

                def __init__(self, server, source):
                    asyncore.dispatcher.__init__(self, server)
                    self.address = server.getsockname()[0]
                    self.port = source[1]
                    self.buffer = bytearray()
                    initialize and initialize(self)
                    self.remainingBytes = 0
                    self.frame_id = 0

                def handle_read(self):
                    if self.remainingBytes == 0:
                        # get the expected frame size
                        self.frame_length = struct.unpack('<I', self.recv(4))[0]
                        # get the timestamp of the current frame
                        self.timestamp = struct.unpack('<d', self.recv(8))
                        self.remainingBytes = self.frame_length

                    # request the frame data until the frame is completely in buffer
                    data = self.recv(self.remainingBytes)
                    self.buffer += data
                    self.remainingBytes -= len(data)
                    # once the frame is fully recived, process/display it
                    if len(self.buffer) == self.frame_length:
                        self.handle_frame()

                def handle_frame(self):
                    # convert the frame from string to numerical data
                    imdata = pickle.loads(self.buffer)
                    func(self, imdata, *args, **kwargs)

                    self.buffer = bytearray()
                    self.frame_id += 1

                def readable(self):
                    return True

            class EtherColorClient(asyncore.dispatcher):
                def __init__(self, ip, port):
                    asyncore.dispatcher.__init__(self)
                    self.server_address = (ip, port)
                    # create a socket for TCP connection between the client and server
                    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket.settimeout(5)

                    self.bind(self.server_address)
                    self.listen(10)

                def writable(self):
                    return False  # don't want write notifies

                def readable(self):
                    return True

                def handle_connect(self):
                    print("connection recvied")

                def handle_accept(self):
                    pair = self.accept()
                    # print(self.recv(10))
                    if pair is not None:
                        sock, addr = pair
                        print('Incoming connection from %s' % repr(addr))
                        # when a connection is attempted, delegate image receival to the ImageClient
                        handler = ImageClient(sock, addr)

            multicast_group = (mc_ip_address, port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # Send data to the multicast group
                print('sending "%s"' % message + str(multicast_group))
                sent = sock.sendto(message.encode(), multicast_group)

                # defer waiting for a response using Asyncore
                client = EtherColorClient('', port)
                asyncore.loop()
            except socket.timeout:
                print('timed out, no more responses')
            finally:
                print(sys.stderr, 'closing socket')
                sock.close()

        return processing

    return decorator


if __name__ == '__main__':
    def show_window(self):
        self.windowName = self.port
        cv2.namedWindow("window" + str(self.windowName))


    @start_color_client(show_window, '127.0.0.1', 1024)
    def process_data(self, data):
        cv2.imshow("window_color" + str(self.windowName), data[:, :, :])
        cv2.waitKey(1)


    process_data()
