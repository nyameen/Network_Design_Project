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

def seq_num_to_bin(num):
    ''' 
        Translate decimal sec num to bin.  
        Use zero-fill to ensure it is 16 bits wide 
        16 bits used here to ensure there is enough space for all potential sequence nums
    '''
    return bin(num)[2:].encode('utf-8').zfill(16)

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
        self.completed = False

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

    def complete(self):
        self.timer.cancel()
        self.completed = True


class SNDPacketBuffer:
    def __init__(self, buf_size, window_size, timeout):
        self.buf = [0] * buf_size
        self.nxt_seq_num = 0
        self.base = 0
        self.window_size = window_size
        self.timers = [RDTTimer(timeout) for _ in range(buf_size)]
        
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

    def increment_base(self):
        """ Increment base to next unacked packet """
        while self.timers[self.base].completed:
            self.base += 1


class RCVPacketBuffer:
    def __init__(self, buf_size, window_size):
        self.buf = [None] * buf_size
        self.base = 0
        self.window_size = window_size

    def includes(self, pkt_num):
        return pkt_num >= self.base and pkt_num < self.base + self.window_size


        


