import socket
import select
import time

##       extract()
##Parameters:
##    sock     - the socket to send through
##    bytesize - size to read
##Return:
##    the packet and data received
##    0 if timeout
def extract(sock, bytesize=1024):
    timeout = 3
    ready = select.select([sock], [], [], timeout)
    if ready[0]:
        data, addr = sock.recvfrom(1024)
        return data, data
    else:
        return 0, 0

##       deliver_data()
##Parameters:
##    file  - file the write
##    data  - the data received
##Return:
##    the packet and data received
##    0 if timeout
def deliver_data(file, data):
    file.write(data)

##       udt_send()
##Parameters:
##    packet - the packet to send
##    server - the IP and Port number of server
##    sock   - the socket to send through
##Return:
##    number of bytes sent
def udt_send(packet, endpoint, sock):
    return sock.sendto(packet, endpoint)

##       make_pkt()
##Parameters:
##    file - the file to create a packet with
##Return:
##    the packet
def make_pkt(file, bytesize=1024):
    return file.read(bytesize)
    
##       rdt_send()
##Parameters:
##    file   - the file to be sent
##    endpoint -
##      If sending to server: (IP, PORT_NUMBER)
##      If sending to client: client addr
##    sock   - the socket to send through
def rdt_send(file, endpoint, sock):
    packet = make_pkt(file)
    while packet:
        if(udt_send(packet, endpoint, sock)):
            packet = make_pkt(file)
            time.sleep(0.005)

##       rdt_rcv()
##Parameters:
##    file     - the file to be sent
##    fileNeam - The name of the file
##    sock     - the socket to send through            
def rdt_rcv(file, fileName, sock):    
    while True:
        packet, data = extract(sock)
        if data:
            deliver_data(file, data)
        else:
            print("%s Finsish!" % fileName)
            file.close()
            break
            
        












        
