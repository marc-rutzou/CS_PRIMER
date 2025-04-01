// loop unrolling
// unnecessary memory references
// reduce procedure calls

/* 
int sum(int *nums, int n) {
  int total = 0;
  long i; 
  int acc1, acc2, acc3, acc4, acc11, acc22;
  for (i = 0; i < n - 7; i += 8)
    acc1 = nums[i] + nums[i + 1];
    acc2 = nums[i + 2] + nums[i + 3];
    acc3 = nums[i + 4] + nums[i + 5];
    acc4 = nums[i + 6] + nums[i + 7];
    acc11 = acc1 + acc2;
    acc22 = acc3 + acc4;
    total += acc11 + acc22;
  for (; i < n; i++)
    total += *(nums + i);
  return total;
}
*/

int sum(int *nums, int n) {
  int t1 = 0, t2 = 0, t3 = 0, t4 = 0;
  for (int i = 0; i < n - 3; i+=4) {
    t1 += nums[i];
    t2 += nums[i + 1];
    t3 += nums[i + 2];
    t4 += nums[i + 3];
  }
  return t1 + t2 + t3 + t4;
}
