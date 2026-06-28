import random
import sqlite3
from datetime import date, timedelta

random.seed(42)

conn = sqlite3.connect("database/erp.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

# ==========================
# CLEAR EXISTING SAMPLE DATA
# ==========================

cursor.execute("DELETE FROM attendance")
cursor.execute("DELETE FROM lectures")
cursor.execute("DELETE FROM student_queries")
cursor.execute("DELETE FROM announcements")
cursor.execute("DELETE FROM subjects")
cursor.execute("DELETE FROM principals")
cursor.execute("DELETE FROM hods")
cursor.execute("DELETE FROM teachers")
cursor.execute("DELETE FROM students")
cursor.execute("DELETE FROM users")
conn.commit()

# ==========================
# CONFIGURATION
# ==========================

departments = [
    "Computer",
    "Information Technology",
    "Electronics",
    "Mechanical",
    "Civil",
]

semesters = list(range(1, 9))

prefix_map = {
    "Computer": "CE",
    "Information Technology": "IT",
    "Electronics": "EC",
    "Mechanical": "ME",
    "Civil": "CV",
}

first_names = [
    "Aarav", "Aditi", "Akash", "Amita", "Ananya", "Aniket", "Arjun", "Ayush", "Bhavya",
    "Chetan", "Deepak", "Dev", "Dhruv", "Divya", "Harsh", "Ishaan", "Kavya", "Khushi",
    "Kiran", "Lakshmi", "Mansi", "Meera", "Mohit", "Neha", "Nikhil", "Nisha", "Pooja",
    "Pranav", "Priya", "Rahul", "Riya", "Rohan", "Sagar", "Sakshi", "Sana", "Shivam",
    "Shruti", "Sneha", "Sonia", "Tanvi", "Tejas", "Vansh", "Varun", "Vikram", "Yash",
]

last_names = [
    "Agarwal", "Bhatia", "Chopra", "Deshmukh", "Gupta", "Jain", "Joshi", "Kapoor", "Khan",
    "Kulkarni", "Malhotra", "Mehta", "Nair", "Pandey", "Patel", "Rao", "Sharma", "Singh",
    "Soni", "Tiwari", "Verma", "Yadav", "Zope",
]

teacher_designations = [
    "Assistant Professor",
    "Assistant Professor",
    "Associate Professor",
    "Professor",
]

subject_pool = [
    "Data Structures",
    "Operating System",
    "Database Management System",
    "Computer Networks",
    "Software Engineering",
    "Digital Electronics",
    "Microprocessors",
    "Signal Processing",
    "Thermodynamics",
    "Fluid Mechanics",
    "Strength of Materials",
    "Surveying",
    "Concrete Technology",
    "Geotechnical Engineering",
    "Hydraulics",
    "Machine Learning",
    "Compiler Design",
    "Embedded Systems",
    "Artificial Intelligence",
    "Web Technologies",
    "Mobile Application Development",
    "Cloud Computing",
    "Cyber Security",
    "Power Systems",
]

# ==========================
# PRINCIPAL
# ==========================

principal_user = ("principal1", "123", "Principal")
cursor.execute("INSERT INTO users(username, password, role) VALUES (?, ?, ?)", principal_user)
principal_user_id = cursor.lastrowid
cursor.execute(
    "INSERT INTO principals(user_id, full_name, email) VALUES (?, ?, ?)",
    (principal_user_id, "Dr. Anil Rao", "anil.rao@college.edu"),
)

# ==========================
# HODS
# ==========================

hod_records = []
hod_user_records = []
for department in departments:
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    username = f"hod_{department.lower().replace(' ', '_')}_{len(hod_user_records) + 1}"
    password = "123"
    hod_user_records.append((username, password, "HOD"))
    hod_records.append(
        (
            None,
            f"Dr. {first_name} {last_name}",
            department,
            f"{first_name.lower()}.{last_name.lower()}@college.edu",
        )
    )

for username, password, role in hod_user_records:
    cursor.execute("INSERT INTO users(username, password, role) VALUES (?, ?, ?)", (username, password, role))

hod_user_ids = [row[0] for row in cursor.execute("SELECT user_id FROM users WHERE role = 'HOD' ORDER BY user_id")]
for user_id, record in zip(hod_user_ids, hod_records):
    cursor.execute(
        "INSERT INTO hods(user_id, full_name, department, email) VALUES (?, ?, ?, ?)",
        (user_id, record[1], record[2], record[3]),
    )

# ==========================
# TEACHERS
# ==========================

teacher_user_records = []
teacher_records = []
for department in departments:
    for designation in teacher_designations:
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        username = f"t_{department.lower().replace(' ', '_')}_{len(teacher_user_records) + 1}"
        teacher_user_records.append((username, "123", "Teacher"))
        teacher_records.append(
            (
                None,
                f"{first_name} {last_name}",
                department,
                designation,
                f"{first_name.lower()}.{last_name.lower()}@college.edu",
            )
        )

for username, password, role in teacher_user_records:
    cursor.execute("INSERT INTO users(username, password, role) VALUES (?, ?, ?)", (username, password, role))

teacher_user_ids = [row[0] for row in cursor.execute("SELECT user_id FROM users WHERE role = 'Teacher' ORDER BY user_id")]
for user_id, record in zip(teacher_user_ids, teacher_records):
    cursor.execute(
        "INSERT INTO teachers(user_id, full_name, department, designation, email) VALUES (?, ?, ?, ?, ?)",
        (user_id, record[1], record[2], record[3], record[4]),
    )

# ==========================
# STUDENTS
# ==========================

student_records = []
student_user_records = []
student_counter = 1
for department in departments:
    for semester in semesters:
        for index in range(10):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            roll_no = f"{prefix_map[department]}{semester}{index + 1:02d}"
            division = random.choice(["A", "B"])
            username = f"s_{roll_no.lower()}"
            student_user_records.append((username, "123", "Student"))
            student_records.append(
                (
                    None,
                    roll_no,
                    f"{first_name} {last_name}",
                    department,
                    semester,
                    division,
                    f"{first_name.lower()}.{last_name.lower()}@college.edu",
                )
            )
            student_counter += 1

for username, password, role in student_user_records:
    cursor.execute("INSERT INTO users(username, password, role) VALUES (?, ?, ?)", (username, password, role))

student_user_ids = [row[0] for row in cursor.execute("SELECT user_id FROM users WHERE role = 'Student' ORDER BY user_id")]
for user_id, record in zip(student_user_ids, student_records):
    cursor.execute(
        "INSERT INTO students(user_id, roll_no, full_name, department, semester, division, email) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, record[1], record[2], record[3], record[4], record[5], record[6]),
    )

# ==========================
# SUBJECTS
# ==========================

subject_records = []
for department in departments:
    for semester in semesters:
        selected_subjects = random.sample(subject_pool, 5)
        for subject_name in selected_subjects:
            teacher_ids_for_department = [
                row[0]
                for row in cursor.execute(
                    "SELECT teacher_id FROM teachers WHERE department = ?",
                    (department,),
                )
            ]
            teacher_id = random.choice(teacher_ids_for_department)
            completion_percentage = random.randint(20, 95)
            subject_records.append((subject_name, department, semester, teacher_id, completion_percentage))

cursor.executemany(
    """
    INSERT INTO subjects(subject_name, department, semester, teacher_id, completion_percentage)
    VALUES (?, ?, ?, ?, ?)
    """,
    subject_records,
)

# ==========================
# LECTURES
# ==========================

subject_rows = cursor.execute("SELECT subject_id, teacher_id FROM subjects ORDER BY subject_id").fetchall()
lecture_records = []
start_date = date(2026, 1, 1)
end_date = date(2026, 6, 30)
for subject_id, teacher_id in subject_rows:
    for _ in range(15):
        random_day = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        lecture_records.append((subject_id, teacher_id, random_day.strftime("%Y-%m-%d")))

cursor.executemany("INSERT INTO lectures(subject_id, teacher_id, lecture_date) VALUES (?, ?, ?)", lecture_records)

# ==========================
# ATTENDANCE
# ==========================

lecture_rows = cursor.execute("SELECT lecture_id, subject_id FROM lectures ORDER BY lecture_id").fetchall()
for lecture_id, subject_id in lecture_rows:
    subject_row = cursor.execute("SELECT department, semester FROM subjects WHERE subject_id = ?", (subject_id,)).fetchone()
    if not subject_row:
        continue
    subject_department, subject_semester = subject_row
    student_rows = cursor.execute(
        "SELECT student_id FROM students WHERE department = ? AND semester = ?",
        (subject_department, subject_semester),
    ).fetchall()
    attendance_records = []
    for (student_id,) in student_rows:
        status = "Present" if random.random() < 0.85 else "Absent"
        attendance_records.append((lecture_id, student_id, status))
    cursor.executemany("INSERT INTO attendance(lecture_id, student_id, status) VALUES (?, ?, ?)", attendance_records)

# ==========================
# ANNOUNCEMENTS
# ==========================

announcement_records = []
principal_user_id = cursor.execute("SELECT user_id FROM users WHERE role = 'Principal' LIMIT 1").fetchone()[0]
hod_user_ids = [row[0] for row in cursor.execute("SELECT user_id FROM users WHERE role = 'HOD' ORDER BY user_id")]
announcement_dates = [
    "2026-01-05",
    "2026-01-20",
    "2026-02-08",
    "2026-02-18",
    "2026-03-04",
    "2026-03-15",
    "2026-03-28",
    "2026-04-10",
    "2026-04-22",
    "2026-05-02",
    "2026-05-15",
    "2026-05-27",
    "2026-06-03",
    "2026-06-12",
    "2026-06-20",
]
for index in range(20):
    created_by = principal_user_id if index % 2 == 0 else random.choice(hod_user_ids)
    creator_role = "Principal" if index % 2 == 0 else "HOD"
    announcement_records.append(
        (
            f"Announcement {index + 1}",
            f"{creator_role} update for the campus academic schedule.",
            announcement_dates[index % len(announcement_dates)],
            created_by,
            creator_role,
        )
    )

cursor.executemany(
    """
    INSERT INTO announcements(title, message, announcement_date, created_by, creator_role)
    VALUES (?, ?, ?, ?, ?)
    """,
    announcement_records,
)

# ==========================
# STUDENT QUERIES
# ==========================

student_ids = [row[0] for row in cursor.execute("SELECT student_id FROM students ORDER BY student_id")]
teacher_ids = [row[0] for row in cursor.execute("SELECT teacher_id FROM teachers ORDER BY teacher_id")]
query_records = []
for index in range(40):
    student_id = random.choice(student_ids)
    message = f"Query {index + 1}: I need guidance regarding the current academic schedule and assessment plan."
    if index < 20:
        query_records.append((student_id, message, None, random.choice(student_ids) if False else None))
    else:
        reply = f"Teacher response to query {index + 1}: Please attend the next mentoring session."
        query_records.append((student_id, message, reply, None))

# The schema expects created_at, so we insert with a date value.
query_values = []
for index, (student_id, message, reply, _) in enumerate(query_records):
    created_at = date(2026, 1, 1) + timedelta(days=index)
    query_values.append((student_id, message, reply, created_at.strftime("%Y-%m-%d")))

cursor.executemany(
    """
    INSERT INTO student_queries(student_id, query_message, teacher_reply, created_at)
    VALUES (?, ?, ?, ?)
    """,
    query_values,
)

conn.commit()
conn.close()

print("Balanced sample data inserted successfully")