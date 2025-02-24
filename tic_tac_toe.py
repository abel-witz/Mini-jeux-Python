grid = [[' ' for j in range(7)] for i in range(6)]

def display_grid(grid):
    print()
    for i in range(6):
        print('| ', end='')
        for j in range(7):
            print(grid[i][j], '| ', end='')
            
        print()
    
    print('+'+'---+'*7)
    print(' ', end='')
    for j in range(7):
        print('', j,' ', end="")
    print()
    
def turn(grid, player):
    insertion = False
    
    while not(insertion):
        column = int(input("Player " + str(player) + ", choose the column where you want to play: "))
        
        for i in range(5, -1, -1):
            if grid[i][column] == ' ':
                if player == 1:
                    grid[i][column] = 'X'
                else:
                    grid[i][column] = 'O'
                insertion = True
                break
                
        if not(insertion):
            print("The column is full")
    
    return column

print()

def test_horizontal(grid, column):
    row = 0
    for i in range(6):
        if grid[i][column] != ' ':
            row = i
            break

    count_x = 0
    count_o = 0
    for j in range(7):
        if grid[row][j] == 'O':
            count_o += 1
            count_x = 0
        elif grid[row][j] == 'X':
            count_x += 1
            count_o = 0
        else:
            count_x = 0
            count_o = 0
            
        if count_x == 4 or count_o == 4:
            return True
        
    return False
    
def test_vertical(grid, column):
    count_x = 0
    count_o = 0
    for i in range(6):
        if grid[i][column] == 'O':
            count_o += 1
            count_x = 0
        elif grid[i][column] == 'X':
            count_x += 1
            count_o = 0
        else:
            count_x = 0
            count_o = 0
            
        if count_x == 4 or count_o == 4:
            return True
        
    return False

def test_diagonal(grid, column):
    row = 0
    for i in range(6):
        if grid[i][column] != ' ':
            row = i
            break

    x = column + 5 - row
    y = 5 - max(x - 6, 0)
    x = min(x, 6)
    
    count_x = 0
    count_o = 0
    while(x >= 0 and y >= 0):
        print(x)
        print(y)
        print()
    
        if grid[y][x] == 'O':
            count_o += 1
            count_x = 0
        elif grid[y][x] == 'X':
            count_x += 1
            count_o = 0
        else:
            count_x = 0
            count_o = 0
        
        if count_x == 4 or count_o == 4:
            return True
        
        x -= 1
        y -= 1
        
    return False
    
def test_anti_diagonal(grid, column):
    row = 0
    for i in range(6):
        if grid[i][column] != ' ':
            row = i
            break

    x = column - (5 - row)
    y = 5 + min(x, 0)
    x = max(x, 0)
    
    count_x = 0
    count_o = 0
    while(x < 7 and y >= 0):
        if grid[y][x] == 'O':
            count_o += 1
            count_x = 0
        elif grid[y][x] == 'X':
            count_x += 1
            count_o = 0
        else:
            count_x = 0
            count_o = 0
        
        x += 1
        y += -1
        
        if count_x == 4 or count_o == 4:
            return True
        
    return False
    
def grid_full(grid):
    for j in range(7):
        if grid[0][j] == " ":
            return False
            
    return True
    
player2 = False
while(True):
    display_grid(grid)

    print()

    column = turn(grid, player2 + 1)
    
    if test_horizontal(grid, column) or test_vertical(grid, column) or test_diagonal(grid, column) or test_anti_diagonal(grid, column):
        display_grid(grid)
        
        print()
        
        print("Player", player2 + 1, "wins!")
        break
    elif grid_full(grid):
        display_grid(grid)
        
        print()
        
        print("Grid is full")
        break
    
    player2 = not(player2)