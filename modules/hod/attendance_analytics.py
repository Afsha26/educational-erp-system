import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database.db import get_connection


def hod_attendance_analytics(user_id):

    st.markdown("""
    <div style="
        background:linear-gradient(135deg,#6A11CB,#2575FC);
        padding:25px;
        border-radius:15px;
        color:white;
        margin-bottom:20px;
    ">
        <h2>📊 Attendance Analytics</h2>
        <p>Department Attendance Monitoring Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()

    # =====================================
    # OVERALL ATTENDANCE
    # =====================================

    attendance_query = """
    SELECT
        status
    FROM attendance
    """

    attendance_df = pd.read_sql_query(
        attendance_query,
        conn
    )

    total_records = len(attendance_df)

    present_count = len(
        attendance_df[
            attendance_df["status"] == "Present"
        ]
    )

    absent_count = len(
        attendance_df[
            attendance_df["status"] == "Absent"
        ]
    )

    overall_attendance = (
        (present_count / total_records) * 100
        if total_records > 0 else 0
    )

    # =====================================
    # TOP CARDS
    # =====================================

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM students
    """)
    total_students = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM lectures
    """)
    total_lectures = cursor.fetchone()[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Students",
            total_students
        )

    with col2:
        st.metric(
            "Lectures Conducted",
            total_lectures
        )

    with col3:
        st.metric(
            "Overall Attendance %",
            f"{overall_attendance:.2f}%"
        )

    st.divider()

    # =====================================
    # PRESENT VS ABSENT
    # =====================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Present vs Absent")

        fig, ax = plt.subplots()

        ax.pie(
            [present_count, absent_count],
            labels=["Present", "Absent"],
            autopct="%1.1f%%"
        )

        st.pyplot(fig)

    # =====================================
    # SUBJECT WISE ATTENDANCE
    # =====================================

    subject_query = """
    SELECT
        sub.subject_name,

        ROUND(
            (
                SUM(
                    CASE
                        WHEN a.status='Present'
                        THEN 1
                        ELSE 0
                    END
                ) * 100.0
            ) / COUNT(*),
            2
        ) AS attendance_percentage

    FROM attendance a

    JOIN lectures l
        ON a.lecture_id=l.lecture_id

    JOIN subjects sub
        ON l.subject_id=sub.subject_id

    GROUP BY sub.subject_name
    """

    subject_df = pd.read_sql_query(
        subject_query,
        conn
    )

    with col2:

        st.subheader("Subject-wise Attendance")

        st.bar_chart(
            subject_df.set_index(
                "subject_name"
            )
        )

    st.divider()

    # =====================================
    # LOW ATTENDANCE STUDENTS
    # =====================================

    st.subheader(
        "⚠ Low Attendance Students (<75%)"
    )

    low_query = """
    SELECT

        s.roll_no,
        s.full_name,

        ROUND(
            (
                SUM(
                    CASE
                        WHEN a.status='Present'
                        THEN 1
                        ELSE 0
                    END
                ) * 100.0
            ) / COUNT(*),
            2
        ) AS attendance_percentage

    FROM attendance a

    JOIN students s
        ON a.student_id=s.student_id

    GROUP BY s.student_id

    HAVING attendance_percentage < 75
    """

    low_df = pd.read_sql_query(
        low_query,
        conn
    )

    if not low_df.empty:

        st.dataframe(
            low_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success(
            "No low attendance students found."
        )

    st.divider()

    # =====================================
    # TEACHER PERFORMANCE
    # =====================================

    st.subheader(
        "👨‍🏫 Teacher-wise Attendance"
    )

    teacher_query = """
    SELECT

        t.full_name,

        ROUND(
            (
                SUM(
                    CASE
                        WHEN a.status='Present'
                        THEN 1
                        ELSE 0
                    END
                ) * 100.0
            ) / COUNT(*),
            2
        ) AS attendance_percentage

    FROM attendance a

    JOIN lectures l
        ON a.lecture_id=l.lecture_id

    JOIN teachers t
        ON l.teacher_id=t.teacher_id

    GROUP BY t.teacher_id
    """

    teacher_df = pd.read_sql_query(
        teacher_query,
        conn
    )

    st.bar_chart(
        teacher_df.set_index(
            "full_name"
        )
    )

    st.dataframe(
        teacher_df,
        use_container_width=True,
        hide_index=True
    )

    conn.close()