import os

def generate_grid():
    configuration = open("configuration.txt", "r")
    lines = configuration.readlines()

    width = 0

    for i in range(len(lines)):
        if len(lines[i]) > width:
            width = len(lines[i])   

    grid = [[False for j in range(width)] for i in range(len(lines))]

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "x":
                grid[i][j] = True
    
    return grid

def surrounding_cells(grid, i, j):
    width = len(grid[0])
    count = 0

    # Top left
    if i-1 >= 0 and j-1 >= 0 and grid[i-1][j-1] == True:
        count += 1
    
    # Top
    if i-1 >= 0 and grid[i-1][j] == True:
        count += 1
    
    # Top right
    if i-1 >= 0 and j+1 < width and grid[i-1][j+1] == True:
        count += 1
    
    # Right
    if j+1 < width and grid[i][j+1] == True:
        count += 1
    
    # Bottom right
    if i+1 < len(grid) and j+1 < width and grid[i+1][j+1] == True:
        count +=1
        
    # Bottom
    if i+1 < len(grid) and grid[i+1][j] == True:
        count += 1
    
    # Bottom left
    if i+1 < len(grid) and j-1 >= 0 and grid[i+1][j-1] == True:
        count += 1
        
    # Left
    if j-1 >= 0 and grid[i][j-1] == True:
        count += 1
        
    return count
    
def copy_list(lst):
    new_lst = [[None for j in range(len(lst[0]))] for i in range(len(lst))]
    
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            new_lst[i][j] = lst[i][j]
    return new_lst
    
        
def evolve(grid):
    new_grid = copy_list(grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            count = surrounding_cells(grid, i, j)
            if count == 3:
                new_grid[i][j] = True
            elif count > 3 or count < 2:
                new_grid[i][j] = False
    return new_grid
                

def display_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == True:
                print("x", end="")
            else:
                print(" ", end="")
        print()

grid = generate_grid()

import time

while(True):
    os.system('cls')
    display_grid(grid)
    grid = evolve(grid)
    time.sleep(0.25)