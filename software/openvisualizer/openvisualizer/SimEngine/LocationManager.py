#!/usr/bin/python
# Copyright (c) 2010-2013, Regents of the University of California. 
# All rights reserved. 
#  
# Released under the BSD 3-Clause license as published at the link below.
# https://openwsn.atlassian.net/wiki/display/OW/License

import random
import logging

import SimEngine
import xmlrpclib
s = xmlrpclib.ServerProxy('http://localhost:8001')
s2 = xmlrpclib.ServerProxy('http://localhost:8001')
class LocationManager(object):
    '''
    The module which assigns locations to the motes.
    '''
    
    def __init__(self):
        
        # store params
        self.engine               = SimEngine.SimEngine()
        
        # local variables
        
        # logging
        self.log                  = logging.getLogger('LocationManager')
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(logging.NullHandler())

    
    #======================== public ==========================================
    
    def getLocation(self,mote_id):
        '''
        # get random location around Cory Hall, UC Berkeley
        lat =   37.875095-0.0005+random.random()*0.0010
        lon = -122.257473-0.0005+random.random()*0.0010
        
        # debug
        if self.log.isEnabledFor(logging.DEBUG):
            self.log.debug('assigning location ({0} {1})'.format(lat,lon))
        '''
	#print "getting location from ros"
	position,neighbors = s.getUAVLocation(mote_id)


        lat =   37.875095-0.0005+position[1]/111000
        lon = -122.257473-0.0005+position[0]/111000
	#print "mote_id: " + str(mote_id) +", location: " + str(position[0]) +', ' + str(position[1])
        return lat, lon

    def getLocationCm(self,mote_id):

	print "getting location from getLcoationCM"
	try:
		position,neighbors = s2.getUAVLocation(mote_id)
	except Exception as ex:
    		template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    		message = template.format(type(ex).__name__, ex.args)
    		print message
		print "error calling s. getUAVLocation while in LocationManager.py"
		pass

	print position
	z = int(position[2]*10)
        y=int(position[1]*10)
        x = int(position[0]*10)
	#print x , y ,z
	#print "mote_id: " + str(mote_id) +", location: " + str(position[0]) +', ' + str(position[1])
	parsed_keys = {}
	parsed_neighbors = {}
	for key in neighbors.iterkeys():
		#print key.split('v')
		parsed_keys[int(key.split('v')[1])]=key
	
	
	sorted_keys=sorted(parsed_keys.iterkeys())
	#print sorted_keys
	#print parsed_keys
	#print neighbors
	neighbor_list = []
	for neighbor in sorted_keys:

	    	coordinates = []
		#print coordinates
	    	for coord in neighbors[parsed_keys[neighbor]]:
		#	print coord
			coordinates.append(int(coord*10))
		#print coordinates
	    	neighbor_list.append(coordinates)

	    
	print neighbor_list
	
        return x , y , z,neighbor_list
    	
    def getLocationNoRPC(self,mote_id):
        '''
        # get random location around Cory Hall, UC Berkeley
        lat =   37.875095-0.0005+random.random()*0.0010
        lon = -122.257473-0.0005+random.random()*0.0010
        
        # debug
        if self.log.isEnabledFor(logging.DEBUG):
            self.log.debug('assigning location ({0} {1})'.format(lat,lon))
        '''
	print "getting location from ros"
	position = s.getUAVLocation(mote_id)



        lat =   37.875095-0.0005+position[1]*0.0001
        lon = -122.257473-0.0005+position[0]*0.0001
	print "mote_id: " + str(mote_id) +", location: " + str(position[0]) +', ' + str(position[1])
        return lat, lon
    	
	
    #======================== private =========================================
    
    #======================== helpers =========================================
    
