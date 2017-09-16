import random, math
import numpy as np

stat_bonus = {}
stat_bonus[3] = -4
stat_bonus[4] = -3
stat_bonus[5] = -3
stat_bonus[6] = -2
stat_bonus[7] = -2
stat_bonus[8] = -1
stat_bonus[9] = -1
stat_bonus[10] = 0
stat_bonus[11] = 0
stat_bonus[12] = 1
stat_bonus[13] = 1
stat_bonus[14] = 2
stat_bonus[15] = 2
stat_bonus[16] = 3
stat_bonus[17] = 3
stat_bonus[18] = 4


class Automata:
    current_lon = 0
    current_lat = 0

    def __init__(self):
        # Stats
        self.str = sum([random.randint(1,6) for x in range(3)])
        self.dex = sum([random.randint(1,6) for x in range(3)])
        self.con = sum([random.randint(1,6) for x in range(3)])
        self.int = sum([random.randint(1,6) for x in range(3)])
        self.wis = sum([random.randint(1,6) for x in range(3)])
        self.cha = sum([random.randint(1,6) for x in range(3)])

        # Personality dimensions
        self.bravado = random.random()
        self.gregariousness = random.random()
        self.aggressiveness = random.random()

        # Health and wellness
        self.hit_points = random.randint(7,12) + stat_bonus[self.con]
        self.current_hit_points = self.hit_points

    def decide_to_travel(self):
        r = math.tanh(self.bravado - self.aggressiveness)
        if random.random() < r:
            return True
        else:
            return False

    def move(self):
        if self.decide_to_travel():
            self.current_lon = self.current_lon + random.randint(-1,1)
            self.current_lat = self.current_lat + random.randint(-1,1)
            print("moving to ({lat}, {lon})".format(lat=self.current_lat, lon=self.current_lon))

    def age(self):
        self.current_hit_points += -1
        return self.current_hit_points

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.fertility = random.random()
        self.fertility = random.random()
        self.food_units = random.randint(0,10)

    def grow(self):
        if random.random() < self.fertility:
            self.food_units += 1


class World:
    def __init__(self, n_lat, n_lon, n_pop):
        self.day = 0
        self.n_lat = n_lat
        self.n_lon = n_lon
        self.cells = np.empty((n_lat, n_lon), dtype=object)
        self.population = []
        for i in range(n_lon):
            for j in range(n_lat):
                self.cells[i,j] = Cell(i,j)

        for i in range(n_pop):
            a = Automata()
            a.current_lon = random.randint(0,self.n_lat-1)
            a.current_lat = random.randint(0,self.n_lon-1)
            self.population.append(a)

    def one_day(self):
        self.day += 1
        for p in self.population:
            h = p.age()
            if h <= 0:
                self.population.remove(p)
            else:
                a_cell = self.cells[p.current_lon, p.current_lat]
                self.consider_move(p, a_cell)
                self.farm_cell(p, a_cell)

        self.day_report()
        if len(self.population) <= 0:
            print("Day {day} APOCALPYSE!".format(day=self.day))
            return False
        else:
            return True

    def consider_move(self, automata, cell):
        automata.move()
        automata.current_lon = max(min(automata.current_lon, self.n_lon-1),0)
        automata.current_lat = max(min(automata.current_lat, self.n_lat-1),0)

    def farm_cell(self, automata, cell):
        fu = min(automata.hit_points - automata.current_hit_points, cell.food_units)
        cell.food_units -= fu
        #print("cell units left: {u}".format(u=cell.food_units))
        automata.current_hit_points = automata.current_hit_points + fu

    def day_report(self):
        print("Day: {day}\n\tliving population: {pop_size}\n".format(day=self.day, pop_size=len(self.population)))
