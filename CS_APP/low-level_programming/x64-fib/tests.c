#include <assert.h>
#include <stdio.h>

extern int fib(int n);

int main(void) {
  assert(fib(0) == 0);
  assert(fib(1) == 1);
  assert(fib(2) == 1);
  assert(fib(3) == 2);
  printf("%d\n", fib(4));
  assert(fib(6) == 8);
  assert(fib(10) == 55);
  assert(fib(12) == 144);
  printf("OK\n");
}
