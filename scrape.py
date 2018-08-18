# Scrapes an entire static website's source and the pdf files it directly links to
# Mainly used for UW CS courses.

# DISCLAIMER: Script should be used on websites that allow this in its terms and conditions.

from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

CONST_HTTP = 'http'
CONST_PDF = '.pdf'
CONST_FILES_FOLDER = './temp/files'
CONST_HTML_FOLDER = './temp/html'

baseurl = 'https://www.student.cs.uwaterloo.ca/~cs135/'

# specify the url
quote_page = 'https://www.student.cs.uwaterloo.ca/~cs135/handout'

# get html
html_doc = urlopen(quote_page)

soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())

# Grab HMTL page source
# page_source = open(quote_page + '.html', 'w')
# page_source.write(soup.prettify())
# page_source.close()

if not os.path.exists(CONST_FILES_FOLDER):
	os.makedirs(CONST_FILES_FOLDER)

if not os.path.exists(CONST_HTML_FOLDER):
	os.makedirs(CONST_HTML_FOLDER)

# find all pdfs on page
for atag in soup.find_all('a'):
	link = atag.get('href')
	print(link)

	if CONST_HTTP not in link and link.endswith(CONST_PDF):
		last_slash_index = link.rfind('/')
		filename = link[last_slash_index + 1:]
		filepath = CONST_FILES_FOLDER + '/' + filename

		fileurl = baseurl + link

		print(fileurl)

		# download the pdf
		pdfdata_response = urlopen(fileurl)
		pdfdata = pdfdata_response.read()

		# store it in current directory
		file = open(filepath, 'wb')
		file.write(pdfdata)
		file.close()

# Zip file up and get rid of temp files/folders, need to provide name
# grab all other types of files as well

# traverse the website to visit page, but beware of cycles (multithreading?)
# Grab the html source as well? Number pages as 1,2,3,4...
# Pass website and stuff in through command line args

# unit tests with dummy page
# use a unit test framework, run and test as I buil and test new things in another file 

# set up with S3, SQL, website and front end