import json
MAP_WIDTH = 49
MAP_HEIGHT = 37


file = open('maps/map', 'r')
map = json.load(file)

for y in xrange(-MAP_HEIGHT / 2 + 1, MAP_HEIGHT / 2 + 1):
    line = ""
    for x in xrange(-MAP_WIDTH / 2 + 1, MAP_WIDTH / 2 + 1):
        if map[str(x)+','+str(y)]=="unwalkable":
            line = line + str(0)
        else:
            line = line + str(1)
    print line
