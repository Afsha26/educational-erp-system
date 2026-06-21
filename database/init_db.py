import sqlite3

# ==========================
# Database Connection
# ==========================

conn = sqlite3.connect("database/erp.db")

# Enable Foreign Keys
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

# ==========================
# Users Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# ==========================
# Students Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    roll_no TEXT UNIQUE,
    full_name TEXT NOT NULL,
    department TEXT,
    semester INTEGER,
    division TEXT,
    email TEXT,

    FOREIGN KEY(user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
)
""")

# ==========================
# Teachers Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers(
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    full_name TEXT NOT NULL,
    department TEXT,
    designation TEXT,
    email TEXT,

    FOREIGN KEY(user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
)
""")

# ==========================
# Subjects Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects(
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT NOT NULL,
    department TEXT,
    semester INTEGER,
    teacher_id INTEGER,
    completion_percentage INTEGER DEFAULT 0,

    FOREIGN KEY(teacher_id)
        REFERENCES teachers(teacher_id)
        ON DELETE SET NULL
)
""")

# ==========================
# Lectures Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS lectures(
    lecture_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    lecture_date TEXT NOT NULL,

    FOREIGN KEY(subject_id)
        REFERENCES subjects(subject_id)
        ON DELETE CASCADE,

    FOREIGN KEY(teacher_id)
        REFERENCES teachers(teacher_id)
        ON DELETE CASCADE
)
""")

# ==========================
# Attendance Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lecture_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    status TEXT NOT NULL,

    FOREIGN KEY(lecture_id)
        REFERENCES lectures(lecture_id)
        ON DELETE CASCADE,

    FOREIGN KEY(student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE
)
""")

# ==========================
# Announcements Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS announcements(
    announcement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    announcement_date TEXT NOT NULL,
    created_by INTEGER,
    creator_role TEXT
)
""")

# ==========================
# Student Queries Table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS student_queries(
    query_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    query_message TEXT NOT NULL,
    teacher_reply TEXT,
    created_at TEXT NOT NULL,

    FOREIGN KEY(student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE
)
""")


# ==========================
# HOD table
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS hods(
    hod_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    full_name TEXT NOT NULL,
    department TEXT,
    email TEXT,

    FOREIGN KEY(user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
)
               """)

# ==========================
# Commit Changes
# ==========================

conn.commit()
conn.close()

print("ERP Database Created Successfully")