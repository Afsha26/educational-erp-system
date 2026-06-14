from database.db import get_connection

def authenticate(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    # ==========================
    # Verify Login
    # ==========================

    cursor.execute("""
        SELECT user_id, username, role
        FROM users
        WHERE username = ?
        AND password = ?
    """, (username, password))

    user = cursor.fetchone()

    if not user:
        conn.close()
        return None

    user_id = user["user_id"]
    role = user["role"]

    result = {
        "user_id": user["user_id"],
        "username": user["username"],
        "role": role
    }

    # ==========================
    # Student Login
    # ==========================

    if role == "Student":

        cursor.execute("""
            SELECT student_id, full_name, roll_no
            FROM students
            WHERE user_id = ?
        """, (user_id,))

        student = cursor.fetchone()

        if student:

            result["student_id"] = student["student_id"]
            result["full_name"] = student["full_name"]
            result["roll_no"] = student["roll_no"]

    elif role == "Teacher":

        cursor.execute("""
                SELECT
                    teacher_id,
                    full_name,
                    department,
                    designation,
                    email
                FROM teachers
                WHERE user_id = ?
            """, (user_id,))

        teacher = cursor.fetchone()

        if teacher:

            result["teacher_id"] = teacher["teacher_id"]
            result["full_name"] = teacher["full_name"]
            result["department"] = teacher["department"]
            result["designation"] = teacher["designation"]
            result["email"] = teacher["email"]
    else:
        pass
    conn.close()

    return result