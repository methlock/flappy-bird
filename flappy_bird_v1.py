##!/usr/bin/env python
'''
dalsi moznost je to delat vektorove, kde by ptak a sloupy byly objekty s pozici
'''

import sys
import os
import time
import platform
import msvcrt
from random import randint



try:
    from msvcrt import getch #for windows

except ImportError: #for linux
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch



class Field:

    def __init__(self):

        self.GAME_SIZE = (12, 7) #x,y - size of live window part
        self.ARRAY = [[' ' for x in range(0, self.GAME_SIZE[0])] for x in range(0, self.GAME_SIZE[1])]

        # bird placing
        self.ARRAY[self.GAME_SIZE[1]//2][3] = '@'


    def render(self):
        print('='*self.GAME_SIZE[0])
        print('\n'.join(''.join(row) for row in self.ARRAY))
        print('='*self.GAME_SIZE[0])
        #sys.stdout.write('\n'.join(''.join(row) for row in self.ARRAY))


    def move(self):
        # cols moving

        for i, row in enumerate(self.ARRAY):
            for j, val in enumerate(row):

                if val == 'X':
                    self.ARRAY[i][j] = ' '
                    self.ARRAY[i][j-1] = 'X'

        # bird moving
        # for i, row in enumerate(self.ARRAY):
        #     for j, val in enumerate(row):
        #
        #         if val == '@':
        #             if pressed:
        #                 self.ARRAY[i][j] = ' '
        #                 self.ARRAY[i-1][j] = '@'
        #             else:
        #                 self.ARRAY[i][j] = ' '
        #                 self.ARRAY[i+1][j] = '@'




    def newCol(self):
        HOLE_SIZE = randint(3, 4)
        HIGHT = randint(0, self.GAME_SIZE[1]-HOLE_SIZE)

        for row in self.ARRAY[:HIGHT]:
            row[-1] = 'X'

        for row in self.ARRAY[HIGHT+HOLE_SIZE:]:
            row[-1] = 'X'



# init
Game = Field()
tick = 0.5
nc_tics = 1

while True:
    nc_tics -= 1
    pressed = False

    # clearing
    # if platform.system() =='Windows':
    #     os.system('cls')
    # elif platform.system() == 'Linux':
    #     os.system('clear')
    print('Game information:')
    Game.render()
    Game.move()
    time.sleep(tick)

    # key pressed checker - only for windows
    if msvcrt.kbhit():
        pressed = True
        if msvcrt.getch() == b'q':
            break


    # column creation
    print('tics to new column:', nc_tics)
    if nc_tics == 0:
        #nc_tics = randint(4, 6)
        nc_tics = 2
        Game.newCol()
                
