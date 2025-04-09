
from controller import Robot,Motor,GPS,Supervisor,Camera,CameraRecognitionObject
import random
<<<<<<< HEAD
=======
import numpy as np
import time
from control_tools import ControlTools

>>>>>>> origin/main
TOTAL_OBS = 6
WIDTH = 8
HEIGHT = 8
TOTAL_GRID = WIDTH * HEIGHT
STARTING_X = -0.88
STARTING_Y = -1.05
STARTING_Z = 0.2
GRID_WIDTH = 0.2514
GRID_HEIGHT = 0.2514
<<<<<<< HEAD

=======
MAX_SPEED = 4
WHEEL_RADIUS = 0.033
WHEEL_BASE = 0.18
>>>>>>> origin/main

robot = Robot()
supervisor = Supervisor()
all_tiles = []
color_dict = {}

<<<<<<< HEAD
=======
theta_integral = 0.0 
distance_integral = 0.0
v = 1.0   # Linear velocity (adjust as needed)

>>>>>>> origin/main
def gen_tile_list():
   tile_list = []
   for y1 in range(-100,100,25):
      for x1 in range(-100,100,25):
         tile_list.append([[x1/100,x1/100+0.25],[y1/100,y1/100+0.25]])
   return tile_list
def random_tiles():
    global all_tiles
    n = 13  # Number of all types of tiles
    result = random.sample(range(0, 64), n)
    all_tiles = result


# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


gps = robot.getDevice("gps")
gps.enable(timestep)

camera = robot.getDevice("camera")
camera.enable(timestep)
<<<<<<< HEAD
# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
=======

# Init motors
>>>>>>> origin/main
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))
left_motor.setVelocity(0)
right_motor.setVelocity(0)

# Init motor controller
controller = ControlTools(robot, left_motor, right_motor)


def gameover():
    gg_tiles = []
    x1 = 0
    y1 = 0
    n = 6  # Number of game over tiles
    result = all_tiles[0:6]
    #tile_list
    tl = gen_tile_list()
    gg_tiles.append([tl[result[0]],tl[result[1]],tl[result[2]],
    tl[result[3]],tl[result[4]],tl[result[5]]])

    update_tiles = gg_tiles
    return gg_tiles

def win():
    w_list= []
    a1 = 0
    b1 = 0
    tile_list = []
    for b1 in range(-100,100,25):
        for a1 in range(-100,100,25):
            tile_list.append([[a1/100,a1/100+0.25],[b1/100,b1/100+0.25]])
    r = 1 # Number of game over tiles
    result = all_tiles[6]
    w_list.append(tile_list[result])
    return w_list
    

