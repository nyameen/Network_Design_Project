import socket
import select
import time
import random

##      corrupt_datat()
##Parameters:
##  data        - either ACK or DATA 
def corrupt_bits(pkt):
    index = random.randint(0, len(pkt)-1)
    pkt = pkt[:index] + bytearray(chr(random.randint(0, 95)),'utf-8') + pkt[index+1:]
    return pkt

##      random
##Parameters:
##  none
def random_channel():

    choice = random.randint(0,100)
    return choice

##       extract()
##Parameters:
##    sock     - the socket to send through
##    bytesize - size to read
##Return:
##    the packet and data received
def extract(sock, bytesize=2048):
    timeout = 3
    ready = select.select([sock], [], [], timeout)
    if ready[0]:
        data, addr = sock.recvfrom(bytesize)
        return data
    else:
        return 0


##       udt_send()
##Parameters:
##    packet - the packet to send
##    server - the IP and Port number of server
##    sock   - the socket to send through
##Return:
##    number of bytes sent
def udt_send(packet, endpoint, sock):
    return sock.sendto(packet, endpoint)

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

##       make_pkt()
##Parameters:
##    file   - the file to create a packet with
##    seqNum - the sequence number to send
##    cksum  - the checksum value
##Return:
##    the packet
def make_pkt(file, seqNum, bytesize=1024):
    data = file.read(bytesize)
    if data == b'':
        return 0
    calc = seqNum + data
    chksum = calc_checksum(calc)

    chksum_bytes = (chksum).to_bytes(2, byteorder='big')
    packet = seqNum + chksum_bytes + data
    return packet
    
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

    packet = make_pkt(file, seq)

    while packet != 0:
        if(udt_send(packet, endpoint, sock)):
            if(rdt_rcv(sock, seq) == 1):
                if(seqNum == 0): # switch sequence numbers
                    seqNum = 1
                else:
                    seqNum = 0
                seq = bin(seqNum)[2:].encode("utf-8")
                packet = make_pkt(file, seq)
                time.sleep(0.005)

##       rdt_rcv()
##Parameters:
##    sock     - the socket to send through
##    seqNum   - the expected sequence number
def rdt_rcv(sock, seqNum):    
    data = extract(sock)

    if data == 0:
        return 0

    # parse packets
    ACK    = data[0:4]
    recSeq = data[4:5]
    rec_cksum  = parse_checksum(data[5:])

    rnd = random_channel()
    if(rnd < 0):
        corruptData = corrupt_bits(ACK)
        calc =  corruptData + recSeq
    else:
        calc = ACK + recSeq
    checksum = calc_checksum(calc)
    
    if ACK == b'1111' and recSeq == seqNum and rec_cksum == checksum:
        #print('OK')
        return 1
    else:
        #print('NOK')
        return 0
            
