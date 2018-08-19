# Scrapes an entire static website's source and the pdf files it directly links to
# Mainly used for UW CS courses.

# DISCLAIMER: Script should be used on websites that allow this in its terms and conditions.

from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import zipfile

# Constants
CONST_HTTP = 'http'
CONST_FILES_FOLDER = './temp/files'
CONST_HTML_FOLDER = './temp/html'
CONST_DESIRED_EXTENSIONS = ['.pdf', '.txt', '.doc', '.docx', '.ppt', '.pptx']

# Zip an entire directory
# top_dir is the path of the directory to zip
# ziph is the zip file handle
# Returns None
def zipdir(top_dir, ziph):
	for root, dir, files in os.walk(top_dir):
		for file in files:
			ziph.write(os.path.join(root, file))

# Checks if link has an extension that we want to download
# link is the url of the file that we may potentially download
# Returns Bool
def is_desired_extension(link):
	for ext in CONST_DESIRED_EXTENSIONS:
		if link.endswith(ext):
			return True
	return False

project_name = 'cs135'
baseurl = 'https://www.student.cs.uwaterloo.ca/~cs135/'

# specify the url
quote_page = 'https://www.student.cs.uwaterloo.ca/~cs135/handout'

html_doc = urlopen(quote_page)

soup = BeautifulSoup(html_doc, 'html.parser')

if not os.path.exists(CONST_FILES_FOLDER):
	os.makedirs(CONST_FILES_FOLDER)

if not os.path.exists(CONST_HTML_FOLDER):
	os.makedirs(CONST_HTML_FOLDER)

# find all downloadable files on page
for atag in soup.find_all('a'):
	link = atag.get('href')

	if CONST_HTTP not in link and is_desired_extension(link):
		last_slash_index = link.rfind('/')
		filename = link[last_slash_index + 1:]
		filepath = CONST_FILES_FOLDER + '/' + filename

		fileurl = baseurl + link

		# download the file
		data_response = urlopen(fileurl)
		data = data_response.read()

		# store it in current directory
		file = open(filepath, 'wb')
		file.write(data)
		file.close()

zipf = zipfile.ZipFile("./temp/" + project_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir(CONST_FILES_FOLDER, zipf)
zipf.close()

# traverse the website to visit page, but beware of cycles (multithreading?)
# Grab the html source as well? Number pages as 1,2,3,4...
# Pass website and stuff in through command line args

# unit tests with dummy page
# use a unit test framework, run and test as I buil and test new things in another file 

# set up with S3, SQL, website and front end