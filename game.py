import sys
import curses
import time
import threading
from board import *
import socket


HEIGHT = 27
WIDTH = 120
TIMEOUT = 300
MY_ID = 0

window_lock = threading.Lock()

other_port = 0

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
                toast("You finished! :)", screen)
                break
            b.refresh()
        time.sleep(.2)

def sendEvent(event_id, player_id):
    global other_port
    global other_ip
    msg = str(event_id) + "," + str(player_id)
    s = socket.socket()         # Create a socket object
    #host = socket.gethostname() # Get local machine name
    host = other_ip
    port = other_port             # Reserve a port for your service.

    s.connect((host, port))
    s.send(msg)
    #print s.recv(1024)
    s.close    

b = None

def handleScreen(screen):
    global b
    curses.curs_set(0)
    screen.addstr(0, 0, " Welcome! :)")
    screen.move(1, 0)
    screen.refresh()

    window = curses.newwin(HEIGHT, WIDTH, 1, 0)
    #window.timeout(TIMEOUT)
    window.keypad(True)
    window.nodelay(1)

    me = Player(MY_ID, 0, MY_ID)
    other = Player(1 - MY_ID, 0, 1 - MY_ID)
    if MY_ID == 0:
        players = [me, other]
    else:
        players = [other, me]

    b = Board(window, MY_ID, players)

    ui = threading.Thread(target=runUI, args=(b, screen, ))
    ui.daemon = True
    ui.start()

    while 1:
        with window_lock:
            c = window.getch()
        
        if c == ord('q'):
            b.q.put(Event(END, MY_ID))
            break
        elif c == curses.KEY_LEFT:
            sendEvent(MOVE_LEFT, MY_ID)
            b.q.put(Event(MOVE_LEFT, MY_ID))
        elif c == curses.KEY_RIGHT:
            sendEvent(MOVE_RIGHT, MY_ID)
            b.q.put(Event(MOVE_RIGHT, MY_ID))
        elif c == curses.KEY_UP:
            sendEvent(MOVE_UP, MY_ID)
            b.q.put(Event(MOVE_UP, MY_ID))
        elif c == curses.KEY_DOWN:
            sendEvent(MOVE_DOWN, MY_ID)
            b.q.put(Event(MOVE_DOWN, MY_ID))
                    

        

def runServer(user_port):
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = user_port                # Reserve a port for your service.
    s.bind(('', port))        # Bind to the port

    s.listen(5)                 # Now wait for client connection.
    while True:
        c, addr = s.accept()     # Establish connection with client.
        #print 'Got connection from', addr
        msg = c.recv(1024)
        handleMessage(msg)
        #c.send('Thank you for connecting')
        c.close()    

def handleMessage(message):
    event_id, player_id = message.split(',')
    event_id = int(event_id)
    player_id = int(player_id)
    b.q.put(Event(event_id, player_id))
    

def main():
    global other_port
    global other_ip
    global MY_ID
    MY_ID = int(sys.argv[1])
    #my_ip = sys.argv[2]
    port =  int(sys.argv[2])
    other_ip = sys.argv[3]
    other_port = int(sys.argv[4])
    

    # print "Enter your ID: "
    # MY_ID = int(raw_input())
    
    # print "Enter your server port: "
    # port = int(raw_input())
    
    server = threading.Thread(target=runServer, args = (port, ))
    server.daemon = True
    server.start()

    # print "Enter other player port: "
    # port = int(raw_input())
    # other_port = port

    print "Type 'y' to start: "
    inp = raw_input()
    if(inp == 'y'):
        curses.wrapper(handleScreen)

main()


