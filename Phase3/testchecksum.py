f = open('spongebob.bmp', 'rb')
data = f.read(1024)

bin_sum = 0
for i in range(2, len(data) - 1, 2):
    bin_sum += (data[i] << 8) | data[i+1]
    if bin_sum & int('0x10000', 16):
        print('b4    ', bin(bin_sum))
        bin_sum = bin_sum & int('0xFFFF', 16)
        bin_sum += 1
        print('after ', bin(bin_sum))

checksum = bin_sum ^ 1
print(checksum)
