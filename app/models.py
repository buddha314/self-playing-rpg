import random, math
import copy
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
        self.inventory = []

    def adaptability(self):
        return (self.wis + self.int)/36

    def get_aggressiveness(self):
        s = (self.str+self.con)/36.0
        if self.total_combats > 0:
            s+= self.adaptability() * (self.successful_combats/self.total_combats - 1/2)
            #s = (self.str+self.con)/36.0 + self.adaptability() * (self.successful_combats/self.total_combats - 1/2)
            #return math.tanh(s)
        else:
            s = (self.str+self.con)/36.0
            return math.tanh(s)
        return math.tanh(s)

    def get_curiosity(self):
        s = self.int/18.0
        if self.total_lootings > 0:
            s+= self.adaptability() * (self.successful_lootings / self.total_lootings - 1/2)
        return math.tanh(s)

    def get_bravado(self):
        s = self.con / 18.0 + self.adaptability() * (self.current_hit_points / self.hit_points - 1/2)
        return math.tanh(s)

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

    def loot_cell(self, cell):
        self.total_lootings += 1
        for item in cell.items:
            if isinstance(item, Weapon):
                self.weapons.append(item)
                if isinstance(self.ready_weapon, Fist):
                    self.ready_weapon = item
            if isinstance(item, (SmallShield, LargeShield)):
                self.inventory.append(item)
                if isinstance(self.shield, NoShield):
                    self.shield = item
            cell.items.remove(item)
        self.gold += cell.gold
        cell.gold = 0

    def farm_cell(self, cell):
        fu = min(self.hit_points - self.current_hit_points, cell.food_units)
        cell.food_units -= fu
        #print("cell units left: {u}".format(u=cell.food_units))
        cell.current_hit_points = self.current_hit_points + fu

    def initiative(self):
        return 10 + stat_bonus[self.dex]


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.fertility = random.random()
        self.fertility = 0
        self.food_units = random.randint(0,10)
        self.items = []
        self.gold = random.randint(0,10)

    def grow(self):
        if random.random() < self.fertility:
            self.food_units += 1
            return 1
        else:
            return 0

class Game:
    def __init__(self, world, ndays=365, nyears=1):
        self.ndays = ndays
        self.nyears = 1
        self.world = world
        self.days = []

    def run(self):
        for i in range(self.ndays * self.nyears):
            today = Day(i)
            go = self.run_day(today)
            if go:
                continue
            else:
                break


    def run_day(self, today):
        # Cell actions
        for i in range(self.world.n_lon):
            for j in range(self.world.n_lat):
                cell = self.world.cells[i,j]
                today.new_food_units += cell.grow()

        # Automata actions
        for p in self.world.population:
            p.age()
            if p.current_hit_points <= 0:
                today.starvations += 1
                self.world.population.remove(p)
                continue
            # Individual actions
            current_cell = self.world.cells[p.current_lon, p.current_lat]
            if random.random() < p.get_curiosity():
                today.lootings += 1
                today.farmings += 1
                p.loot_cell(current_cell)
                p.farm_cell(current_cell)

                # Automata Interactions
                for q in self.world.population[p.ssn+1:]:
                    if p.current_cell == q.current_cell:
                        today.interactions += 1
                        self.interaction(today, p, q)


        if len(self.world.population) <= 0:
            print("Day {day} APOCALPYSE!!".format(day=today.day_number))
            return False
        else:
            self.build_report(today)
            self.days.append(today)
            return True

    def build_report(self, today):
        today.population_size = copy.copy(len(self.world.population))
        for p in self.world.population:
            today.avg_curiosity += p.get_curiosity() / today.population_size
            today.avg_bravado += p.get_bravado() / today.population_size
            today.avg_gold += 1.0 * p.gold / today.population_size
            today.avg_aggression += p.get_aggressiveness() / today.population_size

    def report(self):
        report = []
        for day in self.days:
            day.build_report()
            report.append(day.report)
        return report

    def interaction(self, today, me, you):
        if random.random() < (me.get_aggressiveness() + you.get_aggressiveness()) / 2:
            today.combats += 1
            self.combat(today, me, you)
            print("Fight!")
        else:
            print("no combat")

    def combat(self, today, me, you):
        me.total_combats +=1
        you.total_combats +=1
        if me.initiative() > you.initiative():
            if self.attack(today, me, you):
                self.attack(today, you, me)
        elif me.initiative() < you.initiative():
            if self.attack(today, you, me):
                self.attack(today, me, you)
        elif random.random() < 0.5:
            if self.attack(today, me, you):
                self.attack(today, you, me)
        else:
            if self.attack(today, you, me):
                self.attack(today, me, you)

    def attack(self, today, attacker, target):
        roll = random.randint(1,20)
        if roll + stat_bonus[attacker.str] > target.ac():
            damage = max(0, attacker.ready_weapon.damage()) + stat_bonus[attacker.str]
            target.current_hit_points -= damage
            if target.current_hit_points <= 0:
                print("Murder!")
                self.world.population.remove(target)
                today.murders +=1
                attacker.successful_combats += 1
                return False
            else:
                return True


