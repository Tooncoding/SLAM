# main_controller.py

from controller import Robot, Supervisor
from tools import RobotAgent, VisionProcessor, GridManager, GameController, risk_utils
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
risk = [[False] * 4 for _ in range(64)]
chance = [[False] * 4 for _ in range(64)]

# Mark obstacle tiles on the map
grid.mark_batch(all_tiles[7:13], "B")

# Define game logic helpers
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

# Launch game controller
controller = GameController(grid, vision, agent, all_tiles, risk_utils.update_risk, risk, chance, camera)

# Main loop
while robot.step(timestep) != -1:
    current_pos = gps.getValues()
    result = controller.step(current_pos)
    if result in ["win", "lose"]:
        break

print("yayy")
