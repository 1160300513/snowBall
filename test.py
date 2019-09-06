from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
browser = webdriver.Firefox()
browser.get('https://xueqiu.com')

url = 'https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=BILI&hl=0&source=all&sort=&page=1&q='

browser.get(url)
