from flask import Flask,render_template
import urllib2
from google.appengine.ext import db


app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def index():
    return redirect(url_for('timetable_api'))

@app.route('/ttapi/')
@app.route('/ttapi/<postcode>/')
@app.route('/ttapi/<post>/courses')
@app.route('/ttapi/<post>/<code>/')
def timetable_api(postcode=None, post=None, code=None):
	url = "http://www.artsandscience.utoronto.ca/ofr/timetable/winter/"

	if postcode is None and post is None and code is None:
		return render_template('ttapi_index.html', error=False);
	else:
		if postcode is not None and (post is None and code is None):
			url = 
			urllib2.urlopen("")
			
		if post is not None and (postcode is None and code is None):
			return "this should be a page to show all courses of CSC"
		if (post is not None and code is not None) and postcode is None:
			return "this shoudd be a page for '/csc/343h1' like shits"


	else:
		return render_template('ttapi_index.html', error=True), 404

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

class SubPost(db.model):
	name = db.StringProperty()
	short = db.StringProperty()

class Courses(db.model):
	subPost = db.ReferenceProperty(SubPost, collection_name = "courses")
	title = db.StringProperty()
	courseNum = db.IntegerProperty()
	length = db.StringProperty(choices = ('H','Y'))
	campus = db.IntegerProperty(choices = (1,3,5))
	informationUpdated = db.StringProperty()

class Section(db.model):
	course = db.ReferenceProperty(Courses, collection_name = "sections")
	section = db.StringProperty(choices = ('F','S','Y'))

class Meeting(db.model):
	section = db.ReferenceProperty(Section, collection_name = "meetings")
	code = db.StringProperty()
	time = db.StringProperty()
	location = db.StringProperty()
	instructor = db.StringProperty()
	enrolment_indicator = db.StringProperty(choices = ('P','R','PE','RP','E','AE','P*','PE*','RP*'))
	enrolment_control = db.LinkProperty()
	last_update = db.TimeProperty()






