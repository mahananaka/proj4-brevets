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
    assert brevet.get_control_times() == [{'description':'','distance': 0, "open":brevet.brev_start, "close":brevet.brev_start.replace(hours=+1)}]

def test_add_control():
	"""
	Adding a few new control points
	"""
	brevet = AcpBrevet( 1000, arrow.get('2016-11-10 08:00', 'YYYY-MM-DD HH:mm') )
	cp = brevet.make_controle_point(100,"First Checkpoint")
	brevet.add_controle_point(cp)
	cp = brevet.make_controle_point(199,"2nd")
	brevet.add_controle_point(cp)
	cp = brevet.make_controle_point(350,"")
	brevet.add_controle_point(cp)

	assert brevet.get_control_times() == [{'description':'','distance': 0, "open":brevet.brev_start, "close":brevet.brev_start.replace(hours=+1)}]

