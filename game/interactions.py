import random
import world_config

def interact(obj, obj_other, distance):
    if obj == obj_other:
        return
    elif obj.name == "Player" and obj_other.name == "Player":
        player_interaction(obj["Player"], obj_other["Player"], distance)
    elif obj.name == "Player" and obj_other.name == "Weapon":
        item_interaction(obj["Player"], obj["Weapon"])
    #else:
    #    print("Non-human interaction between %s and %s" % (obj.name, obj_other.name))

def item_interaction(me, it, distance):
    if obj == obj_other:
        return


def player_interaction(me, you, distance):
    if distance < me.perception():
        if me.alive and you.alive:
            if random.random() < (me.get_aggressiveness() + you.get_aggressiveness())/2:
                combat(me, you, distance)

def combat(me, you, distance):
    #print("Fight!")
    me.total_combats +=1
    you.total_combats +=1
    if me.initiative() > you.initiative():
        if attack(me, you, distance):
            attack(you, me, distance)
    elif me.initiative() < you.initiative():
        if attack(you, me, distance):
            attack(me, you, distance)
    elif random.random() < 0.5:
        if attack(me, you, distance):
            attack(you, me, distance)
    else:
        if attack(you, me, distance):
            attack(me, you, distance)

def attack(attacker, target, distance):
    roll = random.randint(1,20)
    if roll + world_config.stat_bonus[attacker.str] > target.ac():
        damage = max(0, attacker.ready_weapon.damage()) + world_config.stat_bonus[attacker.str]
        target.current_hit_points -= max(0,damage)
        print("%s hit for %s damage  hp remaining: %s" % (target.name, damage, target.current_hit_points))
        if target.current_hit_points <= 0:
            #today.murders +=1
            attacker.successful_combats += 1
            target.alive = False
            #return False
        else:
            pass
            #return True
