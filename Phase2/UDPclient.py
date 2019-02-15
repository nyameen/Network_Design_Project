import socket
import time
import select
import os
import sys
import rdt

DEFAULT_FILEPATH = 'spongebob.bmp'
UDP_IP = "127.0.0.1"    # server IP
UDP_PORT = 12001    # server Port


class UDPclient:

    def __init__(self, filepath, callback_func):
        self.cb = callback_func

        self.udp_info = (UDP_IP, UDP_PORT)
        self.img_filepath = filepath or DEFAULT_FILEPATH

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	# open a UDP socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # set options for resuse addr and port

    def send_img(self, filepath):
        f = open(filepath, "rb")  # open that file for reading binary
        filename = os.path.basename(filepath)
        self.print(f"Sending filename {filename} to server")
        self.sock.sendto(filename.encode('utf-8'), self.udp_info) # send file name to server

        self.print('Sending file contents to server')
        rdt.rdt_send(f, self.udp_info, self.sock)
        f.close()


    def wait_and_receive(self):
        data, addr = self.sock.recvfrom(1024)    # receive file name from server
        if not data:
            print('No response received')
            return

        resfile = data.strip().decode('utf-8')
        filename = f'client_recv_{resfile}'
        self.print(f"Response file Name: {filename}")   # print it

        f = open(filename, "wb") # open that file for writing binary

        rdt.rdt_rcv(f, filename, self.sock)
        self.print(f'Finished writing received file {filename}')

    def start_send(self):
        try:
            self.send_img(self.img_filepath)
        except FileNotFoundError:
            self.print(f'{self.img_filepath} does not exist')
            self.cb()
            return
        self.wait_and_receive()
        self.sock.close()    # close socket
        self.cb()

    def print(self, print_str):
        print(f'Client: {print_str}')
