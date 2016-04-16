import curses
import Queue
import random
import pdb


NORMAL = 1
STOPPED = 0
FAST = 2

NOTHING = 10
PLAYER = 11
OBSTACLE = 12

FINISH = 30

MOVE_LEFT = 30
MOVE_RIGHT = 31
MOVE_UP = 32
MOVE_DOWN = 33
EVENT_CRASH = 34
EVENT_FINISH = 35
EVENT_END = 36

END = 40



#exit_codes
PLAYER_EXIT = 243
CRASH = 244
VICTORY = 245

class Event:
    def __init__(self, event_type, player_id):
        self.event_type = event_type
        self.player_id = player_id
    

class Obstacle:

    def __init__(self):
        self.x = random.randint(0, 4)
        self.y = random.randint(3, FINISH)

class Player:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.speed = NORMAL
        self.id = id

class Board:

    def __init__(self, window, me, players):
        self.window = window
        self.players = players
        self.me = me
        self.matrix = [[NOTHING for cell in range(5)] for row in range(5)]
        self.obstacles = [Obstacle() for index in range(10)]
        self.q = Queue.Queue()

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
                    self.window.addstr((row_no * 5) + 0, start + (cell_no * 5), "IIIII")
                    self.window.addstr((row_no * 5) + 1, start + (cell_no * 5), "IIIII")
                    self.window.addstr((row_no * 5) + 2, start + (cell_no * 5), "IIIII")
                    self.window.addstr((row_no * 5) + 3, start + (cell_no * 5), "IIIII")
                    self.window.addstr((row_no * 5) + 4, start + (cell_no * 5), "IIIII")
                else :
                    self.window.addstr((row_no * 5) + 0, start + (cell_no * 5), "     ")
                    self.window.addstr((row_no * 5) + 1, start + (cell_no * 5), "     ")
                    self.window.addstr((row_no * 5) + 2, start + (cell_no * 5), "     ")
                    self.window.addstr((row_no * 5) + 3, start + (cell_no * 5), "     ")
                    self.window.addstr((row_no * 5) + 4, start + (cell_no * 5), "     ")
                if self.players[self.me].y + 4 - row_no == FINISH:
                    self.window.addstr((row_no * 5) + 0, start + (cell_no * 5), "-----")

        

                                
                    
    def render(self):
        
        while not self.q.empty():
            e = self.q.get()
            if e.event_type == MOVE_LEFT:
                if self.players[e.player_id].x != 0:
                    self.players[e.player_id].x -= 1
            elif e.event_type == MOVE_RIGHT:
                if self.players[e.player_id].x != 4:
                    self.players[e.player_id].x += 1
            elif e.event_type == MOVE_UP:
                self.players[e.player_id].speed += 1
                if self.players[e.player_id].speed > FAST:
                    self.players[e.player_id].speed = FAST
            elif e.event_type == MOVE_DOWN:
                self.players[e.player_id].speed -= 1
                if self.players[e.player_id].speed < STOPPED:
                    self.players[e.player_id].speed = STOPPED
            elif e.event_type == END:
                return PLAYER_EXIT
            self.q.task_done()
            
        
        for player in self.players:
            if player.speed == NORMAL:
                player.y += 1
            elif player.speed == FAST:
                player.y += 2

        
        for row in range(len(self.matrix)):
            for cell in range(len(self.matrix[row])):
                self.matrix[row][cell] = NOTHING

        for obstacle in self.obstacles:
            if obstacle.x == self.players[self.me].x and obstacle.y == self.players[self.me].y:
                return CRASH
            if (obstacle.y - self.players[self.me].y) >= 0 and (obstacle.y - self.players[self.me].y) <= 4:
                self.matrix[self.players[self.me].y - obstacle.y + 4][obstacle.x] = OBSTACLE

        for player in self.players:
            #insert into board
            pass
    
            

        #pdb.set_trace()
        self.matrix[4][self.players[self.me].x] = PLAYER
        self.addBorder(5)
        self.drawMatrix(6)
        self.addBorder(31)

        if self.players[self.me].y >= FINISH:
            return VICTORY
        
    
        
