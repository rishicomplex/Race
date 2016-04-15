import curses
from board import *

HEIGHT = 27
WIDTH = 120
TIMEOUT = 1000

def handleLeft(screen):
    (y, x) = screen.getyx()
    screen.addstr(" <")
    screen.move(y + 1, x)

def handleRight(screen):
    (y, x) = screen.getyx()
    screen.addstr(" >")
    screen.move(y + 1, x)

def handleGotKey(screen):
    (y, x) = screen.getyx()
    screen.addstr(" Nothing")
    screen.move(y + 1, x)

def handleScreen(screen):
    curses.curs_set(0)
    screen.addstr(0, 0, " Welcome! :)")
    screen.move(1, 0)
    screen.refresh()

    window = curses.newwin(HEIGHT, WIDTH, 1, 0)
    window.timeout(TIMEOUT)
    window.keypad(True)

    b = Board(window, Player(1, 0))
    
    while 1:
        c = window.getch()
        
        if c == ord('q'):
            break

        b.render(c)
        b.refresh()
        


def main():
    curses.wrapper(handleScreen)

main()


