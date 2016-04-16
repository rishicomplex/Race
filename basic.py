from p2p import *

PEERNAME = "NAME"   # request a peer's canonical id
LISTPEERS = "LIST"
INSERTPEER = "JOIN"
PEERQUIT = "QUIT"
LEFT = "LEFT"
RIGHT = "RIGH"
UP = "ACCL"
DOWN = "DECC"

REPLY = "REPL"
ERROR = "ERRO"

def btdebug( msg ):
	print "[%s] %s" % ( str(threading.currentThread().getName()), msg )

class RacePeer(BTPeer):

	def __init__(self, maxpeers, serverport):
		BTPeer.__init__(self, maxpeers, serverport)
		
		self.addrouter(self.__router)
		
		handlers = {LISTPEERS : self.__handle_listpeers,
			    INSERTPEER : self.__handle_insertpeer,
			    PEERNAME: self.__handle_peername,
			    PEERQUIT: self.__handle_quit,
			    LEFT: self.__handleleft,
			    RIGHT: self.__handleright,
			    UP: self.__handleup,
			    DOWN: self.__handledown,
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
				resp.pop()    # get rid of header count reply
				while len(resp):
				    nextpid,host,port = resp.pop()[1].split()
				    if nextpid != self.myid:
						self.buildpeers(host, port, hops - 1)
		except:
			if self.debug:
				traceback.print_exc()
			self.removepeer(peerid)

	def __handleleft(self, peerconn, data):
		peerid,host,port = data.split()

	def __handleright(self, peerconn, data):
		peerid,host,port = data.split()

	def __handleup(self, peerconn, data):
		peerid,host,port = data.split()

	def __handledown(self, peerconn, data):
		peerid,host,port = data.split()