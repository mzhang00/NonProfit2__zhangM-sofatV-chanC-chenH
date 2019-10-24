#Hong Wei Chen and Michael Zhang (Team Nonprofit)
#SoftDev pd1
#K18 -- Average
#Oct 10 2019

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
import sys

DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

command = "CREATE TABLE IF NOT EXISTS Students (name TEXT, age INTEGER, id INTEGER);" # test SQL stmt in sqlite3 shell, save as string
c.execute(command)
with open('students.csv') as student:
     reader = csv.DictReader(student)
     for row in reader:
         command = "insert into Students (name, age, id) values ('" + row['name'] + "', " + str(row['age']) + ", " + str(row['id']) + ");"
         c.execute(command)
         #print(command)
 # test SQL stmt in sqlite3 shell, save as string
command =  "CREATE TABLE IF NOT EXISTS Courses (code TEXT, mark INTEGER, id INTEGER);"
c.execute(command)
with open('courses.csv') as course:
     reader = csv.DictReader(course)
     for row in reader:
         command = "insert into Courses (code, mark, id) values ('" + row['code'] + "', " + str(row['mark']) + ", " + str(row['id']) + ");"
         c.execute(command)
         #print(command)

def lookUpGrades(myid):
    q = "SELECT code, mark FROM courses WHERE id =" + str(myid) + ";"
    foo = c.execute(q)
    return foo.fetchall()

def average(myid):
    grades = lookUpGrades(myid)
    total = 0
    counter = 0
    for course in grades:
        total += course[1]
        counter += 1
    return total/counter

command = "CREATE TABLE IF NOT EXISTS stu_avg (id INTEGER, average INTEGER);" # test SQL stmt in sqlite3 shell, save as string
c.execute(command)
for i in range(10):
    command = "insert into stu_avg (id, average) values (" + str(i + 1) + ", " + str(average(i + 1)) + ");"
    c.execute(command)

def addRow(code, mark, id):
    command = "insert into Courses (code, mark, id) values ('" + code + "', " + str(mark) + ", " + str(id) + ");"
    c.execute(command)

#Search Function to find a page
def searchBlog(query):
    q = "SELECT average FROM stu_avg WHERE id =" + str(query) + ";"
    foo = c.execute(q)
    return str(foo.fetchall()[0])[1:-2]

#print(sys.argv[1])
print(searchBlog(sys.argv[1]))

#==========================================================

db.commit() #save changes
db.close()

# q = "SELECT name, students.id, mark FROM students, courses WHERE students.id = courses.id;"
# foo = c.execute(q)
# print (foo)
