#%%
from gui import Animation
from d_star_lite import DStarLite
from voxel import OccupancyGridMap, SLAM

OBSTACLE = 255
UNOCCUPIED = 0

if __name__ == '__main__':

    """
    set initial values for the map occupancy grid
    |----------> y, column
    |           (x=0,y=2)
    |
    V (x=2, y=0)
    x, row
    """
    x_dim = 8 
    y_dim = 20
    z_dim = 1
    start = (2, 1, 0)
    goal = (5, 18, 0)
    view_range = 3
 
    gui = Animation(title="D* Lite Path Planning",
                    width=50,
                    height=50,
                    margin=0,
                    x_dim=x_dim,
                    y_dim=y_dim,
                    z_dim=z_dim,
                    start=start,
                    goal=goal,
                    viewing_range=view_range) 

    new_map = gui.world
    old_map = new_map

    new_position = start
    last_position = start

    # new_observation = None
    # type = OBSTACLE

    # D* Lite (optimized)
    dstar = DStarLite(map=new_map,
                      s_start=start,
                      s_goal=goal)

    # SLAM to detect vertices
    slam = SLAM(map=new_map,
                view_range=view_range)

    
    # #Somehow, we need to run the first instance of D* on a populated map, at least with a floor, because otherwise we can't tell it not to fly.
    # slam.set_ground_truth_map(gt_map=new_map)
    # new_edges_and_old_costs, slam_map = slam.rescan(global_position=new_position)

    # dstar.new_edges_and_old_costs = new_edges_and_old_costs
    # dstar.sensed_map = slam_map

    # move and compute path
    path, g, rhs = dstar.move_and_replan(robot_position=new_position)

    while not gui.done:
        # update the map
        # print(path)
        # drive gui
        gui.run_game(path=path)

        new_position = gui.current
        new_observation = gui.observation
        new_map = gui.world

        """
        if new_observation is not None: 
            if new_observation["type"] == OBSTACLE:
                dstar.global_map.set_obstacle(pos=new_observation["pos"])
            if new_observation["pos"] == UNOCCUPIED:
                dstar.global_map.remove_obstacle(pos=new_observation["pos"])
        """  

        if new_observation is not None:
            old_map = new_map
            slam.set_ground_truth_map(gt_map=new_map)

        if new_position != last_position:
            last_position = new_position
            print(new_position)

            # slam
            new_edges_and_old_costs, slam_map = slam.rescan(global_position=new_position)

            dstar.new_edges_and_old_costs = new_edges_and_old_costs
            dstar.sensed_map = slam_map

            # d star
            path, g, rhs = dstar.move_and_replan(robot_position=new_position)
