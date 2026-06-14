import sqlite3

conn = sqlite3.connect("database/erp.db")
cursor = conn.cursor()

# ==========================
# Student Master Data
# ==========================

students = [
    ('CE101', 'Afsha Shaikh', 'Computer', 4, 'A', 'afsha@gmail.com'),
    ('CE102', 'Ayesha Khan', 'Computer', 4, 'A', 'ayesha@gmail.com'),
    ('CE103', 'Mohammed Ali', 'Computer', 4, 'A', 'mohammed@gmail.com'),
    ('CE104', 'Sara Ansari', 'Computer', 4, 'A', 'sara@gmail.com'),
    ('CE105', 'Zain Shaikh', 'Computer', 4, 'A', 'zain@gmail.com'),
    ('CE106', 'Fatima Patel', 'Computer', 4, 'A', 'fatima@gmail.com'),
    ('CE107', 'Rahul Sharma', 'Computer', 4, 'A', 'rahul@gmail.com'),
    ('CE108', 'Priya Verma', 'Computer', 4, 'A', 'priya@gmail.com'),
    ('CE109', 'Arjun Singh', 'Computer', 4, 'A', 'arjun@gmail.com'),
    ('CE110', 'Sneha Joshi', 'Computer', 4, 'A', 'sneha@gmail.com'),
    ('CE111', 'Rohan Deshmukh', 'Computer', 4, 'A', 'rohan@gmail.com'),
    ('CE112', 'Neha Gupta', 'Computer', 4, 'A', 'neha@gmail.com'),
    ('CE113', 'Imran Sheikh', 'Computer', 4, 'A', 'imran@gmail.com'),
    ('CE114', 'Pooja Nair', 'Computer', 4, 'A', 'pooja@gmail.com'),
    ('CE115', 'Karan Mehta', 'Computer', 4, 'A', 'karan@gmail.com')
]

# ==========================
# Create Student Users
# ==========================

for student in students:

    roll_no = student[0]
    full_name = student[1]
    department = student[2]
    semester = student[3]
    division = student[4]
    email = student[5]

    username = roll_no.lower()


    # Create Login Account
    cursor.execute("""
    INSERT INTO users(username, password, role)
    VALUES (?, ?, ?)
    """, (username, "123", "Student"))

    user_id = cursor.lastrowid

    # Create Student Profile
    cursor.execute("""
    INSERT INTO students
    (user_id, roll_no, full_name, department, semester, division, email)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        user_id,
        roll_no,
        full_name,
        department,
        semester,
        division,
        email
    ))

# ==========================
# Teacher Users
# ==========================

teacher_accounts = [
    ("teacher1", "123", "Teacher"),
    ("teacher2", "123", "Teacher"),
    ("teacher3", "123", "Teacher"),
    ("teacher4", "123", "Teacher")
]

teacher_ids = []

for username, password, role in teacher_accounts:

    cursor.execute("""
    INSERT INTO users(username,password,role)
    VALUES(?,?,?)
    """, (username, password, role))

    teacher_ids.append(cursor.lastrowid)
# ==========================
# Teacher Profiles
# ==========================

teachers = [
    (
        teacher_ids[0],
        "Dr. Shahid Khan",
        "Computer",
        "Assistant Professor",
        "shahid.khan@college.edu"
    ),
    (
        teacher_ids[1],
        "Prof. Meera Patil",
        "Computer",
        "Associate Professor",
        "meera.patil@college.edu"
    ),
    (
        teacher_ids[2],
        "Dr. Rajesh Sharma",
        "Computer",
        "Assistant Professor",
        "rajesh.sharma@college.edu"
    ),
    (
        teacher_ids[3],
        "Prof. Snehal Joshi",
        "Computer",
        "Professor",
        "snehal.joshi@college.edu"
    )
]

cursor.executemany("""
INSERT INTO teachers
(user_id,full_name,department,designation,email)
VALUES(?,?,?,?,?)
""", teachers)

# ==========================
# HOD User
# ==========================

cursor.execute("""
INSERT INTO users(username, password, role)
VALUES (?, ?, ?)
""", ("hod1", "123", "HOD"))

# ==========================
# Principal User
# ==========================

cursor.execute("""
INSERT INTO users(username, password, role)
VALUES (?, ?, ?)
""", ("principal1", "123", "Principal"))


# ==========================
# Subject Assignments
# ==========================


subjects = [

    ("Database Management System", "Computer", 4, 1, 85),
    ("Operating System", "Computer", 4, 1, 78),
    ("Computer Networks", "Computer", 4, 2, 72),
    ("Software Engineering", "Computer", 4, 2, 90),

    ("Java Programming", "Computer", 3, 3, 88),
    ("Python Programming", "Computer", 3, 3, 80),
    ("Data Structures", "Computer", 3, 1, 95),
    ("Discrete Mathematics", "Computer", 3, 4, 70),

    ("Artificial Intelligence", "Computer", 6, 4, 60),
    ("Machine Learning", "Computer", 6, 4, 55),
    ("Cloud Computing", "Computer", 6, 2, 65),
    ("Cyber Security", "Computer", 6, 4, 75),

    ("Web Technology", "Computer", 5, 3, 82),
    ("Mobile Application Development", "Computer", 5, 3, 68),
    ("Internet of Things", "Computer", 5, 4, 50),
    ("Big Data Analytics", "Computer", 5, 4, 45),

    ("Computer Graphics", "Computer", 4, 2, 77),
    ("Compiler Design", "Computer", 6, 1, 58),
    ("Theory of Computation", "Computer", 5, 4, 73),
    ("Project Management", "Computer", 7, 2, 40)

]
cursor.executemany("""
INSERT INTO subjects
(
    subject_name,
    department,
    semester,
    teacher_id,
    completion_percentage
)
VALUES (?,?,?,?,?)
""", subjects)

# ==========================
# Lectures
# ==========================

cursor.execute("""
SELECT
    subject_id,
    teacher_id
FROM subjects
""")

subject_records = cursor.fetchall()

lectures = []

lecture_dates = [
    "2026-01-10",
    "2026-02-15",
    "2026-03-20"
]

for subject_id, teacher_id in subject_records:

    for lecture_date in lecture_dates:

        lectures.append(
            (
                subject_id,
                teacher_id,
                lecture_date
            )
        )

cursor.executemany("""
INSERT INTO lectures
(
    subject_id,
    teacher_id,
    lecture_date
)
VALUES (?,?,?)
""", lectures)
# ==========================
# Attendance Records
# ==========================

cursor.execute("""
SELECT lecture_id
FROM lectures
""")

lecture_ids = [
    row[0]
    for row in cursor.fetchall()
]

cursor.execute("""
SELECT student_id
FROM students
""")

student_ids = [
    row[0]
    for row in cursor.fetchall()
]

attendance_records = []

for lecture_id in lecture_ids:

    for student_id in student_ids:

        status = (
            "Absent"
            if student_id % 5 == 0
            else "Present"
        )

        attendance_records.append(
            (
                lecture_id,
                student_id,
                status
            )
        )

cursor.executemany("""
INSERT INTO attendance
(
    lecture_id,
    student_id,
    status
)
VALUES (?,?,?)
""", attendance_records)

conn.commit()
conn.close()


print("Seed Data Inserted Successfully")