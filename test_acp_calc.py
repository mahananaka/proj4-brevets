"""
Nose tests for apc_calc.py
"""

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# module we are testing
from acp_calc import AcpBrevet


def test_new_brevet():
    """
    Testing initializing AcpBrevet
    """
    brevet = AcpBrevet( 1000, arrow.get('2016-11-10 08:00', 'YYYY-MM-DD HH:mm') )
    assert brevet.brev_length == 1000
    assert brevet.brev_start == arrow.get('2016-11-10 08:00', 'YYYY-MM-DD HH:mm')

    array_compare = [{"description":"","distance": 0,"open":arrow.get('2016-11-10T08:00:00+00:00'), "close":arrow.get('2016-11-10T09:00:00+00:00')}]
    assert brevet.get_control_times() == array_compare

def test_add_control():
	"""
	Testing adding a few new control points
	"""
	brevet = AcpBrevet( 1000, arrow.get('2016-11-10 08:00', 'YYYY-MM-DD HH:mm') )
	cp = brevet.make_controle_point(100,"First Checkpoint")
	brevet.add_controle_point(cp)
	cp = brevet.make_controle_point(199,"2nd")
	brevet.add_controle_point(cp)
	cp = brevet.make_controle_point(350,"")
	brevet.add_controle_point(cp)

	should_be = [{"description":"","distance": 0, "open":arrow.get('2016-11-10T08:00:00+00:00'), "close":arrow.get('2016-11-10T09:00:00+00:00')},
					 {"description":"First Checkpoint","distance": 100, "open":arrow.get('2016-11-10T10:56:00+00:00'), "close":arrow.get('2016-11-10T14:40:00+00:00')},
					 {"description":"2nd","distance": 199, "open":arrow.get('2016-11-10T13:51:00+00:00'), "close":arrow.get('2016-11-10T21:16:00+00:00')},
					 {"description":"","distance": 350, "open":arrow.get('2016-11-10T18:34:00+00:00'), "close":arrow.get('2016-11-11T07:20:00+00:00')}]

	assert brevet.get_control_times() == should_be

def test_update_control_point():

	brevet = AcpBrevet( 1000, arrow.get('2016-11-10 08:00', 'YYYY-MM-DD HH:mm') )
	cp = brevet.make_controle_point(100,"First Checkpoint")
	brevet.add_controle_point(cp)

	should_be = [{"description":"","distance": 0, "open":arrow.get('2016-11-10T08:00:00+00:00'), "close":arrow.get('2016-11-10T09:00:00+00:00')},
				 {"description":"First Checkpoint","distance": 100, "open":arrow.get('2016-11-10T10:56:00+00:00'), "close":arrow.get('2016-11-10T14:40:00+00:00')}]

	assert brevet.get_control_times() == should_be

	brevet.update_controle_point(0,0,"Start Line")
	brevet.update_controle_point(1,350,"1st Checkpoint")

	should_be = [{"description":"Start Line","distance": 0, "open":arrow.get('2016-11-10T08:00:00+00:00'), "close":arrow.get('2016-11-10T09:00:00+00:00')},
				 {"description":"1st Checkpoint","distance": 350, "open":arrow.get('2016-11-10T18:34:00+00:00'), "close":arrow.get('2016-11-11T07:20:00+00:00')}]

	assert brevet.get_control_times() == should_be

