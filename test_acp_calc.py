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

def test_brevet_example1():
    """
    Testing initializing AcpBrevet
    """
    brevet = AcpBrevet( 200, arrow.get('2016-11-10 10:00', 'YYYY-MM-DD HH:mm') )
    
    #open
    assert brevet.calc_open(60, brevet.brev_length) == arrow.get('2016-11-10 11:46', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_open(120, brevet.brev_length) == arrow.get('2016-11-10 13:32', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_open(175, brevet.brev_length) == arrow.get('2016-11-10 15:09', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_open(200, brevet.brev_length) == arrow.get('2016-11-10 15:53', 'YYYY-MM-DD HH:mm')

    #closing
    assert brevet.calc_close(60, brevet.brev_length) == arrow.get('2016-11-10 14:00', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_close(120, brevet.brev_length) == arrow.get('2016-11-10 18:00', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_close(175, brevet.brev_length) == arrow.get('2016-11-10 21:40', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_close(200, brevet.brev_length) == arrow.get('2016-11-10 13:30', 'YYYY-MM-DD HH:mm')