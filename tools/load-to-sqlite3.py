#!/usr/bin/env python3

import sqlite3
import os

# Check database file
dbname = "questions.db"
if os.path.exists(dbname):
    os.unlink(dbname)         # delete file.

db = sqlite3.connect(dbname)
db.execute('''create table question(
   image  text,
   answer  fk_choice
)''')
db.execute('''create table choice(
   short_desc  text,
   long_desc   text
)''')

# We will store sign data here.
data = []
lastChoiceIdx = 0
cur = db.cursor()

# load file description we typed into data list.
fh = open("../sign-mapping-singleline.txt")
cnt = 0
for line in fh:
    l = line.strip()
    if len(l) == 0:
        continue

    tokens = l.split('|')
    img = tokens[0]
    shortDesc = tokens[1].strip()
    longDesc  = tokens[2].strip()

    if shortDesc != '"':
        cur.execute('insert into choice values(?,?)', (shortDesc, longDesc))
        lastChoiceIdx = cur.lastrowid

    cur.execute('insert into question values(?,?)', (img, lastChoiceIdx))
    cnt += 1

print(f"{cnt} rows inserted.")
fh.close()
db.commit()
db.close()
