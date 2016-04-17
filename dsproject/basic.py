from p2p import *
from board import *
import Queue
import time
import threading
import curses

HEIGHT = 27
WIDTH = 120
TIMEOUT = 300
MY_ID = 0

PEERNAME = "NAME"   # request a peer's canonical id
LISTPEERS = "LIST"
INSERTPEER = "JOIN"
PEERQUIT = "QUIT"
LEFT = "LEFT"
RIGHT = "RIGH"
UP = "ACCL"
DOWN = "DECC"
MOV = "MOVE"
REPLY = "REPL"
ERROR = "ERRO"
ID = "IDNT"

window_lock = threading.Lock()

def btdebug( msg ):
	print "[%s] %s" % ( str(threading.currentThread().getName()), msg )

class RacePeer(BTPeer):

	def __init__(self, maxpeers, serverport):
		BTPeer.__init__(self, maxpeers, serverport)
		
		self.addrouter(self.__router)
		self.raceQ = Queue.Queue()
		self.id_tuples = []
		self.myraceid = -1
		# self.window_lock = threading.Lock()
		handlers = {LISTPEERS : self.__handle_listpeers,
				INSERTPEER : self.__handle_insertpeer,
				PEERNAME: self.__handle_peername,
				PEERQUIT: self.__handle_quit,
				MOV: self.__handleMove,
				ID:self.__handle_getId
			   }
		for mt in handlers:
			self.addhandler(mt, handlers[mt])
		#print self.handlers

	def __debug(self, msg):
		if self.debug:
			btdebug(msg)

	def __router(self, peerid):
		if peerid not in self.getpeerids():
			return (None, None, None)
		else:
			rt = [peerid]
			rt.extend(self.peers[peerid])
			return rt

	def toast(self, message, screen):
		screen.addstr(0, 0, " " + message, curses.A_BLINK)
		screen.refresh()

	def runUI(self,b, screen):
		while 1:
			with window_lock:
				over = b.render()
				if over == PLAYER_EXIT:
					self.toast("Game stopped, press q and quit", screen)
					break
				elif over == CRASH:
					b.refresh()
					self.toast("You crashed :(", screen)
					break
				elif over == VICTORY:
					b.refresh()
					self.toast("You won! :)", screen)
					break
				b.refresh()
			time.sleep(.2)

        def comp(A, B):
                return A[2] < B[2]

	def handleScreen(self, screen):
		curses.curs_set(0)
		screen.addstr(0, 0, " Welcome! :)")
		screen.move(1, 0)
		screen.refresh()

		window = curses.newwin(HEIGHT, WIDTH, 1, 0)
		#window.timeout(TIMEOUT)
		window.keypad(True)
		window.nodelay(1)

	        players = []


                for pid in self.getpeerids():
			host,port = self.getpeer(pid)
                        self.id_tuples.append((host, port, 0))

                me = -1
                self.id_tuples = sorted(self.id_tuples, comp)
                for ind in range(len(self.id_tuples)):
                        self.id_tuples[2] = ind
                        p = Player(ind, 0, ind)
                        players.append(p)
                        if self.id_tuples[0] == self.serverhost and self.id_tuples[1] == self.serverport:
                                me = ind
                                
                self.b = Board(window, me, players)
                

		ui = threading.Thread(target=self.runUI, args=(self.b, screen, ))
		ui.daemon = True
		ui.start()

		while 1:
			with window_lock:
				c = window.getch()
			
			if c == ord('q'):
				self.b.q.put(Event(END))
				break
			elif c == curses.KEY_LEFT:
				self.b.q.put(Event(MOVE_LEFT, MY_ID))
			elif c == curses.KEY_RIGHT:
				self.b.q.put(Event(MOVE_RIGHT, MY_ID))
			elif c == curses.KEY_UP:
				self.b.q.put(Event(MOVE_UP, MY_ID))
			elif c == curses.KEY_DOWN:
				self.b.q.put(Event(MOVE_DOWN, MY_ID))		

	def __handle_insertpeer(self, peerconn, data):
	
	
		self.peerlock.acquire()
		try:
			try:
				peerid,host,port = data.split()

				if self.maxpeersreached():
					self.__debug('maxpeers %d reached: connection terminating' % self.maxpeers)
					peerconn.senddata(ERROR, 'Join: too many peers')
					return

				# peerid = '%s:%s' % (host,port)
				if peerid not in self.getpeerids() and peerid != self.myid:
					self.addpeer(peerid, host, port)
					self.__debug('added peer: %s' % peerid)
					peerconn.senddata(REPLY, 'Join: peer added: %s' % peerid)
				else:
					peerconn.senddata(ERROR, 'Join: peer already inserted %s'
							   % peerid)
			except:
				self.__debug('invalid insert %s: %s' % (str(peerconn), data))
				peerconn.senddata(ERROR, 'Join: incorrect arguments')
		finally:
			self.peerlock.release()

	# end handle_insertpeer method



	
	def __handle_listpeers(self, peerconn, data):

		self.peerlock.acquire()
		try:
			self.__debug('Listing peers %d' % self.numberofpeers())
			peerconn.senddata(REPLY, '%d' % self.numberofpeers())
			for pid in self.getpeerids():
				host,port = self.getpeer(pid)
				peerconn.senddata(REPLY, '%s %s %d' % (pid, host, port))
		finally:
			self.peerlock.release()

	def __sendtoall(self, msgtype, msgdata):
		self.peerlock.acquire()
		try:
			
			for pid in self.getpeerids():
				self.sendtopeer(pid,msgtype, msgdata)
		finally:
			self.peerlock.release()


	def __sendId(self):
		self.peerlock.acquire()
		try:
			cnt = 1;
			id_tuples.append((0, self.serverhost, serverport))
			for pid in self.getpeerids():
				host,port = self.getpeer(pid)
				self.sendtopeer(pid,ID, '%s %s %d' % (cnt, host, port))
				id_tuples.append((cnt, host, port))
				cnt = cnt+1
		finally:
			self.peerlock.release()
			
	def __handle_getId(self, peerconn, data):
		raceid,host,port = data.strip()
		self.myraceid = raceid

	def __handle_peername(self, peerconn, data):
		peerconn.senddata(REPLY, self.myid)

	def __handle_quit(self, peerconn, data):
		self.peerlock.acquire()
		try:
			peerid = data.lstrip().rstrip()
			if peerid in self.getpeerids():
				msg = 'Quit: peer removed: %s' % peerid 
				self.__debug(msg)
				peerconn.senddata(REPLY, msg)
				self.removepeer(peerid)
			else:
				msg = 'Quit: peer not found: %s' % peerid 
				self.__debug(msg)
				peerconn.senddata(ERROR, msg)
		finally:
			self.peerlock.release()



   
	def buildpeers(self, host, port, hops=1):
		if self.maxpeersreached() or not hops:
			return

		peerid = None

		self.__debug("Building peers from (%s,%s)" % (host,port))

		try:
			_, peerid = self.connectandsend(host, port, PEERNAME, '')[0]

			self.__debug("contacted " + peerid)
			resp = self.connectandsend(host, port, INSERTPEER, 
						'%s %s %d' % (self.myid, 
								  self.serverhost, 
								  self.serverport))[0]
			self.__debug(str(resp))
			if (resp[0] != REPLY) or (peerid in self.getpeerids()):
				return

			self.addpeer(peerid, host, port)

			# do recursive depth first search to add more peers
			resp = self.connectandsend(host, port, LISTPEERS, '',
						pid=peerid)
			if len(resp) > 1:
				resp.reverse()
				resp.pop()	# get rid of header count reply
				while len(resp):
					nextpid,host,port = resp.pop()[1].split()
					if nextpid != self.myid:
						self.buildpeers(host, port, hops - 1)
		except:
			if self.debug:
				traceback.print_exc()
			self.removepeer(peerid)

	def __handleMove(self, peerconn, data):
		#peerid,host,port = data.split()
		direction,player_id = data.split()
		self.b.q.put(Event(direction,player_id))
