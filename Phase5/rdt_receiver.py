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
        return data, addr
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
    pkt = ACK + seq_num
    chksum = rdt_utils.calc_checksum(pkt)
    chksum_bytes = (chksum).to_bytes(2, byteorder='big')
    return pkt + chksum_bytes

##       rdt_rcv()
##Parameters:
##    f- the file to be sent
##    sock     - the socket to send through            
##Return:
##   endpoint that got messages from
def rdt_rcv(fname, sock):
    expected_seq_num = 0
    expected_seq_num_b = rdt_utils.seq_num_to_bin(expected_seq_num)
    ACK = bin(15)[2:].encode('utf-8')

    oncethru = False
    endpoint = None # Endpoint starts off unitialized, get it from first received packet
    f = None # Don't open file until know that we received message
    sndpkt = None
    while True:
        pkt, addr = extract(sock)
        # Initialize endpoint with actual addr received
        if not endpoint and addr:
            endpoint = addr
        # Got actual message
        if pkt and addr:
            # Open file if not opened
            if not f:
                f = open(fname, 'wb')
            #parse packet
            rec_seq = pkt[0:16]
            rec_ck = rdt_utils.parse_checksum(pkt[16:18])
            data = pkt[18:]
            
            
            if rdt_utils.has_data_bit_err() and rdt_utils.random_channel() < config.percent_corrupt:
                if config.debug:
                    print("Bit error encountered in Data!")
                corruptData = rdt_utils.corrupt_bits(data)
                calc = rec_seq + corruptData
            else:
                calc = rec_seq + data
        
            chksum = rdt_utils.calc_checksum(calc)
            
            # correct sequence number
            if expected_seq_num_b == rec_seq and chksum == rec_ck:
                deliver_data(f, data)
                sndpkt = make_pkt(ACK, rec_seq)
                udt_send(sndpkt, endpoint, sock)

                expected_seq_num += 1
                expected_seq_num_b = rdt_utils.seq_num_to_bin(expected_seq_num)
            else:
                # didn't receive right pkt, either seqnum wrong or cksum
                if config.debug:
                    print("Bad data received, sending prev ACK")
                if oncethru and sndpkt:
                    udt_send(sndpkt, endpoint, sock)
        else:
            # Close file if opened
            if f:
                f.close()
            break
        oncethru = True
    return endpoint
            
