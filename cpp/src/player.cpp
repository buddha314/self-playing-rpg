#include "player.h"
#include "globals.h"

Player::Player(std::string n) {
  name = n;
  str=threeD6();
  con=threeD6();
}
