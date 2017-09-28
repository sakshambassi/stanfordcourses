import bs4
from six.moves import urllib

url = "http://online.stanford.edu/courses/allcourses"

html= urllib.request.urlopen(url)
soup = bs4.BeautifulSoup(html, "html.parser")
file = open("testfile.txt","w")				#WRITE TO FILE

prefix = "http://online.stanford.edu"
overviews = ["Overview", "Course Description", "Course Overview", "About this course", "The Course", "STATEMENT OF NEED", "ABOUT THIS SET OF COURSES"]
topics = ["Table of Contents", "You Will Learn", " Course Syllabus", "Learning Objectives", "Learn How To:"]

coursetypes = soup.find_all('div', class_="clearfix block block-views")
for coursetype in coursetypes:
	coursetype = coursetype.find('h2').contents[0]
	ins = coursetype.find_next('tbody')
	trall = ins.find_all('tr')
	for tr in trall:
		temp = tr.find_next('td')
		ct = temp.find_next('a')
		ctcontents = ct.contents[0]
		url2 = prefix+ct['href']
		try:
			html2= urllib.request.urlopen(url2)
		except AttributeError:
			html2 = urllib.urlopen(url)
		soup2 = bs4.BeautifulSoup(html2, "html.parser")

		instructor = ct.find_next('td').contents[0]
		platform = instructor.find_next('td').contents[0]
		startdate = platform.find_next('span').contents[0]
		regfees = startdate.find_next('td').contents[0]
		status = regfees.find_next('td').contents[0]
		dept = status.find_next('a').contents[0]
		platform = platform.lstrip().rstrip()
		status = status.lstrip().rstrip()
		print(ctcontents,"\n")
		file.write('Type of course: ')
		file.write(coursetype)
		file.write("\nCourse Title: ")
		file.write(ctcontents.encode('utf-8'))
		file.write('\nInstructors: ')
		file.write(instructor.lstrip().rstrip())
		file.write('\nPlatform: ')
		file.write(platform)
		file.write('\nStart Date: ')
		file.write(startdate)
		file.write('\nRegistration Fees: ')
		file.write(regfees.lstrip().rstrip())
		file.write('\nStatus: ')
		file.write(status)
		file.write('\nDepartment: ')
		file.write(dept)

		body = soup2.find('div', class_='group-left')

		intro = body.find_all('div', class_='field-item even')
		try:
			nextbo = body.find('span').contents[0]
			if len(nextbo)<10:
				nextbo=nextbo.find_next('span').contents[0]
		except AttributeError:
			pass

		file.write("\nCourse Date:")
		file.write(str(nextbo.encode('utf-8')))
		
		applink = nextbo.find_next('a',href=True)['href']
		file.write("\nCourse Link: ")
		file.write(str(applink))
		
		try:
			coursetopic = nextbo.find_next('div', class_= 'field-item even').contents[0]
			file.write("\nCourse Topic: ")
			try:
				file.write(str(coursetopic.text.encode('utf-8')))			
			except AttributeError:
				file.write(coursetopic)
		except AttributeError:
			pass

		coverimage = body.find_next('div', class_= 'group-right well').find_next('img').get('src')
		file.write("\nCover Image: ")
		file.write(coverimage)

		for overview in overviews:
			try:
				heading = body.find('h2',string=overview)
				file.write("\nOverview: ")
				if overview == "Course Overview":
					try:
						heading = heading.find_next_sibling('p').contents[0].encode('utf-8')
						file.write(str(heading))
					except AttributeError:
						heading = heading.find_next_sibling('div').contents[0].encode('utf-8')
						file.write(str(heading))
				else:
					file.write(str(heading.find_next('p').contents[0].encode('utf-8')))
			except AttributeError:
				pass

		for topic in topics:
			try:
				heading = body.find('h2',string=topic)
				file.out("\nTopics Included: ")
				try:
					file.write(str(heading.find_next_sibling('ol')))
					break
				except AttributeError:
					file.write(str(heading.find_next_sibling('ul')))
					break
			except AttributeError:
				pass

		try:
			heading = body.find('h2',string="Prerequisites")
			file.write("\nPrerequisites: ")
			file.write(str(heading.find_next_sibling('p')))
		except:
			pass

		try:
			heading = body.find('h2',string="Recommended")
			file.write("\nRecommended: ")
			file.write(str(heading.find_next_sibling('p')))
		except:
			pass

		try:
			heading = body.find('h2',string="Certificates and Degrees")
			file.write("\nCertificates and Degrees: ")
			heading = heading.find_next_sibling('ul').text.lstrip().rstrip()
			file.write(str(heading.encode('utf-8')))
		except AttributeError:
			pass
		
		try:
			heading = body.find('h2',string="TO OBTAIN CME CREDITS")
			file.write("\nGrading: ")
			file.write(str(heading.find_next_sibling('ul')))
		except AttributeError:
			pass

		heading = body.find('h2',string='Tuition')
		try:
			heading = heading.find_next_sibling('ul')
			file.write("\nTuition and Fees: ")
			file.write(str(heading))
		except AttributeError:
			try:
				file.write(str(heading.find_next_sibling('ol')))
			except AttributeError:
				pass

		file.write("\n\n")
		print('\n')