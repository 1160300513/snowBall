import sqlite3
import os
oslist = os.listdir()
CNT = 0
a = set()
row = 0
for i in oslist:
    if '.db' in i:
        con = sqlite3.connect(i)
        cur = con.cursor()
        for i in cur.execute('select count() from user'):
            CNT = CNT + int(i[0])
        for i in cur.execute('select * from user'):
            row = row + 1
            if i[1] == '射爆了':
                print(row)
print(CNT)
print(len(a))