class World:
    days = []
    def __init__(self):
        self.day = 0
        self.n_lat = world_config.n_lat
        self.n_lon = world_config.n_lon
        self.cells = np.empty((world_config.n_lat, world_config.n_lon), dtype=object)
        self.population = []
        self.generate_cells()
        self.build_population()

    def generate_cells(self):
        for i in range(world_config.n_lon):
            for j in range(world_config.n_lat):
                c = Cell(i,j)
                c.fertility = world_config.farmland_fertility
                if random.random() < world_config.dagger_density:
                    c.items.append(Dagger())
                if random.random() < world_config.smallshield_density:
                    c.items.append(SmallShield())
                if random.random() < world_config.largeshield_density:
                    c.items.append(LargeShield())
                self.cells[i,j] = c

    def build_population(self):
        for i in range(world_config.initial_population_size):
            a = Automata()
            a.ssn = i
            x = random.randint(0,self.n_lat-1)
            y = random.randint(0,self.n_lon-1)
            #a.current_lon = random.randint(0,self.n_lat-1)
            #a.current_lat = random.randint(0,self.n_lon-1)
            a.current_cell = self.cells[x,y]
            self.population.append(a)

    """
    def one_day(self):
        #today = Day(self.day +1, self.population)
        today = Day(copy.copy(self.day))
        self.day += 1
        today.population_size = copy.copy(len(self.population))
        for p in self.population:
            h = p.age()
            if h <= 0:
                today.starvations += 1
                self.population.remove(p)
            else:
                current_cell = self.cells[p.current_lon, p.current_lat]
                self.consider_move(p, current_cell)
                self.farm_cell(p, current_cell)
                #for you in self.population[p.ssn+1:]:
                for you in today.population[p.ssn+1:]:
                    if p.ssn != you.ssn and you.current_lon == p.current_lon and you.current_lat == p.current_lat:
                        #print("{me} met {you}".format(me=p.ssn, you=you.ssn))
                        self.automata_interaction(today, p, you)
                if random.random() < p.get_curiosity():
                    self.loot_cell(day=today, automata=p, cell=current_cell)
        self.day_report(today)
        self.days.append(today)
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
    """

class Day(object):
    def __init__(self, day):
        self.day_number = day
        self.lootings = 0
        self.report = {}
        self.avg_curiosity = 0.0
        self.avg_bravado = 0.0
        self.avg_gold = 0.0
        self.avg_aggression = 0.0
        self.avg_gregariousness = 0.0
        self.combats = 0.0
        self.murders = 0
        self.starvations = 0
        self.interactions = 0
        self.farmings = 0
        self.new_food_units = 0


    def build_report(self):
        self.report['day_number'] = self.day_number
        self.report['starvations'] = self.starvations
        self.report['combats'] = self.combats
        self.report['avg_gold'] = self.avg_gold
        self.report['avg_aggression'] = self.avg_aggression
        self.report['avg_bravado'] = self.avg_bravado
        self.report['avg_curiosity'] = self.avg_curiosity
        self.report['avg_gregariousness'] = self.avg_gregariousness
        self.report['interactions'] = self.interactions
        self.report['lootings'] = self.lootings
        self.report['farmings'] = self.farmings
        self.report['murders'] = self.murders
        self.report['new_food_units'] = self.new_food_units
        return self.report
