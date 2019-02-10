from board import *


# Find spots where roads can be built
# Can probably optimize by searching from starting settlements outwards?
def find_road_spot(board, color):
    if players[color].roads == 0:
        return []
    
    available = []
    for place in board.vertices:
        if place.owner not in (None, Color[color]) or Color[color] not in place.colors:
            continue
        
        for adj in place.connections:
            if adj[1] == None:
                available.append((place.position, adj[0].position))
    
    return available

# Find spots where settlements can be built
def find_settlement_spot(board, color):
    if players[color].settlements == 0:
        return []

    available = []
    for place in board.vertices:
        if place.owner is not None:
            continue
        
        connected = False
        is_far_enough = True
        for adj in place.connections:
            if adj[0].owner is not None:
                is_far_enough = False
                break
            if adj[1] == color:
                connected = True

        if is_far_enough == True and connected == True:
            available.append(place)
    
    return available

# Find spots where cities can be built
def find_city_spot(board, color):
    if players[color].cities == 0:
        return []

    available = []
    for place in board.vertices:
        if place.owner == color and place.level == 1:
            available.append(place)
    return available

def can_win(player):
    pass

def get_longest_road(player):
    pass

def get_knight(player):
    pass

def turn_objectives(board, color):
    player = players[color]
    vp = player.vp
    
    objectives = ['city', 'settlement', 'road', 'card']
    
    cities = find_city_spot(board, color)
    settlements = find_settlement_spot(board, color)
    roads = find_road_spot(board, color)

    if cities == []:
        objectives.remove('city')

    if settlements == []:
       objectives.remove('settlement')

    if roads == []:
        objectives.remove('roads')

    best_move = can_win(player, cities, settlements, roads)
    time_to_win = ttw(player, cities, settlements, roads)


# Find time to win for each player
def ttw(player, cities, settlements, roads):
    ttw = 1
    if player.vp == 9 or player.vp + player.cards == 9:
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
