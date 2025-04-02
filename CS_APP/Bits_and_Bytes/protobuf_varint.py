import struct

# first solution working with the binary as a string
def encode2(number: int):
    binary = bin(number) # string 0b... 
    binary = binary[binary.find('b') + 1:] # binary without leading zeros

    # split in parts of 7 bits
    i, parts = 0, []
    while True:
        a = max(0, len(binary) - 7 * (i+1))
        b = max(0, len(binary) - 7 * i)
        parts.insert(0, binary[a:b])
 
        i += 1
 
        if a == 0:
            break
 
    # pad with zeros until 8 bits
    parts = [part.zfill(8) for part in parts]
 
    # convert to Little Endian
    parts.reverse()
 
    # Make the continuation bit 1 for all but the last part
    parts[:-1] = ['1' + part[1:] for part in parts[:-1]]
 
    # Convert to hexadecimal
    return [hex(int(part, 2)) for part in parts]

# follow along with the video
def encode(number):
    ans = []
    while True:
        # other option is to mask out anything but the last 7 bits
        # part = number & 0x7f
        part = number % 2**7
        number = number >> 7
        if number > 0:
            part |= 0b10000000
        else:
            ans.append(part)
            break
        ans.append(part)
    return(bytes(ans)) 

def decode(byte):
    byte = int.from_bytes(byte, byteorder='big')
    ans = 0
    while True: 
        part = byte % 2**8
        part = part & 0b01111111

        byte = byte >> 8 

        # the next 7 bits are worth 2^7 times more
        if byte > 0:
            part *= 2**7
        ans += part

        if byte <= 0:
            break
    return(hex(ans))
         
with open('varint/150.uint64', 'rb') as file:
    data = file.read()
    print(data, type(data))
    number = struct.unpack('>Q', data)[0]
    print("input number: ", number)
    parts = encode(number)
    print(decode(parts))

print(f"Your number is encoded as: {parts}")
print(f"Number of used bytes: {len(parts)}!!")
