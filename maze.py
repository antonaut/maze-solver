# coding=utf-8

# Maze solver by <aerholt@kth.se>.
# -- Solves the impossible maze from mazes.org.uk by a simple bfs.

# Uses a coordinate system with origo (0, 0) in topleft position.
# Positive x →
# Positive y ↓
# Coordinates are given as tuples (x, y), sometimes with an added
# direction pointer to the parent location.

from PIL import Image
import os

FILENAME = "impossible.gif"
START_COORD = (1, 1)
END_COORD = (399, 400)

# Tokens used for backtracking
START_TOKEN = 'S'
END_TOKEN = 'E'
LEFT = 'L'
RIGHT = 'R'
UP = 'U'
DOWN = 'D'
UNEXPLORED = 'X'

# Colors used for paths
START_COLOR = (255, 255, 75)
PATH_COLOR = (255, 30, 75)
END_COLOR = (255, 30, 255)


def read_maze_from_file(filename):
    """Reads a .gif and returns a 2d-list of ones and zeroes
    plus its dimension as a 3-tuple.
    Ones represent walls (non-walkable) and zeroes the floor
    (walkable)."""
    im = Image.open(filename).convert("1")
    px = im.load()
    maze = []
    xmax, ymax = im.size
    for y in range(ymax):
        maze.append([])
        for x in range(xmax):
            if px[x,y] == 255:
                maze[y].append(0)
            else:
                maze[y].append(1)
    return maze, xmax, ymax

def print_2d(mat):
    xmax, ymax = len(mat[0]), len(mat)
    for y in range(ymax):
        for x in range(xmax):
            print mat[y][x],
        print


def get_unvisited_neighbours(maze, visited, node):
    x = node[0]
    y = node[1]
    neighbours = []

    #print "checking neighbours of ({}, {}): ".format(x, y)
    if y >= 0 and y < (len(maze)-1):
        n = checkDown(maze, visited, x, y)
        if n != None:
            neighbours.append(n)
    if y > 0 and y <= (len(maze)-1):
        n = checkUp(maze, visited, x, y)
        if n != None:
            neighbours.append(n)

    if x >= 0 and x < (len(maze[0])-1):
        n = checkRight(maze, visited, x, y)
        if n != None:
            neighbours.append(n)
    if x > 0 and x <= (len(maze[0])-1):
        n = checkLeft(maze, visited, x, y)
        if n != None:
            neighbours.append(n)

    return neighbours


def checkLeft(maze, visited, x, y):
    n = (x-1, y, RIGHT)
    if visited[y][x-1] == UNEXPLORED and maze[y][x-1] == 0:
        #print "found neighbour Left ({}, {})".format(x-1, y)
        return n

def checkRight(maze, visited, x, y):
    n = (x+1, y, LEFT)
    if visited[y][x+1] == UNEXPLORED and maze[y][x+1] == 0:
        #print "found neighbour Right ({}, {})".format(x+1, y)
        return n

def checkDown(maze, visited, x, y):
    n = (x, y+1, UP)
    if visited[y+1][x] == UNEXPLORED and maze[y+1][x] == 0:
        #print "found neighbour Down ({}, {})".format(x, y+1)
        return n

def checkUp(maze, visited, x, y):
    n = (x, y-1, DOWN)
    if visited[y-1][x] == UNEXPLORED and maze[y-1][x] == 0:
        #print "found neighbour Up ({}, {})".format(x, y-1)
        return n

def bfs(maze, start, end):
    """Breadth first search.
    - maze is the graph as a 2D-list.
    - get_unvisited_neighbours is the successor function.

    Returns a 2D-list with the visited nodes,
    describing the way from end to start."""

    visited = []
    for i in range(len(maze)):
        visited.append([])
        for j in range(len(maze[0])):
            visited[i].append(UNEXPLORED)

    print "Visited matrix dimensions: {}x{}".format(
    str(len(visited)),
    str(len(visited[0])))


    queue = []
    visited[start[1]][start[0]] = START_TOKEN
    for n in get_unvisited_neighbours(maze, visited, start):
        queue.insert(0, n)

    while len(queue) > 0:
        x, y, parent_direction = queue.pop(0) # dequeue
        node = (x, y, parent_direction)
        visited[y][x] = parent_direction # mark as visited

        if x == end[0] and y == end[1]: # check if done
            print "Found path."
            return visited
        for n in get_unvisited_neighbours(maze, visited, node):
            queue.insert(0, n)
            #print queue
            #print_2d(visited)

    print "Couldn't find path."
    return []


def solve(maze, start, end):
    print "Solving maze of size: {}x{}".format(len(maze),len(maze[0]))
    print "Calling bfs(start={}, end={})".format(start, end)
    visited = bfs(maze, start, end)
    return visited


def backtrack_pixels(sol, out, start, end):
    x, y = end
    sym = sol[y][x]
    print "Backtracking from {},{} = {}".format(x, y, sym)
    while sym != START_TOKEN:
        if sym == UP:
            y = y - 1
        elif sym == DOWN:
            y = y + 1
        elif sym == LEFT:
            x = x - 1
        else: # sym == RIGHT
            x = x + 1
        out.putpixel((x, y), PATH_COLOR)
        sym = sol[y][x]
        print "Backtracking: {},{} = {}".format(x, y, sym)

    print "Backtracking done."
    out.putpixel(start, START_COLOR)
    out.putpixel(end, END_COLOR)
    out.save("SOLUTION.gif")
    print "Solution written to image."
    return



def main():
    maze, xmax, ymax = read_maze_from_file(FILENAME)
    print "Printing maze."
    print_2d(maze)
    start = START_COORD
    end = END_COORD
    sol = solve(maze, start, end)
    print "Printing solution."
    print_2d(sol)
    print "Writing search space image."
    out = Image.new('RGB', (xmax, ymax), 0)
    for j, _ in enumerate(sol):
        for i, px in enumerate(sol[j]):
            c = (0, 0, 0)
            if maze[j][i] == 0:
                c = (255, 255, 255)
            if px != UNEXPLORED:
                c = (c[0]/3, c[1]/3, c[2]/3)
            out.putpixel((i, j), c)
    out.save("SEARCH_SPACE.gif")
    backtrack_pixels(sol, out, start, end)

if __name__ == '__main__':
    main()
