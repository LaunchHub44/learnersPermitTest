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
import random
import os

questions = {}    # ( key=image-name,  value=rowid-of-answer )
answers = {}      # ( key=rowid,   value=( short, long) )

# access database, through db variable. 
# actually, db creates cur.  So, use cur variable to interact with DB.
db = sqlite3.connect("questions.db")
cur = db.cursor()

# We read all data into memory.
# question table will be loaded into `questions` dictionary.
cur.execute("select image, answer from question")
for row in cur.fetchall():
  questions[ row[0]] = row[1]

# choice table into `answers` dictionary.
cur.execute("select rowid, short_desc, long_desc from choice")
for row in cur.fetchall():
  answers[row[0]] = (row[1], row[2])

## DEBUG TEST
#print( questions["No-Left.png"], answers[6] )
#print( answers[6][0], answers[6][1])
#print(questions)

def make_question():
  # Let's make one question.
  qno = random.randint(0, len(questions))
  cur.execute("select image from question where rowid=?", (qno,))
  qimg_name = cur.fetchone()[0]

  # Select unique 4 wrong choices.
  # If answer is chosen, invalidate the selection, and try again.
  choices = []
  while len(choices) != 4:
    for i in range(4):
      choices.append(random.randint(0,len(answers))+1 )
    stest = set(choices)

    # If there was a duplicate choices selected, invalidate
    if len(stest) != len(choices):
      choices = []

    # If 4 wrong choices contain the answer, invalidate
    if questions[qimg_name] in choices:
      choices = []

  # And then, add the right choice.
  choices.append(questions[qimg_name])
  random.shuffle(choices)
  correct_answer = 0
  for i in range(5):
    if choices[i] == questions[qimg_name]:
      correct_answer = i+1

  # Present the question:
  cmd = "/usr/bin/tycat image/" + qimg_name
  os.system(cmd)

  for i in range(len(choices)):
    print(f"{i+1}) {answers[choices[i]][0] }")
    print("")

  # The answer will be returned (1-5)
  return correct_answer 


# Real game starts here
score =0
for i in range(10):
  ans = make_question()
  user = input(f"Question {i+1}. Choose: ")
  if int(user) == ans:
    print("CORRECT!")
    print("")
    score += 1
  else:
    print(f"Incorrect...  Answer is {ans}.")

print(f"You got {score} out of 10 correct.")
if score == 10:
  print("You are ready!")
else:
  print("You are not ready yet.")