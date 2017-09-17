class Armor(object):
    def __init__(self, ac_bonus):
        self.ac_bonus = ac_bonus

class NoShield(Armor):
    def __init__(self):
        super(NoShield, self).__init__(ac_bonus=0)
        self.name="NoShield"

class SmallShield(Armor):
    def __init__(self):
        super(SmallShield, self).__init__(ac_bonus=1)
        self.name="SmallShield"

class LargeShield(Armor):
    def __init__(self):
        super(LargeShield, self).__init__(ac_bonus=2)
        self.name="LargeShield"
