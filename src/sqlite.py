import sqlite3
import random

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('STUDENT.db')
cursor = conn.cursor()

# Create the STUDENT table
cursor.execute('''
CREATE TABLE IF NOT EXISTS STUDENT (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    grade TEXT NOT NULL,
    marks INTEGER NOT NULL
)
''')

# Sample data for random generation
names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Hank', 'Ivy', 'Jack']
departments = ['CS', 'Math', 'Physics', 'Chemistry', 'Biology']
grades = ['A', 'B', 'C', 'D', 'F']

# Insert 10 random records
for _ in range(10):
    name = random.choice(names)
    department = random.choice(departments)
    grade = random.choice(grades)
    marks = random.randint(50, 100)  # Random marks between 50 and 100
    cursor.execute('INSERT INTO STUDENT (name, department, grade, marks) VALUES (?, ?, ?, ?)',
                   (name, department, grade, marks))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database created and 10 random records inserted successfully.")

