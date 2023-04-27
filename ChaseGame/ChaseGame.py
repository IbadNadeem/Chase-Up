import pygame
import random
from pygame import mixer

FPS=60
#initialise
pygame.init()

#screen
screen= pygame.display.set_mode((1150,750))

#title and icon
pygame.display.set_caption("Assests/Cat Mouse Chase Mayhem")
icon= pygame.image.load("Assests/icon.png")
pygame.display.set_icon(icon)

#Loading Assests
titleIMG = pygame.image.load("Assests/pixel grass.png")
obstacleIMG =pygame.image.load("Assests/flower ob2.png")
cheeseIMG = pygame.image.load("Assests/flower cheese.png")
playerIMG = pygame.image.load("Assests/grass mouse.png")
catIMG =  pygame.image.load("Assests/grass cat 1.png")
cat2IMG = pygame.image.load("Assests/grass cat 2.png")
background = pygame.image.load("Assests/background.jpeg")
playerIMG = pygame.transform.scale(playerIMG, (75,75))
catIMG = pygame.transform.scale(catIMG, (75,75))
cheeseIMG = pygame.transform.scale(cheeseIMG, (75,75))
obstacleIMG= pygame.transform.scale(obstacleIMG, (75, 75))
titleIMG= pygame.transform.scale(titleIMG, (75, 75))
cat2IMG = pygame.transform.scale(cat2IMG, (75,75))
font= pygame.font.Font("freesansbold.ttf", 32)
font2= pygame.font.Font("freesansbold.ttf", 60)
#Background MUsics
mixer.music.load("Assests/BackgroundMusic.mp3")
mixer.music.play(-1)

#game music
jump= mixer.Sound("Assests/jump.wav")
cheese= mixer.Sound("Assests/cheese.wav")
caught= mixer.Sound("Assests/caught.wav")

def ending(): #ending messagge
  endmsg=font2.render("You got Caught", True,(0,0,0))
  screen.blit(endmsg,(500,400))

def starting(): #displays intructions
  msg=font.render("Use the Teleportal in the centre to evade the cats", True,(0,0,0))
  screen.blit(msg,(50,600))

#Loading Files
#loads the pixel mao which is the foundation of the playable map.
#it has 0 and 1 . Characters can moved on the spaces with 0 only
def LoadPixelGrid(fileName):
  pixels= []
  this_file = open(fileName, "r")
  enteries = int(this_file.readline())
  for this_line in range(0, enteries):
    pixels.append(this_file.readline().split())
  return pixels

#creates a graph using the location file which tells what directions can the player move while on a certain node
def LoadCordMap(fileName):
  cord_dict= {}
  this_file = open(fileName, "r")
  enteries = int(this_file.readline())
  for this_line in range(0, enteries):
    this_cord = this_file.readline().split() 
    cord_dict[this_cord[0]] = (this_cord[1] , this_cord[2])
  return cord_dict

#Helps creating the graph for game mechanics
def LoadGraph(fileName):
  edges = []
  nodes = []
  this_file = open(fileName, "r")
  enteries = int(this_file.readline())
  for i in range(0, enteries):
    relation = this_file.readline().split()
    if relation[2] == "Right" :
      edges.append((relation[0], relation[1], relation[2], relation[3]))
      edges.append((relation[1], relation[0], "Left", relation[3]))
    else:
      edges.append((relation[0], relation[1], relation[2], relation[3]))
      edges.append((relation[1], relation[0], "Up", relation[3])) 
    if (relation[0] in nodes) == False:
      nodes.append(relation[0])
    if (relation[1] in nodes) == False:
      nodes.append(relation[1])
  this_graph = Create(nodes)
  return AddEdges(this_graph, edges)

#Helper functions 
def Create(nodes):
  graph={}
  for this_node in nodes:
    graph[this_node]=[]
  return graph

def AddEdge(graph, source, target, direction, weight):
  these_edges = graph[source]
  these_edges.append((target, direction, weight)) 
  graph[source] = (these_edges)
  return graph

