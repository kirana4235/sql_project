import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    marks INTEGER
)
""")

cursor.execute("DELETE FROM students")

cursor.executemany(
    "INSERT INTO students (name, marks) VALUES (?, ?)",
    [
        ("Stalin", 85),
        ("Ravi", 78),
        ("Anil", 90),
        ("Kiran", 72)
    ]
)

conn.commit()
conn.close()

print("Database created successfully")