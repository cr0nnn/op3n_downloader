import requests
import bs4
import page_downloader

def get_page_articles(page_number, basedir):
	
	op3n = requests.get("https://www.cybrary.it/cybrary-0p3n/page/" + str(page_number))
	soup = bs4.BeautifulSoup(op3n.content, 'html.parser')
	cards = soup.find_all('div', {'class':'featuredopencard'})
	cards += soup.find_all('div', {'class':'contentcardopenhomepage'})
	print "Getting page number... " + str(page_number)
	for card in cards:
		link = card.find("a")['href']
		print "Getting .... " + link 
		page_downloader.get(link, basedir)

def main():

	op3n = requests.get("https://www.cybrary.it/cybrary-0p3n/")
	soup = bs4.BeautifulSoup(op3n.content, 'html.parser')
	cards = soup.find_all('div', {'class':'featuredopencard'})
	cards += soup.find_all('div', {'class':'contentcardopenhomepage'})
	pages = soup.find('a',{'class':'last'})['href'].split("/")[-2]
	# Main page
	for card in cards:
		link = card.find("a")['href']
		print "Getting .... " + link 
		page_downloader.get(link,'/tmp/test/')
	

if __name__ == "__main__":
	get_page_articles(2,'/tmp/test/')
	#main()
