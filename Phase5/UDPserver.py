import socket
import select
import time
import sys
import os
import rdt_receiver
import rdt_sender

MY_FILENAME = 'server_recv.jpg'
DEFAULT_FILEPATH = 'spongebob.jpg'
UDP_IP = "127.0.0.1"	# Server IP
IN_PORT = 12001	    # port

class UDPserver:
    def __init__(self, filepath, status_msgs):
        self.response_filepath = filepath or DEFAULT_FILEPATH
        self.status_msgs = status_msgs

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		# open a UDP socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# set the socket options to reuse address and port
        self.sock.bind((UDP_IP, IN_PORT))    # bind to address and port

    def send_img(self, client):
        try:
            f = open(self.response_filepath, 'rb') # open file for reading binary
        except FileNotFoundError:
            self.print(f'Response file {self.response_filepath} does not exist')
            return
        self.print("Sending file response")
        rdt_sender.rdt_send(f, client, self.sock) # RDT send
        f.close()

    def listen(self):
        self.print('Listening...')
        while True:
            addr = rdt_receiver.rdt_rcv(MY_FILENAME, self.sock)	# RDT receive
            # If didn't get anything then continue
            if not addr:
                continue
            self.print('Finished writing received file')
            self.send_img(addr) # respond by sending an image

    def print(self, print_str):
        if self.status_msgs:
            print(f'Server: {print_str}') # print to the terminal
