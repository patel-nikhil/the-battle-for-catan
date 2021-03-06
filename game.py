import os
from board import *
from objectives import *
import random


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
    ports = [None] * num_ports
    remaining_rolls = [7, 2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    remaining_tiles = [Terrain.ORE, Terrain.ORE, Terrain.ORE, 
        Terrain.BRICK, Terrain.BRICK, Terrain.BRICK,
        Terrain.WHEAT, Terrain.WHEAT, Terrain.WHEAT, Terrain.WHEAT,
        Terrain.WOOD, Terrain.WOOD, Terrain.WOOD, Terrain.WOOD,
        Terrain.SHEEPS, Terrain.SHEEPS, Terrain.SHEEPS, Terrain.SHEEPS,
        Terrain.NONE]
    remaining_ports = [Terrain.ORE, Terrain.SHEEPS, Terrain.BRICK, Terrain.WHEAT, Terrain.WOOD, 
        Terrain.ANY, Terrain.ANY, Terrain.ANY, Terrain.ANY]

    with open(filename, 'r') as f:
        data = f.readlines()
        for i in range(num_tiles):
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
        
        for i in range(num_tiles + 1, num_ports + 1):
            info = data[i].split(',')
            try:
                resource = Terrain(info)
                if resource not in remaining_ports:
                    return None
                remaining_ports.remove(resource)
                ports[i - num_tiles] = Port(resource)
            except:
                return None

    return (tiles, ports)


def evaluate(color, secondturn=False):
    score = []
    for i in range(54):
        value = board.vertices[i].value(color, secondturn)
        # value = pts[0]/36.0 * sum(pts[1:-1]) - pts[0]/36.0 * pts[-1] ** 0.75
        # value = (pts[0]/36.0 * sum(pts[1:-1]))/pts[-1]
        score.append((i, value))
        
    score.sort(key=lambda x: x[1], reverse=True)
    with open('scoring.txt', 'a+') as out:
        for each in score[:3]:
            out.write(str(each))
            out.write(os.linesep)
            # print(each)
        out.write(os.linesep)
    return score


def drop(turn, num_cards):
    pass


def roll(turn):
    dice = random.randint(1,12)
    print(dice)
    if dice == 7:
        for player in players.values():
            if len(player.hand) > 8:
                drop(turn, players.get(turn).cards/2)
    else:
        for player in players.values():
            for position in player.vertices:
                player.hand += [board.vertices[position].resources[i] for i, x in enumerate(board.vertices[position].paydays) if x == dice]


def place_starting_settlement(board, turn, colour, secondTurn=False):
    score = evaluate(colour)
    print(score[0][0])
    players[colour].add_vertex(score[0][0],secondTurn)
    distance = shortest_path(board,score[0][0],colour)
    
    for pt in score[5-turn:]:
        if distance[0][pt[0]] < 5 and distance[0][pt[0]] > 1:
            break
    index = distance[1][pt[0]]
    while distance[1][index] != score[0][0]:
        index = distance[1][index]

    players[colour].add_road(score[0][0], index)


if __name__ == "__main__":
    turn_order = ['RED', 'BLUE', 'WHITE']
    #tiles = set_layout()
    tiles, ports = read_layout("layout.txt")
    
    if tiles is None:
        raise Exception("Invalid layout")

    board = construct_board(tiles, ports)

    place_starting_settlement(board, 0, 'RED')
    place_starting_settlement(board, 1, 'BLUE')
    place_starting_settlement(board, 2, 'WHITE')

    place_starting_settlement(board, 3, 'WHITE', True)
    place_starting_settlement(board, 4, 'BLUE', True)
    place_starting_settlement(board, 5, 'RED', True)

    print(players['RED'].hand)
    print(players['WHITE'].hand)
    print(players['BLUE'].hand)

    roll(0)
    print('owned', players['RED'].vertices)
    print('roads', find_road_spot(board, 'RED'))
    print('settlement', find_settlement_spot(board, 'RED'))
    print('city', find_city_spot(board, 'RED'))
    score = evaluate('RED')

    obj = turn_objectives(board, turn_order[0])