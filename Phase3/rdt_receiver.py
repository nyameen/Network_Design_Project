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
    pkt = ACK + seqNum
    chksum = calc_checksum(pkt)
    chksum_bytes = (chksum).to_bytes(2, byteorder='big')
    pkt += chksum_bytes
    return pkt

##       calc_checksum()
##Parameters:
##    data - data in bytes format
##Return:
##    checksum (int) calculated via 1's complement of wraparound 16bit sum 
def calc_checksum(data):
    lower_16_bits = int('0xFFFF', 16)

    bin_sum = 0
    for i in range(2, len(data) - 1, 2):
        bin_sum += (data[i] << 8) | data[i+1]
        if bin_sum & int('0x10000', 16):
            bin_sum = bin_sum & lower_16_bits
            bin_sum += 1

    return bin_sum ^ lower_16_bits

##       parse_checksum()
##Parameters:
##    byte_data - 16b checksum in form of 2 bytes (big endian)
##Return:
##    checksum integer
def parse_checksum(byte_data):
    return (byte_data[0] << 8) + byte_data[1]

##       rdt_rcv()
##Parameters:
##    file     - the file to be sent
##    endpoint - the endpoint
##    sock     - the socket to send through            
def rdt_rcv(file, endpoint, sock):
    seqNum = 0
    seq = bin(seqNum)[2:].encode("utf-8")
    ACK = bin(15)[2:].encode('utf-8')
    
    while True:
        pkt = extract(sock)
        if pkt:
            #parse packet
            recSeq = pkt[0:1]
            data   = pkt[1:1025]
            rec_ck = parse_checksum(pkt[1025:])

            chksum = calc_checksum(pkt[:1025])
            
            #channel = random_channel()
            #if(channel == unrealiable):
                #corrupt pkt if need be 
                #corrupt_bits(data)
            
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
            else:
                # didn't receive right pkt, either seqnum wrong or cksum
                pass
        else:
            file.close()
            break
            