def AddEdges(graph, edges):
  for this_edge in edges:
    graph = AddEdge(graph, this_edge[0], this_edge[1], this_edge[2], this_edge[3])
  return graph

#GUI
#creates the visual for the map 
#also controls the mechanics for the movements of the sprites
def map(pixels, player_position, cat1_position, cat2_positon, cheese_position, cordinate_map):
    titleX = 50
    titleY = 50
    cheese_coordinate = cordinate_map[cheese_position]
    player_coordinates = cordinate_map[player_position]
    cat1_coordinates = cordinate_map[cat1_position]
    cat2_coordinates = cordinate_map[cat2_position]
    for i in range(0, len(pixels)):
        for j in range(0,len(pixels[i])):
            if (player_coordinates[0] == str(i)) and (player_coordinates[1] == str(j)):
                screen.blit(playerIMG, ( titleX + 50*(j), titleY ))
            elif ((cat1_coordinates[0] == str(i)) and (cat1_coordinates[1] == str(j))):
                screen.blit(catIMG, ( titleX + 50*(j), titleY ))
            elif ((cat2_coordinates[0] == str(i)) and (cat2_coordinates[1] == str(j))):
                screen.blit(cat2IMG, ( titleX + 50*(j), titleY ))
            elif (cheese_coordinate[0] == str(i)) and (cheese_coordinate[1] == str(j)):
                screen.blit(cheeseIMG, ( titleX + 50*(j), titleY ))
            elif pixels[i][j] == "1":
                screen.blit(obstacleIMG, ( titleX + 50*(j), titleY ))
            else:
                screen.blit(titleIMG, ( (titleX + 50*(j)), titleY ))
        titleY = titleY + 60
        titleX = 50

#displayes the score
def show_score():
  score_display = font.render("Score : " + str(score), True, (0,0,0))
  screen.blit(score_display, (0,0))


#Functions that make the game work

#generates spawning positions
def Positions(game_map):
  # import random
  player_position = str(random.randint(1,len(game_map)))
  cat1_position = str(CPU_Position(player_position, game_map))
  cat2_position = str(CPU_Position(player_position, game_map))
  cheese_position = str(CPU_Position(player_position, game_map))
  return player_position, cat1_position, cheese_position, cat2_position

#generates random position for the CPU 
def CPU_Position(player_position, game_map):
  #import random
  x = random.randint(1,len(game_map))
  while x == player_position :
      x = random.randint(1,36)
  return x

#updates the location of the CPU randomly
def Update_CPU_location(cpu_location, game_map):
    #import random
    places = []
    possible_locations = game_map[cpu_location]
    for this_location in possible_locations:
      places.append(this_location[0])
    return random.choice(places)

def getOutNeighbours(G,node):
    neighbours = []
    these_edges = G[node]
    for i in these_edges:
        neighbours.append(i[0])
    return neighbours


def getShortestPath(graph, source, destination):
  parents, node_cost = Dijkstra(graph, source, destination)
  path = []
  current_node = destination 
  while parents[current_node] != None:
    path.append(parents[current_node])
    current_node= parents[current_node]
  path.reverse()
  if len(path) == 1:
    return destination
  elif len(path) == 0:
    return source
  else:
    return path[1]


#The Intelligent enemy cat uses Djikstra's algorithm to calculate the shortesdt path from the mouse and chase it
def Dijkstra(graph, source, destination):
  priority_queue = []
  visited = {} #Stores which nodes have been visted 
  parents = {} #Stores which node is a parent of which node
  node_cost = {} #Stores the distance from Source node to each node

  #Initalizing Everything 
  for node in graph:
    visited[node] = False 
    parents[node] = None
    if node == source:
      node_cost[node] = 0
      priority_queue.append((0, node))
    else:
      node_cost[node] = 10000000000

  while len(priority_queue) != 0:
    current_node = DeQueue(priority_queue)
    visited[current_node] = True

    adjacent_nodes = getOutNeighbours(graph, current_node)
    for adj_node in adjacent_nodes:
      if visited[adj_node] == False:
        new_cost = node_cost[current_node] + GetWeight(graph, current_node, adj_node)
        if node_cost[adj_node] > new_cost:
          parents[adj_node] = current_node
          node_cost[adj_node] = new_cost
          priority_queue = EnQueue(priority_queue, (new_cost, adj_node))
      if adj_node == destination:
        break
    if adj_node == destination:
      break
  return parents, node_cost

