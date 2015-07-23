import urllib2
from bs4 import BeautifulSoup
import logging
import json
import re

def POSTParser(POSTcode):

	POSTLib = {}
	courseList = getCourses(POSTcode)
	if not courseList:
		return None
	for course in courseList:
		logging.error(course + " started")
		try:
			POSTLib[course] = coursefinderParser(course + ("20161" if course[-1] == 'S' else "20159"))
		except urllib2.HTTPError, err:
			if err.code == 404:
				POSTLib[course] = coursefinderParser(course + ("20161" if course[-1] == 'S' else "20159"))
			else:
				raise
		logging.error(course + " finished")

	return POSTLib

def getAddress(POSTcode):

	url = "http://www.artsandscience.utoronto.ca/ofr/timetable/winter/"
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')

	
	courseTag = soup.find("a", string=re.compile(POSTcode.upper() + " courses"), href=True)

	if courseTag:
		return url + courseTag['href']
	else:
		return None
	
def getCourses(POSTcode):

	url = getAddress(POSTcode)
	if not url:
		return None

	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')

	table = soup.find_all('table')[0]
	courseList = []
	pattern = re.compile('^' + POSTcode.upper())

	for atag in table.find_all('a'):
		if pattern.match(atag.get_text()):
		 	courseList.append(atag.get_text() + atag.find_parent('td').find_next_sibling('td').get_text())
	return courseList

def simplifyList(text):

	textList = text.lstrip().rstrip().split(' ')
	leastRepeated = len(textList)
	for i in textList:
		if i == '':
			textList.remove(i)
		else:
			if textList.count(i) < leastRepeated:
				leastRepeated = textList.count(i)

	if leastRepeated > 1:
		return " ".join(textList[:len(textList) / leastRepeated])
	else:
		return " ".join(textList)

	
	
def waitlistOption(td):

	imgTags = td.find_all('img')
	for img in imgTags:
		if 'checkmark.png' in img['src']:
			return True
	return False

def coursefinderParser(courseCode):
	
	keywords = ["activity","time","instructor","location","classSize","currentEnrolment","waitlist"]
	url = ("http://coursefinder.utoronto.ca/course-search/search/courseInquiry"
			"?methodToCall=start"
			"&viewId=CourseDetails-InquiryView"
			"&courseId=") + courseCode

	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')

	courseData = {}
	courseData["info"] = {}
	courseData["meetings"] = {}

	if soup.find(id="u172") == None and courseData["info"] == {}:
		return None

	table = soup.find(id="u172").tbody.find_all('tr')
	meetings = {}

	for tr in table:
		meeting = {}
		i = 0

		for td in tr.find_all('td'):
			if keywords[i] == 'waitlist':
				meeting[keywords[i]] = waitlistOption(td)
				continue
			if td.div.span != None:
				if td.div.span.get_text().strip('\r\n ') == '':
					meeting[keywords[i]] = None
				else:
					text = td.div.span.get_text().strip('\r\n')
					if keywords[i] == "time":
						meeting[keywords[i]] = re.findall("[a-zA-Z]+ [0-9:-]+",text)
					elif keywords[i] == "location":
						meeting[keywords[i]] = re.findall("[a-zA-Z]+ [0-9]+", simplifyList(text))
					elif keywords[i] == "instructor":
						meeting[keywords[i]] = simplifyList(text)
					else:
						meeting[keywords[i]] = text
			else:
				meeting[keywords[i]] = None
			i += 1

		meetings[meeting['activity']] = meeting

	courseData['meetings'] = meetings
	return courseData
