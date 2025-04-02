#include <stdio.h>
#include <assert.h>
#include <limits.h>

int bitcount(unsigned int);
int fast_bitcount(unsigned int);

int main() { 
    unsigned int n; /*To avoid arithmatic shift*/

    n = 7; 
    assert(bitcount(n) == 3);
    printf("%d\n", fast_bitcount(n));
    printf("%d %u\n", INT_MAX, -1);
}

int fast_bitcount(unsigned int n) {
    /*count the number of times you can do that*/
    for (int i; n; n &= n - 1, i++)
    return i;
}

int bitcount(unsigned int n){
    int count = 0;
    for (; n != 0; n >>= 1) {
        if ((n & 0x01) == 0x01)
            count ++; 
    }
    return count;
}