#caluclates the weight of the edge, assists in Djikstra Algorithm
def GetWeight(graph, source, target):
  these_edges = graph[source]
  for edge in these_edges:
    if edge[0] == target:
      return int(edge[2])
  return -1 


#Queue Helper functions
def DeQueue(pq):
  item = pq[0]
  del pq[0]
  return item[1]

def EnQueue(pq, item):
  if len(pq) == 0:
    pq.append(item)
    return pq
  if item[0] < pq[0][0]:
    pq.insert(0, item)
    return pq
  for i in range(0, len(pq)-1): 
    if pq[i][0] <= item[0] and item[0] < pq[i+1][0]:
      pq.insert(i, item)
      return pq
  pq.append(item)
  return pq






#game loop
running= True

pixels = LoadPixelGrid("Assests/pixel_grid.txt")
cordinate_map = LoadCordMap("Assests/location.txt")
game_map = LoadGraph("Assests/map.txt")
score = 0
print(game_map)

player_position, cat1_position, cheese_position, cat2_position = Positions(game_map)

screen.blit(background, (0,0))
screen.blit(background, (550,0))
screen.blit(background, (1100,0))
screen.blit(background, (0,550))
screen.blit(background, (550, 550))
screen.blit(background, (1100,550))
map(pixels, player_position, cat1_position, cat2_position, cheese_position, cordinate_map)
show_score()
starting()
pygame.display.update()



#mouse=pygame.Rect(100,100,P_height,P_width)
clock=pygame.time.Clock()

while running==True:
    clock.tick(FPS)


    keys_pressed=pygame.key.get_pressed()
    

    # if keys_pressed[pygame.K_UP]:
    #   mouse.y-=3
    # if keys_pressed[pygame.K_DOWN]:
    #   mouse.y+=3
    # if keys_pressed[pygame.K_LEFT]:
    #   mouse.x-=3
    # if keys_pressed[pygame.K_RIGHT]:
    #   mouse.x+=3
    player_move = False 
    while player_move == False: 

        possible_locations = game_map[player_position]
        choices = []
        for this_choice in possible_locations:
            choices.append(this_choice[1])
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
           if event.type== pygame.QUIT:
            running=False
            player_move=True 

           if event.type== pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
              jump.play()
              if ("Left" in choices) == True:
                    for this_location in possible_locations:
                        if this_location[1] == "Left":
                          player_position = this_location[0]
                          player_move = True

            if event.key==pygame.K_RIGHT:
              jump.play()
              if ("Right" in choices) == True:
                    for this_location in possible_locations:
                        if this_location[1] == "Right":
                          player_position = this_location[0]
                          player_move = True

            if event.key==pygame.K_UP:
              jump.play()
              if ("Up" in choices) == True:
                    for this_location in possible_locations:
                        if this_location[1] == "Up":
                          player_position = this_location[0]
                          player_move = True

            if event.key==pygame.K_DOWN:
              jump.play()
              if ("Down" in choices) == True:
                    for this_location in possible_locations:
                        if this_location[1] == "Down":
                          player_position = this_location[0]
                          player_move = True 

    if player_position == cheese_position:
        cheese.play()
        score = score + 100
        cheese_position = str(CPU_Position(player_position, game_map))
        screen.blit(background, (0,0))
        show_score()
    if player_position == "93":
        player_position = str(CPU_Position(player_position, game_map))
    
    cat1_position = Update_CPU_location(cat1_position, game_map)
    cat2_position = getShortestPath(game_map, cat2_position, player_position)
    map(pixels, player_position, cat1_position, cat2_position, cheese_position, cordinate_map)
    pygame.display.update()
    if (player_position == cat1_position) or (player_position == cat2_position):
       #Checking if the cat ran into the player
        ending()
        pygame.display.update()
        pygame.time.delay(500)
        break

pygame.quit()
