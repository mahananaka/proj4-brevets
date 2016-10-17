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
    assert brevet.get_control_times() == [{'description':'','distance': 2, "open":brevet.brev_start, "close":brevet.brev_start.replace(hour=+1)}]