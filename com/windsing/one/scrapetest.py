from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.allitebooks.com/")
# print(html.read())

bsObj = BeautifulSoup(html.read())
# print(bsObj.html)

