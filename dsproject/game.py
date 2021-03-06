import curses
import time
import threading
from board import *


HEIGHT = 27
WIDTH = 120
TIMEOUT = 300
MY_ID = 0

window_lock = threading.Lock()

def toast(message, screen):
    screen.addstr(0, 0, " " + message, curses.A_BLINK)
    screen.refresh()

def runUI(b, screen):
    while 1:
        with window_lock:
            over = b.render()
            if over == PLAYER_EXIT:
                toast("Game stopped, press q and quit", screen)
                break
            elif over == CRASH:
                b.refresh()
                toast("You crashed :(", screen)
                break
            elif over == VICTORY:
                b.refresh()
                toast("You won! :)", screen)
                break
            b.refresh()
        time.sleep(.2)

def handleScreen(self, screen):
    curses.curs_set(0)
    screen.addstr(0, 0, " Welcome! :)")
    screen.move(1, 0)
    screen.refresh()

    window = curses.newwin(HEIGHT, WIDTH, 1, 0)
    #window.timeout(TIMEOUT)
    window.keypad(True)
    window.nodelay(1)

    me = Player(MY_ID, 0, MY_ID)
    players = [me, Player(1, 0, 1)]
    b = Board(window, 0, players)

    ui = threading.Thread(target=runUI, args=(b, screen, ))
    ui.daemon = True
    ui.start()

    while 1:
        with window_lock:
            c = window.getch()
        
        if c == ord('q'):
            b.q.put(Event(END))
            break
        elif c == curses.KEY_LEFT:
            b.q.put(Event(MOVE_LEFT, MY_ID))
        elif c == curses.KEY_RIGHT:
            b.q.put(Event(MOVE_RIGHT, MY_ID))
        elif c == curses.KEY_UP:
            b.q.put(Event(MOVE_UP, MY_ID))
        elif c == curses.KEY_DOWN:
            b.q.put(Event(MOVE_DOWN, MY_ID))
                    

        


def main():
    curses.wrapper(handleScreen)

main()


