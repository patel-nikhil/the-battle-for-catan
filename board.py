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
    WOOD = 0
    BRICK = 1
    WHEAT = 2
    ORE = 3
    SHEEPS = 4
    ANY = 5

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
    
    def __init__(self, position, resources, rolls, port=None):
        self.position = position
        self.resources = resources
        self.paydays = rolls
        self.port = port
        self.connections = []

    def add_resource(self, *resources):
        for resource in resources:
            self.resources.append(resource)
    
    def add_payday(self, *rolls):
        for roll in rolls:
            self.paydays.append(roll)

    def add_port(self, port):
        self.port = port
    
    def setColor(self, color):
        self.color = None

    def reset(self):
        self.color = None
    
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
                if resource not in list(players[color].resources + self.resources):
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


def construct_vertices():
    global board
    board.vertices.append(Vertex(0, (Terrain.ORE,), (10,), Port(Terrain.ANY, 3)))
    board.vertices.append(Vertex(1, (Terrain.ORE,), (10,), Port(Terrain.ANY, 3)))
    board.vertices.append(Vertex(2, (Terrain.ORE, Terrain.SHEEPS,), (10,)))
    board.vertices.append(Vertex(3, (Terrain.SHEEPS,), (2,), Port(Terrain.WHEAT, 2)))
    board.vertices.append(Vertex(4, (Terrain.SHEEPS, Terrain.WOOD,), (2, 9,), Port(Terrain.WHEAT, 2)))
    board.vertices.append(Vertex(5, (Terrain.WOOD,), (9,)))
    board.vertices.append(Vertex(6, (Terrain.WOOD,), (9,)))
    board.vertices.append(Vertex(7, (Terrain.WHEAT,), (12,), Port(Terrain.WOOD, 2)))
    board.vertices.append(Vertex(8, (Terrain.ORE, Terrain.WHEAT,), (10, 12)))
    board.vertices.append(Vertex(9, (Terrain.ORE, Terrain.BRICK, Terrain.WHEAT,), (10, 6, 12)))
    board.vertices.append(Vertex(10, (Terrain.ORE, Terrain.SHEEPS, Terrain.BRICK,), (10, 2, 6)))

    board.vertices.append(Vertex(11, (Terrain.SHEEPS, Terrain.BRICK, Terrain.SHEEPS,), (2, 6, 4)))
    board.vertices.append(Vertex(12, (Terrain.SHEEPS, Terrain.SHEEPS, Terrain.WOOD,), (2, 4, 9)))
    board.vertices.append(Vertex(13, (Terrain.SHEEPS, Terrain.WOOD, Terrain.BRICK,), (4, 9, 10)))
    board.vertices.append(Vertex(14, (Terrain.WOOD, Terrain.BRICK,), (9, 10,), Port(Terrain.ORE, 2)))
    board.vertices.append(Vertex(15, (Terrain.BRICK,), (10,), Port(Terrain.ORE, 2)))

    board.vertices.append(Vertex(16, (Terrain.WHEAT,), (9,), Port(Terrain.ORE, 2)))
    board.vertices.append(Vertex(17, (Terrain.WHEAT, Terrain.WHEAT,), (9, 12,), Port(Terrain.WOOD, 2)))
    board.vertices.append(Vertex(18, (Terrain.WHEAT, Terrain.WHEAT, Terrain.WOOD,), (9, 12, 11)))
    board.vertices.append(Vertex(19, (Terrain.WHEAT, Terrain.WOOD, Terrain.BRICK,), (12, 11, 6)))
    board.vertices.append(Vertex(20, (Terrain.WOOD, Terrain.BRICK,), (11, 6)))
    board.vertices.append(Vertex(21, (Terrain.BRICK, Terrain.SHEEPS,), (6, 4)))
    board.vertices.append(Vertex(22, (Terrain.SHEEPS, Terrain.WOOD,), (4, 3)))
    board.vertices.append(Vertex(23, (Terrain.SHEEPS, Terrain.WOOD, Terrain.BRICK,), (4, 3, 10)))
    board.vertices.append(Vertex(24, (Terrain.WOOD, Terrain.BRICK, Terrain.ORE,), (3, 10, 8)))
    board.vertices.append(Vertex(25, (Terrain.BRICK, Terrain.ORE,), (10, 8)))
    board.vertices.append(Vertex(26, (Terrain.ORE,), (8,), Port(Terrain.ANY, 3)))



    board.vertices.append(Vertex(27, (Terrain.WHEAT,), (9,)))
    board.vertices.append(Vertex(28, (Terrain.WHEAT, Terrain.WOOD,), (9, 8,), Port(Terrain.BRICK, 2)))
    board.vertices.append(Vertex(29, (Terrain.WHEAT, Terrain.WOOD, Terrain.WOOD,), (9, 8, 11)))
    board.vertices.append(Vertex(30, (Terrain.WOOD, Terrain.WOOD, Terrain.ORE,), (8, 11, 3)))
    board.vertices.append(Vertex(31, (Terrain.WOOD, Terrain.ORE,), (11, 3)))
    board.vertices.append(Vertex(32, (Terrain.ORE, Terrain.WHEAT,), (3, 4)))
    board.vertices.append(Vertex(33, (Terrain.WHEAT, Terrain.WOOD,), (4, 3)))
    board.vertices.append(Vertex(34, (Terrain.WHEAT, Terrain.WOOD, Terrain.SHEEPS,), (4, 3, 5)))
    board.vertices.append(Vertex(35, (Terrain.WOOD, Terrain.ORE, Terrain.SHEEPS,), (3, 8, 5)))
    board.vertices.append(Vertex(36, (Terrain.SHEEPS, Terrain.ORE,), (5, 8)))
    board.vertices.append(Vertex(37, (Terrain.ORE,), (8,), Port(Terrain.ORE, 2)))


    board.vertices.append(Vertex(38, (Terrain.WOOD,), (8,), Port(Terrain.WOOD, 2)))
    board.vertices.append(Vertex(39, (Terrain.WOOD, Terrain.BRICK,), (8, 5)))
    board.vertices.append(Vertex(40, (Terrain.WOOD, Terrain.BRICK, Terrain.ORE,), (8, 5, 3)))
    board.vertices.append(Vertex(41, (Terrain.BRICK, Terrain.ORE, Terrain.WHEAT,), (5, 3, 6)))
    board.vertices.append(Vertex(42, (Terrain.ORE, Terrain.WHEAT, Terrain.WHEAT,), (3, 6, 4)))
    board.vertices.append(Vertex(43, (Terrain.WHEAT, Terrain.WHEAT, Terrain.SHEEPS,), (6, 4, 11)))
    board.vertices.append(Vertex(44, (Terrain.WHEAT, Terrain.SHEEPS, Terrain.SHEEPS,), (4, 11, 5)))
    board.vertices.append(Vertex(45, (Terrain.SHEEPS, Terrain.SHEEPS,), (11, 5,), Port(Terrain.SHEEPS, 2)))
    board.vertices.append(Vertex(46, (Terrain.SHEEPS,), (5,), Port(Terrain.SHEEPS, 2)))


    board.vertices.append(Vertex(46, (Terrain.BRICK,), (5,), Port(Terrain.ANY, 3)))
    board.vertices.append(Vertex(47, (Terrain.BRICK,), (5,), Port(Terrain.ANY, 3)))
    board.vertices.append(Vertex(48, (Terrain.BRICK, Terrain.WHEAT,), (5, 6)))
    board.vertices.append(Vertex(49, (Terrain.WHEAT,), (6,), Port(Terrain.ANY, 3)))
    board.vertices.append(Vertex(50, (Terrain.WHEAT, Terrain.SHEEPS,), (6, 11,), Port(Terrain.ANY, 3)))
    board.vertices.append(Vertex(51, (Terrain.SHEEPS,), (11,)))
    board.vertices.append(Vertex(52, (Terrain.SHEEPS,), (11,)))

    

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

def construct_board():
    global board
    construct_vertices()
    construct_edges()
    return board

if __name__ == "__main__":
    construct_board()
    print(board)