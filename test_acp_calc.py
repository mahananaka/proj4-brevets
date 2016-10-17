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
	cp = brevet.make_controle_point(350,"")
	brevet.add_controle_point(cp)
	cp = brevet.make_controle_point(890,"3rd")
	brevet.add_controle_point(cp)

	expected_output = [{"description":"","distance": 0, "open":arrow.get('2016-11-10T08:00:00+00:00'), "close":arrow.get('2016-11-10T09:00:00+00:00')},
					 {"description":"First Checkpoint","distance": 100, "open":arrow.get('2016-11-10T10:56:00+00:00'), "close":arrow.get('2016-11-10T14:40:00+00:00')},
					 {"description":"","distance": 350, "open":arrow.get('2016-11-10T18:34:00+00:00'), "close":arrow.get('2016-11-11T07:20:00+00:00')},
					 {"description":"3rd","distance": 890, "open":arrow.get('2016-11-11T13:09:00+00:00'), "close":arrow.get('2016-11-13T01:23:00+00:00')},]

	assert brevet.get_control_times() == expected_output

def test_update_control_point():
	"""
	This tests the update_control_point method. First assert is testing a baseline.
	"""
	brevet = AcpBrevet( 1000, arrow.get('2016-11-10 08:00', 'YYYY-MM-DD HH:mm') )
	cp = brevet.make_controle_point(100,"First Checkpoint")
	brevet.add_controle_point(cp)

	expected_output = [{"description":"","distance": 0, "open":arrow.get('2016-11-10T08:00:00+00:00'), "close":arrow.get('2016-11-10T09:00:00+00:00')},
				 {"description":"First Checkpoint","distance": 100, "open":arrow.get('2016-11-10T10:56:00+00:00'), "close":arrow.get('2016-11-10T14:40:00+00:00')}]

	assert brevet.get_control_times() == expected_output

	"""
	Next we actually test the update method
	"""
	brevet.update_controle_point(1,0,"Start Line")
	brevet.update_controle_point(2,350,"1st Checkpoint")

	expected_output = [{"description":"Start Line","distance": 0, "open":arrow.get('2016-11-10T08:00:00+00:00'), "close":arrow.get('2016-11-10T09:00:00+00:00')},
				 {"description":"1st Checkpoint","distance": 350, "open":arrow.get('2016-11-10T18:34:00+00:00'), "close":arrow.get('2016-11-11T07:20:00+00:00')}]

	assert brevet.get_control_times() == expected_output

