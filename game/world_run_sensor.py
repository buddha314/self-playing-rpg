import random
import math
import interactions
from mathutils import Vector
from bge import render, events, logic, types

scene = logic.getCurrentScene()

for obj in scene.objects:
    #print(obj.name + " is hanging around " + str(obj.localPosition))
    if obj.name == "Player":
        obj.localPosition += Vector(obj['Player'].move())

        for obj_other in scene.objects:
            dvec = obj.worldPosition - obj_other.worldPosition
            if obj != obj_other and dvec.length < obj['Player'].perception() and obj_other.name == "Player":
                if obj_other.name == "Player":
                    interactions.combat(obj, obj_other)
