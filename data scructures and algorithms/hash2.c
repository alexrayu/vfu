 /**
 * @brief Hash example 2 (in c).
 */  

#include <stdio.h>

unsigned long hash_a(unsigned char *str)
{
  unsigned int hash = 0;
  unsigned int c;
  while (c = *str++)
    hash = ((hash << 5) + hash) + c;
  
  return hash;
}

int main(void)
{
  printf("%lu", hash_a((unsigned char *) "There will come soft rains."));

  return 0;
}
