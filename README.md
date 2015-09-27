# UofT-Course-Timetable-API
http://sneaky-main.appspot.com/parsley/

An API devoted to providing a perfect solution to developers who want to work with the Uoft timetable but hate to parse their ugly pages. 
It's built on Google App Engine and a part of my course scheduling app. Everyone is welcome to use the parsers.

#Usage
*** It's still in development. For now it only supports the courses that are sponsored by the Faculty of Art & Science at St.Geroge Campus.***

##Query a course (/courseCode)
If you want to query a course, please use standard course code.
for example

CSC108H1S ECO100Y1Y

cAsE doEsn'T maTtEr bUt YoU nEEd To aDd seCtIon cODe("F" or "S") 
and lENGth ("H" or "Y", and if it's a full year course, the last "Y" is required)

So the query would be like

http://sneaky-main.appspot.com/parsley/Csc108H1S
or 
http://sneaky-main.appspot.com/parsley/eco100Y1y

##Query all the courses a department provides (/departmentCode)
if you want to query all the course data from a specific department, please use the standard 
abbreviation. (csc for computer science, mus for music, eco for economics ...)

*You can find the abbreviations at http://www.artsandscience.utoronto.ca/ofr/timetable/winter/

So the query would be like
http://sneaky-main.appspot.com/parsley/Csc
or 
http://sneaky-main.appspot.com/parsley/MUS

#Response
The response is in JSON format. On error, an error message will be returned with the HTTP error code 404.
The format is as the following

####Query a course
	 
	 	{
	 	"info":
	 		{"Division":"Faculty of Arts and Science",
	 		 "Term": ...,
	 		 "Exclusion":....
	 		 ...}
	 	"meetings":
	 		{"Lec 0101":
	 			{"currentEnrolment": ...,
	 			 "waitlist": ..., 
	 			 "activity": ...,
	 			 "location": ..., 
	 			 "time": ..., 
	 			 "classSize": ...,
	 			 "instructor":...}, 
	 		 "Lec 0201":
	 		 	...
	 		 "Tut 2201":
	 		 	...
	 		 }
	 	}
	 
####Querying department

	 	{
	 	 "CSC148H1S":{
	 	 		"info": ...
	 	 		"meetings": ...
	 	 		}
	 	 "CSC324H1F":{
	 	 		"info": ...
	 	 		"meetings": ...
	 	 		}
	 	 courses...
	 	 }

#Note

+ Please be informed that it's extreamly time-consuming to query all the courses a department provides. (It takes about 50 seconds to parse all CSC courses.)

+ The dict of meetings has seven, and only seven keys:

	"activity" name of the meeting, string, start with "Lec"(lectures) or "Tut"(tutorials)
	
	"courseEnrolment" the current number of students who have already enrolled in this course, string
	
	"waitlist" whether or not the meeting has a waitlist, boolean
	
	"time" the time of the meeting, list of strings
	
	"classSize" the maximum number of students in this meeting, string
	
	"location" the location(s) of this meeting, list of strings
	
	"instructor" the instructor of this meeting, string

+ The dict of info could have any number of keys, it depends on how much info is provided by the courseFinder. However, all the values in "info" are strings.

+ Notice that all the values could be None if that specific info is provided by the courseFinder




