from controller import Supervisor
import random

TOTAL_OBS = 6
WIDTH = 8
HEIGHT = 8
TOTAL_GRID = WIDTH * HEIGHT
STARTING_X = -0.88
STARTING_Y = -1.05
STARTING_Z = 0.2
GRID_WIDTH = 0.2514
GRID_HEIGHT = 0.2514

supervisor = Supervisor()

time_step = int(supervisor.getBasicTimeStep())

def spawn_boxes(obs_number):
    grid_xs = random.sample(range(WIDTH), obs_number)
    grid_ys = random.sample(range(HEIGHT), obs_number)
    for i in range(obs_number):
        pos_x = round((grid_xs[i])*GRID_WIDTH + STARTING_X, 4)
        pos_y = round((grid_ys[i])*GRID_HEIGHT + STARTING_Y, 4)
        pos_z = STARTING_Z
        id = f"Obstacle {i}"
        position = [pos_x, pos_y, pos_z]
        spawn_box(id, position)
        

def spawn_box(id, position):
    root = supervisor.getRoot()
    children_field = root.getField('children')
    box_string = f'Solid {{children [ Shape {{ appearance PBRAppearance {{ baseColor 0 0 0 }} geometry Box {{ size 0.2 0.2 0.1 }} }} ] name "{id}"}}'
    print(box_string)
    children_field.importMFNodeFromString(-1, box_string)
    new_node = children_field.getMFNode(-1)
    translation_field = new_node.getField('translation')
    translation_field.setSFVec3f(position)

    # Main loop
while supervisor.step(time_step) != -1:
    # Example: Spawn a box at position (1, 0, 1) after 5 seconds
    if supervisor.getTime() > 2.0:
        spawn_boxes(TOTAL_OBS)   
        
        break