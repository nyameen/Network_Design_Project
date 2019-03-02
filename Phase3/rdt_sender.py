import socket
import select
import time

##       extract()
##Parameters:
##    sock     - the socket to send through
##    bytesize - size to read
##Return:
##    the packet and data received
def extract(sock, bytesize=2048):
    data, addr = sock.recvfrom(bytesize)
    return data


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
##    file   - the file to create a packet with
##    seqNum - the sequence number to send
##    cksum  - the checksum value
##Return:
##    the packet
def make_pkt(file, seqNum, cksum, bytesize=1024):
    data = file.read(bytesize)
    if data == b'':
        return 0

    pkt = seqNum + data + cksum
    return pkt
    
##       rdt_send()
##Parameters:
##    file   - the file to be sent
##    endpoint -
##      If sending to server: (IP, PORT_NUMBER)
##      If sending to client: client addr
##    sock   - the socket to send through
def rdt_send(file, endpoint, sock):
    seqNum = 0
    seq = bin(seqNum)[2:].encode("utf-8")
    ck = bin(7)[2:].encode("utf-8")
    
    packet = make_pkt(file, seq, ck)
    while packet != 0:
        if(udt_send(packet, endpoint, sock)):
            if(rdt_rcv(sock, seq) == 1):
                if(seqNum == 0): # switch sequence numbers
                    seqNum = 1
                else:
                    seqNum = 0

                seq = bin(seqNum)[2:].encode("utf-8")
                packet = make_pkt(file, seq, ck)
                time.sleep(0.005)

##       rdt_rcv()
##Parameters:
##    sock     - the socket to send through
##    seqNum   - the expected sequence number
def rdt_rcv(sock, seqNum):    
    data = extract(sock)

    # parse packets
    ACK    = data[0:4]
    recSeq = data[4:5]
    cksum  = data[5:]
    
   channel = random_channel()
   if(channel == unreliable):  
        #corrupt ACK if need be 
        #corrupt_bits(ACK)
    
    if ACK == b'1111' and recSeq == seqNum:
        return 1
    else:
        return 0
            
        












        
