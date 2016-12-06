from randomUtil import arbitrary
from math import sqrt
import json

MAP_WIDTH = 49
MAP_HEIGHT = 37


def generateMap():
    map={}
    for y in xrange(-MAP_HEIGHT/2+1,MAP_HEIGHT/2+1):
        proby = 1 - abs(y)/(float(MAP_HEIGHT-1)/2)
        for x in xrange(-MAP_WIDTH/2+1,MAP_WIDTH/2+1):
            probx = 1 - abs(x)/(float(MAP_WIDTH-1)/2)
            prob = min(probx,proby)+0.3
            if prob >= 1.0:
                map[str(x)+','+str(y)] = arbitrary({'walkable': 1})
            elif prob <= 0.0:
                map[str(x)+','+str(y)] = arbitrary({'unwalkable': 1})
            else:
                map[str(x)+','+str(y)] = arbitrary({'walkable': prob, 'unwalkable': 1-prob})
    return json.dumps(map)

file = open('maps/map', 'w')
file.write(generateMap())
file.close()

