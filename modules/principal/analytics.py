import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database.db import get_connection


def principal_analytics():

    st.markdown("""
    <div style="
        background:linear-gradient(135deg,#58339C,#9043B7);
        padding:25px;
        border-radius:15px;
        color:white;
        margin-bottom:20px;
    ">
        <h2>📊 Institution Analytics</h2>
        <p>Institution-wide academic insights and reports.</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()

    # ==========================================
    # ATTENDANCE SUMMARY
    # ==========================================

    attendance_df = pd.read_sql_query("""
        SELECT status
        FROM attendance
    """, conn)

    st.subheader("Overall Attendance")

    if attendance_df.empty:

        st.info("No attendance records found.")

    else:

        present = len(
            attendance_df[
                attendance_df["status"] == "Present"
            ]
        )

        absent = len(attendance_df) - present

        attendance_percentage = round(
            (present / len(attendance_df)) * 100,
            2
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Present Records",
            present
        )

        col2.metric(
            "Absent Records",
            absent
        )

        col3.metric(
            "Attendance %",
            f"{attendance_percentage}%"
        )

        fig, ax = plt.subplots(figsize=(5,5))

        ax.pie(
            [present, absent],
            labels=["Present", "Absent"],
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title("Attendance Distribution")

        st.pyplot(fig)

    st.divider()

    # ==========================================
    # STUDENTS BY DEPARTMENT
    # ==========================================

    st.subheader("Department-wise Students")

    student_df = pd.read_sql_query("""
        SELECT
            department,
            COUNT(*) AS Students
        FROM students
        GROUP BY department
    """, conn)

    if not student_df.empty:

        fig, ax = plt.subplots(figsize=(8,4))

        ax.bar(
            student_df["department"],
            student_df["Students"]
        )

        ax.set_ylabel("Students")
        ax.set_xlabel("Department")
        ax.set_title("Students per Department")

        st.pyplot(fig)

    st.divider()

    # ==========================================
    # TEACHERS BY DEPARTMENT
    # ==========================================

    st.subheader("Department-wise Teachers")

    teacher_df = pd.read_sql_query("""
        SELECT
            department,
            COUNT(*) AS Teachers
        FROM teachers
        GROUP BY department
    """, conn)

    if not teacher_df.empty:

        fig, ax = plt.subplots(figsize=(8,4))

        ax.bar(
            teacher_df["department"],
            teacher_df["Teachers"]
        )

        ax.set_ylabel("Teachers")
        ax.set_xlabel("Department")
        ax.set_title("Teachers per Department")

        st.pyplot(fig)

    st.divider()

    # ==========================================
    # SUBJECTS BY SEMESTER
    # ==========================================

    st.subheader("Semester-wise Subjects")

    subject_df = pd.read_sql_query("""
        SELECT
            semester,
            COUNT(*) AS Subjects
        FROM subjects
        GROUP BY semester
        ORDER BY semester
    """, conn)

    if not subject_df.empty:

        fig, ax = plt.subplots(figsize=(8,4))

        ax.plot(
            subject_df["semester"],
            subject_df["Subjects"],
            marker="o"
        )

        ax.set_xlabel("Semester")
        ax.set_ylabel("Subjects")
        ax.set_title("Subjects per Semester")

        st.pyplot(fig)

    st.divider()

    # ==========================================
    # SYLLABUS COMPLETION
    # ==========================================

    st.subheader("Department-wise Average Syllabus Completion")

    syllabus_df = pd.read_sql_query("""
        SELECT
            department,
            AVG(completion_percentage) AS Completion
        FROM subjects
        GROUP BY department
    """, conn)

    if not syllabus_df.empty:

        fig, ax = plt.subplots(figsize=(8,4))

        ax.bar(
            syllabus_df["department"],
            syllabus_df["Completion"]
        )

        ax.set_ylabel("Completion (%)")
        ax.set_xlabel("Department")
        ax.set_ylim(0,100)
        ax.set_title("Average Syllabus Completion")

        st.pyplot(fig)

    st.divider()

    # ==========================================
    # DATA TABLES
    # ==========================================

    st.subheader("Analytics Summary")

    tab1, tab2, tab3 = st.tabs(
        [
            "Students",
            "Teachers",
            "Subjects"
        ]
    )

    with tab1:
        st.dataframe(
            student_df,
            use_container_width=True,
            hide_index=True
        )

    with tab2:
        st.dataframe(
            teacher_df,
            use_container_width=True,
            hide_index=True
        )

    with tab3:
        st.dataframe(
            syllabus_df,
            use_container_width=True,
            hide_index=True
        )

    conn.close()