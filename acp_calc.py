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

Control location has been converted to a span instead.
Ex: 600-1000 becomes 1000-600=400.
"""
CONTROL_MAX = [ (200,34), (200,32), (200,30), (400,28), (300,26) ]
CONTROL_MIN = [ (200,15), (200,15), (200,15), (400,11.428), (300,13.333) ]
BREVET_END = {"200":810, "300":1200, "400":1620, "600":2400, "1000":4500}
MINUTES_PER_HOUR = 60
#13:30 for 200 KM, 20:00 for 300 KM, 27:00 for 400 KM, 40:00 for 600 KM, and 75:00 for 1000 KM

class AcpBrevet():

	def __init__(self, length, start):

		self.brev_length = length
		self.brev_start = start #arrow datetime
		self.controles = []

	def calc_close(self,dist,total):
		hrs = 0
		mins = 0		

		#when distance 0, this controle is the start line and has a static open and close
		if(dist == 0):
			return self.brev_start.replace(hours=+1)
		
		if(dist >= total):
			mins = BREVET_END[str(total)]
		else:
			#calculation for controle points after start control
			remaining_dist = dist
			for i,(span,speed) in enumerate(CONTROL_MIN):
				if(remaining_dist>0):
					dist_seg = min(remaining_dist,span)
					hrs = int(hrs + dist_seg / speed)
					mins = mins + int(round((dist_seg%speed/speed)*MINUTES_PER_HOUR))
					remaining_dist = remaining_dist - span
				else:
					break

		if(mins >= MINUTES_PER_HOUR):
			hrs += int(mins / MINUTES_PER_HOUR)
			mins = mins % MINUTES_PER_HOUR

		if(dist > total):
			print(hrs + "-" + mins)

		return self.brev_start.replace(hours=+hrs,minutes=+mins)

	def calc_open(self,dist,total):
		#when distance 0, this controle is the start line and has a static open and close
		if(dist == 0):
			return self.brev_start

		#calculation for controle points after start control
		remaining_dist = dist
		hrs = 0
		mins = 0

		for i,(span,speed) in enumerate(CONTROL_MAX):
			if(remaining_dist>0):
				dist_seg = min(remaining_dist,span)
				hrs = int(hrs + dist_seg / speed)
				mins = mins + int(round((dist_seg%speed/speed)*MINUTES_PER_HOUR))
				remaining_dist = remaining_dist - span
			else:
				break

		if(mins >= MINUTES_PER_HOUR):
			hrs += int(mins / MINUTES_PER_HOUR)
			mins = mins % MINUTES_PER_HOUR

		return self.brev_start.replace(hours=+hrs,minutes=+mins)


