import random, math
from bge import render, events, logic, types
import bpy
from mathutils import Vector

import world_config, models
from models import Player

def main():
    cont = logic.getCurrentController()
    own = cont.owner
    scene = logic.getCurrentScene()

    grounds = scene.objects["Ground"]
    grounds.position = Vector((0,0,0))
    grounds.localScale = Vector((world_config.n_lon, world_config.n_lat, 0.1))
    print(" ground local scale" + str(grounds.localScale))
    print(" ground world scale" + str(grounds.worldScale))


    for i in range(world_config.initial_population_size):
        pos = Vector((random.uniform(-10,10),
                     random.uniform(-10,10),
                     3))
        p = Player(world_config.random_name())
        t = own.scene.addObject("Player")
        #bpy.ops.logic.add_sensor(type="ALWAYS", object=t.name)

        t["Player"] = p
        t.worldPosition = pos

main()
