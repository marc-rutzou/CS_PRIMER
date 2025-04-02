import struct

def conceal(s):
    b = bytes(s, encoding='ascii')
    assert len(b) <= 6, "Your message needs to be shorter!"
    if len(b) < 6:
        b = bytes(6 - len(b)) + b
    return struct.unpack('>d', bytes([0b01111111, 0b11110000, \
                                b[-6], b[-5], b[-4], b[-3], b[-2], b[-1]]))[0]

def extract(x):
    m = struct.pack('>d', x)[2:]
    i = 0
    for i in range(len(m)):
        if m[i] == 0x00:
            out = m[i+1:]
        else:
            break
    return str(out, encoding='ascii')

if __name__ == "__main__":
    s = 'hello'

    print(conceal(s))

    print(extract(conceal(s)))
    assert extract(conceal(s)) == s
