import socket
import select
import time
import sys
import os
from collections import deque
import utils

UDP_IP = "127.0.0.1"	# Server IP
IN_PORT = 12001	    # port
timeout = 3	# timeout

if len(sys.argv) < 2:
    print('Please provide path to response file')
    sys.exit(1)

response_filename = sys.argv[1]

# function to send an image
def send_img(socket, client, filepath):
    try:
        f = open(filepath, 'rb')
    except FileNotFoundError:
        print(f'Response file {filepath} does not exist')
        return
    filename = os.path.basename(filepath)
    print ("Sending filename of response")
    socket.sendto(filename.encode('utf-8'), client)

    # read 1024 bytes
    packets = utils.make_packets(f, 1024)

    # while theres data keep sending
    print("Sending response file")
    while packets:
        if not socket.sendto(packets.popleft(), client):
            print('Error sending packet')
    
    f.close()
            
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		# open a UDP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# set the socket options to reuse address and port
sock.bind((UDP_IP, IN_PORT))    # bind to address and port

while True:
    data, addr = sock.recvfrom(1024)    # receive from client
    if data:
        file_name = data.strip().decode('utf-8')    # strip the header
        print ("Recieved file name:", file_name)  # print file received

    f = open(file_name, 'wb')   # open that file for writing binary

    while True:
        ready = select.select([sock], [], [], timeout) # wait until sock is ready for I/O
        if ready[0]:
            data, addr = sock.recvfrom(1024)	# receive 1024 from client
            f.write(data)   # write it to a file
        else:
            print ("%s Finish!" % file_name)    # finished writing 
            f.close()	# close file
            break

    send_img(sock, addr, response_filename)
