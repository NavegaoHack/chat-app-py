import sqlite3
import uuid

dbconnection = sqlite3.connect("chat-database.db")
dbcursor = dbconnection.cursor()

"""
dbcursor.execute(""
    CREATE TABLE users (
        id varchar(36),
        name TEXT,
        password TEXT,
        PRIMARY KEY(id)
    )
"")

# Creating Users

users = [
    (str(uuid.uuid1()), "manolo", "1234"),
    (str(uuid.uuid1()), "petra", "5678"),
    (str(uuid.uuid1()), "juan", "abcd"),
]

dbcursor.executemany("INSERT INTO users VALUES(?, ?, ?)", users)
dbconnection.commit()
"""
#consulting
for row in dbcursor.execute("SELECT * FROM users"):
    print(row)

#deleting the table
#dbcursor.execute("DROP TABLE users")
#dbconnection.commit()
dbconnection.close()

#print(len(str(uuid.uuid1())))
