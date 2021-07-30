# Python3 program for pathfinding visualization
#ref - https://www.youtube.com/watch?v=JtiK0DOeI4A
#ref - https://www.youtube.com/watch?v=OXi4T58PwdM
#ref - https://www.youtube.com/watch?v=jl5yUEdekEM


#We import pygame as this is where most the visualization of program is shown
import pygame
import math
#The priority queue works as an auto-ordering list which is important when we want to decide which node we want to move to.
from queue import PriorityQueue

#Defining WIDTH of my window
WIDTH = 600   #WIDTH determines the number of pixels on the screen
#Setting up the display
WIN = pygame.display.set_mode((WIDTH, WIDTH))   #WIN creates the window we play on
pygame.display.set_caption("A* Path Finding Algorithm")


"""Defining bunch of colours because we are going to need to be using them 
   for actually making the path and making the different squares
   and changing the colour of things and all that"""

#If the colour is red that means we have already looked at it
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
#If the colour is white well then this is a square that we have not yet looked at we could visit it.
WHITE = (255, 255, 255)
#If the colour is black it's a barrier that's something we have to avoid that the algorithm can't use as a node to visit
BLACK = (0, 0, 0)
#If it's purple in colour it will be representing the shortest path
PURPLE = (128, 0, 128)
#If it's orange in colour it's the start node
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


"""Defining a class called spot containing a bunch of methods
    that essentially tell us the state of this spot and also tell 
    us to update the state of this spot as well"""

class Spot:
# Defining a method init
    # Width for how wide is this Spot
    # We are calling total_rows because we need to keep track of how many total rows are there
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        # I can figure out x and y position is, by taking the row that I’m at and multiplying that by the width of all of these cubes
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

#Defining a method get_pos
   #This will just simply be going to return self.row and self.col
    def get_pos(self):
        return self.row, self.col

#Defining a method is_closed
   #In this case we’re going to say what makes a Spot closed.
    def is_closed(self):
        return self.color == RED

#Defining a method is_open
   #is_open is just going to be return self.color == Green so essentially are we in the open set
    def is_open(self):
        return self.color == GREEN

#Defining a method is_barrier
    #is_barrier makes this an obstacle that’s if the colour is equal to black.
    #because we are going to punch it in and we’re going to draw all the obstacles then this is a barrier so what’s we are doing.
    def is_barrier(self):
        return self.color == BLACK

#Defining a method is_start
    #is_start is just going to be return self.color == Orange. So, for the start colour we’ll just go with orange.
    def is_start(self):
        return self.color == ORANGE

#Defining a method is_end
    #is_end is just going to be return self.color == Turquoise. So, for the end colour we’ll just go with turquoise.
    def is_end(self):
        return self.color == TURQUOISE

#Defining a method reset
    #This method simply going to change the colour back to white
    def reset(self):
        self.color = WHITE


    """Now I am going to define pretty much duplicates of methods which I have mentioned above
       with just make in front of them so when I call this it will make this cube whatever it is I’m saying.
       This time instead of just giving them back like are you red are you green this will actually change the colour."""

#Defining a method make_start
    def make_start(self):
        self.color = ORANGE

#Defining a method make_closed
    #with make_closed it stays consistent
    def make_closed(self):
        self.color = RED

#Defining a method make_open
    def make_open(self):
        self.color = GREEN

#Defining a method make_barrier
    def make_barrier(self):
        self.color = BLACK

#Defining a method make_end
    #make_end is just going to be self. self.color == TURQUOISE. So the end colour will be turquoise.
    def make_end(self):
        self.color = TURQUOISE

#Defining a method make_path
    #This is going to be method that tells the path will be in purple colour.
    def make_path(self):
        self.color = PURPLE

    """These methods are a bit more complicated and are involved with the logic behind the drawing."""

#Defining a method draw
    #This line is simply telling pygame to draw a rectangle at the point we specify.This is useful if when we draw the final path back to the start.
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

#Defining a method update_neighbors
    #This is going to take self and this is going to take a grid.
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

#Defining a method  __lt__
   #This performs the same role as an < operator by comparing the values we pass in
    def __lt__(self, other):   #where lt stands for less than
        return False

# Defining a heuristic function that we are going to use for our algorithm
# This function will take 2 co-ordinates of nodes of the grid one being the end node
# and the other being the co-ordinates of the neighbours of the tile we’re on
def h(p1, p2): #Here p1 is point 1 and p2 is point 2
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2) #Here abs is absolute distance

#Defining a method reconstruct_path
#This method is used once we have found the fastest path and reconstructs the path that we have made
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

#Defining a function algorithm
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

# open_set_hash puts a value into the priority queue. We do this so we can run the the while loop on the next line
    # and also we can use this priority queue to backtrack where we have travelled.
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

#This if statement will check if the new g_score is better and if it is then we will make it the next node to use.
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

#Defining a function make_grid
#This function is outside of the spot class and is responsible with making the arrangement of spots so that it makes out a grid.
def make_grid(rows, width):    #rows will be how many rows we have  width of entire grid
    grid = []
    #Doing an integer division will just give us what the gap should be between each of these rows
    #or in other words what the width of each of these cubes should be
    gap = width // rows
    for i in range(rows):
        grid.append([])       #I am going to make 2d list
        for j in range(rows):
            spot = Spot(i, j, gap, rows) #i gonna be row, j gonna be a column, gap that's gonna be it's width
            grid[i].append(spot) #In grid row i we just created that is  grid.append([])
                                 # we're going to append the spot into it.So we have bunch of lists inside lists that all store Spots

    return grid

#Defining a function draw_grid
#Now we draw the grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        #multiply whatever the current index of the row that we're on by the gap
        #and what that will do is it will essentially tell us where we should be drawing the grid line
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

#This draw function is called every time the screen is updated(which is the same as the frame rate of your computer),
# it will also be responsible for the white canvas and then placing each spot into the right place on the grid
def draw(win, grid, rows, width):
    win.fill(WHITE)    #fills the entire screen with white colour

    for row in grid:
        for spot in row:
            spot.draw(win)
    #draw grid lines on top
    draw_grid(win, rows, width)
    pygame.display.update()

#Defining a function get_clicked_pos
#function that can take a mouse position/position and figure out what cube or what spot we actually clicked on
def get_clicked_pos(pos, rows, width): #Here pos is mouse position
    gap = width // rows
    y, x = pos
    #figuring out whatever the position of y and dividing it by the width of each of the cubes
    # so that will give us where we are and what cube I've clicked on
    row = y // gap
    # figuring out whatever the position of x and dividing it by the width of each of the cubes
    # so that will give us where we are and what cube I've clicked on
    col = x // gap

    return row, col

"""This function is the control hub of this entire program and lets us run everything in the correct order. 
   We decide the number of rows here so if you want more or less rows, simply change the value of the rows variable. 
   We first want the grid created so we run the function for it and passing in rows which will alter the sizes of the nodes 
    and grid accordingly so everything fits on the 600x600 pixel window."""

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

#These line are just booleans and variables to make sure the program doesn't start until there is a start and end node.
    start = None
    end = None
    run = True

#These lines are all responsible for the creating the course part of the program before we actually run the pathfinding portion of it.
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

#It will exists the pygame window
    pygame.quit()

main(WIN, WIDTH)

