from controller import Robot,Motor,GPS,Supervisor,Camera,CameraRecognitionObject
import random
from tools import RobotAgent, VisionProcessor, GridManager

TOTAL_OBS = 6
WIDTH = 8
HEIGHT = 8
TOTAL_GRID = WIDTH * HEIGHT
STARTING_X = -0.88
STARTING_Y = -1.05
STARTING_Z = 0.2
GRID_WIDTH = 0.2514
GRID_HEIGHT = 0.2514


robot = Robot()
supervisor = Supervisor()
vision = VisionProcessor(robot)
agent = RobotAgent(robot)
grid =  GridManager(width=8, height=8, start_x=-0.88, start_y=-1.05, tile_w=0.2514, tile_h=0.2514)

all_tiles = []
color_dict = {}
map = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
risk = []
chance = []
#setting up initial values of the risk and chance map
# risk map is to evaluate risk of the point to be lose  in map
# chance map is to evaluate chance of the point to be win in map
for point in range(0,64):
    #left right up down to that specific point
    risk.append([False,False,False,False])
    chance.append([False,False,False,False])
risk[0][0] = True
risk[0][3] = True
risk[7][1] = True
risk[7][3] = True
risk[56][0] = True
risk[56][2] = True
risk[63][1] = True
risk[63][2] = True
risk[1][3] = True
risk[2][3] = True
risk[3][3] = True
risk[4][3] = True
risk[5][3] = True
risk[6][3] = True
risk[8][0] = True
risk[16][0] = True
risk[24][0] = True
risk[32][0] = True
risk[40][0] = True
risk[48][0] = True
risk[7][1] = True
risk[15][1] = True
risk[23][1] = True
risk[31][1] = True
risk[39][1] = True
risk[47][1] = True
risk[57][2] = True
risk[58][2] = True
risk[59][2] = True
risk[60][2] = True
risk[61][2] = True
risk[62][2] = True

chance[0][0] = True
chance[0][3] = True
chance[7][1] = True
chance[7][3] = True
chance[56][0] = True
chance[56][2] = True
chance[63][1] = True
chance[63][2] = True
chance[1][3] = True
chance[2][3] = True
chance[3][3] = True
chance[4][3] = True
chance[5][3] = True
chance[6][3] = True
chance[8][0] = True
chance[16][0] = True
chance[24][0] = True
chance[32][0] = True
chance[40][0] = True
chance[48][0] = True
chance[7][1] = True
chance[15][1] = True
chance[23][1] = True
chance[31][1] = True
chance[39][1] = True
chance[47][1] = True
chance[57][2] = True
chance[58][2] = True
chance[59][2] = True
chance[60][2] = True
chance[61][2] = True
chance[62][2] = True
print(risk)
print(chance)

for obs in all_tiles[7:13]:
    if obs not in [0,1,2,3,4,5,6,7,8,16,24,32,40,48,56,15,23,31,39,47,55,57,58,59,60,61,62,63]:
        risk[obs+1][0] = True #left
        risk[obs-1][1] = True #right
        risk[obs-8][2] = True #up
        risk[obs+8][3] = True #down
        chance[obs+1][0] = True #left
        chance[obs-1][1] = True #right
        chance[obs-8][2] = True #up
        chance[obs+8][3] = True #down
    elif obs == 0:
        risk[obs+1][0] = True #left
        risk[obs+8][3] = True #down
        chance[obs+1][0] = True #left
        chance[obs+8][3] = True #down
    elif obs == 7:
        risk[obs-1][1] = True #right
        risk[obs+8][3] = True #down  
        chance[obs-1][1] = True #right
        chance[obs+8][3] = True #down  
    elif obs == 56:
        risk[obs+1][0] = True #left
        risk[obs-8][2] = True #up
        chance[obs+1][0] = True #left
        chance[obs-8][2] = True #up
    elif obs == 63:  
        risk[obs-1][1] = True #right  
        risk[obs-8][2] = True #up
        risk[obs+8][3] = True #down 
        chance[obs-1][1] = True #right  
        chance[obs-8][2] = True #up
        chance[obs+8][3] = True #down 
    elif obs in [1,2,3,4,5,6]:
        risk[obs+1][0] = True #left
        risk[obs-1][1] = True #right
        risk[obs+8][3] = True #down 
        chance[obs+1][0] = True #left
        chance[obs-1][1] = True #right
        chance[obs+8][3] = True #down 
    elif obs in [8,16,24,32,40,48]:
        risk[obs+1][0] = True #left
        risk[obs+8][3] = True #down 
        risk[obs-8][2] = True #up  
        chance[obs+1][0] = True #left
        chance[obs+8][3] = True #down 
        chance[obs-8][2] = True #up     
    elif obs in [15,23,31,39,47,55]:
        risk[obs-1][1] = True #right
        risk[obs+8][3] = True #down 
        risk[obs-8][2] = True #up 
        chance[obs-1][1] = True #right
        chance[obs+8][3] = True #down 
        chance[obs-8][2] = True #up 
    elif obs in [57,58,59,60,61,62]:
        risk[obs-1][1] = True #right
        risk[obs+1][0] = True #left 
        risk[obs-8][2] = True #up 
        chance[obs-1][1] = True #right
        chance[obs+1][0] = True #left 
        chance[obs-8][2] = True #up 

