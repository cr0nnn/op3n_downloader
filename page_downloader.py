import re
import requests
import os
from threading import BoundedSemaphore, Thread

threadLimiter = BoundedSemaphore(20)

class DownloadThread(Thread):

	def __init__(self,link,folder):
		Thread.__init__(self)
		self.link = link
		self.folder = folder 

	def run(self):
		threadLimiter.acquire()
		try:
			self.download_img()
		finally:
			threadLimiter.release()

	def download_img(self):
		r = requests.get(self.link, stream=True)
		if r.status_code == 200:
			path = self.folder + "/images/" + self.link.split("/")[-1]
			with open(path, 'wb') as f:
				for chunk in r:
					f.write(chunk)

def convert_img(page, folder):
	
	# Delete alt rendering images
	new_content = re.sub(r"(srcset\=\"[^\"]+?\")","", page)
	# Create directoy for images
	if not os.path.exists(folder + "/images/"): os.mkdir(folder + "/images/" ) 
	# Find out images and download 
	pattern = re.compile(r"\<img [^\>]+? src\=\"(http[^\"]+?)\"")
	images = pattern.findall(page)
	threads = []
	for i in images:
		t = DownloadThread(i,folder).start()
		threads.append(t)	
		new_content = re.sub(i,"images/" + i.split("/")[-1], new_content) 	
	return new_content

def get(link, basedir):

	page = requests.get(link)
	if not link.endswith("/"): 
		path = link.split("/")[-1] 
	else:
		path = link.split("/")[-2]
	if not basedir.ends("/"): basedir = basedir + "/"
	path = basedir + path
	if not os.path.exists(path) : os.mkdir(path)
	content = convert_img(page.content, path)
	with open(path + "/index.html","w") as f:
			f.write(content)

if __name__ == "__main__":
	download_page("https://www.cybrary.it/0p3n/lets-enumerate-bonus/")
