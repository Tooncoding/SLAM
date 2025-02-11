"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,Motor,GPS
import random

robot = Robot()
# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


gps =robot.getDevice("gps")
gps.enable(timestep)

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

def gameover():
    x1 = 0
    y1 = 0
    tile_list = []
    for y1 in range(-100,100,25):
        for x1 in range(-100,100,25):
            tile_list.append([[x1/100,x1/100+0.25],[y1/100,y1/100+0.25]])
    n = 6  # Number of game over tiles
    result = random.sample(range(0, 64), n)
    gg_tiles = []
    gg_tiles.append([tile_list[result[0]],tile_list[result[1]],tile_list[result[2]],
    tile_list[result[3]],tile_list[result[4]],tile_list[result[5]]])
    
    update_tiles = gg_tiles
    return gg_tiles

def win():
    a1 = 0
    b1 = 0
    tile_list = []
    w_list = []
    for b1 in range(-100,100,25):
        for a1 in range(-100,100,25):
            tile_list.append([[a1/100,a1/100+0.25],[b1/100,b1/100+0.25]])
    r = 2 # Number of game over tiles
    result = random.sample(range(0, 64), r)
    if tile_list[result[0]] in lose[0]:
        w_list.append(tile_list[result[1]])
    if tile_list[result[1]] in lose[0]:
        w_list.append(tile_list[result[0]])
    else:
        w_list.append(tile_list[result[0]])
    return w_list 
        
    
    

def forward(speed):
   left_motor.setPosition(float("inf"))
   left_motor.setVelocity(speed)
   right_motor.setPosition(float("inf"))
   right_motor.setVelocity(speed)
   #  ds = robot.getDevice('dsname')
#  ds.enable(timestep)
lose = gameover()
print(lose)
win = win()
print("win", win)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    current_pos = gps.getValues()
    print(current_pos)
    #just to reduce the complexity
    con = lose[0]
    if ((con[0][0][0]<=current_pos[0]<=con[0][0][1] and con[0][1][0]<=current_pos[1]<=con[0][1][1])
    or (con[1][0][0]<=current_pos[0]<=con[1][0][1] and con[1][1][0]<=current_pos[1]<=con[1][1][1])
    or (con[2][0][0]<=current_pos[0]<=con[2][0][1] and con[2][1][0]<=current_pos[1]<=con[2][1][1])
    or (con[3][0][0]<=current_pos[0]<=con[3][0][1] and con[3][1][0]<=current_pos[1]<=con[3][1][1])
    or (con[4][0][0]<=current_pos[0]<=con[4][0][1] and con[4][1][0]<=current_pos[1]<=con[4][1][1])
    or (con[5][0][0]<=current_pos[0]<=con[5][0][1] and con[5][1][0]<=current_pos[1]<=con[5][1][1])):
       print("you lost")
       print("you lost")
       print("you lost")
       break
    elif (win[0][0][0] <= current_pos[0]<= win[0][0][1]) and (win[0][1][0] <= current_pos[1]<= win[0][1][1]):
       print("win")
       print("win")
       print("win")
       break
         
        
       
    
     

    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
