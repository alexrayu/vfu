#include <set>
#include <iostream>
using namespace std;

int main() {
  set <int> sl;

  sl.insert(3);
  sl.insert(5);
  sl.insert(3); // This value is a duplicate of [0] and should vanish.
  cout << *sl.begin(); // Prints the first element.
  cout << *sl.begin(); // Prints the first element (again).

  return 0;
}
