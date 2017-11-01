CC=clang++
EXEC=celf
INCLUDE=-I/usr/local/include
SRC=celf.cpp player.cpp globals.cpp
FLAGS=-std=c++11
all: $(SRC)
	$(CC) $(FLAGS)  -Wall -o $(EXEC) $(SRC)

run:
	./$(EXEC)
