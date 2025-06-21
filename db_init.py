
import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS donors (
    donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    blood_group TEXT,
    phone TEXT,
    last_donation DATE
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS blood_stock (
    blood_group TEXT PRIMARY KEY,
    units INTEGER
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_name TEXT,
    blood_group TEXT,
    units_required INTEGER,
    request_date DATE,
    status TEXT
)
''')

# Initialize blood stock (optional)
groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
for group in groups:
    cur.execute("INSERT OR IGNORE INTO blood_stock (blood_group, units) VALUES (?, ?)", (group, 0))

conn.commit()
conn.close()
print("Tables created successfully.")
