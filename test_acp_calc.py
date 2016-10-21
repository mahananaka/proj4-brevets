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
    Running example 1 of ACP rules
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
    assert brevet.calc_close(200, brevet.brev_length) == arrow.get('2016-11-10 23:30', 'YYYY-MM-DD HH:mm')

def test_brevet_example2():
    """
    Running example 2 of ACP rules
    """
    brevet = AcpBrevet( 600, arrow.get('2016-11-10 01:00', 'YYYY-MM-DD HH:mm') )
    
    #open
    assert brevet.calc_open(100, brevet.brev_length) == arrow.get('2016-11-10 03:56', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_open(200, brevet.brev_length) == arrow.get('2016-11-10 06:53', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_open(350, brevet.brev_length) == arrow.get('2016-11-10 11:34', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_open(550, brevet.brev_length) == arrow.get('2016-11-10 18:08', 'YYYY-MM-DD HH:mm')

    #closing
    assert brevet.calc_close(550, brevet.brev_length) == arrow.get('2016-11-11 13:40', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_close(600, brevet.brev_length) == arrow.get('2016-11-11 17:00', 'YYYY-MM-DD HH:mm')

def test_brevet_example3():
    """
    Running example 3 of ACP rules
    """
    brevet = AcpBrevet( 1000, arrow.get('2016-11-10 01:00', 'YYYY-MM-DD HH:mm') )
    
    #open
    assert brevet.calc_open(890, brevet.brev_length) == arrow.get('2016-11-11 06:09', 'YYYY-MM-DD HH:mm')

    #closing
    assert brevet.calc_close(890, brevet.brev_length) == arrow.get('2016-11-12 18:23', 'YYYY-MM-DD HH:mm')

def test_brevet_final_closes():
    """
    Testing final closes for 200,300,400,600, and 1000 km.
    """
    brevet = AcpBrevet( 200, arrow.get('2016-11-10 01:00', 'YYYY-MM-DD HH:mm') )
    
    #closing
    assert brevet.calc_close(201, 200) == arrow.get('2016-11-10 14:30', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_close(301, 300) == arrow.get('2016-11-10 21:00', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_close(401, 400) == arrow.get('2016-11-11 04:00', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_close(601, 600) == arrow.get('2016-11-11 17:00', 'YYYY-MM-DD HH:mm')
    assert brevet.calc_close(1001, 1000) == arrow.get('2016-11-13 04:00', 'YYYY-MM-DD HH:mm')
