import random, math
import numpy as np
import world_config

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

class Weapon(object):
    def __init__(self, n_die, die):
        self.n_die = n_die
        self.die = die

    def damage(self):
        return sum([random.randint(1,self.die) for x in range(self.n_die)])

class Dagger(Weapon):
    def __init__(self):
        super(Dagger, self).__init__(1, 4)
        self.name = "dagger"

class LongSword(Weapon):
    def __init__(self):
        super(Dagger, self).__init__(1, 8)
        self.name = "LongSword"

class Fist(Weapon):
    def __init__(self):
        super(Fist, self).__init__(1,2)
        self.name = "Fist"

class Automata:
    current_lon = 0
    current_lat = 0
    ssn = 0

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
        self.curiosity = random.random()

        # Health and wellness
        self.hit_points = random.randint(7,12) + stat_bonus[self.con]
        self.current_hit_points = self.hit_points

        # Inventory
        self.gold = random.randint(50, 150)
        self.armor_class = 10 + stat_bonus[self.dex]
        self.xp = 0
        self.weapons = []
        self.weapons.append(Fist())

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
            #print("moving to ({lat}, {lon})".format(lat=self.current_lat, lon=self.current_lon))

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
        self.items = []

    def grow(self):
        if random.random() < self.fertility:
            self.food_units += 1


class World:
    #def __init__(self, n_lat, n_lon, n_pop):
    def __init__(self):
        self.day = 0
        self.n_lat = world_config.n_lat
        self.n_lon = world_config.n_lon
        self.cells = np.empty((world_config.n_lat, world_config.n_lon), dtype=object)
        self.population = []
        for i in range(world_config.n_lon):
            for j in range(world_config.n_lat):
                c = Cell(i,j)
                if random.random() < world_config.dagger_density:
                    c.items.append(Dagger())
                self.cells[i,j] = c

        for i in range(world_config.initial_population_size):
            a = Automata()
            a.ssn = i
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
                current_cell = self.cells[p.current_lon, p.current_lat]
                self.consider_move(p, current_cell)
                self.farm_cell(p, current_cell)
                for you in self.population[p.ssn+1:]:
                    if p.ssn != you.ssn and you.current_lon == p.current_lon and you.current_lat == p.current_lat:
                        #print("{me} met {you}".format(me=p.ssn, you=you.ssn))
                        self.automata_interaction(p, you)
                if random.random() < p.curiosity:
                    self.loot_cell(p, current_cell)

        #self.day_report()=
        if len(self.population) <= 0:
            print("Day {day} APOCALPYSE!".format(day=self.day))
            return False
        else:
            return self.day_report()

    def consider_move(self, automata, cell):
        automata.move()
        automata.current_lon = max(min(automata.current_lon, self.n_lon-1),0)
        automata.current_lat = max(min(automata.current_lat, self.n_lat-1),0)

    def farm_cell(self, automata, cell):
        fu = min(automata.hit_points - automata.current_hit_points, cell.food_units)
        cell.food_units -= fu
        #print("cell units left: {u}".format(u=cell.food_units))
        automata.current_hit_points = automata.current_hit_points + fu

    def loot_cell(self, automata, cell):
        for item in cell.items:
            if isinstance(item, Weapon):
                print("got a weapon!")
                automata.weapons.append(item)
                cell.items.remove(item)

    def automata_interaction(self, me, you):
        pass

    def day_report(self):
        #print("Day: {day}\n\tliving population: {pop_size}\n".format(day=self.day, pop_size=len(self.population)))
        return (self.day, len(self.population))
