import curses
import pdb


NORMAL = 1
STOPPED = 0
FAST = 2

NOTHING = 10
PLAYER = 11
OBSTACLE = 12

class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = NORMAL

class Board:

    def __init__(self, window, player):
        self.window = window
        self.players = []
        self.me = player
        self.matrix = [[NOTHING for cell in range(5)] for row in range(5)]

    def refresh(self):
        self.window.refresh()

    def addPlayer(self, player):
        self.players.append(player)

    def addBorder(self, column):
        (height, width) = self.window.getmaxyx()
        #pdb.set_trace()
        for row in range(height):
            self.window.addstr(row, column, "|")

    def drawMatrix(self, start):
        for row_no in range(len(self.matrix)):
            for cell_no in range(len(self.matrix[row_no])):
                if self.matrix[row_no][cell_no] == PLAYER:
                    self.window.addstr((row_no * 5) + 1, start + (cell_no * 5) + 1, "HHH")
                    self.window.addstr((row_no * 5) + 2, start + (cell_no * 5) + 1, "HHH")
                    self.window.addstr((row_no * 5) + 3, start + (cell_no * 5) + 1, "HHH")
                else :
                    self.window.addstr((row_no * 5) + 1, start + (cell_no * 5) + 1, "   ")
                    self.window.addstr((row_no * 5) + 2, start + (cell_no * 5) + 1, "   ")
                    self.window.addstr((row_no * 5) + 3, start + (cell_no * 5) + 1, "   ")

        

                                
                    
    def render(self, key):

        if key == curses.KEY_LEFT:
            if self.me.x != 0:
                self.me.x -= 1
        elif key == curses.KEY_RIGHT:
            if self.me.x != 4:
                self.me.x += 1
        
        if self.me.speed == NORMAL:
            self.me.y += 1
        elif self.me.speed == FAST:
            self.me.y += 2
        for row in range(len(self.matrix)):
            for cell in range(len(self.matrix[row])):
                self.matrix[row][cell] = NOTHING

        #pdb.set_trace()
        self.matrix[4][self.me.x] = PLAYER
        self.addBorder(0)
        self.drawMatrix(1)
        self.addBorder(26)
    
        
