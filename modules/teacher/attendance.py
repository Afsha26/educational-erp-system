import sqlite3
from datetime import date
import plotly.express as px
import pandas as pd
import streamlit as st
from io import BytesIO


# =====================================================
# DATABASE
# =====================================================

conn = sqlite3.connect(
    "database/erp.db",
    check_same_thread=False
)

conn.execute("PRAGMA foreign_keys = ON")


# =====================================================
# TEACHER ATTENDANCE
# =====================================================

def teacher_attendance(user_id: int):

    # ===========================================
    # PURPLE ERP THEME
    # ===========================================

    st.markdown("""
    <style>

    /* Primary Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6D28D9, #8B5CF6);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #5B21B6, #7C3AED);
        color: white;
    }

    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6D28D9, #8B5CF6);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #5B21B6, #7C3AED);
    }

    /* Selectbox */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px;
    }

    /* Date Input */
    .stDateInput input {
        border-radius: 10px;
    }

    /* Text Input */
    .stTextInput input {
        border-radius: 10px;
    }

    /* Checkbox */
    input[type="checkbox"] {
        accent-color: #7C3AED;
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg,#6D28D9,#A855F7);
    }

    /* Focused Input Border */
    div[data-baseweb="input"]:focus-within {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 1px #7C3AED !important;
    }

    /* Metric Cards */
    div[data-testid="metric-container"] {
        border: 1px solid #E5E7EB;
        border-radius: 14px;
        padding: 15px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.08);
    }
    .stDataEditor input[type="checkbox"] {
    accent-color: #7C3AED !important;
    }

    </style>
    """, unsafe_allow_html=True)
    
    st.html("""
    <div style="
        background:linear-gradient(
            135deg,
            #58339C,
            #9043B7
        );
        padding:25px;
        border-radius:15px;
        color:white;
        margin-bottom:20px;
    ">
        <h2>📋 Attendance Management</h2>

        <p>
        Create lecture attendance, manage student attendance,
        and monitor attendance records.
        </p>

    </div>
    """)

    # ===========================================
    # FETCH SUBJECTS OF LOGGED IN TEACHER
    # ===========================================
    teacher_id = st.session_state.get("teacher_id", None)
    subject_query = """
    SELECT
        subject_id,
        subject_name,
        department,
        semester
    FROM subjects
    WHERE teacher_id=?
    ORDER BY subject_name
    """

    subjects = pd.read_sql_query(
        subject_query,
        conn,
        params=(teacher_id,)
    )

    if subjects.empty:

        st.warning(
            "No subjects are assigned to you."
        )
        return

    # ===========================================
    # FILTERS
    # ===========================================

    col1, col2, col3 = st.columns(3)

    with col1:

        selected_subject = st.selectbox(
            "Subject",
            subjects["subject_name"]
        )

    selected_subject_row = subjects[
        subjects["subject_name"] == selected_subject
    ].iloc[0]

    subject_id = int(
        selected_subject_row["subject_id"]
    )

    department = selected_subject_row["department"]

    semester = int(
        selected_subject_row["semester"]
    )

    with col2:

        division = st.selectbox(
            "Division",
            ["A", "B"]
        )

    with col3:

        lecture_date = st.date_input(
            "Lecture Date",
            value=date.today()
        )

    st.info(
        f"{selected_subject} | {department} | Semester {semester} | Division {division}"
    )
    # ===========================================
    # FETCH STUDENTS
    # ===========================================

    student_query = """
    SELECT
        student_id,
        roll_no,
        full_name
    FROM students
    WHERE department=?
    AND semester=?
    AND division=?
    ORDER BY roll_no
    """

    students = pd.read_sql_query(
        student_query,
        conn,
        params=(
            department,
            semester,
            division
        )
    )

    if students.empty:

        st.warning(
            "No students found."
        )

        return

    # ===========================================
    # CREATE ATTENDANCE SHEET
    # ===========================================

    attendance_df = students.copy()
    # ===========================================
    # LOAD EXISTING ATTENDANCE
    # ===========================================

    existing_query = """
    SELECT
        student_id,
        status
    FROM attendance
    WHERE lecture_id = (
        SELECT lecture_id
        FROM lectures
        WHERE subject_id = ?
        AND lecture_date = ?
    )
    """

    existing = pd.read_sql_query(
        existing_query,
        conn,
        params=(
            subject_id,
            str(lecture_date)
        )
    )

    attendance_df["Present"] = True

    # Create empty dictionary first
    status_map = {}

    if not existing.empty:

        status_map = dict(
            zip(
                existing["student_id"],
                existing["status"]
            )
        )

    attendance_df["Present"] = attendance_df["student_id"].map(
        lambda student_id:
            status_map.get(student_id, "Present") == "Present"
    )

    st.subheader("Mark Attendance")
    # ===========================================
    # SEARCH STUDENT
    # ===========================================

    search = st.text_input(
        "🔍 Search by Roll No or Student Name"
    )

    if search:

        attendance_df = attendance_df[
            attendance_df["roll_no"]
            .str.contains(search, case=False)
            |
            attendance_df["full_name"]
            .str.contains(search, case=False)
        ]
    edited_df = st.data_editor(
        attendance_df,
        hide_index=True,
        use_container_width=True,
        disabled=[
            "student_id",
            "roll_no",
            "full_name"
        ],
        column_config={
            "student_id": None,
            "roll_no": st.column_config.TextColumn(
                "Roll No"
            ),
            "full_name": st.column_config.TextColumn(
                "Student Name"
            ),
            "Present": st.column_config.CheckboxColumn(
                "Present"
            ),
        }
    )

    save_button = st.button(
        "💾 Save Attendance",
        use_container_width=True,
        type="primary"
    )   
    # ===========================================
    # EXPORT EXCEL
    # ===========================================

    excel = BytesIO()

    edited_df.to_excel(
        excel,
        index=False
    )

    st.download_button(

        "📥 Download Attendance",

        excel.getvalue(),

        file_name=f"{selected_subject}_{lecture_date}.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )
    st.divider()
    # ===========================================
    # KPI CARDS
    # ===========================================

    total_students = len(students)

    present_default = total_students
    absent_default = 0

    attendance_default = (
        (present_default / total_students) * 100
        if total_students
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👨‍🎓 Students",
            total_students
        )

    with col2:
        st.metric(
            "✅ Present",
            present_default
        )

    with col3:
        st.metric(
            "❌ Absent",
            absent_default
        )

    with col4:
        st.metric(
            "📊 Attendance %",
            f"{attendance_default:.1f}%"
        )
    # ===========================================
    # SAVE ATTENDANCE
    # ===========================================

    if save_button:

        cursor = conn.cursor()

        # ---------------------------------------
        # Check if lecture already exists
        # ---------------------------------------

        cursor.execute(
            """
            SELECT lecture_id
            FROM lectures
            WHERE subject_id=?
            AND lecture_date=?
            """,
            (
                subject_id,
                str(lecture_date)
            )
        )

        lecture = cursor.fetchone()

        # ---------------------------------------
        # Create lecture if not exists
        # ---------------------------------------

        if lecture is None:

            cursor.execute(
                """
                INSERT INTO lectures(
                    subject_id,
                    teacher_id,
                    lecture_date
                )
                VALUES(?,?,?)
                """,
                (
                    subject_id,
                    teacher_id,
                    str(lecture_date)
                )
            )

            lecture_id = cursor.lastrowid

        else:

            lecture_id = lecture[0]

            # Remove previous attendance
            # so teacher can edit attendance

            cursor.execute(
                """
                DELETE FROM attendance
                WHERE lecture_id=?
                """,
                (lecture_id,)
            )

        # ---------------------------------------
        # Insert attendance
        # ---------------------------------------

        attendance_records = []

        for _, row in edited_df.iterrows():

            status = (
                "Present"
                if row["Present"]
                else "Absent"
            )

            attendance_records.append(

                (
                    lecture_id,
                    int(row["student_id"]),
                    status
                )

            )

        cursor.executemany(
            """
            INSERT INTO attendance(
                lecture_id,
                student_id,
                status
            )
            VALUES(?,?,?)
            """,
            attendance_records
        )

        conn.commit()

        st.success(
            "Attendance saved successfully."
        )

        # =======================================
        # TODAY SUMMARY
        # =======================================

        total_students = len(attendance_records)

        present_students = sum(
            1
            for record in attendance_records
            if record[2] == "Present"
        )

        absent_students = (
            total_students
            - present_students
        )

        attendance_percentage = (
            present_students
            / total_students
            * 100
            if total_students
            else 0
        )

        st.divider()

        st.subheader("Today's Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Students",
            total_students
        )

        col2.metric(
            "Present",
            present_students
        )

        col3.metric(
            "Absent",
            absent_students
        )

        col4.metric(
            "Attendance %",
            f"{attendance_percentage:.1f}%"
        )
        st.progress(attendance_percentage/100)

        st.caption(

            f"Overall Attendance : {attendance_percentage:.1f}%"

        )
    # ===========================================
    # RECENT LECTURES
    # ===========================================

    st.divider()
    st.subheader("📚 Recent Lectures")

    recent_query = """
    SELECT
        l.lecture_date,
        s.subject_name,

        SUM(
            CASE
                WHEN a.status='Present'
                THEN 1
                ELSE 0
            END
        ) AS present,

        SUM(
            CASE
                WHEN a.status='Absent'
                THEN 1
                ELSE 0
            END
        ) AS absent

    FROM lectures l

    JOIN attendance a
        ON l.lecture_id=a.lecture_id

    JOIN subjects s
        ON l.subject_id=s.subject_id

    WHERE l.teacher_id=?

    GROUP BY l.lecture_id

    ORDER BY l.lecture_date DESC

    LIMIT 10
    """

    recent_df = pd.read_sql_query(
        recent_query,
        conn,
        params=(teacher_id,)
    )

    if recent_df.empty:

        st.info("No attendance records available.")

    else:

        st.dataframe(
            recent_df,
            hide_index=True,
            use_container_width=True
        )

    # ===========================================
    # SUBJECT ATTENDANCE ANALYTICS
    # ===========================================

    st.divider()

    st.subheader("📊 Subject-wise Attendance")

    analytics_query = """
    SELECT

        s.subject_name,

        ROUND(

            100.0 *

            SUM(
                CASE
                    WHEN a.status='Present'
                    THEN 1
                    ELSE 0
                END
            )

            /

            COUNT(a.attendance_id)

        ,2)

        AS attendance_percentage

    FROM attendance a

    JOIN lectures l

        ON a.lecture_id=l.lecture_id

    JOIN subjects s

        ON l.subject_id=s.subject_id

    WHERE l.teacher_id=?

    GROUP BY s.subject_id
    """

    analytics_df = pd.read_sql_query(

        analytics_query,

        conn,

        params=(teacher_id,)

    )

    if not analytics_df.empty:

        fig = px.bar(

            analytics_df,

            x="subject_name",

            y="attendance_percentage",

            text="attendance_percentage",

            title="Average Attendance by Subject"

        )

        fig.update_traces(

            texttemplate="%{text}%",

            textposition="outside"

        )

        fig.update_layout(

            yaxis_range=[0,100],

            height=450

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ===========================================
    # MONTHLY TREND
    # ===========================================

    st.divider()

    st.subheader("📈 Monthly Attendance Trend")

    trend_query = """

    SELECT

        strftime('%m',l.lecture_date) AS month,

        ROUND(

            100.0 *

            SUM(
                CASE
                    WHEN a.status='Present'
                    THEN 1
                    ELSE 0
                END
            )

            /

            COUNT(*)

        ,2)

        AS attendance

    FROM attendance a

    JOIN lectures l

        ON a.lecture_id=l.lecture_id

    WHERE l.teacher_id=?

    GROUP BY month

    ORDER BY month

    """

    trend_df = pd.read_sql_query(

        trend_query,

        conn,

        params=(teacher_id,)

    )

    if not trend_df.empty:

        month_names = {

            "01":"Jan",
            "02":"Feb",
            "03":"Mar",
            "04":"Apr",
            "05":"May",
            "06":"Jun",
            "07":"Jul",
            "08":"Aug",
            "09":"Sep",
            "10":"Oct",
            "11":"Nov",
            "12":"Dec"

        }

        trend_df["month"] = trend_df["month"].map(month_names)

        fig = px.line(

            trend_df,

            x="month",

            y="attendance",

            markers=True,

            title="Monthly Attendance Trend"

        )

        fig.update_layout(

            yaxis_range=[0,100],

            height=450

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ===========================================
    # LOW ATTENDANCE STUDENTS
    # ===========================================

    st.divider()

    st.subheader("🚨 Low Attendance Students")

    low_query = """

    SELECT

        st.roll_no,

        st.full_name,

        ROUND(

            100.0 *

            SUM(
                CASE
                    WHEN a.status='Present'
                    THEN 1
                    ELSE 0
                END
            )

            /

            COUNT(*)

        ,2)

        AS attendance_percentage

    FROM attendance a

    JOIN students st

        ON a.student_id=st.student_id

    JOIN lectures l

        ON a.lecture_id=l.lecture_id

    WHERE l.teacher_id=?

    GROUP BY st.student_id

    HAVING attendance_percentage < 75

    ORDER BY attendance_percentage ASC

    """

    low_df = pd.read_sql_query(

        low_query,

        conn,

        params=(teacher_id,)

    )

    if low_df.empty:

        st.success(
            "🎉 No students are below 75% attendance."
        )

    else:

        st.dataframe(

            low_df,

            hide_index=True,

            use_container_width=True

        )