def spawn_boxes(obs_number):
    global all_tiles
    grid_xs = [a-((a//8)*8) for a in all_tiles[7:13]]
    grid_ys = [(a//8) for a in all_tiles[7:13]]
<<<<<<< HEAD
    
   
=======
>>>>>>> origin/main

    for i in range(obs_number):
        pos_x = round((grid_xs[i])*GRID_WIDTH + STARTING_X, 4)
        pos_y = round((grid_ys[i])*GRID_HEIGHT + STARTING_Y, 4)
        pos_z = STARTING_Z
        id = f"Obstacle {i}"
        position = [pos_x, pos_y, pos_z]
        spawn_box(id, position)
        
<<<<<<< HEAD

def spawn_box(id, position):
    root = supervisor.getRoot()
    children_field = root.getField('children')
    box_string = f'Solid {{children [ Shape {{ appearance PBRAppearance {{ baseColor 0 0 0 }} geometry Box {{ size 0.2 0.2 0.1 }} }} ] name "{id}"}}'
    children_field.importMFNodeFromString(-1, box_string)
    new_node = children_field.getMFNode(-1)
    translation_field = new_node.getField('translation')
    translation_field.setSFVec3f(position)      
    
    

def forward(speed):
   left_motor.setPosition(float("inf"))
   left_motor.setVelocity(speed)
   right_motor.setPosition(float("inf"))
   right_motor.setVelocity(speed)
   #  ds = robot.getDevice('dsname')
#  ds.enable(timestep)
=======

def spawn_box(id, position):
    root = supervisor.getRoot()
    children_field = root.getField('children')
    box_string = f'Solid {{children [ Shape {{ appearance PBRAppearance {{ baseColor 0 0 0 }} geometry Box {{ size 0.2 0.2 0.1 }} }} ] name "{id}"}}'
    children_field.importMFNodeFromString(-1, box_string)
    new_node = children_field.getMFNode(-1)
    translation_field = new_node.getField('translation')
    translation_field.setSFVec3f(position)      
    
    
>>>>>>> origin/main
def col_match(color):
  col = 0
  if [253,236,253]<color<[253,240,253]: #[[253,236,253],[253,237,253],[253,238,253]]:
      #print("col1")
      col = 1
  elif [226,0,0]<color<[228,255,255]:  #[[226,226,253],[226,227,253],[227,227,253]]:
      #print("col2")
      col = 2
  elif [222,253,253]<color <[225,255,255]:#[[223,253,253],[224,253,253],[225,253,253]]:
      #print("col3")
      col = 3
  elif [238,255,250]<color< [243,255,250]:#[[240,255,250],[241,255,250],[242,255,250]]:
      #print("col4")
      col = 4
  elif [253,250,0]<color< [253,255,255]:#[[253,252,215],[253,252,216],[253,252,217]]:
      #print("col5")
      col = 5
  elif [230,120,120]<color< [233,255,255]: #[[232,170,153],[232,171,153],[232,172,153]]:
      #print("col6")
      col = 6
  elif [253,170,200]<color< [253,300,255]:#[[253,194,202],[253,195,202],[253,196,202]]:
      #print("col7")
      col = 7
  elif [213,195,200]<color< [220,199,202]:#[[214,198,200],[214,199,200],[214,200,200]]:
      #print("col8")
      col = 8
  else:
      col = 0
  return col
<<<<<<< HEAD
=======

>>>>>>> origin/main
def pixel_area(col,img):
    count = 0
    end = 0
    if col == 1:
        for j in range(0,256):
            for i in range(0,256):
                if  [253,236,253]<img[i][j] <[253,240,253]: 
                    count += 1    
        return count   
    if col == 2:
       for j in range(0,256):
            for i in range(0,256):
                if [226,0,0]<img[i][j]<[228,255,255]:
                    count += 1
       return count   
    if col == 3:
       for j in range(0,256):
            for i in range(0,256):
                if [222,253,253]<img[i][j] <[225,253,253]:
                    count += 1
       return count
    if col == 4:
       for j in range(0,256):
            for i in range(0,256):
                if [238,255,250]<img[i][j] < [243,255,250]:
                    count += 1
       return count   
    if col == 5:
       for j in range(0,256):
            for i in range(0,256):
                if [253,250,0]<img[i][j]< [253,255,255]:
                    count += 1
       return count   
    if col == 6:
       for j in range(0,256):
            for i in range(0,256):
                if [231,120,120]<img[i][j]< [233,255,255]:
                    count += 1
       return count
    if col == 7:
       for j in range(0,256):
            for i in range(0,256):
                if [253,170,200]<img[i][j]< [253,200,255]:
                    count += 1
       return count   
    if col == 8:
       for j in range(0,256):
            for i in range(0,256):
                if [213,195,200]<img[i][j]< [220,199,202]:
                    count += 1
       return count 
    else:
        return count  
def row_match(count):
    if count > 38000:
        return "row1"
    elif 20000<count < 38000:
        return "row2"
    elif 10000<count < 20000:
        return "row3"
    elif 7000<count < 10000:
        return "row4"
    elif 4000<count <7000:
        return "row5"
    elif 2700<count < 4000:
        return "row6"
    elif 2000<count < 2700:
        return "row7"
    elif 0<=count < 2000:
        return "row8"    
                   
                                                
random_tiles()
<<<<<<< HEAD

lose = gameover()

=======

lose = gameover()

>>>>>>> origin/main
win = win()

spawn_boxes(TOTAL_OBS) 
# Main loop:
# - perform simulation steps until Webots is stopping the controller


#just to reduce the complexity

#img_R = camera.imageGetRed(img)

#move this line to the main loop in the real game
current_pos = gps.getValues()

<<<<<<< HEAD
=======
controller.move_forward()
controller.clockwise_spin()
controller.move_forward()
controller.clockwise_spin()
controller.move_forward()
controller.clockwise_spin()
controller.move_forward()
>>>>>>> origin/main
    
while robot.step(timestep) != -1:
   
    """
    for x in range(0,camera.getWidth()):
     for y in range(0,camera.getHeight()):
          red   = img[x][y][0]
          green = img[x][y][1]
          blue  = img[x][y][2]
    """ 
    """
    img = camera.getImageArray()
    w = camera.getWidth()
    h = camera.getHeight() 
    red   = img[int(w/2)][int(h/2)][0] 
    green = img[int(w/2)][int(h/2)][1]
    blue  = img[int(w/2)][int(h/2)][2]  
    print(str(red) +","+ str(green) +","+ str(blue)) 
    
    """
    img = camera.getImageArray()
    w = camera.getWidth()
    h = camera.getHeight() 
    red   = img[int(w/2)][int(h/2)][0] 
    green = img[int(w/2)][int(h/2)][1]
    blue  = img[int(w/2)][int(h/2)][2]  
    color = [red,green,blue]
    camera.saveImage("test.jpg",100)
    #break
    #print(str(red) +","+ str(green) +","+ str(blue)) 
    #c = column
    c = col_match(color)
    print(c)
    print(pixel_area(c,img))
    print(row_match(pixel_area(c,img)))
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
<<<<<<< HEAD
     
        
       
    
     
=======
>>>>>>> origin/main

    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass





# Enter here exit cleanup code.
