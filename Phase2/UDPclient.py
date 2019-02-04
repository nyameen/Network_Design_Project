import socket
import time
import select

UDP_IP = "127.0.0.1"    # server IP
UDP_PORT = 12001    # server Port


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	# open a UDP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # set options for resuse addr and port

# change file name in file.jpg
sock.sendto('file.jpg'.encode('utf-8'), (UDP_IP, UDP_PORT)) # send file name to server
print ("Sending ")

# change file name in file.jpg
f = open("file.jpg", "rb")  # open that file for reading binary
data = f.read(1024) # read 1024 bytes

# while there is still data to send
while(data):
    if(sock.sendto(data, (UDP_IP, UDP_PORT))):	# send data to server
        data = f.read(1024) # read another 1024
        time.sleep(0.02)    # small wait


f.close()


data, addr = sock.recvfrom(1024)    # receive file name from server
if(data):
    print("File Name:", data)   # print it
    file = data.strip() # strip the name

f = open(file, "wb") # open that file for writing binary

while(1):
    ready = select.select([sock], [], [], 3)	# wait until sock is ready for I/O
    if(ready[0]):
        data, addr = sock.recvfrom(1024)    # read 1024 from server
        f.write(data)	# write it to a file
    else:
        print("%s Finsih!" % file)  # finished reading file
        break

sock.close()    # close socket
f.close()   # close port
