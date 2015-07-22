from google.appengine.ext import db
from parsers import POSTParser,coursefinderParser
import re
class SubPost(db.Model):
	name = db.StringProperty()
	short = db.StringProperty()
	last_update = db.TimeProperty()

class Course(db.Model):
	subPost = db.ReferenceProperty(SubPost, collection_name = "courses")
	title = db.StringProperty()
	courseNum = db.IntegerProperty()
	length = db.StringProperty(choices = ('H','Y'))
	campus = db.IntegerProperty(choices = (1,3,5))
	section = db.StringProperty(choices = ('F','S','Y'))

class Meeting(db.Model):
	course = db.ReferenceProperty(Course, collection_name = "meetings")
	code = db.StringProperty()
	time = db.ListProperty()
	location = db.ListProperty()
	instructor = db.StringProperty()

def subPostConstructor(postCode):
	subPostData = {"CSC108H1F": coursefinderParser("CSC108H1F20159")}#POSTParser(POSTcode)
	newSubPost = SubPost(name = "computer science", short = postCode) #write a uitility function to find the full name 
	newSubPost.put()

	for courseCode, courseData in subPostData.items():
		courseCode = re.split('([0-9]+)',courseCode)
		courseNow = Course(
					subPost = newSubPost, title = "", 
					courseNum = int(courseCode[1]), 
					length = courseCode[2], 
					campus = int(courseCode[3]), 
					section = courseCode[4])
		courseNow.put()

		for meetingCode,meeting in courseData['meetings'].items():
			newMeeting = Meeting(
							course = courseNow,
							code = meetingCode,
							time = meeting['time'],
							location = meeting['location'],
							instructor = meeting['instructor'])
			newMeeting.put()
	return "suceed"
	"""
	response = db.GqlQuery("SELECT * FROM Meeting")
	ans = ""
	for q in response:
		 ans += q.time[0]
	return ans
	"""