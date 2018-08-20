# Scrapes an entire static website's source and the pdf files it directly links to
# Mainly used for UW CS courses.

# DISCLAIMER: Script should be used on websites that allow this in its terms and conditions.

from urllib.request import urlopen
from urllib.error import HTTPError
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


# Downloads all relevant files on directly linked by the page
# Returns None
def scrape_page(baseurl, cururl):
	print("scraping page: " + cururl)

	# grab the html
	html_doc = urlopen(cururl)
	soup = BeautifulSoup(html_doc, 'html.parser')

	for atag in soup.find_all('a'):
		link = atag.get('href')

		if link and is_desired_extension(link):
			last_slash_index = link.rfind('/')
			filename = link[last_slash_index + 1:]
			filepath = CONST_FILES_FOLDER + '/' + filename
			fileurl = link

			if CONST_HTTP not in link:
				fileurl = baseurl + link

			print("downloading file: " + fileurl)

			# download the file
			try:
				data_response = urlopen(fileurl)
			except HTTPError as e:
				print("ERROR: " + str(e))
				return

			data = data_response.read()

			# store it in current directory
			file = open(filepath, 'wb')
			file.write(data)
			file.close()


# Adds all pages to be scraped to the queue
# Returns None
def traverse_pages(baseurl, cururl, visited_pages, pages_to_scrape):
	print(cururl)

	visited_pages[cururl] = True

	# grab the html
	try:
		html_doc = urlopen(cururl)
	except HTTPError as e:
		print("ERROR: " + str(e))
		return

	soup = BeautifulSoup(html_doc, 'html.parser')

	for atag in soup.find_all('a'):
		link = atag.get('href')

		if link and link not in visited_pages and baseurl in link:
			pages_to_scrape.append(link)
			traverse_pages(baseurl, link, visited_pages, pages_to_scrape)


# Traverse all pages linked to baseurl and downloads hosted files
# Returns None
def traverse_and_scrape_pages(baseurl):
	visited_pages = {}
	pages_to_scrape = [baseurl]

	traverse_pages(baseurl, baseurl, visited_pages, pages_to_scrape)

	while pages_to_scrape != []:
		link = pages_to_scrape.pop()
		scrape_page(baseurl, link)


if __name__ == "__main__":
	project_name = 'cs135'
	baseurl = 'https://www.student.cs.uwaterloo.ca/~cs135/'

	# Stores the files scraped
	if not os.path.exists(CONST_FILES_FOLDER):
		os.makedirs(CONST_FILES_FOLDER)

	# Stores the HTML source scraped
	if not os.path.exists(CONST_HTML_FOLDER):
		os.makedirs(CONST_HTML_FOLDER)

	traverse_and_scrape_pages(baseurl)

	# Zip the files
	zipf = zipfile.ZipFile("./temp/" + project_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
	zipdir(CONST_FILES_FOLDER, zipf)
	zipf.close()

# download images as well

# Grab the html source as well? Number pages as 1,2,3,4...
# Pass website and stuff in through command line args

# unit tests with dummy page
# use a unit test framework, run and test as I buil and test new things in another file 

# set up with S3, SQL, website and front end; multithread requests?