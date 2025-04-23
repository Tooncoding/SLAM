# my_controller.py

from controller import Robot, Supervisor
from tools import RobotAgent, VisionProcessor, GridManager
import random

# Constants
TOTAL_OBS = 6
WIDTH, HEIGHT = 8, 8
STARTING_X, STARTING_Y, STARTING_Z = -0.88, -1.05, 0.2
GRID_WIDTH, GRID_HEIGHT = 0.2514, 0.2514

# Initialization
robot = Robot()
supervisor = Supervisor()
vision = VisionProcessor(robot)
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))
left_motor.setVelocity(0)
right_motor.setVelocity(0)

agent = RobotAgent(robot, left_motor, right_motor)
grid = GridManager(WIDTH, HEIGHT, STARTING_X, STARTING_Y, GRID_WIDTH, GRID_HEIGHT)

# Randomly generate tile indices
all_tiles = random.sample(range(64), 14)

# Mark obstacle tiles on the map
grid.mark_batch(all_tiles[7:13], "B")

# Define game logic helpers
def get_win_tile():
    return grid.get_tile_bounds(all_tiles[6])

def get_lose_tiles():
    return grid.get_region_bounds(all_tiles[0:6])

def is_within(pos, bounds):
    return bounds[0][0] <= pos[0] <= bounds[0][1] and bounds[1][0] <= pos[1] <= bounds[1][1]

def spawn_robot():
    robo_node = supervisor.getFromDef('TurtleBot3Burger')
    center = grid.get_tile_center(all_tiles[13])
    if center:
        robo_node.getField('translation').setSFVec3f([center[0], center[1], 0.159505])

def spawn_obstacles():
    root = supervisor.getRoot()
    children_field = root.getField('children')
    for i, idx in enumerate(all_tiles[7:13]):
        pos = grid.get_tile_center(idx)
        if pos:
            pos_x = round(pos[0], 4)
            pos_y = round(pos[1], 4)
            pos_z = STARTING_Z
            box_string = f'Solid {{children [ Shape {{ appearance PBRAppearance {{ baseColor 0 0 0 }} geometry Box {{ size 0.2 0.2 0.1 }} }} ] name "Obstacle {i}"}}'
            children_field.importMFNodeFromString(-1, box_string)
            children_field.getMFNode(-1).getField('translation').setSFVec3f([pos_x, pos_y, pos_z])

# Setup devices
timestep = int(robot.getBasicTimeStep())
gps = robot.getDevice("gps")
gps.enable(timestep)
camera = robot.getDevice("camera")
camera.enable(timestep)

# Spawn world elements
spawn_robot()
spawn_obstacles()

# Main Loop
while robot.step(timestep) != -1:
    current_pos = gps.getValues()
    grid.update_robot_position(current_pos)
    grid.print_map()

    color = vision.get_center_pixel_color()
    label = vision.match_color(color)
    print("Color Label:", label)

    for bounds in get_lose_tiles():
        if is_within(current_pos, bounds):
            print("you lost")
            break
    else:
        win_tile = get_win_tile()
        if is_within(current_pos, win_tile):
            print("win")
            break

