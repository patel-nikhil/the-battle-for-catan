from enum import Enum
from itertools import islice

from stats import *

class Colour(Enum):
    RED = 0,
    BLUE = 1,
    WHITE = 2,
    ORANGE = 3

class Connection:
    
    def __init__(self, vertex, colour):
        self.vertex = vertex
        self.colour = colour

    def __eq__(self, other):
        return self.vertex == other.vertex

class Player():

    def __init__(self, colour):
        self.colour = colour
        self.vp = 0
        self.roads = 15
        self.settlements = 5
        self.cities = 4
        self.cards = []
        self.hand = []
        self.vertices = []
        self.resources = []
        self.port_resources = []
    
    def add_vertex(self, position, starting_resource=False):
        self.settlements -= 1
        self.vertices.append(position)
        board.vertices[position].owner = self.colour
        board.vertices[position].colours.append(self.colour)
        for resource in board.vertices[position].resources:
            self.resources.append(resource)
            if starting_resource == True:
                self.hand.append(resource)
        if board.vertices[position].port is not None:
            self.port_resources.append(board.vertices[position].port.resource)
    
    def add_road(self, start, end):
        self.roads -= 1
        
        board.vertices[start].connections[end].colour = self.colour # = Connection(board.vertices[end], self.colour)
        board.vertices[end].connections[start].colour = self.colour # = Connection(board.vertices[start], self.colour)
        board.vertices[start].colours.append(self.colour)
        board.vertices[end].colours.append(self.colour)

class Buildings(Enum):
    city = 'city'
    road = 'road'
    settlement = 'settlement'

