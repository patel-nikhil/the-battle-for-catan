from enum import Enum
from itertools import islice

from stats import *

class Color(Enum):
    RED = 0,
    BLUE = 1,
    WHITE = 2,
    ORANGE = 3

class Player():

    def __init__(self, color):
        self.color = color
        self.vp = 0
        self.roads = 15
        self.settlements = 5
        self.cities = 4
        self.cards = []
        self.vertices = []
        self.resources = []
        self.port_resources = []
    
    def add_vertex(self, position):
        self.vertices.append(position)
        for resource in board.vertices[position].resources:
            self.resources.append(resource)
        if board.vertices[position].port is not None:
            self.port_resources.append(board.vertices[position].port.resource)

players = {
    'RED' : Player(Color.RED,),
    'BLUE': Player(Color.BLUE,),
    'WHITE': Player(Color.WHITE,),
    'ORANGE': Player(Color.ORANGE)
}


class Terrain(Enum):
    WOOD = 'L'
    BRICK = 'B'
    WHEAT = 'W'
    ORE = 'O'
    SHEEPS = 'S'
    ANY = 'A'
    NONE = 'N'

class Tile:

    def __init__(self, resource, roll):
        self.resource = resource
        self.roll = roll


c_city = ((Terrain.ORE, 3,), (Terrain.WHEAT, 2))
c_settlement = ((Terrain.WOOD, 1,), (Terrain.BRICK, 1,), (Terrain.WHEAT, 1,), (Terrain.SHEEPS, 1))
c_devcard = ((Terrain.ORE, 1,), (Terrain.WHEAT, 1,), (Terrain.SHEEPS, 1))
c_road = ((Terrain.WOOD, 1,), (Terrain.BRICK, 1))

num_tiles = 19

class Port:

    def __init__(self, resource, ratio):
        self.resource = resource
        self.amount = ratio

class Vertex:
    
    def __init__(self, position, tiles, port=None):
        self.owner = None
        self.position = position
        self.resources = []
        self.paydays = []
        self.port = port
        self.connections = []

        for hex in tiles:
            self.resources.append(hex.resource)
            self.paydays.append(hex.roll)

    def add_resource(self, *resources):
        for resource in resources:
            self.resources.append(resource)
    
    def add_payday(self, *rolls):
        for roll in rolls:
            self.paydays.append(roll)

    def add_port(self, port):
        self.port = port
    
    def build(self, color):
        self.owner = color

    def reset(self):
        self.owner = None
    
    # Factor in potential riskiness of having settlements on same number/resource
    def value(self, color, secondturn=False):
        dvalue = 0
        for roll in self.paydays:
            dvalue += p_roll[roll]
        
        rvalue = 0
        avalue = 0
        pvalue = 0
        lvalue = 0
        
        for resource in self.resources:
            if resource not in players[color].resources:
                rvalue += 1
            if resource in players[color].resources:
                avalue += 1
            if self.port is not None and resource == self.port.resource:
                pvalue += 1
        
        for resource in set(players[color].resources + list(self.resources)):
            if resource in players[color].port_resources:
                if players[color].resources.count(resource) > 1:
                    pvalue += 3
            else:
                if players[color].port_resources.count(Terrain.ANY) and players[color].resources.count(resource) > 2:
                    pvalue += 2

        if secondturn == True:
            for resource in islice(Terrain, 0, 4):
                if resource not in list(players[color].resources + self):
                    lvalue += 1

        return (dvalue, rvalue, avalue, pvalue, lvalue)
        



class Edge:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.color = None

    def set_color(self, color):
        self.color = color

    def reset(self):
        self.color = None


## Board has 19 tiles, one of which is a desert tile
class Board:

    def __init__(self):
        self.vertices = []
        self.edges = []

board = Board()

