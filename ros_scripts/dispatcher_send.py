from pydispatch import dispatcher
import time
def handle_event(sender):
	print 'signal was sent by', sender

dispatcher.send(signal='hi',sender='ros')

import xmlrpclib

s = xmlrpclib.ServerProxy('http://localhost:8001')
print s.pow(2,3)  # Returns 2**3 = 8
print s.add(2,3)  # Returns 5
print s.div(5,2)  # Returns 5//2 = 2
print s.prt(11,12)


# Print list of available methods
print s.system.listMethods()
