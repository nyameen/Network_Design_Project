import socket
import select
import time
import random
import config
import rdt_utils

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
    chksum = rdt_utils.calc_checksum(calc)

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
    timer = rdt_utils.RDTTimer(config.timeout)

    # Returns callback function for when timeout reached
    def timeout_func(packet, endpoint, sock):
        def ret_func():
            if config.debug:
                print("Timeout for ACK exceeded, resending packet")
            udt_send(packet, endpoint, sock)
            # Forget last timer and start new one
            timer.start(timeout_func(packet, endpoint, sock))
        return ret_func

    seqNum = 0
    seq = bin(seqNum)[2:].encode("utf-8")
    packet = make_pkt(file, seq)

    while packet != 0:
        if rdt_utils.has_data_packet_loss() and rdt_utils.random_channel() < config.percent_corrupt:
            pass
        else:
            udt_send(packet, endpoint, sock)
        timer.start(timeout_func(packet, endpoint, sock))
        while not rdt_rcv(sock, seq):
            pass
        timer.cancel()
        if seqNum == 0: # switch sequence numbers
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
    rec_cksum  = rdt_utils.parse_checksum(data[5:])
    
    if rdt_utils.has_ack_bit_err() and rdt_utils.random_channel() < config.percent_corrupt:
        if config.debug:
            print("Bit error encountered in ACK!")
        corruptData = rdt_utils.corrupt_bits(ACK)
        calc =  corruptData + recSeq
    elif rdt_utils.has_ack_packet_loss() and rdt_utils.random_channel() < config.percent_corrupt:
        if config.debug:
            print("ACK Packet Dropped!")
        return 0
    else:
        calc = ACK + recSeq
    checksum = rdt_utils.calc_checksum(calc)
    
    return ACK == b'1111' and recSeq == seqNum and rec_cksum == checksum
