from libs.sudoku import solve, validate, find_empty
import pygame
from pygame.locals import *
import os
import time

class Board:
    # Import board from difficulty level
    def __init__(self, difficulty='easy', rows=9, cols=9, width=540):
        self.rows = rows
        self.cols = cols
        self.board = []
        self.getBoard(difficulty)
        self.cubes = [[Cube(self.board[i][j], i, j, width) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.model = [[self.cubes[i][j].value for j in range(cols)] for i in range(rows)]
        self.selected = None

    def getBoard(self, difficulty):
        # Get location of working directory + file path
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(),
            os.path.dirname(__file__)))

        # Convert file into 2D list
        with open(os.path.join(__location__, 'boards/' + \
            difficulty + '/1.txt'), 'r') as f:
            contents = f.readlines()
            count = 0
            for line in contents:
                row = []
                for c in line:
                    if c.isdigit():
                        row.append(int(c))
                self.board.append(row)
                count += 1

    # Displays lines on board
    def setDisplay(self, screen):
        # Draws major 3 x 3 lines
        gap = self.width / self.rows
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            # Parameters: screen, color, (begin x, begin y), (end x, end y), thickness
            # Horizontal lines
            pygame.draw.line(screen, (0,0,0), (0, i * gap), \
                (self.width, i * gap), thickness)
            # Vertical lines
            pygame.draw.line(screen, (0,0,0), (i * gap, 0), \
                (i * gap, self.width), thickness)
        
        # display board numbers
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].setDisplay(screen, self.rows)

    def select(self, position):
        # Clear all other selected
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[position[0]][position[1]].selected = True
        self.selected = position

    def clearSelected(self):
        if self.selected:
            row, col = self.selected
            if self.cubes[row][col].value == 0:
                self.cubes[row][col].setTemp(0)

    def answer(self, num):
        row, col = self.selected
        
        # Check if selected cube is empty
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].setValue(num)
            self.model[row][col] = num

            if validate(self.model, num, (row, col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].setValue(0)
                self.cubes[row][col].setTemp(0)
                self.model[row][col] = 0
                return False

    def isComplete(self):
        return not find_empty(self.board)

    def registerClick(self, position):
        if position[0] < self.width and position[1] < self.width:
            gap = self.width / 9
            x = position[0] // gap
            y = position[1] // gap
            return (int(y), int(x))
        return None

    # Place temp value in selected cube
    def prefill(self, num):
        row, col = self.selected
        self.cubes[row][col].setTemp(num)

class Cube:
    def __init__(self, value, row, col, width):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.selected = False

    # Displays numbers on board
    def setDisplay(self, screen, rows):
        # Set font for numbers
        fnt = pygame.font.SysFont('calibri', 40)

        # Divide screen size by 9 to get spacing
        gap = self.width / rows
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            screen.blit(text, (x + 5, y + 5))
        elif self.value != 0:
            text = fnt.render(str(self.value), 1, (0,0,0))
            screen.blit(text, (x + (gap / 2 - text.get_width() / 2), \
                        y + (gap / 2 - text.get_height() / 2)))

        # Draws red line around selected Cube
        if self.selected:
            pygame.draw.rect(screen, (205,0,0), (x, y, gap, gap), 3)

    def setValue(self, value):
        self.value = value

    def setTemp(self, value):
        self.temp = value

def runSudoku(difficulty='easy', rows=9, cols=9, window_size=[540, 540]):
    pygame.init()

    current_path = os.path.dirname(__file__)
    image_path = os.path.join(current_path, 'images')

    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption('Sudoku')
    icon = pygame.image.load(os.path.join(image_path, 'sudoku.png'))
    pygame.display.set_icon(icon)

    board = Board()

    loop = 1
    while loop:
        
        screen.fill((245,245,245))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0

            # Register keystrokes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clearSelected()
                    key = None
                if event.key == pygame.K_RETURN:
                    if board.selected:
                        i, j = board.selected
                        if board.cubes[i][j].temp != 0:
                            if board.answer(board.cubes[i][j].temp):
                                print("Maru")
                            else:
                                print("Batsu")
                            key = None

                            if board.isComplete():
                                print("Board Complete!")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                reg = board.registerClick(pos)
                if reg:
                    board.select(reg)
                    key = None
            
        if board.selected and key != None:
            board.prefill(key)
            #print(board.cubes[board.selected[0]][board.selected[1]].temp)
        
        board.setDisplay(screen)
        pygame.display.update()


def mainMenu():
    runSudoku()

if __name__ == '__main__':
    mainMenu()
    pygame.quit()
