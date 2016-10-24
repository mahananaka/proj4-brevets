# Proj4-Brevet
This is a redesigned ACP Brevet Calculator. The original example is located at
https://rusa.org/octime_acp.html

## Author
Jared Paeschke, paeschke@cs.uoregon.edu

## Overview
The
calculator is built using Flask and Jinja2 templating. Arrow was used for proper date
time calculations. The render html page uses jQuery, Bootstrap, and Ajax to give
quick response to the user.

This Brevet Calculator uses the rules for an ACP Brevet. These rules can be located
at https://rusa.org/octime_alg.html and https://rusa.org/pages/rulesForRiders A synopsis
of these rules are that all brevets are either 200, 300, 400, 600, or 1000km. They 
generally end a small distance past these points but a static timer for the endpoint is
used regardless. Open and close on a distance is based on all the bracets of distance 
lower than it. For example a 250km controle in a 300km brevet uses the speeds of both
200 and 300 kilometer brevets. The first 200km is calculated at the speed for 0-200. 
Then the remaining 50km calculated for 200-400 bracket of distance. These two times
are summed and that is the final time.

## Installation
When writing and testing this program, the test machine was a Raspberry Pi 3 running
Raspian Jesse. This is the best sure fire way that the install will go smoothly. 
However you should have success as long as you have bash and make on your server machine

* git clone https://github.com/mahananaka/proj3-anagrams.git < install directory >
* cd < install directory >
* bash ./configure
* make run

The program should then sit idle and wait for page requests. The default port is
port 5000, to get the main page surf to http://< serverip >:5000/ or if you're 
on the server machine http://localhost:5000/. To stop the program at any time 
use ctrl+c.

## Tests
An automated test file was created using nose. If you wish to examine these tests
they are located in test_acp_calc.py. To run the tests used the command 'make test'.
These tests run through the examles that are dicussed on the https://rusa.org/octime_alg.html 
and a few other examples I thought of to add.

## Usage
The landing page will have a drop-down menu and two inputs for date and time. The 
drop-down menu is defaulted to 200km. The date and time fields will automatically
update with each keyup. When you enter a valid date-time the first controle which is
also at zero distance, and one additional controle will display. You may enter miles 
or kilometers, the other value will be changed to match. This way you can see 
distances in both measurements. When you create a control that is the last in the 
list, another will be added. You may only have 20 max controls. This should be more 
than enough for even a 1000km brevet. Updates will be posted in a box at the top of 
the page and auto disappear after a few seconds. Once you are done you click finish 
and it will display the output into a table for you.