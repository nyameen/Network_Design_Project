import socket
import select
import time
import sys
import os
import rdt

DEFAULT_FILEPATH = os.path.join('..', 'spongebob.bmp')
UDP_IP = "127.0.0.1"	# Server IP
IN_PORT = 12001	    # port


class UDPserver:
    def __init__(self, filepath):
        
        self.response_filepath = filepath or DEFAULT_FILEPATH

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		# open a UDP socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# set the socket options to reuse address and port
        self.sock.bind((UDP_IP, IN_PORT))    # bind to address and port

    def send_img(self, client):
        try:
            f = open(self.response_filepath, 'rb')
        except FileNotFoundError:
            self.print(f'Response file {self.response_filepath} does not exist')
            return
        filename = os.path.basename(self.response_filepath)
        self.print("Sending filename of response")
        self.sock.sendto(filename.encode('utf-8'), client)
        self.print("Sending file response")
        rdt.rdt_send(f, client, self.sock)
        f.close()

    def listen(self):
        while True:
            self.print('Listening...')
            msg, addr = self.sock.recvfrom(1024)
            
            if msg:
                fileName = msg.strip().decode('utf-8')
                self.print(f"Recieved file name: {fileName}")

            fileName = f'server_recv_{fileName}'
            self.print(f'Writing filename {fileName}')
            f = open(fileName, 'wb')
            
            rdt.rdt_rcv(f, fileName, self.sock)
            self.print(f'Finished writing received file {fileName}')
            self.send_img(addr)

    def print(self, print_str):
        print(f'Server: {print_str}')
