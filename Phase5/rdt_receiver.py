import socket
import select
import time
import config
import rdt_utils

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
    pkt = ACK + seqNum
    chksum = rdt_utils.calc_checksum(pkt)
    chksum_bytes = (chksum).to_bytes(2, byteorder='big')
    pkt += chksum_bytes
    return pkt

##       rdt_rcv()
##Parameters:
##    file     - the file to be sent
##    endpoint - the endpoint
##    sock     - the socket to send through            
def rdt_rcv(file, endpoint, sock):
    oncethru = 0
    seqNum = 0
    seq = bin(seqNum)[2:].encode("utf-8")
    ACK = bin(15)[2:].encode('utf-8')
    
    while True:
        pkt = extract(sock)
        if pkt:
            #parse packet
            recSeq = pkt[0:1]
            rec_ck = rdt_utils.parse_checksum(pkt[1:3])
            data = pkt[3:]
            
            
            if rdt_utils.has_data_bit_err() and rdt_utils.random_channel() < config.percent_corrupt:
                if config.debug:
                    print("Bit error encountered in Data!")
                corruptData = rdt_utils.corrupt_bits(data)
                calc = recSeq + corruptData
            else:
                calc = recSeq + data
        
            chksum = rdt_utils.calc_checksum(calc)
            
            # correct sequence number
            if seq == recSeq and chksum == rec_ck:
                deliver_data(file, data)
                sndpkt = make_pkt(ACK, recSeq, chksum)
                udt_send(sndpkt, endpoint, sock)

                # switch sequence number
                if seqNum == 0:
                    seqNum = 1
                else:
                    seqNum = 0
                seq = bin(seqNum)[2:].encode("utf-8")
                oncethru = 1
            else:
                # didn't receive right pkt, either seqnum wrong or cksum
                if oncethru == 1:
                    if config.debug:
                        print("Bad data received, sending prev ACK")
                    udt_send(sndpkt, endpoint, sock)
                else:
                    if config.debug:
                        print("Bad data received in first packet")
        else:
            file.close()
            break
            
