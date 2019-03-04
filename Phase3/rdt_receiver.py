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
def make_pkt(ACK, seq_num):
    data = bytes(ACK)
    chksum = calc_checksum(seqNum, bytes(ACK))
    chksum_bytes = (chksum).to_bytes(2, byteorder='big')
    packet = seq_num + chksum_bytes + data
    return packet

def calc_checksum(header, data):
    data = header + data
    bin_sum = 0
    for i in range(2, len(data) - 1, 2):
        bin_sum += (data[i] << 8) | data[i+1]
        if bin_sum & int('0x10000', 16):
            bin_sum = bin_sum & int('0xFFFF', 16)
            bin_sum += 1

    return bin_sum ^ 1

def parse_checksum(packet):
    return (packet[1] << 8) + packet[2]

##       rdt_rcv()
##Parameters:
##    file     - the file to be sent
##    endpoint - the endpoint
##    sock     - the socket to send through            
def rdt_rcv(file, endpoint, sock):
    seq = 0
    #seq = bin(seqNum)[2:].encode("utf-8")
    #ACK = bin(15)[2:].encode('utf-8')
    #ck = bin(7)[2:].encode("utf-8")
    
    while True:
        pkt = extract(sock)        
        if pkt:
            #parse packet
            rec_seq = packet[0]
            rec_chk = parse_checksum(pkt)
            data = packet[3:]
            
            #channel = random_channel()
            #if(channel == unrealiable):
                #corrupt pkt if need be 
                #corrupt_bits(data)
            
            checksum = calc_checksum(rec_seq, data)
            # correct sequence number
            if seq == rec_seq and checksum == rec_chk:
                deliver_data(file, data)
                sndpkt = make_pkt(1, recSeq)
                udt_send(sndpkt, endpoint, sock)

                # switch sequence number
                seq = seqNum ^= 1
            else:
                # didn't receive right pkt, either seqnum wrong or cksum
                # todo
                sndpkt = make_pkt(1, recSeq ^ 1)
                udt_send(sndpkt, endpoint, sock)
        else:
            file.close()
            break
            
        