#generate the tile range scope list in meter
def gen_tile_list():
   tile_list = []
   for y1 in range(-120,100,25):
      for x1 in range(-100,100,25):
         tile_list.append([[x1/100,x1/100+0.25],[y1/100,y1/100+0.25]])
   return tile_list
#random all special tiles
def random_tiles():
    global all_tiles
    n = 14  # Number of all types of tiles
    result = random.sample(range(0, 64), n)
    all_tiles = result
#locate the number of grid 0-63 from the given position in the field
def locate_grid(pos):
    global all_tiles
    count = 0
    for e in gen_tile_list():
        if e[0][0] <= pos[0] <= e[0][1] and e[1][0] <= pos[1] <= e[1][1]:
            return count
        count += 1
#build the 8x8 map with tracking the movement of the robot    

def build_map(cur_pos):
    global map
    print("Global Map is", map)
    grid = locate_grid(cur_pos)
    map[grid//8][grid-(grid//8)*8] = "R"
    print(*map[7])
    print(*map[6])
    print(*map[5])
    print(*map[4])
    print(*map[3])
    print(*map[2])
    print(*map[1])
    print(*map[0])
    
    map[grid//8][grid-(grid//8)*8] = 1
     
#spawn the robot in the grid that does not intefere with others   
def spawn_robot():   
    robo = supervisor
    robo_node = robo.getFromDef('TurtleBot3Burger')    
    range = gen_tile_list()
    translation_field = robo_node.getField('translation') 
    translation_field.setSFVec3f([(range[all_tiles[13]][0][0]+range[all_tiles[13]][0][1])/2,(range[all_tiles[13]][1][0]+range[all_tiles[13]][1][1])/2,0.159505])

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


gps = robot.getDevice("gps")
gps.enable(timestep)

camera = robot.getDevice("camera")
camera.enable(timestep)
# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

#generate the gameover tiles
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
#generate the win tiles
def win():
    w_list= []
    a1 = 0
    b1 = 0
    tile_list = []
    for b1 in range(-120,100,25):
        for a1 in range(-100,100,25):
            tile_list.append([[a1/100,a1/100+0.25],[b1/100,b1/100+0.25]])
    r = 1 # Number of game over tiles
    result = all_tiles[6]
    w_list.append(tile_list[result])
    return w_list
    
#generate the obstacle using spawn_box function
def spawn_boxes(obs_number):
    global all_tiles
    grid_xs = [a-((a//8)*8) for a in all_tiles[7:13]]
    grid_ys = [(a//8) for a in all_tiles[7:13]]
    
   

    for i in range(obs_number):
        pos_x = round((grid_xs[i])*GRID_WIDTH + STARTING_X, 4)
        pos_y = round((grid_ys[i])*GRID_HEIGHT + STARTING_Y, 4)
        pos_z = STARTING_Z
        id = f"Obstacle {i}"
        position = [pos_x, pos_y, pos_z]
        spawn_box(id, position)
        
#make the obstacles appear in the real world
def spawn_box(id, position):
    root = supervisor.getRoot()
    children_field = root.getField('children')
    box_string = f'Solid {{children [ Shape {{ appearance PBRAppearance {{ baseColor 0 0 0 }} geometry Box {{ size 0.2 0.2 0.1 }} }} ] name "{id}"}}'
    children_field.importMFNodeFromString(-1, box_string)
    new_node = children_field.getMFNode(-1)
    translation_field = new_node.getField('translation')
    translation_field.setSFVec3f(position)      
    
    
#run the motor forward
def forward(speed):
   left_motor.setPosition(float("inf"))
   left_motor.setVelocity(speed)
   right_motor.setPosition(float("inf"))
   right_motor.setVelocity(speed)
   #  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

def update_risk(current,stat):
    global risk
    grid_id = locate_grid(current_pos)
    if stat == -1:
       if grid_id not in [0,1,2,3,4,5,6,7,8,16,24,32,40,48,56,15,23,31,39,47,55,57,58,59,60,61,62,63]:
           risk[grid_id+1][0] = True #left
           risk[grid_id-1][1] = True #right
           risk[grid_id-8][2] = True #up
           risk[grid_id+8][3] = True #down
       elif grid_id == 0:
           risk[grid_id+1][0] = True #left
           risk[grid_id+8][3] = True #down
       elif grid_id == 7:
           risk[grid_id-1][1] = True #right
           risk[grid_id+8][3] = True #down  
       elif grid_id == 56:
           risk[grid_id+1][0] = True #left
           risk[grid_id-8][2] = True #up
       elif grid_id == 63:  
           risk[grid_id-1][1] = True #right  
           risk[grid_id-8][2] = True #up
           risk[grid_id+8][3] = True #down 
       elif grid_id in [1,2,3,4,5,6]:
           risk[grid_id+1][0] = True #left
           risk[grid_id-1][1] = True #right
           risk[grid_id+8][3] = True #down 
       elif grid_id in [8,16,24,32,40,48]:
           risk[grid_id+1][0] = True #left
           risk[grid_id+8][3] = True #down 
           risk[grid_id-8][2] = True #up    
       elif grid_id in [15,23,31,39,47,55]:
           risk[grid_id-1][1] = True #right
           risk[grid_id+8][3] = True #down 
           risk[grid_id-8][2] = True #up 
       elif grid_id in [57,58,59,60,61,62]:
           risk[grid_id-1][1] = True #right
           risk[grid_id+1][0] = True #left 
           risk[grid_id-8][2] = True #up 
    elif stat == 1:
       if grid_id not in [0,1,2,3,4,5,6,7,8,16,24,32,40,48,56,15,23,31,39,47,55,57,58,59,60,61,62,63]:
           chance[grid_id+1][0] = True #left
           chance[grid_id-1][1] = True #right
           chance[grid_id-8][2] = True #up
           chance[grid_id+8][3] = True #down
       elif grid_id == 0:
           chance[grid_id+1][0] = True #left
           chance[grid_id+8][3] = True #down
       elif grid_id == 7:
           chance[grid_id-1][1] = True #right
           chance[grid_id+8][3] = True #down  
       elif grid_id == 56:
           chance[grid_id+1][0] = True #left
           chance[grid_id-8][2] = True #up
       elif grid_id == 63:  
           chance[grid_id-1][1] = True #right  
           chance[grid_id-8][2] = True #up
           chance[grid_id+8][3] = True #down 
       elif grid_id in [1,2,3,4,5,6]:
           chance[grid_id+1][0] = True #left
           chance[grid_id-1][1] = True #right
           chance[grid_id+8][3] = True #down 
       elif grid_id in [8,16,24,32,40,48]:
           chance[grid_id+1][0] = True #left
           chance[grid_id+8][3] = True #down 
           chance[grid_id-8][2] = True #up    
       elif grid_id in [15,23,31,39,47,55]:
           chance[grid_id-1][1] = True #right
           chance[grid_id+8][3] = True #down 
           chance[grid_id-8][2] = True #up 
       elif grid_id in [57,58,59,60,61,62]:
           chance[grid_id-1][1] = True #right
           chance[grid_id+1][0] = True #left 
           chance[grid_id-8][2] = True #up                
                                                
random_tiles()

lose = gameover()

win = win()

spawn_boxes(TOTAL_OBS) 

for num in all_tiles[7:13]:
    map[num//8][num-(num//8)*8] = "B"
# Main loop:
# - perform simulation steps until Webots is stopping the controller


#just to reduce the complexity

#img_R = camera.imageGetRed(img)

#move this line to the main loop in the real game
current_pos = gps.getValues()

spawn_robot()    
while robot.step(timestep) != -1:
    st = 0
    current_pos = gps.getValues()
    build_map(current_pos)
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
    c = vision.match_color(color)
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
    
    if (locate_grid(current_pos)+8 in all_tiles[0:6]) or (locate_grid(current_pos)-8 in all_tiles[0:6]) or (locate_grid(current_pos)+1 in all_tiles[0:6]) or (locate_grid(current_pos)-1 in all_tiles[0:6]):
        st = -1
        print("Danger !")
    elif (locate_grid(current_pos)+8 == all_tiles[6]) or (locate_grid(current_pos)-8 == all_tiles[6]) or (locate_grid(current_pos)+1 == all_tiles[6])  or (locate_grid(current_pos)-1 == all_tiles[6]):
        st = 1
        print("Lucky Enough!")
    else:
        print("Still Safe")  
    
    update_risk(current_pos,st)   
    
    ct1 = 0
    for one in risk:
        if one[0] & one[1] & one[2] & one[3] == True:
            map[ct1//8][ct1-(8*(ct1//8))] = "L"
        ct1 += 1
        
    ct2 = 0
    for two in chance:
        if two[0] & two[1] & two[2] & two[3] == True:
            map[ct2//8][ct2-(8*(ct2//8))] = "W"
        ct2 += 1
     

    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass





# Enter here exit cleanup code.
