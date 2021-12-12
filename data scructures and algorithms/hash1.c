 /**
 * @brief Hash example 1 (in c).
 */  

#include <stdio.h>

unsigned long hashFunction(const char *key, unsigned long size)
{
  unsigned long result = 0;
  while (*key)
    result += (unsigned char) *key++;
  return result % size;
}

int main(void)
{
  printf("%lu", hashFunction("12345", 3));

  return 0;
}
