# UofT-Course-Timetable-API


*** It's still in development. For now it only supports the courses that are sponsored by the Faculty of Art & Science at St.Geroge Campus.***

An API devoted to providing a perfect solution to developers who want to work with the Uoft timetable but hate to parse their ugly pages
It's built on Google App Engine and a part of my course scheduling app. Everyone is welcome to use the parsers.

Usage:
	If you want to query a course, please use standard course code.
	for example
	
	CSC108H1S ECO100Y1Y
	
	case doesn't matter but you need to add section code("F" or "S") 
	and length("H" or "Y", and if it's a full year course, the last "Y" is required)
	
	so the query would be
	http://sneaky-main.appspot.com/Csc108H1S
	or 
	http://sneaky-main.appspot.com/eco100Y1y
	
	if you want to query all the course data from a specific department, please use the standard 
	abbreviation.
	for example:
	
	use csc for computer science
		mus for music
		eco for economics
	
	*you can find the abbreviations at http://www.artsandscience.utoronto.ca/ofr/timetable/winter/

	so the query would be
	http://sneaky-main.appspot.com/Csc
	or 
	http://sneaky-main.appspot.com/MUS

The response is in JSON format. On error, an error message will be returned with the HTTP error code 404.
*Please be informed that it's extreamly time-consuming to query all the courses a department provides. (It takes about 50 seconds to parse all CSC courses.)

