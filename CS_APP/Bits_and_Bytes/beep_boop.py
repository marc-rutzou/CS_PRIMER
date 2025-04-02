import sys
import tty

tty.setcbreak(0)

while True:
    x = sys.stdin.read(1)

    try:
        x = int(x)
    except ValueError:
        print(f"input must be an integer")
        continue 

    for _ in range(x):
        sys.stdout.buffer.write(b'\x07')
        
    sys.stdout.buffer.flush()   
