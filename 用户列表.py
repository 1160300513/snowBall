from selenium import webdriver
import time
from bs4 import BeautifulSoup
import sqlite3
def getTotPageNum(soup):
    pageNum = list()
    for i in soup.find_all('a',attrs={'data-page':True}):
        try:
            a = int(i.text)
        except:
            continue
        pageNum.append(a)
    pageNum.sort()
    return pageNum[len(pageNum)-1]
def checkIfHasFollows(soup):
    if soup.text[:3] == '404':
        return False
    return True
def initBrowser():
    browser = webdriver.Firefox()
    browser.set_page_load_timeout(100)
    browser.set_script_timeout(100)
    return browser
def getUserId(soup):
    ids = list()
    for i in soup.find('ul',attrs={'class':'users-list'}).find_all('li'):
        div = i.find('a')
        ids.append([div['data-id'],div['data-name']])
    return ids
def initDB(name):
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute('''create table user(
                    uid varchar, 
                    name nvarchar, 
                    stockCode varchar,
                    coleTime nvarchar
                    );''')
    con.commit()
    return con
def insertDB(idlis, cur, code, coleTime):
    for i in idlis:
        cur.execute('insert into user values(?,?,?)',tuple(list(i)+[code,coleTime]))


con = initDB('user2.db')
cur = con.cursor()
stockCode = 'SH603712'
pre = 'https://xueqiu.com/S/'+stockCode+'/follows'
browser = initBrowser()
browser.get(pre)
soup = BeautifulSoup(browser.page_source,'lxml')
if(checkIfHasFollows(soup)):
    totPage = getTotPageNum(soup)
else:
    print('this one doesn\'t have follows.')

browser.close()
