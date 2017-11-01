#include "celf.h"
#include <iostream>
#include <time.h>
#include<random>
#include<vector>

int main() {
  srand(time(NULL));
  std::cout<< threeD6()  <<std::endl;
  Player bob("bob");
  std::cout << "Bob's str: " << bob.str << std::endl;
  std::cout << "Bob's con: " << bob.con << std::endl;

  std::vector<std::string> v = {"alice", "betty", "chuck", "deacon", "efram"};

  std::random_device random_device;
  std::mt19937 engine{random_device()};
  std::uniform_int_distribution<int> dist(0, v.size() - 1);
  std::string random_element = v[dist(engine)];
  std::cout << "random element: " << random_element << std::endl;

  for (int i = 0; i < v.size(); i++) {
    Player p(v[dist(engine)]);
    std::cout << "Player " << p.name;
    std::cout << " str: " << p.str;
    std::cout << std::endl;
  }
}
