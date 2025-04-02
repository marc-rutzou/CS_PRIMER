
def bytes_to_int(byte_str):
    """ reverse the byte str because little endian """
    n = 0
    for byte in byte_str[::-1]:
        n = (n << 8) + byte
    return n


def rotate(image, width, height, bytes_per_pixel):
    row_length = width * bytes_per_pixel

    keys = range(height)
    r_image = dict(zip(list(keys), [b''] * len(list(keys))))
    print(r_image)

    temp_image = b''

    row_number = 0
    for i in range(0, len(image), row_length):
        row = image[i:i + row_length]
        
        first_pixel = row[:3]
        
        r_image[row_number] = first_pixel + r_image[row_number]

        # remove the first pixel from the original image
        temp_image += image[i+3:i + row_length]
        
        row_number += 1


    print(r_image)




with open('image-rotate/teapot.bmp', 'rb') as f:
    file_header = f.read(14)

    offset = bytes_to_int(file_header[10:])
    print("offset: ", offset)
    
    # the rest of the header
    dib_header = f.read(124)
    width = bytes_to_int(dib_header[4:8])
    height = bytes_to_int(dib_header[8:12])
    bytes_per_pixel = bytes_to_int(dib_header[14:16]) // 8

    print(f"width: {width}, height: {height}, bytes per pixel: {bytes_per_pixel}")

    image = f.read()
    rotated_image = rotate(image, width, height, bytes_per_pixel)

# In the end I need to concat the header and the rotated image data to get a valid BMP
