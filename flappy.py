#!/usr/bin/env python

import sys
import pandas as pd
import time
from random import randint
import os
from threading import Timer

try:
    import msvcrt
    PLATFORM = "win"
except ImportError:
    PLATFORM = "unix"
    import tty
    import termios
    from select import select

def getch():
    if PLATFORM == "win":
        ch = msvcrt.getch()
        return ch
    elif PLATFORM == "unix":
        fd = sys.stdin.fileno()
        old_setting = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            i, o, e = select([sys.stdin.fileno()], [], [], 5)
            if i:
                ch = sys.stdin.read(1)

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_setting)
        return ch

def key_pressed():
    global KEY_PRESSED, KEY
    KEY = getch()
    if KEY:
        KEY_PRESSED = True


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
            sys.exit('The bird flew off.')
        elif self.DF[Bird.pos_x][Bird.pos_y] == 'X':
            sys.exit('You broke the bird - GAME OVER')
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




# game parameters
tick = 0.35
column_step = 8
# init
i = 0
KEY_PRESSED = False
KEY = ''
Board = Board()
Bird = Bird()


while True:

    # key event
    key_event = Timer(tick, key_pressed)
    key_event.start()
    time.sleep(tick)

    # clearing
    if PLATFORM =='win':
        os.system('cls')
    elif PLATFORM == 'unix':
        os.system('clear')

    # new column checker
    i += 1
    if i % column_step == 0:
        Board.createColumn()

    # key pressed checker - only for windows
    # if msvcrt.kbhit():
    #     Bird.changePosY(1)
    #     if msvcrt.getch() == b'q':
    #         break
    # else:
    #     Bird.changePosY(-1)

    if KEY_PRESSED:
        if KEY == b'q':
            key_event.cancel()
            sys.exit('Exited')
        KEY_PRESSED = False
        Bird.changePosY(1)
    else:
        Bird.changePosY(-1)

    # draw
    print (f'Score: {i}')
    Board.draw()
    print ('Press any key to fly up and <q> to quit.')
