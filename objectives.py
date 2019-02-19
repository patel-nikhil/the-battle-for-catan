from board import *


# Find spots where roads can be built
# Can probably optimize by searching from starting settlements outwards?
def find_road_spot(board, colour):
    if players[colour].roads == 0:
        return []
    
    available = []
    for place in board.vertices:
        if place.owner not in (None, Colour[colour]) or Colour[colour] not in place.colours:
            continue
        
        for adj in place.connections.values():
            if adj.colour == None:
                available.append((place.position, adj.vertex.position))
    
    return available


# Find spots where settlements can be built
def shortest_path(board, start, colour):
    if players[colour].settlements == 0:
        return [-1]*54

    distanceTo = [0]*54
    source = board.vertices[start]
    visited = [source.position]
    queue = [source]
    path = [0]*54; path[source.position] = source.position
    while len(queue) > 0:
        current = queue.pop()
        if current.owner not in (None, Colour[colour]):
            continue
        for dest in current.connections.values():
            # print('Position:', dest[0].position)
            if distanceTo[dest.vertex.position] > distanceTo[current.position] + 1 or (distanceTo[dest.vertex.position] == 0 and dest.vertex.position != start):
                # print('weight', distanceTo[current.position] + 1)
                distanceTo[dest.vertex.position] = distanceTo[current.position] + 1
                path[dest.vertex.position] = current.position
            if dest.vertex.position not in visited:
                queue.append(dest.vertex)
                visited.append(dest.vertex.position)
    return [distanceTo, path]



# Find spots where settlements can be built
def find_settlement_spot(board, colour):
    if players[colour].settlements == 0:
        return []

    available = []
    for place in board.vertices:
        if place.owner is not None:
            continue
        
        connected = False
        is_far_enough = True
        for adj in place.connections.values():
            if adj.vertex.owner is not None:
                is_far_enough = False
                break
            if adj.colour == colour:
                connected = True

        if is_far_enough == True and connected == True:
            available.append(place)
    
    return available

# Find spots where cities can be built
def find_city_spot(board, colour):
    if players[colour].cities == 0:
        return []

    available = []
    for place in board.vertices:
        if place.owner == colour and place.level == 1:
            available.append(place)
    return available

def can_build(player):
    pass

def can_win(player, cities, settlements, roads):
    pass

def get_longest_road(player):
    pass

def get_knight(player):
    pass

def turn_objectives(board, colour):
    player = players[colour]
    vp = player.vp
    
    objectives = ['city', 'settlement', 'road', 'card']
    
    cities = find_city_spot(board, colour)
    settlements = find_settlement_spot(board, colour)
    roads = find_road_spot(board, colour)

    if cities == []:
        objectives.remove('city')

    if settlements == []:
       objectives.remove('settlement')

    if roads == []:
        objectives.remove('road')
    
    missing = {}
    trading = {}
    for btype in objectives:
        for resource in building_types[btype].keys():
            needed = building_types[btype][resource] - players[colour].hand.count(resource)
            if needed <= 0:
                continue
            else:
                try:
                    missing[btype] += [resource, needed]
                except KeyError:
                    missing[btype] = [resource, needed]
        for resource in players[colour].hand:
            try:
                extra = players[colour].hand.count(resource) - building_types[btype][resource]
                if extra <= 0:
                    continue
                trading[btype] += [resource, extra]
            except KeyError:
                try:
                    trading[btype] = [resource, players[colour].hand.count(resource) - building_types[btype][resource]]
                except KeyError:
                    trading[btype] = [resource, players[colour].hand.count(resource)]

    best_move = can_win(player, cities, settlements, roads)
    time_to_win = ttw(player, cities, settlements, roads)

    return None

# Find time to win for each player
def ttw(player, cities, settlements, roads):
    ttw = 1
    if player.vp == 9 or player.vp + len(player.cards) == 9:
        if len(cities) + len(settlements) == 0:
            ttw += 0.5
        if not(get_longest_road(player)):
            ttw += 0.1
        if not(get_knight(player)):
            ttw += 0.1
    elif player.vp == 8:
        if player.cards == 0:
            ttw += 0.5
        if not(get_longest_road(player)):
            ttw += 0.1
        if not(get_knight(player)):
            ttw += 0.1
    elif player.vp == 7:
        if len(cities) + len(settlements) == 0:
            ttw += 1.5
        if not(get_longest_road(player)):
            ttw += 2
        if not(get_knight(player)):
            ttw += 2
    elif player.vp < 7:
        ttw += 4
    return ttw
