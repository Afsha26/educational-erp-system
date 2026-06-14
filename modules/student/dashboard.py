import streamlit as st
import sqlite3
import pandas as pd


def show_dashboard():

    student_id = st.session_state.user_id

    conn = sqlite3.connect("database/erp.db")

    # ==================================
    # STUDENT DETAILS
    # ==================================

    student_df = pd.read_sql_query(
        """
        SELECT *
        FROM students
        WHERE student_id=?
        """,
        conn,
        params=(student_id,)
    )

    full_name = student_df.iloc[0]["full_name"]

    # ==================================
    # ATTENDANCE %
    # ==================================

    attendance_df = pd.read_sql_query(
        """
        SELECT status
        FROM attendance
        WHERE student_id=?
        """,
        conn,
        params=(student_id,)
    )

    total_lectures = len(attendance_df)

    present_lectures = len(
        attendance_df[
            attendance_df["status"] == "Present"
        ]
    )

    attendance_percentage = (
        round(
            (present_lectures / total_lectures) * 100,
            2
        )
        if total_lectures > 0
        else 0
    )

    # ==================================
    # SUBJECT COUNT
    # ==================================

    subject_count = pd.read_sql_query(
        """
        SELECT COUNT(*) AS total
        FROM subjects
        WHERE semester=?
        """,
        conn,
        params=(student_df.iloc[0]["semester"],)
    )["total"][0]

    # ==================================
    # ANNOUNCEMENTS
    # ==================================

    announcement_count = pd.read_sql_query(
        """
        SELECT COUNT(*) AS total
        FROM announcements
        """,
        conn
    )["total"][0]

    latest_announcement = pd.read_sql_query(
        """
        SELECT title
        FROM announcements
        ORDER BY announcement_id DESC
        LIMIT 1
        """,
        conn
    )

    announcement_title = (
        latest_announcement.iloc[0]["title"]
        if not latest_announcement.empty
        else "No announcements available"
    )

    # ==================================
    # QUERIES
    # ==================================

    query_count = pd.read_sql_query(
        """
        SELECT COUNT(*) AS total
        FROM student_queries
        WHERE student_id=?
        """,
        conn,
        params=(student_id,)
    )["total"][0]

    reply_count = pd.read_sql_query(
        """
        SELECT COUNT(*) AS total
        FROM student_queries
        WHERE student_id=?
        AND teacher_reply IS NOT NULL
        """,
        conn,
        params=(student_id,)
    )["total"][0]

    # ==================================
    # SYLLABUS PROGRESS
    # ==================================

    syllabus_df = pd.read_sql_query(
        """
        SELECT AVG(completion_percentage)
        AS progress
        FROM subjects
        WHERE semester=?
        """,
        conn,
        params=(student_df.iloc[0]["semester"],)
    )

    syllabus_progress = round(
        syllabus_df.iloc[0]["progress"]
        if syllabus_df.iloc[0]["progress"]
        else 0,
        2
    )

    conn.close()

    # ==================================
    # CSS
    # ==================================

    st.html("""
    <style>

    .welcome-card{
        background:linear-gradient(135deg,#58339C,#9043B7);
        padding:25px;
        border-radius:20px;
        color:white;
        margin-bottom:20px;
    }

    .welcome-title{
        font-size:30px;
        font-weight:bold;
    }

    .welcome-subtitle{
        font-size:16px;
        opacity:0.9;
    }

    .section-title{
        color:#58339C;
        font-size:22px;
        font-weight:bold;
        margin-top:10px;
        margin-bottom:10px;
    }

    .info-card{
        background:white;
        padding:18px;
        border-radius:15px;
        border-left:5px solid #C8A2C8;
        box-shadow:0px 2px 8px rgba(0,0,0,0.08);
        margin-bottom:15px;
    }

    .info-title{
        color:#58339C;
        font-size:18px;
        font-weight:bold;
    }

    .info-text{
        color:#555;
        font-size:14px;
    }

    </style>
    """)

    # ==================================
    # WELCOME
    # ==================================

    st.html(f"""
    <div class="welcome-card">

        <div class="welcome-title">
            🎓 Welcome, {full_name}
        </div>

        <div class="welcome-subtitle">
            Student Academic Dashboard
        </div>

    </div>
    """)

    # ==================================
    # OVERVIEW
    # ==================================

    st.subheader("📊 Academic Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Attendance",
            f"{attendance_percentage}%"
        )

    with col2:
        st.metric(
            "Subjects",
            subject_count
        )

    with col3:
        st.metric(
            "Announcements",
            announcement_count
        )

    with col4:
        st.metric(
            "Queries",
            query_count
        )

    st.divider()

    # ==================================
    # ATTENDANCE SUMMARY
    # ==================================

    st.subheader("📈 Attendance Progress")

    st.progress(
        attendance_percentage / 100
    )

    if attendance_percentage >= 75:

        st.success(
            f"Current Attendance: {attendance_percentage}%"
        )

    elif attendance_percentage >= 60:

        st.warning(
            f"Current Attendance: {attendance_percentage}%"
        )

    else:

        st.error(
            f"Current Attendance: {attendance_percentage}%"
        )

    st.divider()

    # ==================================
    # QUICK INFO
    # ==================================

    col1, col2 = st.columns(2)

    with col1:

        st.html(f"""
        <div class="info-card">

            <div class="info-title">
                📚 Syllabus Progress
            </div>

            <div class="info-text">
                Overall syllabus completion:
                <b>{syllabus_progress}%</b>
            </div>

        </div>
        """)

        st.html(f"""
        <div class="info-card">

            <div class="info-title">
                📢 Latest Announcement
            </div>

            <div class="info-text">
                {announcement_title}
            </div>

        </div>
        """)

    with col2:

        st.html(f"""
        <div class="info-card">

            <div class="info-title">
                💬 Teacher Replies
            </div>

            <div class="info-text">
                {reply_count} queries answered
            </div>

        </div>
        """)

        st.html("""
        <div class="info-card">

            <div class="info-title">
                🎯 Academic Status
            </div>

            <div class="info-text">
                Keep tracking attendance and syllabus progress regularly.
            </div>

        </div>
        """)