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
    rcv_buf = rdt_utils.RCVPacketBuffer(config.max_buf_size, config.window_size)
    ACK = bin(15)[2:].encode('utf-8')

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
            
            rec_seq_int = int(rec_seq, 2)
            if chksum == rec_ck:
                sndpkt = make_pkt(ACK, rec_seq)
                if rcv_buf.includes(rec_seq_int):
                    udt_send(sndpkt, endpoint, sock)
                    rcv_buf.buf[rec_seq_int] = data
                    # Inorder
                    if rec_seq_int == rcv_buf.base:
                        while rcv_buf.buf[rcv_buf.base] is not None:
                            deliver_data(f, rcv_buf.buf[rcv_buf.base])
                            rcv_buf.base += 1
                elif rec_seq_int < rcv_buf.base:
                    udt_send(sndpkt, endpoint, sock)
            else:
                # didn't receive right pkt, wrong cksum
                if config.debug:
                    print("Bad data received, doing nothing")
        else:
            # Close file if opened
            if f:
                f.close()
            break
    return endpoint
            
