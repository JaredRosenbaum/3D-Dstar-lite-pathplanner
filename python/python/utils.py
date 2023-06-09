import math
from typing import List



class Vertex:
    def __init__(self, pos: (int, int, int)):
        self.pos = pos
        self.edges_and_costs = {}

    def add_edge_with_cost(self, succ: (int, int, int), cost: float):
        if succ != self.pos:
            self.edges_and_costs[succ] = cost

    @property
    def edges_and_c_old(self):
        return self.edges_and_costs


class Vertices:
    def __init__(self):
        self.list = []

    def add_vertex(self, v: Vertex):
        self.list.append(v)

    @property
    def vertices(self):
        return self.list

# Previous, 2d heuristic
# def heuristic(p: (int, int), q: (int, int)) -> float:
#     """
#     Helper function to compute distance between two points.
#     :param p: (x,y)
#     :param q: (x,y)
#     :return: manhattan distance
#     """
#     return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def heuristic(p: (int, int, int), q: (int, int, int)) -> float:
    try:
        answer = math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2]-q[2])**2)
    except TypeError:
        print('You are on an obstacle!')
    return answer

# def gnd_heuristic(p: (int, int, int), map):
#     if map.occupancy_grid_map[p[0]][p[1]][p[2]] == 0 and map.occupancy_grid_map[p[0]][p[1]][p[2]-1] == 255:
#         return 0
#     else:
#         #Arbitrarily large number, might need to be increased for larger maps
#         return 1000
def gnd_heuristic(p: (int, int, int), map):
    zlist = [0]
    for z in range(0, p[2]):
        if map.occupancy_grid_map[p[0]][p[1]][z] == 255:
            zlist.append(z)
    # print(p, p[2]-max(zlist))
    if p[2]>0:
        return (p[2]-max(zlist))*100
    else:
        return 100
    

#I don't think any of these return cost, that's calculated elsewhere.
def get_movements_4n(x: int, y: int) -> List:
    """
    get all possible 4-connectivity movements.
    :return: list of movements with cost [(dx, dy, movement_cost)]
    """
    return [(x + 1, y + 0),
            (x + 0, y + 1),
            (x - 1, y + 0),
            (x + 0, y - 1)]


def get_movements_8n(x: int, y: int) -> List:
    """
    get all possible 8-connectivity movements.
    :return: list of movements with cost [(dx, dy, movement_cost)]
    """
    return [(x + 1, y + 0),
            (x + 0, y + 1),
            (x - 1, y + 0),
            (x + 0, y - 1),
            (x + 1, y + 1),
            (x - 1, y + 1),
            (x - 1, y - 1),
            (x + 1, y - 1)]

def get_movements_3d_6n(x: int, y: int, z: int) -> List:
    """
    get all possible 6-connectivity movements.
    :return: list of movements with cost [(dx, dy, dz, movement_cost)]
    """
    return [(x+1, y+0, z+0),
            (x-1, y+0, z+0),
            (x+0, y+1, z+0),
            (x+0, y-1, z+0),
            (x+0, y+0, z+1),
            (x+0, y+0, z-1)]
    
def get_movements_3d_26n(x: int, y: int, z: int) -> List:
    """
    get all possible 26-connectivity movements. 
    :return: list of movements with cost [(dx, dy, dz, movement_cost)]
    """
    return [(x+1, y+0, z+0),
            (x+1, y+0, z+1),
            (x+1, y+0, z-1),
            (x+1, y+1, z+0),
            (x+1, y+1, z+1),
            (x+1, y+1, z-1),
            (x+1, y-1, z+0),
            (x+1, y-1, z+1),
            (x+1, y-1, z-1),
            
            (x-1, y+0, z+0),
            (x-1, y+0, z+1),
            (x-1, y+0, z-1),
            (x-1, y+1, z+0),
            (x-1, y+1, z+1),
            (x-1, y+1, z-1),
            (x-1, y-1, z+0),
            (x-1, y-1, z+1),
            (x-1, y-1, z-1),
            
            (x+0, y+0, z+1),
            (x+0, y+0, z-1),
            (x+0, y+1, z+0),
            (x+0, y+1, z+1),
            (x+0, y+1, z-1),
            (x+0, y-1, z+0),
            (x+0, y-1, z+1),
            (x+0, y-1, z-1),
            ]
