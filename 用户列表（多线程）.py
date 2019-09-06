import threading
import time
import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
class myThread(threading.Thread):
    def __init__(self, left, right, stockCode, pre, num):
        threading.Thread.__init__(self)
        self.left = left
        self.right = right
        self.stockCode = stockCode
        self.soup = soup
        self.pre = pre
        self.browser = browser
        self.num = num

    def run(self):
        left = self.left
        right = self.right
        pre = self.pre
        browser = initBrowser()
        stockCode = self.stockCode
        con = self.initDB('user'+str(self.num)+'.db')
        cur = con.cursor()
        f = open('log'+str(self.num)+'.txt','w')
        for i in range(left, right):
            coleTime = time.ctime()
            suf = '?page=' + str(i)
            url = pre + suf
            f.write(str(i)+'\n')
            browser.refresh()
            time.sleep(2)
            try:
                browser.get(url)
                soup = BeautifulSoup(browser.page_source, 'lxml')
                self.insertDB(self.getUserId(soup), cur, stockCode, coleTime)
                con.commit()
            except:
                continue
        f.close()
        browser.quit()


    def initDB(self, name):
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

    def initBrowser(self):
        browser = webdriver.Firefox()
        browser.set_page_load_timeout(20)
        browser.set_script_timeout(20)
        return browser

    def getUserId(self, soup):
        ids = list()
        for i in soup.find('ul', attrs={'class': 'users-list'}).find_all('li'):
            div = i.find('a')
            ids.append([div['data-id'], div['data-name']])
        return ids

    def insertDB(self, idlis, cur, code, coleTime):
        for i in idlis:
            cur.execute('insert into user values(?,?,?,?)', tuple(list(i) + [code, coleTime]))


def initBrowser():
    browser = webdriver.Firefox()
    browser.set_page_load_timeout(100)
    browser.set_script_timeout(100)
    return browser
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
stockCode = 'SH600000'
pre = 'https://xueqiu.com/S/'+stockCode+'/follows'
browser = initBrowser()
browser.get(pre)
soup = BeautifulSoup(browser.page_source,'lxml')
browser.quit()
if(checkIfHasFollows(soup)):
    totPage = getTotPageNum(soup)
    for i in range(0,5):
        t = totPage/5.0
        thread = myThread(int(t*i)+1,int(t*(i+1))+1,stockCode,pre,i+1)
        thread.start()
else:
    print('this one doesn\'t have follows.')