def construct_vertices(tiles):
    global board
    board.vertices.append(Vertex(0, (tiles[0],), Port(Terrain.ANY, 3)))
    board.vertices.append(Vertex(1, (tiles[0],), Port(Terrain.ANY, 3)))
    board.vertices.append(Vertex(2, (tiles[0], tiles[1])))
    board.vertices.append(Vertex(3, (tiles[1],), Port(Terrain.WHEAT, 2)))
    board.vertices.append(Vertex(4, (tiles[1], tiles[2]), Port(Terrain.WHEAT, 2)))
    board.vertices.append(Vertex(5, (tiles[2],)))
    board.vertices.append(Vertex(6, (tiles[2],)))
    board.vertices.append(Vertex(7, (tiles[3],), Port(Terrain.WOOD, 2)))
    board.vertices.append(Vertex(8, (tiles[0], tiles[3])))
    board.vertices.append(Vertex(9, (tiles[0], tiles[4], tiles[3])))
    board.vertices.append(Vertex(10, (tiles[0], tiles[1], tiles[4])))

    board.vertices.append(Vertex(11, (tiles[1], tiles[4], tiles[5])))
    board.vertices.append(Vertex(12, (tiles[1], tiles[5], tiles[2])))
    board.vertices.append(Vertex(13, (tiles[5], tiles[2], tiles[6])))
    board.vertices.append(Vertex(14, (tiles[2], tiles[6]), Port(Terrain.ORE, 2)))
    board.vertices.append(Vertex(15, (tiles[0],), Port(Terrain.ORE, 2)))

    board.vertices.append(Vertex(16, (tiles[7],)))
    board.vertices.append(Vertex(17, (tiles[7], tiles[3]), Port(Terrain.WOOD, 2)))
    board.vertices.append(Vertex(18, (tiles[7], tiles[3], tiles[8])))
    board.vertices.append(Vertex(19, (tiles[3], tiles[8], tiles[4])))
    board.vertices.append(Vertex(20, (tiles[8], tiles[4], tiles[9])))
    board.vertices.append(Vertex(21, (tiles[4], tiles[5], tiles[9])))
    board.vertices.append(Vertex(22, (tiles[5], tiles[10], tiles[9])))
    board.vertices.append(Vertex(23, (tiles[5], tiles[10], tiles[6])))
    board.vertices.append(Vertex(24, (tiles[10], tiles[6], tiles[11])))
    board.vertices.append(Vertex(25, (tiles[6], tiles[11])))
    board.vertices.append(Vertex(26, (tiles[11],), Port(Terrain.ANY, 3)))



    board.vertices.append(Vertex(27, (tiles[7],)))
    board.vertices.append(Vertex(28, (tiles[7], tiles[12]), Port(Terrain.BRICK, 2)))
    board.vertices.append(Vertex(29, (tiles[7], tiles[12], tiles[8])))
    board.vertices.append(Vertex(30, (tiles[12], tiles[8], tiles[13])))
    board.vertices.append(Vertex(31, (tiles[12], tiles[13], tiles[9])))
    board.vertices.append(Vertex(32, (tiles[10], tiles[14], tiles[9])))
    board.vertices.append(Vertex(33, (tiles[14], tiles[10], tiles[9])))
    board.vertices.append(Vertex(34, (tiles[14], tiles[10], tiles[15])))
    board.vertices.append(Vertex(35, (tiles[10], tiles[11], tiles[15])))
    board.vertices.append(Vertex(36, (tiles[15], tiles[11])))
    board.vertices.append(Vertex(37, (tiles[11],), Port(Terrain.ORE, 2)))


    board.vertices.append(Vertex(38, (tiles[12],), Port(Terrain.WOOD, 2)))
    board.vertices.append(Vertex(39, (tiles[12], tiles[16])))
    board.vertices.append(Vertex(40, (tiles[12], tiles[16], tiles[13])))
    board.vertices.append(Vertex(41, (tiles[16], tiles[13], tiles[17])))
    board.vertices.append(Vertex(42, (tiles[13], tiles[17], tiles[14])))
    board.vertices.append(Vertex(43, (tiles[17], tiles[14], tiles[18])))
    board.vertices.append(Vertex(44, (tiles[14], tiles[18], tiles[15])))
    board.vertices.append(Vertex(45, (tiles[18], tiles[15]), Port(Terrain.SHEEPS, 2)))
    board.vertices.append(Vertex(46, (tiles[18],), Port(Terrain.SHEEPS, 2)))


    board.vertices.append(Vertex(46, (tiles[16],), Port(Terrain.ANY, 3)))
    board.vertices.append(Vertex(47, (tiles[16],), Port(Terrain.ANY, 3)))
    board.vertices.append(Vertex(48, (tiles[16], tiles[17])))
    board.vertices.append(Vertex(49, (tiles[17],), Port(Terrain.ANY, 3)))
    board.vertices.append(Vertex(50, (tiles[17], tiles[18]), Port(Terrain.ANY, 3)))
    board.vertices.append(Vertex(51, (tiles[18],)))
    board.vertices.append(Vertex(52, (tiles[18],)))

def append(first, second):
    global board
    board.vertices[first].connections.append((second, None))
    board.vertices[second].connections.append((first, None))

def construct_edges():
    global board

    append(0,1)
    append(0,8)
    append(1,2)
    append(2,3)
    append(2,10)
    append(3,4)
    append(4,5)
    append(4,12)
    append(5,6)
    append(7,8)
    append(7,17)
    append(8,9)
    append(9,10)
    append(9,19)
    append(10,11)
    append(11,12)
    append(11,21)
    append(12,13)
    append(13,14)
    append(13,23)
    append(14,15)
    append(15,16)
    append(15,25)
    append(16,17)
    append(16,27)


    append(17,18)
    append(18,19)
    append(18,29)
    append(19,20)
    append(20,21)
    append(20,31)
    append(21,22)
    append(22,23)
    append(22,33)
    append(23,24)
    append(24,25)
    append(24,35)
    append(25,26)
    append(26,37)

    append(27,28)
    append(28,29)
    append(28,38)
    append(29,30)
    append(30,31)
    append(30,40)
    append(31,32)
    append(32,33)
    append(32,42)
    append(33,34)
    append(34,35)
    append(34,44)
    append(35,36)
    append(36,37)
    append(36,46)

    append(38,39)
    append(39,40)
    append(39,47)
    append(40,41)
    append(41,42)
    append(41,49)
    append(42,43)
    append(43,44)
    append(43,51)
    append(44,45)
    append(45,46)
    append(45,53)

    append(47,48)
    append(48,49)
    append(49,50)
    append(50,51)
    append(51,52)

def construct_board(tiles=None):
    global board
    construct_vertices(tiles)
    construct_edges()
    return board

if __name__ == "__main__":
    construct_board()
    print(board)