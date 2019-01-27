from board import *


# Find spots where roads can be built
# Can probably optimize by searching from starting settlements outwards?
def find_road_spot(board, color):
    if players[color].roads == 0:
        return
    
    available = []
    for place in board.vertices:
        if place.owner not in (None, color) or color not in place.colours:
            continue
        
        for adj in place.connections:
            if adj[1] == None:
                available.append(place.position, adj.position)
    
    return available

# Find spots where settlements can be built
def find_settlement_spot(board, color):
    if players[color].settlements == 0:
        return

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
        return

    available = []
    for place in board.vertices:
        if place.owner == color and place.level == 1:
            available.append(place)


def set_layout():
    tiles = [None] * num_tiles
    remaining_rolls = [7, 2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    remaining_tiles = [Terrain.ORE, Terrain.ORE, Terrain.ORE, 
        Terrain.BRICK, Terrain.BRICK, Terrain.BRICK,
        Terrain.WHEAT, Terrain.WHEAT, Terrain.WHEAT, Terrain.WHEAT,
        Terrain.WOOD, Terrain.WOOD, Terrain.WOOD, Terrain.WOOD,
        Terrain.SHEEPS, Terrain.SHEEPS, Terrain.SHEEPS, Terrain.SHEEPS,
        Terrain.NONE]

    for i in range(num_tiles):
        resource = ''
        while resource not in remaining_tiles:
            resource = input("Tile " + str(i) + " resource: ")
            try:
                resource = Terrain(resource)
            except ValueError:
                resource = None
        remaining_tiles.remove(Terrain(resource))
        
        if resource == Terrain.NONE:
            tiles[i] = Tile(resource, 7)
            remaining_rolls.remove(7)
            continue

        number = 0
        while number not in remaining_rolls:
            try:
                number = int(input("Tile " + str(i) + " number: "))
            except:
                number = 0
        
        remaining_rolls.remove(number)
        tiles[i] = Tile(resource, number)

    return tiles


def read_layout(filename):
    tiles = [None] * num_tiles
    remaining_rolls = [7, 2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    remaining_tiles = [Terrain.ORE, Terrain.ORE, Terrain.ORE, 
        Terrain.BRICK, Terrain.BRICK, Terrain.BRICK,
        Terrain.WHEAT, Terrain.WHEAT, Terrain.WHEAT, Terrain.WHEAT,
        Terrain.WOOD, Terrain.WOOD, Terrain.WOOD, Terrain.WOOD,
        Terrain.SHEEPS, Terrain.SHEEPS, Terrain.SHEEPS, Terrain.SHEEPS,
        Terrain.NONE]

    with open(filename, 'r') as f:
        data = f.readlines()
        for i in range(len(data)):
            info = data[i].split(',')
            try:
                resource = Terrain(info[0])
                roll = int(info[1])
                if resource not in remaining_tiles or roll not in remaining_rolls:
                    return None
                remaining_tiles.remove(resource)
                remaining_rolls.remove(roll)
                tiles[i] = Tile(resource, roll) 
            except:
                return None
                
    return tiles

if __name__ == "__main__":
    #tiles = set_layout()
    tiles = read_layout("layout.txt")
    board = construct_board(tiles)

    score = []
    for i in range(52):
        pts = board.vertices[i].value('RED')
        value = pts[0]/36.0 * sum(pts[1:])
        score.append((i, value, pts))

    score.sort(key=lambda x: x[1], reverse=True)

    for each in score:
        print(each)