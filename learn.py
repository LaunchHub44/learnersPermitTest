#!/usr/bin/env python3

"""
Run this program in `terminology` for the best result.

inline image printing: `tycat <image-name>`
  - from:  https://askubuntu.com/questions/97542/how-do-i-make-my-terminal-display-graphical-pictures
  - `which tycat`  : /usr/bin/tycat

NOTE:  Debian useful tip:
  - dpkg -L <package-name>
  - dpkg -S <file-name>

"""

import sqlite3

questions = {}    # ( key=image-name,  value=rowid-of-answer )
answers = {}      # ( key=rowid,   value=( short, long) )

db = sqlite3.connect("questions.db")
cur = db.cursor()

cur.execute("select image, answer from question")
for row in cur.fetchall():
  questions[ row[0]] = row[1]

cur.execute("select rowid, short_desc, long_desc from choice")
for row in cur.fetchall():
  answers[row[0]] = (row[1], row[2])

## DEBUG TEST
print( questions["No-Left.png"], answers[6] )
print( answers[6][0], answers[6][1])
