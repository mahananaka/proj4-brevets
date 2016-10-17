"""
An ACP Brevet checkpoint calculator for determining when to
open and close a checkpoint by ACP rules. All distances are in
kilometers. Convert before inputting.
"""

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

"""
CONTROL_MAX and CONTROL_MIN are representations of the ACP table:
=================================================
Control location	Min Speed	Max Speed
-------------------------------------------------
0-200				15			34
200-400				15			32
400-600				15			30
600-1000			11.428		28
1000-1300			13.333		26
=================================================

Control location has been converted to a range instead.
Ex: 600-1000 becomes 1000-600=400.
"""
CONTROL_MAX = [ (200,34), (200,32), (200,30), (400,28), (300,26) ]
CONTROL_MIN = [ (200,15), (200,15), (200,15), (400,11.428), (300,13.333) ]
MINUTES_PER_HOUR = 60

class AcpBrevet():

	def __int__(self, length, starttime):

		self.brev_length = length
		self.brev_start = starttime #arrow datetime
		self.controles = []

		#make the initial controle point
		self.controles.append(make_controle_point(0,""))

	def make_controle_point(distance,descriptor):
		controle_point = {"description": descriptor, "distance": distance }
		return controle_point

	def add_controle_point(self,controle):
		self.controles.append(controle)

	def update_controle_point(control_num, distance, descriptor):
		if control_num <= len(self.controles):
			controle_point = make_controle_point(distance,descriptor)
			self.controles[control_num-1] = controle_point

	def output_controles(self):

		#update open and close times
		for ctrlpnt in self.controles:
			ctrlpnt["open"] = calc_control_time(self,ctrlpnt["distance"],CONTROL_MAX)
			ctrlpnt["close"] = calc_control_time(self,cntrlpnt["distance"],CONTROL_MIN)

		return self.controles

	def calc_control_time(self,distance,chart):
		#when distance 0, this controle is the start line and has a static open and close
		if(distance == 0):
			if(chart == CONTROL_MAX):
				return self.starttime
			else
				return self.starttime.replace(hour=+1)

		#calculation for controle points after start control
		remaining_dist = distance
		hours = 0
		minutes = 0

		for i,(span,speed) in enumerate(chart):
			if(remaining_dist>0):
				dist_seg = min(remaining_dist,span)
				hours = hours + dist_seg / speed
				minutes = minutes + int(round((dist_seg % speed)*MINUTES_PER_HOUR))
				remaining_dist = remaining_dist - span
			else:
				break

		return self.starttime.replace(hour=+hours,minute=+minutes)


