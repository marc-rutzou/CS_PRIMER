import os
import re

def hex_to_rgb(hexa):
    """
    problem: if the left byte is zero then int(a, 16) does cut it off
    """
    hexa_mod = hexa.split('#')[1]
    out = []

    if len(hexa_mod) < 6:
        # double the first three digits
        hexa_mod_mod = ''
        for i in range(3):
            hexa_mod_mod += hexa_mod[i] + hexa_mod[i]
        hexa_mod = hexa_mod_mod + hexa_mod[3:]

    opacity = ''
    if len(hexa_mod) > 6:
        opacity = hexa_mod[6:]
        if len(opacity) == 1:
            opacity = opacity + opacity
        hexa_mod = hexa_mod[:6]


    print("hexa", hexa_mod)

    n = int(hexa_mod, 16) 
    while True:
        byte = n & 0xff
        out.insert(0, byte)

        n >>= 8

        if n <= 0:
            break

    while len(out) < 3:
        out.insert(0, 0)

    if opacity:
        out.append(int(opacity, 16)/255)
        
    return out

files = ['simple.css', 'advanced.css']
for file in files:
    with open('color-convert/' + file, 'r') as f: 
        css = f.read()
        colors_hex = re.findall('#[0-9a-fA-F]+', css)
        for hexa in colors_hex:
            print("ans: ", hex_to_rgb(hexa))
            # print(hex_to_rgb(hexa))
