#!/usr/bin/python
import sys, getopt
import asyncore
import numpy as np
import pickle
import socket
import struct
import functools

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
mc_ip_address = '172.27.15.168'
local_ip_address = '0.0.0.0'
port = 1024
chunk_size = 4096


def start_client(func):
    @functools.wraps(func)
    def processed(*args, **kwargs):

        # UDP client for each camera server
        class ImageClient(asyncore.dispatcher):
            def __init__(self, server, source):
                asyncore.dispatcher.__init__(self, server)
                self.address = server.getsockname()[0]
                self.port = source[1]
                self.buffer = bytearray()
                self.windowName = self.port
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

                res = func(imdata, *args, **kwargs)

                self.buffer = bytearray()
                self.frame_id += 1

            def readable(self):
                return True

        class EtherSenseClient(asyncore.dispatcher):
            def __init__(self):
                asyncore.dispatcher.__init__(self)
                self.server_address = ('', 1024)
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

        def multi_cast_message(ip_address, port, message):
            # send the multicast message
            multicast_group = (ip_address, port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            connections = {}
            try:
                # Send data to the multicast group
                print('sending "%s"' % message + str(multicast_group))
                sent = sock.sendto(message.encode(), multicast_group)
                print(sent)

                # defer waiting for a response using Asyncore
                client = EtherSenseClient()
                asyncore.loop()

                # Look for responses from all recipients

            except socket.timeout:
                print('timed out, no more responses')
            finally:
                print(sys.stderr, 'closing socket')
                sock.close()

        multi_cast_message(mc_ip_address, port, 'EtherSensePing!!')

    return processed


if __name__ == '__main__':
    @start_client
    def print_hello(x):
        print(type(x))


    print_hello()
