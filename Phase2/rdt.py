import socket

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
            
