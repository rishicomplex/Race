import curses


def handleLeft(screen):
    (y, x) = screen.getyx()
    screen.addstr(" <")
    screen.move(y + 1, x)

def handleRight(screen):
    (y, x) = screen.getyx()
    screen.addstr(" >")
    screen.move(y + 1, x)

def handleScreen(screen):
    curses.curs_set(0)
    screen.addstr(0, 0, " Welcome! :)")
    screen.move(1, 0)
    screen.refresh()
    while 1:
        c = screen.getch()
        if c == curses.KEY_LEFT:
            handleLeft(screen)
        elif c == curses.KEY_RIGHT:
            handleRight(screen)
        elif c == ord('q'):
            break


def main():
    curses.wrapper(handleScreen)

main()


