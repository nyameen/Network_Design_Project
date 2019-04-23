import random
import config
from threading import Timer

#      corrupt_bits()
##Parameters:
##  pkt        - either ACK or DATA 
def corrupt_bits(pkt):
    index = random.randint(0, len(pkt)-1)
    pkt = pkt[:index] + bytearray(chr(random.randint(0, 95)),'utf-8') + pkt[index+1:]
    return pkt

##      random
##Parameters:
##  none
def random_channel():

    choice = random.randint(0,99)
    return choice

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

def num_to_bin(num, num_bits=1):
    return bin(num)[2:].encode('utf-8').zfill(num_bits)

##       parse_checksum()
##Parameters:
##    byte_data - 16b checksum in form of 2 bytes (big endian)
##Return:
##    checksum integer
def parse_checksum(byte_data):
    return (byte_data[0] << 8) + byte_data[1]

# Corruption helper functions below 
def has_ack_bit_err():
    return config.corrupt_option == 2

def has_data_bit_err():
    return config.corrupt_option == 3

def has_ack_packet_loss():
    return config.corrupt_option == 4

def has_data_packet_loss():
    return config.corrupt_option == 5


class RDTTimer:
    """ Timer class for usage in RDT """
    def __init__(self, timeout):
        self.timeout = timeout
        self.timer = None

    def start(self, func):
        """ 
            Start a timer with the given timeout function
            Cancels running timer if applicable
        """
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.timeout, func)
        self.timer.start()

    def cancel(self):
        """ Cancel current timer """
        self.timer.cancel()


class PacketBuffer:
    def __init__(self, buf_size, window_size):
        self.buf = [0] * buf_size
        self.nxt_seq_num = 0
        self.base = 0
        self.window_size = window_size
        
    def update_window_size(self, new_size):
        self.window_size = new_size

    def cur_window(self):
        """ Returns list slice of packets from base to nxt_seq_num """
        return self.buf[self.base:self.nxt_seq_num]

    def add(self, pkt):
        """ Add packet to buffer """
        self.buf[self.nxt_seq_num] = pkt

    def cur(self):
        """ Returns packet at next seq num """
        return self.buf[self.nxt_seq_num]

    def equal_index(self):
        """ Retuns if base has caught up to nxt_seq_num """
        return self.base == self.nxt_seq_num

    def ready(self):
        """ Ready to send more packets """
        return self.nxt_seq_num < self.base + self.window_size


class TCPData:
    def __init__(self, seq_num, ack_num, use_ack, rst, syn, fin, chksum, data):
        self.seq_num_b = seq_num
        self.ack_num_b = ack_num
        self.use_ack_b = use_ack
        self.rst_b = rst
        self.syn_b = syn
        self.fin_b = fin
        self.data_b = data

        self.seq_num = int(seq_num, 2)
        self.ack_num = int(ack_num, 2)
        self.use_ack = int(use_ack, 2)
        self.rst = int(rst, 2)
        self.syn = int(syn, 2)
        self.fin = int(fin, 2)
        self.data = int(data, 2)

    def chksum_data(self):
        return seq_num_b + ack_num_b + use_ack_b + rst_b + syn_b + fin_b + data_b

class TCPPacket:
    @staticmethod
    def make(seq_num, rcv_window, f=None, bytesize=1024, ack_num=None, rst=0, syn=0, fin=0):
        use_ack = ack_num is not None
        if ack_num is None:
            ack_num = 0

        seq_num_b = rdt_utils.num_to_bin(seq_num, 32)
        ack_num_b = rdt_utils.num_to_bin(ack_num, 32)
        use_ack_b = rdt_utils.num_to_bin(use_ack)
        rst_b = rdt_utils.num_to_bin(rst)
        syn_b = rdt_utils.num_to_bin(syn)
        fin_b = rdt_utils.num_to_bin(fin)

        data = f.read(bytesize) if f else 0
        if data == b'':
            return 0
        calc = seq_num_b + ack_num_b + use_ack_b + rst_b + syn_b + fin_b + data
        chksum = rdt_utils.calc_checksum(calc)

        chksum_bytes = (chksum).to_bytes(2, byteorder='big')
        packet = seq_num_b + ack_num_b + use_ack_b + rst_b + syn_b + fin_b + chksum_bytes + data
        return packet

    @staticmethod
    def parse(packet):
        seq_num = packet[0:32]
        ack_num = packet[32:64]
        use_ack = packet[64:65]
        rst = packet[65:66]
        syn = packet[66:67]
        fin = packet[67:68]
        chksum = packet[68:84]
        data = packet[84:]

        return TCPData(seq_num, ack_num, use_ack, rst, syn, fin, chksum, data)


