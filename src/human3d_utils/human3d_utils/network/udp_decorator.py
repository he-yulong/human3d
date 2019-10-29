"""
UDP client/server decorator

UDP client: to send data.
UDP server: to perform operation on the frame it receives.
"""
import functools
import socket
import json
import time


def process_udp_server(ip='0.0.0.0', port=8999, data_size=1024 * 10):
    """
    UDP server decorator
    :param ip:
    :param port:
    :param data_size:
    :return:
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((ip, port))
    print('UDP server started at {}.'.format(str(ip) + ":" + str(port)))

    def start_server(func):
        @functools.wraps(func)
        def processed(*args, **kwargs):
            while True:
                data = server.recv(data_size)
                data = json.loads(data.decode())
                res = func(data, *args, **kwargs)
                if res == -1:
                    break

        return processed

    return start_server


def camera_udp_client(ip, port):
    """
    UDP client decorator
    :param ip:
    :param port:
    :return:
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start_client(func):
        @functools.wraps(func)
        def send_data(*args, **kwargs):
            data = func(*args, **kwargs)
            client.sendto(str.encode(json.dumps(data)), (ip, port))

        return send_data

    return start_client


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, help='server/client mode', default='server')
    parser.add_argument('-i', '--ip', type=str, help='IP address', default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, help='UDP port', default=8999)
    parser.add_argument('-c', '--camera', type=int, help='camera number', default=0)
    args = parser.parse_args()

    if args.mode == 'server':
        @process_udp_server(args.ip, args.port, 1024 * 1024)
        def multiply(x):
            time.sleep(1)
            print(x * 2)


        multiply()
    elif args.mode == 'client':
        @camera_udp_client(args.ip, args.port)
        def send_single_data(x):
            return x


        while True:
            send_single_data(8)
            time.sleep(1)
    else:
        print('python udp_decorator.py -m [server|client]')
