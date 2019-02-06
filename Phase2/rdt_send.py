import socket

##       udt_send()
##Parameters:
##    packet - the packet to send
##    server - the IP and Port number of server
##    sock   - the socket to send through
##Return:
##    number of bytes sent
def udt_send(packet, server, sock):
    return sock.sendto(packet, server)

##       make_pkt()
##Parameters:
##    file - the file to create a packet with
##Return:
##    the packet
def make_pkt(file):
    return file.read(1024)
    
##       rdt_send()
##Parameters:
##    file   - the file to be sent
##    server - the IP and Port number of server
##    sock   - the socket to send through
def rdt_send(file, server, sock):
    packet = make_pkt(file)
    while packet:
        if(udt_send(packet, server, sock)):
            packet = make_pkt(file)
            

def main():
    UDP_IP = "127.0.0.1"    # server IP
    UDP_PORT = 12001	    # server Port
    server = (UDP_IP, UDP_PORT)

    # open a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # set options for resuse addr and port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # change file name in file.jpg
    sock.sendto('file.jpg'.encode('utf-8'), server) # send file name to server
    print ("Sending...")

    # change file name in file.jpg
    f = open("file.jpg", "rb") # open that file for reading binary
    
    rdt_send(f, server, sock)

    f.close()   # close file
    sock.close()# clsoe socket


if __name__ == "__main__":

    main()
