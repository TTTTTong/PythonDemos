from selenium import webdriver

path = '/usr/local/bin/chromedriver.exe'
browser = webdriver.Chrome(path)
browser.get('http://www.google.com')