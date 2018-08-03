# Copyright (c) 2010-2013, Regents of the University of California. 
# All rights reserved. 
#  
# Released under the BSD 3-Clause license as published at the link below.
# https://openwsn.atlassian.net/wiki/display/OW/License
import logging
log = logging.getLogger('moteProbe')
log.setLevel(logging.ERROR)
log.addHandler(logging.NullHandler())
import xmlrpclib
s = xmlrpclib.ServerProxy('http://localhost:8001')
import os
if os.name=='nt':       # Windows
   import _winreg as winreg
elif os.name=='posix':  # Linux
   import glob
   import platform      # To recognize MAC OS X
import threading
import binascii
import serial
import socket
import time
import sys
import struct
import numpy
from   pydispatch import dispatcher
import OpenHdlc
import openvisualizer.openvisualizer_utils as u
from   openvisualizer.moteConnector import OpenParser
from   openvisualizer.moteConnector.SerialTester import SerialTester

#============================ functions =======================================

BAUDRATE_LOCAL_BOARD  = 115200
BAUDRATE_IOTLAB       = 500000

def findSerialPorts(isIotMotes=False):
    '''
    Returns the serial ports of the motes connected to the computer.
    
    :returns: A list of tuples (name,baudrate) where:
        - name is a strings representing a serial port, e.g. 'COM1'
        - baudrate is an int representing the baurate, e.g. 115200
    '''
    serialports = []
    
    if os.name=='nt':
        path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
        skip = False
        try :
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        except :
            # No mote is connected
            skip = True
        if not skip :
            for i in range(winreg.QueryInfoKey(key)[1]):
                try:
                    val = winreg.EnumValue(key,i)
                except:
                    pass
                else:
                    serialports.append( (str(val[1]),BAUDRATE_LOCAL_BOARD) )
    elif os.name=='posix':
        if platform.system() == 'Darwin':
            portMask = ['/dev/tty.usbserial-*']
        else:
            portMask = ['/dev/ttyUSB*']
        for mask in portMask :
            serialports += [(s,BAUDRATE_IOTLAB) for s in glob.glob(mask)]

    mote_ports = []

    if isIotMotes:
        # this is IoTMotes, use the ports directly
        mote_ports = serialports
    else:
        # Find all OpenWSN motes that answer to TRIGGERSERIALECHO commands
        for port in serialports:
            probe = moteProbe(serialport=(port[0],BAUDRATE_LOCAL_BOARD))
            tester = SerialTester(probe.portname)
            tester.setNumTestPkt(1)
            tester.setTimeout(2)
            tester.test(blocking=True)
            if tester.getStats()['numOk'] >= 1:
                mote_ports.append((port[0],BAUDRATE_LOCAL_BOARD));
            probe.close()
            probe.join()
    
    # log
    log.info("discovered following COM port: {0}".format(['{0}@{1}'.format(s[0],s[1]) for s in mote_ports]))
    
    return mote_ports

#============================ class ===========================================

