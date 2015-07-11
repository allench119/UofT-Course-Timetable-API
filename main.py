from flask import Flask,render_template,redirect,url_for
import urllib2
from bs4 import BeautifulSoup
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

@app.route('/test')
def test():
	
	url = 'http://www.artsandscience.utoronto.ca/ofr/timetable/winter/csc.html'
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	return soup.title.string

class SubPost(db.Model):
	name = db.StringProperty()
	short = db.StringProperty()

class Course(db.Model):
	subPost = db.ReferenceProperty(SubPost, collection_name = "courses")
	title = db.StringProperty()
	courseNum = db.IntegerProperty()
	length = db.StringProperty(choices = ('H','Y'))
	campus = db.IntegerProperty(choices = (1,3,5))
	informationUpdated = db.StringProperty()

class Section(db.Model):
	course = db.ReferenceProperty(Course, collection_name = "sections")
	section = db.StringProperty(choices = ('F','S','Y'))

class Meeting(db.Model):
	section = db.ReferenceProperty(Section, collection_name = "meetings")
	code = db.StringProperty()
	time = db.StringProperty()
	location = db.StringProperty()
	instructor = db.StringProperty()
	enrolment_indicator = db.StringProperty(choices = ('P','R','PE','RP','E','AE','P*','PE*','RP*'))
	enrolment_control = db.LinkProperty()
	last_update = db.TimeProperty()



def dbConstructor():

	csc = SubPost(name = "computer science", short = "csc")
	csc.put()
	csc343 = Course(csc, title = "Intro to Database", courseNum = 343, length = "H", campus = 1, informationUpdated = None)
	csc343.put()
	csc343h1f = Section(csc343, section = "F")
	csc343h1f.put()
	L101 = Meeting(csc343h1f, code = "L101", time = "T1-3 R1", location = "blah", instructor = "B.Simon", enrolment_indicator = "P")
	L101.put()

	response = db.GqlQuery("SELECT * FROM Meeting")
	ans = ""
	for q in response:
		 ans += q.instructor
	return ans







