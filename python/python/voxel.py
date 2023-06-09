import numpy as np
from utils import get_movements_3d_6n, get_movements_3d_26n, heuristic, Vertices, Vertex
from typing import Dict, List

OBSTACLE = 255
UNOCCUPIED = 0


class OccupancyGridMap:
    def __init__(self, x_dim, y_dim, z_dim, exploration_setting='6N'):
        """
        set initial values for the map occupancy grid
        |----------> y, column
        |           (x=0,y=2)
        |
        V (x=2, y=0)
        x, row
        :param x_dim: dimension in the x direction
        :param y_dim: dimension in the y direction
        """
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.z_dim = z_dim

        # the map extents in units [m]
        self.map_extents = (x_dim, y_dim, z_dim)

        # the obstacle map
        self.occupancy_grid_map = np.zeros(self.map_extents, dtype=np.uint8)

        # obstacles
        self.visited = {}
        self.exploration_setting = exploration_setting

    def get_map(self):
        """
        :return: return the current occupancy grid map
        """
        return self.occupancy_grid_map

    def set_map(self, new_ogrid):
        """
        :param new_ogrid:
        :return: None
        """
        self.occupancy_grid_map = new_ogrid

    def is_unoccupied(self, pos: (int, int, int)) -> bool:
        """
        :param pos: cell position we wish to check
        :return: True if cell is occupied with obstacle, False else
        """
        (x, y, z) = (round(pos[0]), round(pos[1]), round(pos[2]))  # make sure pos is int

        # if not self.in_bounds(cell=(x, y)):
        #    raise IndexError("Map index out of bounds")

        return self.occupancy_grid_map[x][y][z] == UNOCCUPIED

    def in_bounds(self, cell: (int, int, int)) -> bool:
        """
        Checks if the provided coordinates are within
        the bounds of the grid map
        :param cell: cell position (x,y)
        :return: True if within bounds, False else
        """
        (x, y, z) = cell
        return 0 <= x < self.x_dim and 0 <= y < self.y_dim and 0 <= z < self.z_dim
    
    def is_grounded(self, pos: (int, int, int)) -> bool:
        """
        Checks if the provided coordinates are a free cell 
        with an obstacle cell (ground) below.
        """
        (x,y,z) = pos
        if z>0:
            return self.is_unoccupied(pos) and not self.is_unoccupied((x,y,z-1))
        else:
            return self.is_unoccupied(pos)

    def filter(self, neighbors: List, avoid_obstacles: bool):
        """
        :param neighbors: list of potential neighbors before filtering
        :param avoid_obstacles: if True, filter out obstacle cells in the list
        :return:
        """
        if avoid_obstacles:
            return [node for node in neighbors if self.in_bounds(node) and self.is_unoccupied(node)]
        return [node for node in neighbors if self.in_bounds(node)]
    
    # def filter(self, neighbors: List, avoid_obstacles: bool):
    #     """
    #     :param neighbors: list of potential neighbors before filtering
    #     :param avoid_obstacles: if True, filter out obstacle cells in the list
    #     :return:
    #     """
    #     if avoid_obstacles:
    #         return [node for node in neighbors if self.in_bounds(node) and self.is_unoccupied(node) and self.is_grounded(node)]
    #     return [node for node in neighbors if self.in_bounds(node) and self.is_grounded(node)]

    def succ(self, vertex: (int, int, int), avoid_obstacles: bool = True) -> list:
        """
        :param avoid_obstacles:
        :param vertex: vertex you want to find direct successors from
        :return:
        """
        (x, y, z) = vertex

        if self.exploration_setting == '6N':  # change this
            movements = get_movements_3d_6n(x=x, y=y, z=z)
        else:
            movements = get_movements_3d_26n(x=x, y=y, z=z)

        # # not needed. Just makes aesthetics to the path --- commented out
        # if (x + y) % 2 == 0: movements.reverse()

        filtered_movements = self.filter(neighbors=movements, avoid_obstacles=avoid_obstacles)
        return list(filtered_movements)

    def set_obstacle(self, pos: (int, int, int)):
        """
        :param pos: cell position we wish to set obstacle
        :return: None
        """
        (x, y, z) = (round(pos[0]), round(pos[1]), round(pos[2]))  # make sure pos is int
        self.occupancy_grid_map[x, y, z] = OBSTACLE

    def remove_obstacle(self, pos: (int, int, int)):
        """
        :param pos: position of obstacle
        :return: None
        """
        (x, y, z) = (round(pos[0]), round(pos[1]), round(pos[2]))  # make sure pos is int
        self.occupancy_grid_map[x, y, z] = UNOCCUPIED

    def local_observation(self, global_position: (int, int, int), view_range: int = 2) -> Dict:
        """
        :param global_position: position of robot in the global map frame
        :param view_range: how far ahead we should look
        :return: dictionary of new observations
        """
        (px, py, pz) = global_position
        nodes = [(x, y, z) for x in range(px - view_range, px + view_range + 1)
                 for y in range(py - view_range, py + view_range + 1)
                 for z in range(pz - view_range, pz + view_range + 1)
                 if self.in_bounds((x, y, z))]
        return {node: UNOCCUPIED if self.is_unoccupied(pos=node) else OBSTACLE for node in nodes}


class SLAM:
    def __init__(self, map: OccupancyGridMap, view_range: int):
        self.ground_truth_map = map
        self.slam_map = OccupancyGridMap(x_dim=map.x_dim,
                                         y_dim=map.y_dim,
                                         z_dim=map.z_dim,
                                         exploration_setting='26N')
        self.view_range = view_range

    def set_ground_truth_map(self, gt_map: OccupancyGridMap):
        self.ground_truth_map = gt_map

    def c(self, u: (int, int, int), v: (int, int, int)) -> float:
        """
        calcuclate the cost between nodes
        :param u: from vertex
        :param v: to vertex
        :return: euclidean distance to traverse. inf if obstacle in path
        """
        if not self.slam_map.is_unoccupied(u) or not self.slam_map.is_unoccupied(v):
            return float('inf')
        else:
            return heuristic(u, v)

    def rescan(self, global_position: (int, int, int)):

        # rescan local area
        local_observation = self.ground_truth_map.local_observation(global_position=global_position,
                                                                    view_range=self.view_range)

        vertices = self.update_changed_edge_costs(local_grid=local_observation)
        return vertices, self.slam_map

    def update_changed_edge_costs(self, local_grid: Dict) -> Vertices:
        vertices = Vertices()
        for node, value in local_grid.items():
            # if obstacle
            if value == OBSTACLE:
                if self.slam_map.is_unoccupied(node):
                    v = Vertex(pos=node)
                    succ = self.slam_map.succ(node)
                    for u in succ:
                        v.add_edge_with_cost(succ=u, cost=self.c(u, v.pos))
                    vertices.add_vertex(v)
                    self.slam_map.set_obstacle(node)
            else:
                # if white cell
                if not self.slam_map.is_unoccupied(node):
                    v = Vertex(pos=node)
                    succ = self.slam_map.succ(node)
                    for u in succ:
                        v.add_edge_with_cost(succ=u, cost=self.c(u, v.pos))
                    vertices.add_vertex(v)
                    self.slam_map.remove_obstacle(node)
        return vertices
