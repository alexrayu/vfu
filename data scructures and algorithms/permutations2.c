/**
 * @brief Permutations example 2 (in c).
 */  

#include <stdio.h>
#define MAXN 100
const unsigned n = 5;
unsigned a[MAXN];

void print(void)
{
  unsigned i;  
  for (i = 0; i < n; i++) {
    printf("%u", a[i] + 1);
  }
  printf("\n");
}

void permut(unsigned k)
{
  unsigned i, swap;
  if (k == 0) {
    print();
  }
  else {
    permut(k - 1);
    for (i = 0; i < k - 1; i++) {
      swap = a[i];
      a[i] = a[k - 1];
      a[k - 1] = swap;
      permut(k - 1);
      swap = a[i];
      a[i] = a[k - 1];
      a[k - 1] = swap;
    }
  }
}

int main(void)
{
  unsigned i;
  for (i = 0; i < n; i++) {
    a[i] = i;
  }
  permut(n);
  return 0;
}
