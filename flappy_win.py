import sys
import pandas as pd
import time
from random import randint
import platform
import os
import msvcrt


class Board:
    '''
    Board is dataframe.

    Example:
         01234567
        0.......X
        1.......X
        2..@.....
        3........
        4.......X
    @ - bird
    X - column
    . - empty
    '''

    def __init__(self):
        self.size_x = 15
        self.size_y = 9
        self.DF = pd.DataFrame([[' ' for x in range(0, self.size_x)] for y in range(0, self.size_y)])
        self.columns = []


    def draw(self):
        self.insertColumns()
        self.insertBird()
        #print (self.DF)
        print ('=' * self.size_x)
        for row in self.DF.values.tolist():
            print (''.join(row))
        print ('=' * self.size_x)
        self.clearBoard()


    def insertBird(self):
        # collision
        if Bird.pos_y < 0 or Bird.pos_y > self.size_y-1:
            print ('The bird flew off.')
            sys.exit()
        elif self.DF[Bird.pos_x][Bird.pos_y] == 'X':
            print ('GAME OVER')
            sys.exit()
        else:
            self.DF[Bird.pos_x][Bird.pos_y] = '@'


    def createColumn(self):
        self.columns.append(Column())


    def insertColumns(self):
        for col in self.columns.copy():
            self.DF[col.pos_x][col.pos_y] = 'X'
            col.move()
            if col.pos_x < 0:
                del self.columns[0]


    def clearBoard(self):
        self.DF = pd.DataFrame([[' ' for x in range(0, self.size_x)] for y in range(0, self.size_y)])


class Bird:
    '''
    Object with cordinates.
    '''

    def __init__(self):
        self.pos_x = 2
        self.pos_y = 3

    def changePosY(self, y):
        self.pos_y -= y


class Column:
    '''
    Column object is initialized with random parameters - hight and hole size.
    It is created in last column in dataframe by default.
    It has the property of which cells occupy.
    '''

    def __init__(self):
        self.hole_size = randint(1, 3)
        self.height = randint(0, 9-self.hole_size)
        self.pos_x = Board.size_x-1
        self.pos_y = [x for x in range(0,self.height)] + [x for x in range(self.height+self.hole_size, Board.size_y)]

    def move(self):
        self.pos_x -= 1


# game parameters and init
tick = 0.75
column_step = 7
i = 0
Board = Board()
Bird = Bird()

while True:

    # clearing
    if platform.system() =='Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')

    # new column checker
    i += 1
    if i % column_step == 0:
        Board.createColumn()

    # key pressed checker - only for windows
    if msvcrt.kbhit():
        Bird.changePosY(1)
        if msvcrt.getch() == b'q':
            break
    else:
        Bird.changePosY(-1)

    # draw
    print (f'Score: {i}')
    Board.draw()
    print ('Press any key to fly up and <q> to quit.')
    time.sleep(tick)
