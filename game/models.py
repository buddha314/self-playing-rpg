import random, math
import world_config
from world_config import stat_bonus

class Player:
    current_lon = 0
    current_lat = 0
    ssn = 0
    total_combats = 0
    successful_combats = 0
    total_lootings = 0
    successful_lootings = 0

    def __init__(self, name):
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
        self.shield = None
        self.armor = None
        self.ready_weapon = Fist()
        self.inventory = []
        self.speed = 5.25
        self.name = name
        self.alive = True

    def adaptability(self):
        return (self.wis + self.int)/36

    def get_aggressiveness(self):
        s = (self.str+self.con)/36.0
        if self.total_combats > 0:
            s+= self.adaptability() * (self.successful_combats/self.total_combats - 1/2)
        return math.tanh(s)

    def get_curiosity(self):
        s = self.int/18.0
        if self.total_lootings > 0:
            s+= self.adaptability() * (self.successful_lootings / self.total_lootings - 1/2)
        return math.tanh(s)

    def get_bravado(self):
        s = self.con / 18.0 + self.adaptability() * (self.current_hit_points / self.hit_points - 1/2)
        return math.tanh(s)

    def choose_direction(self):
        theta = 2 * math.pi * random.random()
        return theta

    def get_speed(self):
        return 5.25

    """
     Returns a tuple of (delta_x, delta_y, delta_z)
    """
    def move(self):
        if random.random() < self.get_bravado():
            return (self.get_speed() * math.cos(self.choose_direction())
                  , self.get_speed() * math.sin(self.choose_direction())
                  ,0)
        else:
            return (0,0,0)

    def age(self):
        self.current_hit_points += -1
        return self.current_hit_points

    def ac(self):
        #return self.shield.ac_bonus + self.armor_bonus + stat_bonus[self.dex]
        if self.shield is None:
            return stat_bonus[self.dex]
        else:
            return self.shield.ac_bonus  + stat_bonus[self.dex]

    def loot_cell(self, cell):
        self.total_lootings += 1
        wpns = 0
        gld = 0
        armr = 0
        for item in cell.items:
            if isinstance(item, Weapon):
                self.weapons.append(item)
                if isinstance(self.ready_weapon, Fist):
                    self.ready_weapon = item
                wpns += 1
            if isinstance(item, (SmallShield, LargeShield)):
                self.inventory.append(item)
                if isinstance(self.shield, NoShield):
                    self.shield = item
                armr += 1
            cell.items.remove(item)
        gld += cell.gold
        self.gold += cell.gold
        cell.gold = 0
        return (wpns, armr, gld)


    def farm_cell(self, cell):
        fu = min(self.hit_points - self.current_hit_points, cell.food_units)
        cell.food_units -= fu
        #print("cell units left: {u}".format(u=cell.food_units))
        self.current_hit_points = self.current_hit_points + fu
        return fu

    def initiative(self):
        return 10 + stat_bonus[self.dex]

    def perception(self):
        return 10 *(self.wis + self.int)/36.0

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
        super(LongSword, self).__init__(1, 8)
        self.name = "LongSword"

class Fist(Weapon):
    def __init__(self):
        super(Fist, self).__init__(1,2)
        self.name = "Fist"
