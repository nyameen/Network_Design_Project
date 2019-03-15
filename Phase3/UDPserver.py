import socket
import select
import time
import sys
import os
import rdt_receiver
import rdt_sender

DEFAULT_FILEPATH = 'spongebob.bmp'
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
            f = open(self.response_filepath, 'rb') # open file for reading binary
        except FileNotFoundError:
            self.print(f'Response file {self.response_filepath} does not exist')
            return
        filename = os.path.basename(self.response_filepath)	# path to file
        self.print("Sending filename of response")
        self.sock.sendto(filename.encode('utf-8'), client) # send filename to client
        self.print("Sending file response")
        rdt_sender.rdt_send(f, client, self.sock) # RDT send
        f.close()

    def listen(self):
        while True:
            self.print('Listening...')
            msg, addr = self.sock.recvfrom(1024) # receive filename from client
            
            if msg:
                fileName = msg.strip().decode('utf-8') # decode name 
                self.print(f"Recieved file name: {fileName}")

            fileName = f'server_recv_{fileName}' # append server_recv to filename
            self.print(f'Writing filename {fileName}')
            f = open(fileName, 'wb') # open for writing binary
            
            rdt_receiver.rdt_rcv(f, addr, self.sock)	# RDT receive
            self.print(f'Finished writing received file {fileName}')
            self.send_img(addr) # respond by sending an image

    def print(self, print_str):
        print(f'Server: {print_str}') # print to the terminal
