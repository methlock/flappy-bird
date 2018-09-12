##!/usr/bin/env python

import sys
import time


class Field:

    def __init__(self):

        self.GAME_SIZE = (30, 10) #x,y - size of live window part
        def_row = ['o' for x in range(0, self.GAME_SIZE[0])]
        self.array = [def_row for x in range(0, self.GAME_SIZE[1])]



    def render(self):

        print('\n'.join(''.join(row) for row in self.array))
        #sys.stdout.write('\n'.join(''.join(row) for row in self.array))

        # modifying array for next render

        # projede array, posune ptaka a sloupy
        # pri projizdeni si musim pamatovat index toho kde jsem
        # randint pro diru a jeji polohu a vydalenost mezi sloupy



while True:

    game = Field()
    game.render()

    time.sleep(1)
    sys.exit()
