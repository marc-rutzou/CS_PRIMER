import struct

def le(bs):
    n = 0
    for i, b in enumerate(bs):
        n += b << (8 * i)
    return n

def be(bs):
    n = 0
    for b in bs: 
        n = (n << 8) + b
    return n

with open('syn-flood/synflood.pcap', 'rb') as f:
    data = f.read()

# first 24 bytes are PCAP header
snaplen = le(data[16:20])
print(f"SnapLen: {snaplen}")

packets = data[24:]

i, good, attack = 0, 0, 0
while i < len(packets):
    cap_len = le(packets[i+8:i+12])
    ori_len = le(packets[i+12:i+16])

    # different size if packet is truncated to max packet length: never
    assert cap_len == ori_len

    packet = packets[i + 16: i + 16 + cap_len]

    link_header = le(packet[:4])
    assert link_header == 2

    # number of 32-bit (4 byte) words in IPv4 packet header
    ihl = int(hex(packet[4])[-1]) * 4
    ip_header = packet[4:4 + ihl]

    # TCP begins after ihl + 4
    begin = ihl + 4
    flags = packet[begin + 13: begin + 14]
    binary = struct.unpack('b', flags)[0]

    syn, ack = 0, 0 
    if binary & 0x02 == 2:
        syn = 1
    
    if binary & 0x10 == 16:
        ack = 1

    if syn == 1 and ack == 1:
        good += 1
    elif syn == 1 and ack == 0:
        attack += 1
    
    i += 16 + cap_len 

print(good, attack)
print(attack / (attack + good))

