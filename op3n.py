import requests
import bs4
import page_downloader
import os
import sys

def test_existence(link, basedir):
	
	return os.path.exists(basedir + "/" + link.split("/")[-2])	
	

def get_page_articles(page_number, basedir):
	
	op3n = requests.get("https://www.cybrary.it/cybrary-0p3n/page/" + str(page_number))
	soup = bs4.BeautifulSoup(op3n.content, 'html.parser')
	cards = soup.find_all('div', {'class':'featuredopencard'})
	cards += soup.find_all('div', {'class':'contentcardopenhomepage'})
	print "Getting page number... " + str(page_number)
	result = 0 
	for card in cards:
		link = card.find("a")['href']
		print "Getting .... " + link 
		page_downloader.get(link, basedir)
		result = test_existence(link, basedir)
	return result

def main(basedir):
	
	if not os.path.exists(basedir): os.makedirs(basedir)
	op3n = requests.get("https://www.cybrary.it/cybrary-0p3n/")
	soup = bs4.BeautifulSoup(op3n.content, 'html.parser')
	cards = soup.find_all('div', {'class':'featuredopencard'})
	cards += soup.find_all('div', {'class':'contentcardopenhomepage'})
	pages = int(soup.find('a',{'class':'last'})['href'].split("/")[-2])
	# Main page
	for card in cards:
		link = card.find("a")['href']
		print "Getting .... " + link 
		page_downloader.get(link, basedir)

	for i in range(2, pages + 1):
		result = get_page_articles(i, basedir)
		if result == 1 : 
			print "Page downloaded before..\nStopping..."
			break

if __name__ == "__main__":
	
	if len(sys.argv) != 2 :
		print "Invoked incorrectly..."
		sys.exit(-1)	
	basedir = sys.argv[1]
	main(basedir)
