import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3


def teacher_dashboard():

    # ==========================
    # USER INFO
    # ==========================

    teacher_name = st.session_state.get(
        "full_name",
        "Teacher"
    )

    teacher_id = st.session_state.user_id

    # ==========================
    # DATABASE
    # ==========================

    conn = sqlite3.connect("database/erp.db")

    # Total Students

    total_students = pd.read_sql_query(
        """
        SELECT COUNT(*) AS total
        FROM students
        """,
        conn
    )["total"][0]

    # Subjects Assigned

    subject_df = pd.read_sql_query(
        """
        SELECT
            subject_name,
            completion_percentage
        FROM subjects
        WHERE teacher_id=?
        """,
        conn,
        params=(teacher_id,)
    )

    subject_count = len(subject_df)

    # Pending Queries

    pending_queries = pd.read_sql_query(
        """
        SELECT COUNT(*) AS total
        FROM student_queries
        WHERE teacher_reply IS NULL
           OR teacher_reply=''
        """,
        conn
    )["total"][0]

    # Average Syllabus Completion

    if not subject_df.empty:

        syllabus_completion = round(
            subject_df[
                "completion_percentage"
            ].mean(),
            2
        )

    else:

        syllabus_completion = 0

    # Recent Lectures

    lecture_df = pd.read_sql_query(
        """
        SELECT
            s.subject_name,
            l.lecture_date
        FROM lectures l

        JOIN subjects s
        ON l.subject_id=s.subject_id

        WHERE l.teacher_id=?

        ORDER BY l.lecture_date DESC

        LIMIT 5
        """,
        conn,
        params=(teacher_id,)
    )

    # Recent Announcements

    announcement_df = pd.read_sql_query(
        """
        SELECT
            title,
            announcement_date
        FROM announcements

        ORDER BY announcement_id DESC

        LIMIT 2
        """,
        conn
    )

    conn.close()

    # ==========================
    # CSS
    # ==========================

    st.html("""
    <style>

    .welcome-card{
        background:linear-gradient(
            135deg,
            #58339C,
            #9043B7
        );
        color:white;
        padding:25px;
        border-radius:20px;
        margin-bottom:20px;
    }

    .welcome-title{
        font-size:30px;
        font-weight:bold;
    }

    .welcome-subtitle{
        font-size:15px;
        opacity:0.9;
    }

    </style>
    """)

    # ==========================
    # HEADER
    # ==========================

    st.html(f"""
    <div class="welcome-card">

        <div class="welcome-title">
            👨‍🏫 Welcome, {teacher_name}
        </div>

        <div class="welcome-subtitle">
            Manage attendance, syllabus,
            announcements and student queries.
        </div>

    </div>
    """)

    # ==========================
    # QUICK STATS
    # ==========================

    st.subheader("📊 Academic Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Students",
            total_students
        )

    with col2:

        st.metric(
            "Subjects",
            subject_count
        )

    with col3:

        st.metric(
            "Pending Queries",
            pending_queries
        )

    with col4:

        st.metric(
            "Syllabus",
            f"{syllabus_completion}%"
        )

    st.divider()

    # ==========================
    # TODAY'S SUMMARY
    # ==========================

    left, right = st.columns(2)

    with left:

        st.subheader(
            "📅 Recent Lectures"
        )

        if lecture_df.empty:

            st.info(
                "No lectures found."
            )

        else:

            for _, row in lecture_df.iterrows():

                st.info(
                    f"{row['subject_name']}\n\n"
                    f"{row['lecture_date']}"
                )

    with right:

        st.subheader(
            "💬 Pending Queries"
        )

        st.warning(
            f"{pending_queries} Student "
            f"Queries awaiting response."
        )

    st.divider()

    # ==========================
    # SYLLABUS CHART
    # ==========================

    st.subheader(
        "📚 Subject-wise Syllabus Completion"
    )

    if not subject_df.empty:

        syllabus_chart_df = subject_df.rename(
            columns={
                "subject_name": "Subject",
                "completion_percentage":
                "Completion"
            }
        )

        fig = px.bar(
            syllabus_chart_df,
            x="Subject",
            y="Completion",
            text="Completion",
            title="Syllabus Progress"
        )

        fig.update_traces(
            texttemplate="%{text}%",
            textposition="outside"
        )

        fig.update_layout(
            yaxis_range=[0, 100],
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No subjects assigned."
        )

    st.divider()

    # ==========================
    # RECENT ANNOUNCEMENTS
    # ==========================

    st.subheader(
        "📢 Recent Announcements"
    )

    if announcement_df.empty:

        st.info(
            "No announcements available."
        )

    else:

        for _, row in announcement_df.iterrows():

            st.html(f"""
            <div style="
                background:white;
                border-left:5px solid #9043B7;
                padding:15px;
                border-radius:12px;
                margin-bottom:10px;
                box-shadow:0px 2px 8px
                rgba(0,0,0,0.08);
            ">

                <b>{row['title']}</b>

                <br><br>

                {row['announcement_date']}

            </div>
            """)