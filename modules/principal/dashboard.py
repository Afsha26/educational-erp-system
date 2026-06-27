import streamlit as st
import pandas as pd
from database.db import get_connection


def principal_dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    # ==================================
    # COUNTS
    # ==================================

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM teachers")
    total_teachers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM hods")
    total_hods = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM subjects")
    total_subjects = cursor.fetchone()[0]

    # ==================================
    # ATTENDANCE
    # ==================================

    attendance_df = pd.read_sql_query("""
        SELECT status
        FROM attendance
    """, conn)

    if len(attendance_df) > 0:

        present = len(
            attendance_df[
                attendance_df["status"] == "Present"
            ]
        )

        attendance_percentage = round(
            (present / len(attendance_df)) * 100,
            2
        )

    else:
        attendance_percentage = 0

    # ==================================
    # SYLLABUS
    # ==================================

    cursor.execute("""
        SELECT AVG(completion_percentage)
        FROM subjects
    """)

    avg_completion = cursor.fetchone()[0]

    if avg_completion is None:
        avg_completion = 0

    avg_completion = round(avg_completion, 2)

    # ==================================
    # HEADER
    # ==================================

    st.markdown("""
    <div style="
        background:linear-gradient(135deg,#58339C,#9043B7);
        padding:25px;
        border-radius:15px;
        color:white;
        margin-bottom:20px;
    ">
        <h2>🏛 Principal Dashboard</h2>
        <p>Institution Overview</p>
    </div>
    """, unsafe_allow_html=True)

    # ==================================
    # KPI CARDS
    # ==================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Students",
        total_students
    )

    col2.metric(
        "Teachers",
        total_teachers
    )

    col3.metric(
        "HODs",
        total_hods
    )

    col4.metric(
        "Subjects",
        total_subjects
    )

    st.divider()

    col5, col6 = st.columns(2)

    col5.metric(
        "Overall Attendance",
        f"{attendance_percentage}%"
    )

    col6.metric(
        "Average Syllabus Completion",
        f"{avg_completion}%"
    )

    st.divider()

    # ==================================
    # STUDENT DISTRIBUTION
    # ==================================

    st.subheader("📊 Department-wise Student Distribution")

    department_df = pd.read_sql_query("""
        SELECT
            department,
            COUNT(*) AS Students
        FROM students
        GROUP BY department
    """, conn)

    if not department_df.empty:

        st.bar_chart(
            department_df.set_index("department")
        )

    else:
        st.info("No student data available.")

    st.divider()

    # ==================================
    # RECENT ANNOUNCEMENTS
    # ==================================

    st.subheader("📢 Recent Announcements")

    announcement_df = pd.read_sql_query("""
        SELECT
            title,
            announcement_date,
            creator_role
        FROM announcements
        ORDER BY announcement_date DESC
        LIMIT 5
    """, conn)

    if not announcement_df.empty:

        st.dataframe(
            announcement_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No announcements available.")

    st.divider()

    # ==================================
    # QUICK ACCESS
    # ==================================

    st.subheader("⚡ Quick Access")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("📚 Manage Subjects")

    with c2:
        st.info("👨‍💼 Manage HODs")

    with c3:
        st.info("📊 View Analytics")

    conn.close()