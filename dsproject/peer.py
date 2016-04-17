import sys
import threading
import socket
import curses

from basic import *

from Tkinter import *
import Tkinter
from random import *

class RaceMain:
	def __init__( self, firstpeer, hops=2, maxpeers=5, serverport=5678, master=None ):
		
		self.racepeer = RacePeer( maxpeers, serverport )
		host,port = firstpeer.split(':')
		
		self.racepeer.buildpeers( host, int(port), hops=hops )
		#
		self.peerList = {}
		self.updatePeerList()
		print self.peerList
		self.window = Tkinter.Tk()
		
		t = threading.Thread( target = self.racepeer.mainloop, args = [] )
		t.start()		
		self.racepeer.startstabilizer( self.racepeer.checklivepeers, 3 )
		self.window.after( 3000, self.onTimer )


	def onTimer( self ):
		print 'Strat Game ?'
		self.onRefresh()
		if len( self.racepeer.getpeerids()) == 1 :
			if self.racepeer.serverhost==host and self.racepeer.serverport==port:
				self.racepeer.__sendId()
			curses.wrapper(self.racepeer.handleScreen)
		self.window.after( 3000, self.onTimer )
		#self.after_idle( self.onTimer )



	def updatePeerList( self ):
		if len(self.peerList) > 0:
			self.peerList.pop(0, len(self.peerList) - 1)
		for p in self.racepeer.getpeerids():
			self.peerList[END] = p



	def onRefresh(self):
		print("refreshing......")
		self.updatePeerList()
		print peerList
def main():
	if len(sys.argv) < 4:
		print "Syntax: %s server-port max-peers peer-ip:port" % sys.argv[0]
		sys.exit(-1)

	serverport = int(sys.argv[1])
	maxpeers = sys.argv[2]
	peerid = sys.argv[3]
	# s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	# s.connect( ( "iitkgp.ac.in", 80 ) )
	# serverhost = s.getsockname()[0]
	# print serverhost
	# s.close()

	app = RaceMain( firstpeer=peerid, maxpeers=maxpeers, serverport=serverport )

	#app.mainloop()



# setup and run app
if __name__=='__main__':
	main()