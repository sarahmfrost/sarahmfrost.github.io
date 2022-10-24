import urllib
import requests
from bs4 import BeautifulSoup

titles = []

r = urllib.request.urlopen('https://americanindian.si.edu/explore/collections').read()
soup = BeautifulSoup(r)

for i in soup.find_all('div', {'class': "webmedia"}):
	titles.append(i.p.text) 

print(titles)

