import random, math
import numpy as np
import world_config
from weapons import *
from armor import *

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
    ssn = 0
    total_combats = 0
    successful_combats = 0
    total_lootings = 0
    successful_lootings = 0

    def __init__(self):
        # Stats
        self.str = sum([random.randint(1,6) for x in range(3)])
        self.dex = sum([random.randint(1,6) for x in range(3)])
        self.con = sum([random.randint(1,6) for x in range(3)])
        self.int = sum([random.randint(1,6) for x in range(3)])
        self.wis = sum([random.randint(1,6) for x in range(3)])
        self.cha = sum([random.randint(1,6) for x in range(3)])

        # Personality dimensions
        self.bravado = math.tanh(random.random())
        self.gregariousness = math.tanh(random.random())
        self.aggressiveness = math.tanh(random.random())
        self.curiosity = math.tanh(random.random())

        # Health and wellness
        self.hit_points = random.randint(7,12) + stat_bonus[self.con]
        self.current_hit_points = self.hit_points

        # Inventory
        self.gold = random.randint(50, 150)
        self.armor_class = 10 + stat_bonus[self.dex]
        self.xp = 0
        self.weapons = []
        self.weapons.append(Fist())
        self.shield = NoShield()
        self.armor = None
        self.ready_weapon = Fist()

    def get_aggressiveness(self):
        if self.total_combats > 0:
            return math.tanh(self.successful_combats / self.total_combats)
        else:
            return math.tanh(random.random())

    def get_curiosity(self):
        if self.total_lootings > 0:
            return math.tanh(self.successful_lootings / self.total_lootings)
        else:
            return math.tanh(random.random())

    def get_bravado(self):
        return math.tanh(random.random())

    def decide_to_travel(self):
        r = self.get_bravado()
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

    def ac(self):
        #return self.shield.ac_bonus + self.armor_bonus + stat_bonus[self.dex]
        return self.shield.ac_bonus  + stat_bonus[self.dex]

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
                if random.random() < world_config.smallshield_density:
                    c.items.append(SmallShield())
                if random.random() < world_config.largeshield_density:
                    c.items.append(LargeShield())

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
                if random.random() < p.get_curiosity():
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
        automata.total_lootings += 1
        if len(cell.items) > 0:
            automata.successful_lootings += 1
            automata.curiosity +=  math.tanh(automata.successful_lootings/automata.total_lootings)
        for item in cell.items:
            if isinstance(item, Weapon):
                automata.weapons.append(item)
                cell.items.remove(item)
                if isinstance(automata.ready_weapon, Fist):
                    automata.ready_weapon = item
            if isinstance(item, (SmallShield, LargeShield)) and isinstance(automata.shield, NoShield):
                automata.shield = item
                cell.items.remove(item)

    def automata_interaction(self, me, you):
        self.combat(me, you)

    def combat(self, me, you):
        me.total_combats += 1
        you.total_combats += 1
        first = me
        second = you
        if me.dex < you.dex:
            first = you
            second = me
        elif me.dex == you.dex:
            first = me
            second = you
        print("Fight! {id} goes first".format(id=first.ssn))
        roll = random.randint(1,20)
        if roll + stat_bonus[first.str] > second.ac():
            damage = max(0,first.ready_weapon.damage() + stat_bonus[first.str])
            second.current_hit_points -= damage
            print("\tA touch! Damage: {d}".format(d= damage))
        if second.current_hit_points <= 0:
            first.successful_combats += 1
            first.aggressiveness += first.successful_combats / first.total_combats
            first.gold += second.gold
            self.population.remove(second)
            print("\t{id} is dead".format(id=second.ssn))
            return
        # Second gets her turn
        roll = random.randint(1,20)
        if roll + stat_bonus[second.str] > first.ac():
            damage = max(0,second.ready_weapon.damage() + stat_bonus[second.str])
            first.current_hit_points -= damage
            print("\tA touch! Damage: {d}".format(d= damage))
        if first.current_hit_points <= 0:
            second.successful_combats += 1
            second.aggressiveness += second.successful_combats / second.total_combats
            second.gold += first.gold
            self.population.remove(first)
            print("\t{id} is dead".format(id=first.ssn))
            return

    def day_report(self):
        #print("Day: {day}\n\tliving population: {pop_size}\n".format(day=self.day, pop_size=len(self.population)))
        numcur = 0
        numbrv = 0
        numagg = 0
        numgreg = 0
        numgold = 0
        for p in self.population:
            numcur += p.get_curiosity()
            numbrv += p.bravado
            numagg += p.get_aggressiveness()
            numgreg += p.gregariousness
            numgold += p.gold
        return (self.day, len(self.population)
            , numcur/len(self.population)
            , numbrv/len(self.population)
            , numagg/len(self.population)
            , numgreg/len(self.population)
            , numgold/len(self.population)
            )

class Day(object):
    def __init__(self):
        self.fights = 0
        self.population = 0
        self.murders = 0
