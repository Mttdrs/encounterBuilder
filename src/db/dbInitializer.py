import sqlite3
import dbConst


conn = sqlite3.connect(dbConst.dbPath)
cur = conn.cursor()

with open("db/initDB.sql") as file:
    sql_script = file.read()

cur.executescript(sql_script)

conn.commit()

cur.close()
conn.close()