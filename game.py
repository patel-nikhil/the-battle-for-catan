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


if __name__ == "__main__":
    board = construct_board()

    score = []
    for i in range(52):
        pts = board.vertices[i].value('RED')
        value = pts[0]/36.0 * sum(pts[1:])
        score.append((i, value, pts))

    score.sort(key=lambda x: x[1], reverse=True)

    for each in score:
        print(each)