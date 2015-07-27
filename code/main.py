from flask import Flask,render_template,redirect,url_for,Response
import parsers
import json
import re
import urllib2

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def index():
	usage = r"""
			Usage:
				if you want to query a course, please use standard course code.
				for example:

					CSC108H1S ECO100Y1Y

				case doesn't matter but you need to add section code("F" or "S") 
					and length("H" or "Y", and if it's a full year course, the last "Y" is required)

				so the query would be
					http://sneaky-main.appspot.com/Csc108H1S
					or 
					http://sneaky-main.appspot.com/eco100Y1y

				if you want to query all the course data from a specific department, please use the standard abbreviation.
				for example:

					use csc for computer science
						mus for music
						eco for economics

					*you can find the abbreviations at http://www.artsandscience.utoronto.ca/ofr/timetable/winter/

				so the query would be
					http://sneaky-main.appspot.com/Csc
					or 
					http://sneaky-main.appspot.com/MUS
			"""

	return Response(usage, mimetype='text/plain')

@app.route('/<code>/')
def timetableAPI(code=None):

	result = None
	if code is None:
		return redirect("/")
	else:
		code = code.upper()
		if re.match("([A-Z]+[0-9]+H[135][FS])|([A-Z]+[0-9]+Y[135]Y)",code):
			try:
				result = parsers.coursefinderParser(code + ("20161" if code[-1] == 'S' else "20159"))
			except urllib2.HTTPError, err:
				if err.code == 404:
					result = parsers.coursefinderParser(code + ("20161" if code[-1] == 'S' else "20159"))
				else:
					return "Sorry, the query failed for an unknown reason. Please try again. (The error is most likely caused by CourseFinder server failing to response.)", 404
			if result:
				return json.dumps(result)
			else:
				return "We couldn't find the course you input or the query is invalid, please refer to the index page.", 404

		elif re.match("^[A-Z]+$",code):
			code = code.upper()
			try:
				result = parsers.POSTParser(code)
			except urllib2.HTTPError, err:
				if err.code == 404:
					result = parsers.POSTParser(code)
				else:
					return "Sorry, the query failed for an unknown reason. Please try again. (The error is most likely caused by CourseFinder server failing to response.)", 404
			if result:
				return json.dumps(result)
			else:
				return "We couldn't find the course you input or the query is invalid, please refer to the index page.", 404
		else:
			return "Query is invalid, please refer to the index page", 404

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

	

