#!/usr/bin/env python

import rospy

import logging
import logging.handlers as Handlers

#http://www.senseair.se/wp-content/uploads/2014/06/Modbus-on-tSENSE-1_00_20140220.pdf

#pip install pymodbus
from pymodbus.client.sync import ModbusSerialClient
#http://pymodbus.readthedocs.org

from pymodbus.diag_message import *
from pymodbus.file_message import *
from pymodbus.other_message import *
from pymodbus.mei_message import *

from pprint import pprint

class SenseAirDevice(object):

	def __init__(self):
		#---------------------------------------------------------------------------#
		# This will simply send everything logged to console
		#---------------------------------------------------------------------------#
		logging.basicConfig()
		log = logging.getLogger()
		log.setLevel(logging.DEBUG)
		self.client = None

	def connect(self, deviceName):
	  self.client = ModbusSerialClient(method='rtu',port=deviceName,stopbits=1, bytesize=8, baudrate=9600, timeout=0.2)
	  if not self.client.connect():
	      rospy.logerr("Unable to connect to %s", device)
	      return False
	  return True

	def close(self):
		self.client.close()

	# Not working right now
	def getDeviceIdentification(self, objectId):

		rq = ReadDeviceInformationRequest(read_code=4, object_id=objectId, unit=0xFE)
		#rospy.loginfo("encoded: %h", encoded[0])
		rr = self.client.execute(rq)
		print rr

		return ""
		if rr is None:
			rospy.logerr("No response from device")
			return None

		if rr.function_code < 0x80:                 # test that we are not an error
			return  rr.information[0]
			#vendor_name = rr.information[0]
			#product_code = rr.information[1]
			#code_revision = rr.information[2]

			#rospy.loginfo("vendor: %s", vendor_name)
			#rospy.loginfo("product code: %s", product_code)
			#rospy.loginfo("revision: %s", code_revision)

		else:
			rospy.logwarn("error reading device identification: %h", rr.function_code)


	def getVendor(self):

		vendor = self.getDeviceIdentification(0)
		print vendor

	def readCO2(self):
		response = self.client.read_input_registers(address=3, count=1, unit=0xFE )
		return response.getRegister(0)

	def readTemperature(self):
		response = self.client.read_input_registers(address=4, count=1, unit=0xFE )
		return response.getRegister(0)*100.0

	def sendCommand(self, data):
	  #make sure data has an even number of elements
	  if(len(data) % 2 == 1):
	     data.append(0)

	  #Initiate message as an empty list
	  message = []

	  #Fill message by combining two bytes in one register
	  for i in range(0, len(data)/2):
	     message.append((data[2*i] << 8) + data[2*i+1])

	  #To do!: Implement try/except
	  self.client.write_registers(0x03E8, message, unit=0x0009)


	def getStatus(self, numBytes):
	  """Sends a request to read, wait for the response and returns the Gripper status. The method gets the number of bytes to read as an argument"""
	  numRegs = int(ceil(numBytes/2.0))

	  #To do!: Implement try/except
	  #Get status from the device
	  response = self.client.read_holding_registers(0x07D0, numRegs, unit=0x0009)

	  #Instantiate output as an empty list
	  output = []

	  #Fill the output with the bytes in the appropriate order
	  for i in range(0, numRegs):
	     output.append((response.getRegister(i) & 0xFF00) >> 8)
	     output.append( response.getRegister(i) & 0x00FF)

	  #Output the result
	  return output
