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
def extract(sock, bytesize=2048):
    timeout = 3
    ready = select.select([sock], [], [], timeout)
    if ready[0]:
        data, addr = sock.recvfrom(bytesize)
        return data
    else:
        return 0

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
##    packet   - the packet to send
##    endpoint - the endpoint
##    sock     - the socket to send through
##Return:
##    number of bytes sent
def udt_send(packet, endpoint, sock):
    return sock.sendto(packet, endpoint)

##       make_pkt()
##Parameters:
##    ACK     - acknowledgement
##    seqNum  - sequence number
##    cksum   - checksum
##Return:
##    the packet
def make_pkt(ACK, seqNum, cksum):
    pkt = ACK + seqNum + cksum
    return pkt

##       rdt_rcv()
##Parameters:
##    file     - the file to be sent
##    endpoint - the endpoint
##    sock     - the socket to send through            
def rdt_rcv(file, endpoint, sock):
    seqNum = 0
    seq = bin(seqNum)[2:].encode("utf-8")
    ACK = bin(15)[2:].encode('utf-8')
    ck = bin(7)[2:].encode("utf-8")
    
    while True:
        pkt = extract(sock)        
        if pkt:
            #parse packet
            recSeq = pkt[0:1]
            data   = pkt[1:1025]
            ck     = pkt[1025:]

            # correct sequence number
            if seq == recSeq:
                deliver_data(file, data)
                sndpkt = make_pkt(ACK, recSeq, ck)
                udt_send(sndpkt, endpoint, sock)

                # switch sequence number
                if seqNum == 0:
                    seqNum = 1
                else:
                    seqNum = 0
                seq = bin(seqNum)[2:].encode("utf-8")
            else:
                # didn't receive right pkt, either seqnum wrong or cksum
        else:
            file.close()
            break
            
        












        
