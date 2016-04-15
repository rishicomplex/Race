import curses
import random
import pdb


NORMAL = 1
STOPPED = 0
FAST = 2

NOTHING = 10
PLAYER = 11
OBSTACLE = 12

FINISH = 30

class Obstacle:

    def __init__(self):
        self.x = random.randint(0, 4)
        self.y = random.randint(0, FINISH)

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
        self.obstacles = [Obstacle() for index in range(10)]

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
                    self.window.addstr((row_no * 5) + 0, start + (cell_no * 5), "     ")
                    self.window.addstr((row_no * 5) + 1, start + (cell_no * 5), " /A\ ")
                    self.window.addstr((row_no * 5) + 2, start + (cell_no * 5), " [H] ")
                    self.window.addstr((row_no * 5) + 3, start + (cell_no * 5), " [=] ")
                    self.window.addstr((row_no * 5) + 4, start + (cell_no * 5), "     ")
                elif self.matrix[row_no][cell_no] == OBSTACLE:
                    self.window.addstr((row_no * 5) + 0, start + (cell_no * 5), "OOOOO")
                    self.window.addstr((row_no * 5) + 1, start + (cell_no * 5), "OOOOO")
                    self.window.addstr((row_no * 5) + 2, start + (cell_no * 5), "OOOOO")
                    self.window.addstr((row_no * 5) + 3, start + (cell_no * 5), "OOOOO")
                    self.window.addstr((row_no * 5) + 4, start + (cell_no * 5), "OOOOO")
                else :
                    self.window.addstr((row_no * 5) + 0, start + (cell_no * 5), "     ")
                    self.window.addstr((row_no * 5) + 1, start + (cell_no * 5), "     ")
                    self.window.addstr((row_no * 5) + 2, start + (cell_no * 5), "     ")
                    self.window.addstr((row_no * 5) + 3, start + (cell_no * 5), "     ")
                    self.window.addstr((row_no * 5) + 4, start + (cell_no * 5), "     ")
                if self.me.y + 4 - row_no == FINISH:
                    self.window.addstr((row_no * 5) + 0, start + (cell_no * 5), "-----")

        

                                
                    
    def render(self, key):

        if key == curses.KEY_LEFT:
            if self.me.x != 0:
                self.me.x -= 1
        elif key == curses.KEY_RIGHT:
            if self.me.x != 4:
                self.me.x += 1
        elif key == curses.KEY_UP:
            self.me.speed += 1
            if self.me.speed > FAST:
                self.me.speed = FAST
        elif key == curses.KEY_DOWN:
            self.me.speed -= 1
            if self.me.speed < STOPPED:
                self.me.speed = STOPPED
                
        
        if self.me.speed == NORMAL:
            self.me.y += 1
        elif self.me.speed == FAST:
            self.me.y += 2

        
        for row in range(len(self.matrix)):
            for cell in range(len(self.matrix[row])):
                self.matrix[row][cell] = NOTHING

        for obstacle in self.obstacles:
            if obstacle.x == self.me.x and obstacle.y == self.me.y:
                return 2
            if (obstacle.y - self.me.y) >= 0 and (obstacle.y - self.me.y) <= 4:
                self.matrix[self.me.y - obstacle.y + 4][obstacle.x] = OBSTACLE

        #pdb.set_trace()
        self.matrix[4][self.me.x] = PLAYER
        self.addBorder(5)
        self.drawMatrix(6)
        self.addBorder(31)

        if self.me.y >= FINISH:
            return 1
        
    
        
