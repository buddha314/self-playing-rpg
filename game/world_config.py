import numpy as np

initial_population_size=5
dagger_density=0.1
sword_density=0.01
smallshield_density = 0.1
largeshield_density = 0.01
n_lat = 150
n_lon = 150
n_days= 365
n_years = 2
desert_fertility=0.05
farmland_fertility=0.75

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

names = [
"Fred"
,"Bob"
,"Alice"
,"Betty"
,"Charles"
,"Diderot"
,"Francois"
,"Voltaire"
,"Rousseau"
,"Dinah"
]

def random_name():
    return np.random.choice(names)
