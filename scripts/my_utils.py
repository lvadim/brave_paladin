from scripts import actor
import math
import random

def distBetweenActors(actor1, actor2):
    return math.dist(actor1.getPosition(), actor2.getPosition()) 

def isActor1LookAtActor2(actor1, actor2):
    x1, y1 = actor1.getPosition()
    x2, y2 = actor2.getPosition()
    if actor1.isRightDierction():
        return x2 >= x1
    else:
        return x2 <= x1

def getRandomPointNear(point, delta):
    x, y = point
    dx = x + random.randrange(delta) - delta / 2
    dy = y + random.randrange(delta) - delta / 2
    return (dx, dy)