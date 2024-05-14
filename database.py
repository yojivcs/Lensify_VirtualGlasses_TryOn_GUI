import sqlite3

conn = sqlite3.connect('glasses.db')
c = conn.cursor()

# Create the glasses table
c.execute('''CREATE TABLE glasses (
             id INTEGER PRIMARY KEY,
             path TEXT NOT NULL
         )''')

# Insert data into the glasses table
c.execute("INSERT INTO glasses (id, path) VALUES (1, 'E:\\MyProjects\\Lensify Try on Your Vision, Virtually\\Source Code\\Test Flight\\glasses.png')")
c.execute("INSERT INTO glasses (id, path) VALUES (2, 'E:\\MyProjects\\Lensify Try on Your Vision, Virtually\\Source Code\\Test Flight\\sunglasses.png')")

conn.commit()
conn.close()