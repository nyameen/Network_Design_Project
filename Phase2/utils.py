from collections import deque

def make_packets(fileobj, byte_per_pack):
    data = fileobj.read(byte_per_pack)
    packets = deque()
    while data:
        packets.append(data)
        data = fileobj.read(byte_per_pack)
    return packets
