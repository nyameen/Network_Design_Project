import socket
import time
import select
import os
import sys

UDP_IP = "127.0.0.1"    # server IP
UDP_PORT = 12001    # server Port


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	# open a UDP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # set options for resuse addr and port

def send_img(filepath):
    try:
        f = open(filepath, "rb")  # open that file for reading binary
    except FileNotFoundError:
        print(f'{filename} does not exist')
        return

    filename = os.path.basename(filepath)
    print("Sending filename to server")
    sock.sendto(filename.encode('utf-8'), (UDP_IP, UDP_PORT)) # send file name to server

    data = f.read(1024) # read 1024 bytes

    # while there is still data to send
    print('Sending file contents to server')
    while(data):
        if(sock.sendto(data, (UDP_IP, UDP_PORT))):	# send data to server
            data = f.read(1024) # read another 1024
            time.sleep(0.02)    # small wait

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

    while(True):
        ready = select.select([sock], [], [], 3)    # wait until sock is ready for I/O
        if(ready[0]):
            data, addr = sock.recvfrom(1024)    # read 1024 from server
            f.write(data)	# write it to a file
        else:
            print(f'{filename} finished')  # finished reading file
            break

    f.close()



if len(sys.argv) < 2:
    print('Please provide filepath to send')
    sys.exit(1)

send_img(sys.argv[1])
wait_and_receive()

sock.close()    # close socket
