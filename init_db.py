import sqlite3
import csv
flist= [tuple(row) for row in csv.reader(open('static/data/out.csv', 'rU'))]
connection = sqlite3.connect('database.db')


#with open('schema.sql') as f:
    #connection.executescript(f.read())
    
cur = connection.cursor()
print(flist)
for x in flist[1:]:

    cur.execute("INSERT INTO houses (id,CRIM,ZN,INDUS,CHAS,NOX,RM,AGE,DIS,RAD,TAX,PTRATION,B,LSTAT,MEDV) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                x)

connection.commit()
connection.close()