players = {
    'RED' : Player(Colour.RED),
    'BLUE': Player(Colour.BLUE),
    'WHITE': Player(Colour.WHITE),
    'ORANGE': Player(Colour.ORANGE)
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

building_types = {
    'city' : {Terrain.ORE : 3, Terrain.WHEAT : 2},
    'settlement' : {Terrain.WOOD : 1, Terrain.BRICK : 1, Terrain.WHEAT : 1, Terrain.SHEEPS : 1},
    'card' : {Terrain.ORE : 1, Terrain.WHEAT : 1, Terrain.SHEEPS : 1},
    'road' : {Terrain.WOOD : 1, Terrain.BRICK : 1}
}

num_tiles = 19
num_ports = 9

class Port:

    def __init__(self, resource):
        self.resource = resource
        self.amount = (3 if resource == Terrain.ANY else 2)

class Vertex:
    
    def __init__(self, position, tiles, port=None):
        self.owner = None
        self.position = position
        self.resources = []
        self.paydays = []
        self.port = port
        self.connections = {}
        self.colours = []

        for hex in tiles:
            self.resources.append(hex.resource)
            self.paydays.append(hex.roll)

    def __eq__(self, other):
        return self.position == other.position

    def add_resource(self, *resources):
        for resource in resources:
            self.resources.append(resource)
    
    def add_payday(self, *rolls):
        for roll in rolls:
            self.paydays.append(roll)

    def add_port(self, port):
        self.port = port

    def build(self, colour):
        self.owner = colour

    def reset(self):
        self.owner = None
    
    # Factor in potential riskiness of having settlements on same number/resource
    def value(self, colour, secondturn=False):
        dvalue = 0
        for roll in self.paydays:
            dvalue += p_roll[roll]
        
        rvalue = 0
        avalue = 0
        pvalue = 0
        lvalue = 1
        
        if self.owner is not None:
            return (0, 0, 0, 0, 1)
        
        for adj in self.connections.values():
            if adj.vertex.owner is not None:
                return (0, 0, 0, 0, 1)

        for resource in self.resources:
            if resource not in players[colour].resources:
                rvalue += 1
            if resource in players[colour].resources:
                avalue += 1
            if self.port is not None and resource == self.port.resource:
                pvalue += 1
        
        for resource in set(players[colour].resources + list(self.resources)):
            if resource in players[colour].port_resources:
                if players[colour].resources.count(resource) > 1:
                    pvalue += 3
            else:
                if players[colour].port_resources.count(Terrain.ANY) and players[colour].resources.count(resource) > 2:
                    pvalue += 2

        if secondturn == True:
            for resource in islice(Terrain, 0, 4):
                if resource not in list(players[colour].resources + self.resources):
                    lvalue += 0.03

        return (dvalue, rvalue, avalue, pvalue, lvalue)
        



class Edge:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.colour = None

    def set_colour(self, colour):
        self.colour = colour

    def reset(self):
        self.colour = None


## Board has 19 tiles, one of which is a desert tile
class Board:

    def __init__(self):
        self.vertices = []
        self.edges = []

board = Board()

def construct_vertices(tiles, ports):
    global board
    board.vertices.append(Vertex(0, (tiles[0],), ports[0]))
    board.vertices.append(Vertex(1, (tiles[0],), ports[0]))
    board.vertices.append(Vertex(2, (tiles[0], tiles[1])))
    board.vertices.append(Vertex(3, (tiles[1],), ports[1]))
    board.vertices.append(Vertex(4, (tiles[1], tiles[2]), ports[1]))
    board.vertices.append(Vertex(5, (tiles[2],)))
    board.vertices.append(Vertex(6, (tiles[2],)))
    board.vertices.append(Vertex(7, (tiles[3],), ports[8]))
    board.vertices.append(Vertex(8, (tiles[0], tiles[3])))
    board.vertices.append(Vertex(9, (tiles[0], tiles[4], tiles[3])))
    board.vertices.append(Vertex(10, (tiles[0], tiles[1], tiles[4])))

    board.vertices.append(Vertex(11, (tiles[1], tiles[4], tiles[5])))
    board.vertices.append(Vertex(12, (tiles[1], tiles[5], tiles[2])))
    board.vertices.append(Vertex(13, (tiles[5], tiles[2], tiles[6])))
    board.vertices.append(Vertex(14, (tiles[2], tiles[6]), ports[2]))
    board.vertices.append(Vertex(15, (tiles[0],), ports[2]))

    board.vertices.append(Vertex(16, (tiles[7],)))
    board.vertices.append(Vertex(17, (tiles[7], tiles[3]), ports[8]))
    board.vertices.append(Vertex(18, (tiles[7], tiles[3], tiles[8])))
    board.vertices.append(Vertex(19, (tiles[3], tiles[8], tiles[4])))
    board.vertices.append(Vertex(20, (tiles[8], tiles[4], tiles[9])))
    board.vertices.append(Vertex(21, (tiles[4], tiles[5], tiles[9])))
    board.vertices.append(Vertex(22, (tiles[5], tiles[10], tiles[9])))
    board.vertices.append(Vertex(23, (tiles[5], tiles[10], tiles[6])))
    board.vertices.append(Vertex(24, (tiles[10], tiles[6], tiles[11])))
    board.vertices.append(Vertex(25, (tiles[6], tiles[11])))
    board.vertices.append(Vertex(26, (tiles[11],), ports[3]))



    board.vertices.append(Vertex(27, (tiles[7],)))
    board.vertices.append(Vertex(28, (tiles[7], tiles[12]), ports[7]))
    board.vertices.append(Vertex(29, (tiles[7], tiles[12], tiles[8])))
    board.vertices.append(Vertex(30, (tiles[12], tiles[8], tiles[13])))
    board.vertices.append(Vertex(31, (tiles[12], tiles[13], tiles[9])))
    board.vertices.append(Vertex(32, (tiles[10], tiles[14], tiles[9])))
    board.vertices.append(Vertex(33, (tiles[14], tiles[10], tiles[9])))
    board.vertices.append(Vertex(34, (tiles[14], tiles[10], tiles[15])))
    board.vertices.append(Vertex(35, (tiles[10], tiles[11], tiles[15])))
    board.vertices.append(Vertex(36, (tiles[15], tiles[11])))
    board.vertices.append(Vertex(37, (tiles[11],), ports[3]))


    board.vertices.append(Vertex(38, (tiles[12],), ports[8]))
    board.vertices.append(Vertex(39, (tiles[12], tiles[16])))
    board.vertices.append(Vertex(40, (tiles[12], tiles[16], tiles[13])))
    board.vertices.append(Vertex(41, (tiles[16], tiles[13], tiles[17])))
    board.vertices.append(Vertex(42, (tiles[13], tiles[17], tiles[14])))
    board.vertices.append(Vertex(43, (tiles[17], tiles[14], tiles[18])))
    board.vertices.append(Vertex(44, (tiles[14], tiles[18], tiles[15])))
    board.vertices.append(Vertex(45, (tiles[18], tiles[15]), ports[4]))
    board.vertices.append(Vertex(46, (tiles[18],), ports[4]))


    board.vertices.append(Vertex(47, (tiles[16],), ports[6]))
    board.vertices.append(Vertex(48, (tiles[16],), ports[6]))
    board.vertices.append(Vertex(49, (tiles[16], tiles[17])))
    board.vertices.append(Vertex(50, (tiles[17],), ports[5]))
    board.vertices.append(Vertex(51, (tiles[17], tiles[18]), ports[5]))
    board.vertices.append(Vertex(52, (tiles[18],)))
    board.vertices.append(Vertex(53, (tiles[18],)))

def append(first, second):
    global board
    board.vertices[first].connections[second] = Connection(board.vertices[second], None)
    board.vertices[second].connections[first] = Connection(board.vertices[first], None)

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
    append(52,53)

def construct_board(tiles, ports):
    global board
    construct_vertices(tiles, ports)
    construct_edges()
    return board