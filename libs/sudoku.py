# Methods for solving sudoku

# Checks for empty squares
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None


# Finds empty square and
# Runs through all possible inputs and
# runs validates
def solve(board):
    position = find_empty(board)
    if not position:
        return True
    
    # Try each number from 1-9
    for i in range(1, 10):
        if validate(board, i, position):
            board[position[0]][position[1]] = i

            # Recursively fills out remaining board
            # to see if this is the correct value
            if solve(board):
                return True

            # Otherwise, reset position to 0
            board[position[0]][position[1]] = 0
    
    return False

# Validates if value works in row, col, and square
# Parameters: sudoku board, value to check, value's array position on board
def validate(board, value, position):
    # Check if value is valid in row
    for col in range(len(board[0])):
        if board[position[0]][col] == value and position[1] != col:
            return False
    
    # Check if value is valid in column
    for row in range(len(board)):
        if board[row][position[1]] == value and position[0] != row:
            return False

    # Check is value is in position box
    # for 9x9: 3 possible rows (y), 3 possible cols (x)
    box_x = position[1] // 3
    box_y = position[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == value and (i, j) != position:
                return False
    
    return True