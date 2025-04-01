#include <stdio.h>

extern unsigned char quantize(unsigned char red, unsigned char green, unsigned char blue);

int main() {
    unsigned char red = 0xff, green = 0x00, blue = 0x00, out;
    out = quantize(red, green, blue);
    printf("\n%x\n", out & 0xff); 
    printf("\n%d\n", 100 / 64);
}
