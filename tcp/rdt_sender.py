import threading
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
    if rdt_utils.has_data_packet_loss() and rdt_utils.random_channel() < config.percent_corrupt:
            if config.debug:
                print("DATA Packet Dropped!")
            return
    return sock.sendto(packet, endpoint)

##       rdt_send()
##Parameters:
##    f   - the file to be sent
##    endpoint -
##      If sending to server: (IP, PORT_NUMBER)
##      If sending to client: client addr
##    sock   - the socket to send through
def rdt_send(f, endpoint, sock):
    # Buffer to hold packets to be sent
    pkt_buff = rdt_utils.PacketBuffer(config.max_buf_size, 1)
    timer = rdt_utils.RDTTimer(config.timeout)

    def go_back_n(endpoint, sock):
        """ Go Back N and resend packets """
        for pkt in pkt_buff.cur_window():
            udt_send(pkt, endpoint, sock)
    
    def timeout_func(endpoint, sock):
        """ Returns callback func for when timeout reached """
        def ret_func():
            """ Restart timer and go back N """
            if config.debug:
                print(f"Timeout for ACK exceeded, resending un-ACKed packets")
            # Tahoe -> reset to 1
            pkt_buff.window_size = 1
            # Forget last timer and start new one
            timer.start(timeout_func(endpoint, sock))
            go_back_n(endpoint, sock)
        return ret_func
    
    def rcv_listen_cb(acknum):
        """ 
            Callback for successful receive 
            Increment base and either cancel or restart timer
        """
        nxt = acknum + 1
        # Don't care if getting previous ack
        if nxt < pkt_buff.base:
            return
        pkt_buff.base = nxt
        if pkt_buff.equal_index():
            timer.cancel()
        else:
            # Restart timer for new window
            timer.start(timeout_func(endpoint, sock))

    # Start thread to get received packets and do callback actions
    # This is necessary as we can't block the main thread from sending packets while we are waiting to receive
    stop_event = threading.Event()
    rcv_listen_thread = threading.Thread(target=rdt_rcv_listen, args=(sock, rcv_listen_cb, stop_event))
    rcv_listen_thread.start()

    # Beginning 3-way handshake
    seq_num = random.randint(0, 1000)
    pkt = TCPPacket.make(seq_num, config.default_window, syn=1)
    rcv_pkt = rdt_rcv(sock)
    if not rcv_pkt.syn or not rcv_pkt.use_ack or rcv_pkt.ack_num != seq_num + 1:
        print("Got bad data")
        return
    ack_num = rcv_pkt.seq_num + 1

    #Begin sending data
    while True:
        time.sleep(0.005)
        # Wait till get acks back so base moves up 
        if not pkt_buff.ready():
            continue
        # Make packet
        pkt = make_pkt(f, pkt_buff.nxt_seq_num)
        # No more packets to make - all sent
        if not pkt:
            # All packets acked -> done
            if pkt_buff.equal_index():
                break
            # Need to keep waiting until all packets acked
            else:
                continue
        # Add to buffer and send
        pkt_buff.add(pkt)
        udt_send(pkt_buff.cur(), endpoint, sock)
        # Start timeout for group
        if pkt_buff.equal_index():
            timer.start(timeout_func(endpoint, sock))
        pkt_buff.nxt_seq_num += 1

    # Send thread event to terminate itself, then wait for join 
    timer.cancel()
    stop_event.set()
    rcv_listen_thread.join()


##       rdt_rcv_listen()
##Parameters:
##    sock     - the socket to send through
##    cb   - callback to execute once non-corrupt pkt is received
##    stop_event - threading stop event to check.  Will exit when set
def rdt_rcv_listen(sock, cb, stop_event):
    while True:
        data = None
        # Do nothing if corrupt - break from loop if set stop condition
        while data is None and not stop_event.is_set():
            data = rdt_rcv(sock)
        # Return from thread if set stop condition
        if stop_event.is_set():
            break
        cb(data)

##       rdt_rcv()
##Parameters:
##    sock     - the socket to send through
def rdt_rcv(sock):    
    data = extract(sock)

    if data == 0:
        return None

    # parse packets
    data = TCPPacket.parse(data)
    my_chksum = rdt_utils.calc_checksum(data.chksum_data())
    if data.chksum != my_chksum:
        print("Checksums didn't match!")
        return None

    return data

