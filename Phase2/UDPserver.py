import socket
import select
import time
import sys
import os
import rdt

UDP_IP = "127.0.0.1"	# Server IP
IN_PORT = 12001	    # port
DEFAULT_FILEPATH = '../spongebob.bmp'
timeout = 3	# timeout

if len(sys.argv) > 1:
    response_filepath = sys.argv[1]
else:
    response_filepath = DEFAULT_FILEPATH

# function to send an image
def send_img(sock, client, filepath):
    try:
        f = open(filepath, 'rb')
    except FileNotFoundError:
        print(f'Response file {filepath} does not exist')
        return
    filename = os.path.basename(filepath)
    print ("Sending filename of response")
    sock.sendto(filename.encode('utf-8'), client)
    print("Sending file response")
    rdt.rdt_send(f, client, sock)
    f.close()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		# open a UDP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# set the socket options to reuse address and port
sock.bind((UDP_IP, IN_PORT))    # bind to address and port

while True:
    print('Server listening...')
    msg, addr = sock.recvfrom(1024)
    if msg:
        fileName = msg.strip().decode('utf-8')
        print ("Recieved file name:", fileName)

    f = open(fileName, 'wb')
    
    rdt.rdt_rcv(f, fileName, sock)
    send_img(sock, addr, response_filepath)
