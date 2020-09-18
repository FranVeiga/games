'''
This creates a Sudoku GUI where you can play sudoku.
'''

import sys, os
import pygame as pg
from Sudoku_dep import createSudokuBoard
from Sudoku_dep import solver

pg.init()


class Sudoku():
    '''
    A class that handles the sudoku board and all the related function. It also
    contains all the Square objects. It's basically the class for the entire game.
    '''

    def __init__(self):
        self.running = True
        self.path = os.path.dirname(".\\sudoku.py")
        
        self.clock = pg.time.Clock()

        # Display variables
        self.w = 9
        self.h = 9       
        self.height = self.y_to_pxl(self.h)
        self.width = self.x_to_pxl(self.w)
        self.display = pg.display.set_mode((self.width, self.height))
        self.icon = pg.image.load(f'{self.path}\\Sudoku_dep\\sudoku.png')
        pg.display.set_icon(self.icon)
        pg.display.set_caption('Sudoku')

        self.r_button_font = pg.font.SysFont("calibri", 30)
        self.return_button_text = self.r_button_font.render("Return", True, (150, 150, 150))
        self.rb_dims = self.r_button_font.size("Return")
        self.return_button_rect = pg.Rect(self.x_to_pxl(self.w) - self.rb_dims[0] - 10, 12, \
                                         self.rb_dims[0], self.rb_dims[1])
        
        # Board variables
        self.board = self.createNumBoard()
        self.columnsList = []
        self.subBlocks = []        
        self.selectedSquare = None
        self.createSquareArray()

        


    def x_to_pxl(self, v):
        return v * 60
    def y_to_pxl(self, v):
        return v * 60 + 50 
    
    
    # Function to set the numbers on the board,
    # will pick random board from a file and convert it to an array
    def createNumBoard(self):
        
        file = self.showSelectScreen()
        
        board = createSudokuBoard.main(file)
        # Almost done board (for testing)
        '''
        TEST BOARD
            board = [
        [1, 2, 3, 7, 8, 9, 4, 5, 6],
        [4, 5, 6, 1, 2, 3, 7, 8, 9],
        [7, 8, 9, 4, 5, 6, 1, 2, 3],
        [3, 1, 2, 9, 7, 8, 6, 4, 5],
        [6, 4, 5, 3, 1, 2, 9, 7, 8],
        [9, 7, 8, 6, 4, 5, 3, 1, 2],
        [2, 3, 1, 8, 9, 7, 5, 6, 4],
        [5, 6, 4, 2, 3, 1, 8, 0, 7],
        [8, 9, 7, 5, 6, 4, 2, 3, 1]]'''
        return board

    # Creates Square objects and assigns them their corresponding value
    def createSquareArray(self):
        squareArray = [[] for i in range(9)]
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                squareArray[y].append(Square(self, x, y, self.board[y][x]))
                if squareArray[y][x].value != 0:
                    squareArray[y][x].isConstant = True
        self.squareArray = squareArray

    # Updates the value of each Square() object, updates columns list and the subBlocks list
    def updateSquareArray(self):

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                self.squareArray[y][x].value = self.board[y][x]

        columns = [[], [], [], [], [], [], [], [], []]
        for y in range(len(self.board)):
            for x in range(len(self.board)):
                columns[y].append(self.board[x][y])
        self.columnsList = columns

        subBlocks = [
            [[], [], []],
            [[], [], []],
            [[], [], []]
        ]
        for y in range(len(self.board)):
            for x in range(len(self.board)):
                subBlocks[y//3][x//3].append(self.board[y][x])
        self.subBlocks = subBlocks

    # Draw the board
    def renderBoard(self):
        for y in self.squareArray:
            for x in y:
                pg.draw.rect(self.display, x.color, x.rect, x.borderWidth)

                font = pg.font.Font('freesansbold.ttf', x.xdim)
                if x.value != 0:
                    if x.isConstant:
                        number = font.render(str(x.value), True, (255, 255, 255))
                    else:
                        number = font.render(
                            str(x.value), True, (150, 150, 150))
                    self.display.blit(
                        number, (int(x.x + x.xdim*0.25), x.y + 5))

                for i in range(1, int(self.w/3)):
                    # pg.draw.line(self.display, (150, 150, 150),
                    #              (i*int(self.width/(self.w/3)), 60),
                    #              (i*int(self.width/(self.w/3)), self.height), 5)
                    # for j in range(1, int(self.h/3)):
                    #     pg.draw.line(self.display, (150, 150, 150),
                    #                  (0, j*int(self.height / (self.h/3))),
                    #                  (self.width, j*int(self.height/(self.h/3))), 5)
                    pg.draw.line(self.display, (150, 150, 150), 
                                 (self.x_to_pxl(i) * 3, self.y_to_pxl(0)), 
                                 (self.x_to_pxl(i) * 3, self.y_to_pxl(self.h)), 5)
                    for j in range(1, int(self.h/3)):
                        pg.draw.line(self.display, (150, 150, 150), 
                                     (self.x_to_pxl(0), self.y_to_pxl(j * 3)), 
                                     (self.x_to_pxl(self.w), self.y_to_pxl(j * 3)), 5)

    # Check if the player won, and creates a WinScreen() object.
    def checkWin(self):
        win = True
        for count in range(1, self.w + 1):
            for y in self.board:
                if y.count(count) != 1:
                    win = False
            for x in self.columnsList:
                if x.count(count) != 1:
                    win = False
            for y in self.subBlocks:
                for x in y:
                    if x.count(count) != 1:
                        win = False
        if win:
            victoryScreen = WinScreen(self)
            victoryScreen.show()
            self.updateSquareArray()
            pg.display.update()

    # Selects a square
    def selectSquare(self):
        mousePos = pg.mouse.get_pos()
        for y in self.squareArray:
            for x in y:
                x.color = (150, 150, 150)
                x.borderWidth = 1
                if x.rect.collidepoint(mousePos):
                    self.selectedSquare = x
                    self.selectedSquare.color = (255, 0, 0)
                    self.selectedSquare.borderWidth = 3
        for y in self.squareArray:
            for x in y:
                if self.selectedSquare \
                   and x.value == self.selectedSquare.value \
                   and x != self.selectedSquare \
                   and self.selectedSquare.value != 0:
                    x.color = (0, 255, 0)
                    x.borderWidth = 3

    # Sets the pressed number on the selected square, updates the board and calls checkWin().
    # Event argument is the event to check.
    def setNumber(self, event):
        if self.selectedSquare is not None and not self.selectedSquare.isConstant:
            try:
                indexBoard = self.board[self.selectedSquare.ypos][self.selectedSquare.xpos]
                if event.key == pg.K_BACKSPACE:
                    indexBoard = 0
                elif event.key == pg.K_1 or event.key == pg.K_KP1:
                    indexBoard = 1
                elif event.key == pg.K_2 or event.key == pg.K_KP2:
                    indexBoard = 2
                elif event.key == pg.K_3 or event.key == pg.K_KP3:
                    indexBoard = 3
                elif event.key == pg.K_4 or event.key == pg.K_KP4:
                    indexBoard = 4
                elif event.key == pg.K_5 or event.key == pg.K_KP5:
                    indexBoard = 5
                elif event.key == pg.K_6 or event.key == pg.K_KP6:
                    indexBoard = 6
                elif event.key == pg.K_7 or event.key == pg.K_KP7:
                    indexBoard = 7
                elif event.key == pg.K_8 or event.key == pg.K_KP8:
                    indexBoard = 8
                elif event.key == pg.K_9 or event.key == pg.K_KP9:
                    indexBoard = 9
                self.board[self.selectedSquare.ypos][self.selectedSquare.xpos] = indexBoard
            except AttributeError:
                pass
        self.updateSquareArray()
        self.checkWin()

    def showSelectScreen(self):
        selecting = True
        
        title_font = pg.font.Font('freesansbold.ttf', 30)
        text_font = pg.font.Font('freesansbold.ttf', 20)

        title_text = title_font.render('SELECT A DIFFICULTY', True, (150, 150, 150))
        title_size = title_font.size('SELECT A DIFFICULTY')
        
        diff1 = text_font.render('Easy: press 1', True, (0, 255, 0))
        
        diff2 = text_font.render('Medium: press 2', True, (175, 175, 0))
        diff2_size = text_font.size('Medium: press 2')

        diff3 = text_font.render('Hard: press 3', True, (255, 0, 0))
        diff3_size = text_font.size('Hard: press 3')       

        diff4 = text_font.render('Impossible: press 4', True, (106, 31, 255))
        diff4_size = text_font.size('Impossible: press 4')             
              
        while selecting:
            self.clock.tick(15)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        selecting = False
                        return f'{self.path}\\Sudoku_dep\\easy_boards.txt'
                    if event.key == pg.K_2:
                        selecting = False
                        return f'{self.path}\\Sudoku_dep\\medium_boards.txt'
                    if event.key == pg.K_3:
                        selecting = False
                        return f'{self.path}\\Sudoku_dep\\hard_boards.txt'
                    if event.key == pg.K_4:
                        selecting = False
                        return f'{self.path}\\Sudoku_dep\\impossible_boards.txt'
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.return_button_rect.collidepoint(pg.mouse.get_pos()):
                        self.running = False
                        selecting = False
                        return f'{self.path}\\Sudoku_dep\\impossible_boards.txt'
                
            
            self.display.fill((0, 0, 0))
            
            self.display.blit(self.return_button_text, (self.return_button_rect.left, self.return_button_rect.top))
            self.display.blit(title_text, (int(self.width / 2) - int(title_size[0] / 2), 60))
            self.display.blit(diff1, (10, int(self.height / 4)))
            self.display.blit(diff2, (10, int(self.height / 4) + diff2_size[1] + 5))
            self.display.blit(diff3, (10, int(self.height / 4) + diff3_size[1] * 2 + 10)) 
            self.display.blit(diff4, (10, int(self.height / 4) + diff4_size[1] * 3 + 15))            
            
            pg.display.update()

    
    # Main run loop
    def run(self):
        while self.running:
            self.clock.tick(15)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.return_button_rect.collidepoint(pg.mouse.get_pos()):
                        self.running = False
                    self.selectSquare()
                if event.type == pg.KEYDOWN:
                    self.setNumber(event)
                    if event.key == pg.K_s:
                        solver.solveBoard(self.board)
                        self.updateSquareArray()

            self.display.fill((0, 0, 0))
            self.renderBoard()
            self.display.blit(self.return_button_text, (self.return_button_rect.left, self.return_button_rect.top))
            pg.display.update()


class Square():
    '''
    A class for a single square in the board
    '''

    # Master is the Sudoku() object, x and y its grid coordinates, and value its value (0-9)
    def __init__(self, master, x, y, value):
        # Grid coordinates
        self.xpos = x
        self.ypos = y
        # Width and height of each square
        self.xdim = int(master.width / master.w)
        self.ydim = int((master.height - 50) / master.h)
        # Screen position
        self.x = x * self.xdim
        self.y = y * self.ydim + 50

        self.rect = pg.Rect(self.x, self.y, self.xdim, self.ydim)
        self.value = value
        self.isSelected = False
        self.isConstant = False

        # Appearence variables
        self.color = (150, 150, 150)
        self.borderWidth = 1


class WinScreen():
    '''
    A class for the victory screen
    '''

    # Master would be the Sudoku() class
    def __init__(self, master):
        self.master = master
        self.display = master.display
        self.clock = pg.time.Clock()

        # Font and text of the displayed text.
        self.font = pg.font.Font('freesansbold.ttf', 15)
        self.winText = 'You win! Press enter to play again.'
        self.renderedText = self.font.render(self.winText, True, (150, 150, 150))

    # Blit the text in the center of the screen
    def createWinText(self):

        screenCenter = self.display.get_rect().center
        textCenter = self.renderedText.get_rect().center
        self.display.blit(
            self.renderedText, (screenCenter[0] - textCenter[0],
                                screenCenter[1] - textCenter[1])
        )

    # Resets the sudoku board when the user presses enter
    def resetSudoku(self):
        self.master.board = self.master.createNumBoard()
        self.master.createSquareArray()
        self.master.selectedSquare = None

    # Main loop for showing the victory screen
    def show(self):
        showscreen = True
        while showscreen:
            self.clock.tick(5)
            self.display.fill((0, 0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.master.return_button_rect.collidepoint(pg.mouse.get_pos()):
                        self.master.running = False
                        showscreen = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        showscreen = False
                    if event.key == pg.K_RETURN:
                        self.resetSudoku()
                        showscreen = False
            self.createWinText()
            self.master.display.blit(self.master.return_button_text, (self.master.return_button_rect.left, self.master.return_button_rect.top))
            pg.display.update()


if __name__ == '__main__':
    sudoku = Sudoku()
    sudoku.run()
