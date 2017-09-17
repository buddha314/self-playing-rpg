import random

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
