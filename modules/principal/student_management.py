import sqlite3
import pandas as pd
import streamlit as st
from io import BytesIO
import plotly.express as px


# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = sqlite3.connect(
    "database/erp.db",
    check_same_thread=False
)

conn.execute("PRAGMA foreign_keys = ON")


# =====================================================
# STUDENT MANAGEMENT
# =====================================================

def student_management():

    cursor = conn.cursor()

    # =====================================================
    # CSS
    # =====================================================

    st.markdown("""
    <style>

    .stButton>button{
        background:linear-gradient(135deg,#6D28D9,#8B5CF6);
        color:white;
        border:none;
        border-radius:10px;
        font-weight:600;
    }

    .stButton>button:hover{
        background:linear-gradient(135deg,#5B21B6,#7C3AED);
        color:white;
    }

    div[data-testid="metric-container"]{
        border-radius:15px;
        border:1px solid #E5E7EB;
        padding:15px;
        box-shadow:0 3px 10px rgba(0,0,0,.08);
    }

    </style>
    """, unsafe_allow_html=True)

    # =====================================================
    # HEADER
    # =====================================================

    st.html("""
    <div style="
        background:linear-gradient(135deg,#4F46E5,#7C3AED);
        padding:25px;
        border-radius:15px;
        color:white;
        margin-bottom:20px;
    ">

    <h2>👨‍🎓 Student Management</h2>

    <p>
    Manage student records, update information,
    search students and maintain academic data.
    </p>

    </div>
    """)

    # =====================================================
    # KPI CARDS
    # =====================================================

    total_students = cursor.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    total_departments = cursor.execute(
        """
        SELECT COUNT(DISTINCT department)
        FROM students
        """
    ).fetchone()[0]

    total_semesters = cursor.execute(
        """
        SELECT COUNT(DISTINCT semester)
        FROM students
        """
    ).fetchone()[0]

    total_divisions = cursor.execute(
        """
        SELECT COUNT(DISTINCT division)
        FROM students
        """
    ).fetchone()[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Students",
        total_students
    )

    c2.metric(
        "Departments",
        total_departments
    )

    c3.metric(
        "Semesters",
        total_semesters
    )

    c4.metric(
        "Divisions",
        total_divisions
    )

    st.divider()

    # =====================================================
    # STUDENT ANALYTICS
    # =====================================================

    analytics_col1, analytics_col2 = st.columns(2)

    with analytics_col1:

        male_division = cursor.execute(
            """
            SELECT COUNT(*)
            FROM students
            WHERE division='A'
            """
        ).fetchone()[0]

        female_division = cursor.execute(
            """
            SELECT COUNT(*)
            FROM students
            WHERE division='B'
            """
        ).fetchone()[0]

        st.info(
            f"""
    ### Quick Statistics

    👨‍🎓 Total Students : **{total_students}**

    🏫 Departments : **{total_departments}**

    📚 Semesters : **{total_semesters}**

    🏛 Divisions : **{total_divisions}**
    """
        )

    with analytics_col2:

        st.success(
            """
    ### Principal Dashboard

    ✔ Add Students

    ✔ Update Student Details

    ✔ Delete Student Records

    ✔ Export Student List

    ✔ Search & Filter Students
    """
        )

    # =====================================================
    # SEARCH & FILTERS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        search = st.text_input(
            "🔍 Search Student"
        )

    with col2:

        department = st.selectbox(

            "Department",

            ["All"] +

            list(pd.read_sql_query(
                """
                SELECT DISTINCT department
                FROM students
                ORDER BY department
                """,
                conn
            )["department"])

        )

    with col3:

        semester = st.selectbox(

            "Semester",

            ["All"] +

            list(pd.read_sql_query(
                """
                SELECT DISTINCT semester
                FROM students
                ORDER BY semester
                """,
                conn
            )["semester"])

        )

    with col4:

        division = st.selectbox(

            "Division",

            ["All"] +

            list(pd.read_sql_query(
                """
                SELECT DISTINCT division
                FROM students
                ORDER BY division
                """,
                conn
            )["division"])

        )

    st.divider()

    # =====================================================
    # LOAD STUDENTS
    # =====================================================

    query = """

    SELECT

        s.student_id,

        u.user_id,

        u.username,

        s.roll_no,

        s.full_name,

        s.department,

        s.semester,

        s.division,

        s.email

    FROM students s

    JOIN users u

    ON s.user_id=u.user_id

    WHERE 1=1

    """

    params = []

    if department != "All":

        query += " AND s.department=?"

        params.append(department)

    if semester != "All":

        query += " AND s.semester=?"

        params.append(semester)

    if division != "All":

        query += " AND s.division=?"

        params.append(division)

    students = pd.read_sql_query(
        query,
        conn,
        params=params
    )

    # =====================================================
    # SEARCH
    # =====================================================

    if search:

        students = students[

            students["roll_no"]

            .str.contains(
                search,
                case=False
            )

            |

            students["full_name"]

            .str.contains(
                search,
                case=False
            )

            |

            students["username"]

            .str.contains(
                search,
                case=False
            )

        ]

    # =====================================================
    # ACTION BUTTONS
    # =====================================================

    b1, b2 = st.columns([1,6])

    with b1:

        # =====================================================
        # ADD STUDENT
        # =====================================================
        add_student = st.button("➕ Add Student")
        if add_student:

            @st.dialog("➕ Add New Student", width="large")
            def add_student_dialog():

                st.subheader("Student Information")

                col1, col2 = st.columns(2)

                with col1:

                    username = st.text_input("Username")

                    password = st.text_input(
                        "Password",
                        type="password"
                    )

                    roll_no = st.text_input(
                        "Roll Number"
                    )

                    full_name = st.text_input(
                        "Full Name"
                    )

                with col2:

                    department = st.selectbox(
                        "Department",
                        [
                            "Computer",
                            "Information Technology",
                            "Electronics",
                            "Mechanical",
                            "Civil"
                        ]
                    )

                    semester = st.selectbox(
                        "Semester",
                        list(range(1,9))
                    )

                    division = st.selectbox(
                        "Division",
                        [
                            "A",
                            "B"
                        ]
                    )

                    email = st.text_input(
                        "Email"
                    )

                st.divider()

                c1, c2 = st.columns(2)

                save = c1.button(
                    "💾 Save Student",
                    use_container_width=True,
                    type="primary"
                )

                cancel = c2.button(
                    "❌ Cancel",
                    use_container_width=True
                )

                if cancel:
                    st.rerun()

                if save:

                    # =====================================
                    # VALIDATION
                    # =====================================

                    if (
                        username == ""
                        or password == ""
                        or roll_no == ""
                        or full_name == ""
                        or email == ""
                    ):

                        st.error(
                            "Please fill all fields."
                        )

                        return

                    cursor = conn.cursor()

                    # Username exists?

                    cursor.execute(

                        """
                        SELECT 1
                        FROM users
                        WHERE username=?
                        """,

                        (username,)

                    )

                    if cursor.fetchone():

                        st.error(
                            "Username already exists."
                        )

                        return

                    # Roll exists?

                    cursor.execute(

                        """
                        SELECT 1
                        FROM students
                        WHERE roll_no=?
                        """,

                        (roll_no,)

                    )

                    if cursor.fetchone():

                        st.error(
                            "Roll Number already exists."
                        )

                        return

                    # =====================================
                    # INSERT USER
                    # =====================================

                    cursor.execute(

                        """
                        INSERT INTO users(

                            username,

                            password,

                            role

                        )

                        VALUES(?,?,?)

                        """,

                        (

                            username,

                            password,

                            "Student"

                        )

                    )

                    user_id = cursor.lastrowid

                    # =====================================
                    # INSERT STUDENT
                    # =====================================

                    cursor.execute(

                        """
                        INSERT INTO students(

                            user_id,

                            roll_no,

                            full_name,

                            department,

                            semester,

                            division,

                            email

                        )

                        VALUES(

                            ?,?,?,?,?,?,?

                        )

                        """,

                        (

                            user_id,

                            roll_no,

                            full_name,

                            department,

                            semester,

                            division,

                            email

                        )

                    )

                    conn.commit()

                    st.success(
                        "Student added successfully."
                    )

                    st.balloons()

                    st.rerun()

            add_student_dialog()

    with b2:

        refresh = st.button(
            "🔄 Refresh",
            use_container_width=True
        )

    if refresh:
        st.rerun()

    st.divider()

    # =====================================================
    # STUDENT RECORDS
    # =====================================================

    st.subheader("📋 Student Records")

    st.dataframe(
        students.drop(columns=["user_id"]),
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    selected_student = st.selectbox(
        "Select Student",
        students["roll_no"] + " - " + students["full_name"]
    )

    selected_row = students[
        (students["roll_no"] + " - " + students["full_name"])
        == selected_student
    ].iloc[0]

    col1, col2 = st.columns(2)

    edit_student = col1.button(
        "✏️ Edit Student",
        use_container_width=True
    )

    delete_student = col2.button(
        "🗑 Delete Student",
        use_container_width=True
    )
    if students.empty:

        st.info(
        "No students available."
        )

        return
    # =====================================================
    # EDIT STUDENT
    # =====================================================
    
    if edit_student:

        @st.dialog("✏️ Edit Student", width="large")
        def edit_dialog():

            username = st.text_input(
                "Username",
                value=selected_row["username"]
            )

            roll_no = st.text_input(
                "Roll Number",
                value=selected_row["roll_no"]
            )

            full_name = st.text_input(
                "Full Name",
                value=selected_row["full_name"]
            )

            department = st.selectbox(
                "Department",
                [
                    "Computer",
                    "Information Technology",
                    "Electronics",
                    "Mechanical",
                    "Civil"
                ],
                index=[
                    "Computer",
                    "Information Technology",
                    "Electronics",
                    "Mechanical",
                    "Civil"
                ].index(selected_row["department"])
            )

            semester = st.selectbox(
                "Semester",
                list(range(1,9)),
                index=int(selected_row["semester"])-1
            )

            division = st.selectbox(
                "Division",
                ["A","B"],
                index=0 if selected_row["division"]=="A" else 1
            )

            email = st.text_input(
                "Email",
                value=selected_row["email"]
            )

            new_password = st.text_input(
                "New Password (Optional)",
                type="password"
            )

            save = st.button(
                "💾 Update Student",
                type="primary",
                use_container_width=True
            )

            if save:

                cursor = conn.cursor()

                if new_password.strip():

                    cursor.execute(
                        """
                        UPDATE users
                        SET username=?,
                            password=?
                        WHERE user_id=?
                        """,
                        (
                            username,
                            new_password,
                            int(selected_row["user_id"])
                        )
                    )

                else:

                    cursor.execute(
                        """
                        UPDATE users
                        SET username=?
                        WHERE user_id=?
                        """,
                        (
                            username,
                            int(selected_row["user_id"])
                        )
                    )

                cursor.execute(
                    """
                    UPDATE students
                    SET

                    roll_no=?,
                    full_name=?,
                    department=?,
                    semester=?,
                    division=?,
                    email=?

                    WHERE student_id=?
                    """,
                    (
                        roll_no,
                        full_name,
                        department,
                        semester,
                        division,
                        email,
                        int(selected_row["student_id"])
                    )
                )

                conn.commit()

                st.success(
                    "Student updated successfully."
                )

                st.rerun()

        edit_dialog()
    # =====================================================
    # DELETE STUDENT
    # =====================================================

    if delete_student:

        @st.dialog("Delete Student")
        def delete_dialog():

            st.warning(
                f"Are you sure you want to delete "
                f"{selected_row['full_name']}?"
            )

            col1, col2 = st.columns(2)

            yes = col1.button(
                "Yes, Delete",
                type="primary",
                use_container_width=True
            )

            no = col2.button(
                "Cancel",
                use_container_width=True
            )

            if no:
                st.rerun()

            if yes:

                cursor = conn.cursor()

                cursor.execute(
                    """
                    DELETE FROM users
                    WHERE user_id=?
                    """,
                    (
                        int(selected_row["user_id"]),
                    )
                )

                conn.commit()

                st.success(
                    "Student deleted successfully."
                )

                st.rerun()

        delete_dialog()
    # =====================================================
    # DEPARTMENT CHART
    # =====================================================

    department_df = pd.read_sql_query(
        """
        SELECT

        department,

        COUNT(*) AS total

        FROM students

        GROUP BY department
        """,
        conn
    )

    if not department_df.empty:

        fig = px.bar(

            department_df,

            x="department",

            y="total",

            text="total",

            title="Students by Department"

        )

        fig.update_layout(
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        semester_df = pd.read_sql_query(
        """
        SELECT

        semester,

        COUNT(*) total

        FROM students

        GROUP BY semester

        ORDER BY semester
        """,
        conn
    )

    if not semester_df.empty:

        fig = px.line(

            semester_df,

            x="semester",

            y="total",

            markers=True,

            title="Semester-wise Student Count"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    # =====================================================
    # EXPORT EXCEL
    # =====================================================

    excel = BytesIO()

    students.drop(
        columns=["user_id"]
    ).to_excel(
        excel,
        index=False
    )

    st.download_button(

        "📥 Export Student List",

        excel.getvalue(),

        file_name="students.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

)