/**
 * @brief Sets example 2.
 * @see "https://www.cplusplus.com/reference/set/set/"
 */

#include <set>
#include <iostream>
using namespace std;

int main() {
  set <int> sl;
  set <int> ::iterator si;

  sl.insert(3);
  sl.insert(5);
  sl.insert(3); // This value is a duplicate of [0] and should vanish.
  
  for (si = sl.begin(); si != sl.end(); si++) {
    cout << *si << "\n";
  }

  // Oputput: "3\n5";

  return 0;
} 
