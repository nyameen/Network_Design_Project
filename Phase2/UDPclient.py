import socket
import time
import select
import os
import sys
import rdt


def main(f):

    UDP_IP = "127.0.0.1"    # server IP
    UDP_PORT = 12001    # server Port
    DEFAULT_FILEPATH = '../spongebob.bmp'

    img_filepath = f or DEFAULT_FILEPATH

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	# open a UDP socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # set options for resuse addr and port

    def send_img(filepath):
        try:
            f = open(filepath, "rb")  # open that file for reading binary
        except FileNotFoundError:
            print(f'{filepath} does not exist')
            return

        print("Sending filename to server")
        filename = os.path.basename(filepath)
        print(filename)
        sock.sendto(filename.encode('utf-8'), (UDP_IP, UDP_PORT)) # send file name to server

        print('Sending file contents to server')
        rdt.rdt_send(f, (UDP_IP, UDP_PORT), sock)
        f.close()


    def wait_and_receive():
        data, addr = sock.recvfrom(1024)    # receive file name from server
        if not data:
            print('No response received')
            return

        resfile = data.strip().decode('utf-8')
        filename = f'reponse_{resfile}'
        print("Response file Name:", filename)   # print it

        f = open(filename, "wb") # open that file for writing binary

        rdt.rdt_rcv(f, filename, sock)


    send_img(img_filepath)
    wait_and_receive()

    sock.close()    # close socket
