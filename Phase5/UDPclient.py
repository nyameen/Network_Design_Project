import socket
import time
import select
import os
import sys
import rdt_receiver
import rdt_sender

DEFAULT_FILEPATH = 'spongebob.jpg'
MY_FILENAME = 'client_recv.jpg'
UDP_IP = "127.0.0.1"    # server IP
UDP_PORT = 12001    # server Port


class UDPclient:

    def __init__(self, filepath, status_msgs):
        self.status_msgs = status_msgs

        self.udp_info = (UDP_IP, UDP_PORT)
        self.img_filepath = filepath or DEFAULT_FILEPATH

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	# open a UDP socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # set options for resuse addr and port

    def send_img(self, filepath):
        f = open(filepath, "rb")  # open that file for reading binary
        self.print('Sending file contents to server')
        rdt_sender.rdt_send(f, self.udp_info, self.sock)
        f.close()


    def wait_and_receive(self):
        rdt_receiver.rdt_rcv(MY_FILENAME, self.sock)
        self.print('Finished writing received file')

    def start_send(self):
        starttime = time.time()
        try:
            self.send_img(self.img_filepath)
        except FileNotFoundError:
            self.print(f'{self.img_filepath} does not exist')
            return
        self.wait_and_receive()
        self.sock.close()    # close socket
        endtime = time.time()
        elapsedtime = "{:.4f}".format(endtime - starttime)

        # Don't use self.print because want to print no matter value of self.status_msgs
        print(f'Time to finish {elapsedtime}')

    def print(self, print_str):
        if self.status_msgs:
            print(f'Client: {print_str}')
