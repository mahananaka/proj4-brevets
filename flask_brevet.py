"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
# import acp_limits
from acp_calc import AcpBrevet

###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return flask.render_template('page_not_found.html'), 404


###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############
@app.route("/_set_start", methods = ["POST"])
def set_start():
  """
  Creates and AcpBrevet object with from total length and start time.
  """
  app.logger.debug("Got a JSON set_start post");
  reply = {}

  flask.session["bStart"] = request.form["bStart"]
  flask.session["bLength"] = int(request.form["bLength"])

  try:
    start = arrow.get(flask.session["bStart"], "YYYY/MM/DD HH:mm")
  except:
    reply["message"] = "Bad date Time."
    return jsonify(result=reply)
  
  brevet = AcpBrevet(request.form["bLength"], start)
  open_limit = brevet.calc_open(0,flask.session["bLength"])
  close_limit = brevet.calc_close(0,flask.session["bLength"])

  reply["message"] = "Start of event and length set."
  reply["open"] = open_limit.format("MMM DD, HH:mm")
  reply["close"] = close_limit.format("MMM DD, HH:mm")
  return jsonify(result=reply)

#----------------------

@app.route("/_calc_times", methods = ["POST"])
def calc_times():
  """
  Calculates open/close times from kilometers, using rules 
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of miles. 
  """
  app.logger.debug("Got a JSON calc_time post");
  reply = {}

  try:
    start = arrow.get(flask.session["bStart"], "YYYY/MM/DD HH:mm")
  except:
    reply["message"] = "Bad date Time."
    return jsonify(result=reply)

  brevet = AcpBrevet(flask.session["bLength"], start)
  open_limit = brevet.calc_open(int(request.form["dist"]),flask.session["bLength"])
  close_limit = brevet.calc_close(int(request.form["dist"]),flask.session["bLength"])

  reply["message"] = "Controle added or updated."
  reply["open"] = open_limit.format("MMM DD, YYYY HH:mm")
  reply["close"] = close_limit.format("MMM DD, YYYY HH:mm")

  return jsonify(result=reply)
 
#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try: 
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"



#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT, host="0.0.0.0")

    
