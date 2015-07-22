from flask import Flask,render_template,redirect,url_for
import parsers
import database
import re

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def index():
    #return simplifyList("MB 121 MB 121 MB 121 MU 121")
	#return str(re.findall("[A-Z][a-zA-Z]* [A-Z][a-zA-Z]+", "G Baumgartner "))
	#return str(parsers.coursefinderParser("CSC108H1F20159"))
	#return parsers.POSTParser('CSC')
	return database.subPostConstructor('CSC')
	#return "1"
	#return str(re.split('([0-9]+)',"CSC108H1S"))


@app.route('/ttapi/')
@app.route('/ttapi/<postcode>/')
@app.route('/ttapi/<post>/courses')
@app.route('/ttapi/<post>/<code>/')
def timetable_api(postcode=None, post=None, code=None):
	

	if postcode is None and post is None and code is None:
		return render_template('ttapi_index.html', error=False);
	else:
		if postcode is not None and (post is None and code is None):
			return "Nothing"
		if post is not None and (postcode is None and code is None):
			return "this should be a page to show all courses of CSC"
		if (post is not None and code is not None) and postcode is None:
			return "this shoudd be a page for '/csc/343h1' like shits"

	return render_template('ttapi_index.html', error=True), 404

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

	