class moteProbe(threading.Thread):
    
    MODE_SERIAL    = 'serial'
    MODE_EMULATED  = 'emulated'
    MODE_IOTLAB    = 'IoT-LAB'
    MODE_ALL       = [
        MODE_SERIAL,
        MODE_EMULATED,
        MODE_IOTLAB,
    ]
    
    def __init__(self,serialport=None,emulatedMote=None,iotlabmote=None):
        # verify params
        if   serialport:
            assert not emulatedMote
            assert not iotlabmote
            self.mode             = self.MODE_SERIAL
        elif emulatedMote:
            assert not serialport
            assert not iotlabmote
            self.mode             = self.MODE_EMULATED
        elif iotlabmote:
            assert not serialport
            assert not emulatedMote
            self.mode             = self.MODE_IOTLAB
        else:
            raise SystemError()
        
        # store params
        if   self.mode==self.MODE_SERIAL:
            self.serialport       = serialport[0]
            self.baudrate         = serialport[1]
            self.portname         = self.serialport
        elif self.mode==self.MODE_EMULATED:
            self.emulatedMote     = emulatedMote
            self.portname         = 'emulated{0}'.format(self.emulatedMote.getId())
        elif self.mode==self.MODE_IOTLAB:
            self.iotlabmote       = iotlabmote
            self.portname         = 'IoT-LAB{0}'.format(iotlabmote)
        else:
            raise SystemError()
        
        # log
        log.info("creating moteProbe attaching to {0}".format(
                self.portname,
            )
        )
        
        # local variables
        self.hdlc                 = OpenHdlc.OpenHdlc()
        self.lastRxByte           = self.hdlc.HDLC_FLAG
        self.busyReceiving        = False
        self.inputBuf             = ''
        self.outputBuf            = []
        self.outputBufLock        = threading.RLock()
        self.dataLock             = threading.Lock()
        # flag to permit exit from read loop
        self.goOn                 = True
        
        # initialize the parent class
        threading.Thread.__init__(self)
        
        # give this thread a name
        self.name                 = 'moteProbe@'+self.portname
        
        if self.mode in [self.MODE_EMULATED,self.MODE_IOTLAB]:
            # Non-daemonized moteProbe does not consistently die on close(),
            # so ensure moteProbe does not persist.
            self.daemon           = True
        
        # connect to dispatcher
        dispatcher.connect(
            self._bufferDataToSend,
            signal = 'fromMoteConnector@'+self.portname,
        )
    
        # start myself
        self.start()
    
    #======================== thread ==========================================
    
    def run(self):
        try:
            # log
            log.info("start running")
        
            while self.goOn:     # open serial port
                
                # log 
                log.info("open port {0}".format(self.portname))
                
                if   self.mode==self.MODE_SERIAL:
                    self.serial = serial.Serial(self.serialport,self.baudrate,timeout=1,rtscts=False,dsrdtr=False)
                elif self.mode==self.MODE_EMULATED:
                    self.serial = self.emulatedMote.bspUart
                elif self.mode==self.MODE_IOTLAB:
                    self.serial = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    self.serial.connect((self.iotlabmote,20000))
                else:
                    raise SystemError()
                
                while self.goOn: # read bytes from serial port
                    try:
                        if   self.mode==self.MODE_SERIAL:
                            rxBytes = self.serial.read(1)
                            if rxBytes == 0: # timeout
                                continue
                        elif self.mode==self.MODE_EMULATED:
                            rxBytes = self.serial.read()
                            
			    #if len(rxBytes )==2:
			        #print "made it to moteprobe:"
				#print rxBytes
				#print ""
				#print s.prt(rxBytes[0],rxBytes[1])
			    if (len(rxBytes)==12 and (rxBytes[0] != '~')):
				#send bytes to ros node
			
	
				#for byte in rxBytes:
				 #   decodedBytes +=ord(byte)
				#print decodedBytes
				#print "".join(rxBytes[0:4]),"".join(rxBytes[4:8]),"".join(rxBytes[8:12])
	
				xcontrol = struct.unpack('=f',"".join(rxBytes[4:8]))
				ycontrol = struct.unpack('=f',"".join(rxBytes[4:8]))
				zcontrol = struct.unpack('=f',"".join(rxBytes[8:12]))
				#print xcontrol[0],ycontrol[0],zcontrol[0]
				#request imu data from ros node
				#print self.emulatedMote.bspUart.engine.pause()
				accel_data,timestamp = s.prt2('fromMoteProbe@'+self.portname,xcontrol[0],ycontrol[0],zcontrol[0],self.emulatedMote.bspUart.timeline.getCurrentTime())
				#accel_data,timestamp = s.prt2('fromMoteProbe@'+self.portname,ord(rxBytes[0]),ord(rxBytes[1]),ord(rxBytes[2]),self.emulatedMote.bspUart.timeline.getCurrentTime())
				print "made it past the rpc call in moteprobe.py"
               			 #pause engine if timestamp is greater than current time
                		#while timestamp<self.emulatedMote.bspUart.timeline.getCurrentTime():
				 #   print "pausing"
                                  #  print self.emulatedMote.bspUart.engine.getNumMotes()
				   # print self.emulatedMote.bspUart.engine.isPaused
                    		   # self.emulatedMote.bspUart.engine.pause()
                                    #print self.emulatedMote.bspUart.engine.isPaused
				packed_data = []
				for d in accel_data:
 				    packed_data += struct.pack("=h",numpy.clip(int(d*32767/16/9.8),-32768,32767))
				#print "packed data:"    
				#print packed_data
				unpacked_data =[]
				for d in packed_data:
				    unpacked_data += struct.unpack("=b",d) 

				#print "uint8 unpacked data:"    
				#print unpacked_data

				chrData =''
				chrData =['~']
				#for d in unpacked_data[0:3]:
				 #   chrData+=chr(d)
				for d in packed_data[0:6]:
				    chrData+=d
				chrData +=['~']
				#print chrData
				#chrData = self.hdlc.hdlcify(chrData)  this created and error -11
				#write response data to mote
                                #print chrData
				self.serial.write(chrData)
				

                        elif self.mode==self.MODE_IOTLAB:
                            rxBytes = self.serial.recv(1024)
                        else:
                            raise SystemError()
                    except Exception as err:
                        print err
                        log.warning(err)
                        time.sleep(1)
                        break
                    else:
                        for rxByte in rxBytes:
                            if      (
                                        (not self.busyReceiving)             and 
                                        self.lastRxByte==self.hdlc.HDLC_FLAG and
                                        rxByte!=self.hdlc.HDLC_FLAG
                                    ):
                                # start of frame
                                if log.isEnabledFor(logging.DEBUG):
                                    log.debug("{0}: start of hdlc frame {1} {2}".format(self.name, u.formatStringBuf(self.hdlc.HDLC_FLAG), u.formatStringBuf(rxByte)))
                                self.busyReceiving       = True
                                self.inputBuf            = self.hdlc.HDLC_FLAG
                                self.inputBuf           += rxByte
                            elif    (
                                        self.busyReceiving                   and
                                        rxByte!=self.hdlc.HDLC_FLAG
                                    ):
                                # middle of frame
                                
                                self.inputBuf           += rxByte
                            elif    (
                                        self.busyReceiving                   and
                                        rxByte==self.hdlc.HDLC_FLAG
                                    ):
                                # end of frame
                                if log.isEnabledFor(logging.DEBUG):
                                    log.debug("{0}: end of hdlc frame {1} ".format(self.name, u.formatStringBuf(rxByte)))
                                self.busyReceiving       = False
                                self.inputBuf           += rxByte
                                
                                try:
                                    tempBuf = self.inputBuf
                                    with open(socket.gethostname()+'.log','a') as f:
                                        f.write(self.inputBuf)
				
                                    self.inputBuf        = self.hdlc.dehdlcify(self.inputBuf)
                                    if log.isEnabledFor(logging.DEBUG):
                                        log.debug("{0}: {2} dehdlcized input: {1}".format(self.name, u.formatStringBuf(self.inputBuf), u.formatStringBuf(tempBuf)))
                                except OpenHdlc.HdlcException as err:
                                    log.warning('{0}: invalid serial frame: {2} {1}'.format(self.name, err, u.formatStringBuf(tempBuf)))
                                else:
                                    if self.inputBuf==chr(OpenParser.OpenParser.SERFRAME_MOTE2PC_REQUEST):
                                        with self.outputBufLock:
                                            if self.outputBuf:
                                                outputToWrite = self.outputBuf.pop(0)
						
                                                self.serial.write(outputToWrite)
                                    else:
                                        # dispatch
                                        dispatcher.send(
                                            sender        = self.name,
                                            signal        = 'fromMoteProbe@'+self.portname,
                                            data          = [ord(c) for c in self.inputBuf],
                                        )
			                if len(rxBytes) ==2:
			                    print "message dipatched"
                                            
                            
                            self.lastRxByte = rxByte
			if len(rxBytes) ==2:
			    print "HDLC packet generated by moteprobe:"
                            print self.inputBuf
			    outputToWrite = self.inputBuf
			    print "------------------------",type(outputToWrite)
			    #self.serial.write(outputToWrite)

                    if self.mode==self.MODE_EMULATED:
                        self.serial.doneReading()
        except Exception as err:
            errMsg=u.formatCrashMessage(self.name,err)
            print errMsg
            log.critical(errMsg)
            sys.exit(-1)
        finally:
            if self.mode==self.MODE_SERIAL and self.serial is not None:
                self.serial.close()
    
    #======================== public ==========================================
    
    def getPortName(self):
        with self.dataLock:
            return self.portname
    
    def getSerialPortBaudrate(self):
        with self.dataLock:
            return self.baudrate
    
    def close(self):
        self.goOn = False
    
    #======================== private =========================================
    
    def _bufferDataToSend(self,data):
        
        # abort for IoT-LAB
        if self.mode==self.MODE_IOTLAB:
            return
        
        # frame with HDLC
        hdlcData = self.hdlc.hdlcify(data)
        
        # add to outputBuf
        with self.outputBufLock:
            self.outputBuf += [hdlcData]
