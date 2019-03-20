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

##       parse_checksum()
##Parameters:
##    byte_data - 16b checksum in form of 2 bytes (big endian)
##Return:
##    checksum integer
def parse_checksum(byte_data):
    return (byte_data[0] << 8) + byte_data[1]

def has_ack_bit_err():
    return config.corrupt_option == 2

def has_data_bit_err():
    return config.corrupt_option == 3

def has_ack_packet_loss():
    return config.corrupt_option == 4

def has_data_packet_loss():
    return config.corrupt_option == 5

class RDTTimer:
    def __init__(self, timeout):
        self.timeout = timeout

    def start(self, func):
        self.timer = Timer(self.timeout, func)
        self.timer.start()

    def cancel(self):
        self.timer.cancel()