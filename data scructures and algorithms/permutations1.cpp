/**
 * @brief Permutations example 1.
 */  

#include <iostream>
#include <algorithm>
using namespace std;

int main() 
{
  char v[] = "abcd";

  do {
    cout << v << endl;
  } while (next_permutation(v, v + 4));

  return 0;
}