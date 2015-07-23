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
	time = db.StringListProperty()
	location = db.StringListProperty()
	instructor = db.StringProperty()
	classSize = db.IntegerProperty()
	currentEnrol = db.IntegerProperty()

def subPostConstructor(postCode):
	subPostData = POSTParser(postCode)#{"CSC108H1F": coursefinderParser("CSC108H1F20159")}
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
							time = meeting['time'] if meeting['time'] is not None else [],
							location = meeting['location'] if meeting['location'] is not None else [],
							instructor = meeting['instructor'],
							classSize = int(meeting['classSize']),
							currentEnrol = int(meeting['currentEnrolment'])
							)
			newMeeting.put()

	
	return "suceed"
