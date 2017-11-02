import requests
from bs4 import BeautifulSoup

url = 'https://nba.hupu.com/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
print(soup.select('#J-t-game '))