import sys

with open(sys.argv[1], 'rb') as f:
    for line in f:
        n, line = line[0], line[:-1] # get rid of new_line char

        # loop until you find an ascii char
        while True:
            t = line[1:n + 1]
            if n + 2 < len(line) and line[n + 2] % 0x80 == 0x80:
                n -= 1
            else:
                break


        sys.stdout.buffer.write(t + b'\x0a')


