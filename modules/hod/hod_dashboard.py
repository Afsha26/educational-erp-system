import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px


def hod_dashboard(user_id):

    name = st.session_state.get(
        "full_name",
        "HOD"
    )
    conn = sqlite3.connect("database/erp.db")

    # ==================================
    # LOAD COUNTS
    # ==================================

    total_students = pd.read_sql_query(
        """
        SELECT COUNT(*) total
        FROM students
        """,
        conn
    ).iloc[0]["total"]

    total_teachers = pd.read_sql_query(
        """
        SELECT COUNT(*) total
        FROM teachers
        """,
        conn
    ).iloc[0]["total"]

    total_subjects = pd.read_sql_query(
        """
        SELECT COUNT(*) total
        FROM subjects
        """,
        conn
    ).iloc[0]["total"]

    total_queries = pd.read_sql_query(
        """
        SELECT COUNT(*) total
        FROM student_queries
        """,
        conn
    ).iloc[0]["total"]

    # ==================================
    # ATTENDANCE %
    # ==================================

    attendance_df = pd.read_sql_query(
        """
        SELECT status
        FROM attendance
        """,
        conn
    )

    present = len(
        attendance_df[
            attendance_df["status"] == "Present"
        ]
    )

    attendance_percentage = round(
        (present / len(attendance_df)) * 100,
        2
    ) if len(attendance_df) > 0 else 0

    # ==================================
    # SYLLABUS DATA
    # ==================================

    syllabus_df = pd.read_sql_query(
        """
        SELECT
            subject_name,
            completion_percentage
        FROM subjects
        ORDER BY completion_percentage DESC
        """,
        conn
    )

    average_completion = round(
        syllabus_df[
            "completion_percentage"
        ].mean(),
        2
    )

    # ==================================
    # PENDING QUERIES
    # ==================================

    pending_queries = pd.read_sql_query(
        """
        SELECT COUNT(*) total
        FROM student_queries
        WHERE teacher_reply IS NULL
           OR teacher_reply = ''
        """,
        conn
    ).iloc[0]["total"]

    # ==================================
    # HEADER
    # ==================================

    st.html(f"""
    <div style="
        background:linear-gradient(
            135deg,
            #58339C,
            #9043B7
        );
        color:white;
        padding:25px;
        border-radius:20px;
        margin-bottom:20px;
    ">
        <h2>🎓 Welcome, {name} </h2>

        <p>
            Monitor academic activities,
            attendance, syllabus progress
            and departmental performance.
        </p>
    </div>
    """)

    # ==================================
    # KPI CARDS
    # ==================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Students",
            total_students
        )

    with col2:
        st.metric(
            "Teachers",
            total_teachers
        )

    with col3:
        st.metric(
            "Subjects",
            total_subjects
        )

    with col4:
        st.metric(
            "Pending Queries",
            pending_queries
        )

    st.divider()

    # ==================================
    # OVERVIEW SECTION
    # ==================================

    left, right = st.columns(2)

    with left:

        st.subheader(
            "📊 Department Attendance"
        )

        st.progress(
            attendance_percentage / 100
        )

        st.success(
            f"{attendance_percentage}% Overall Attendance"
        )

    with right:

        st.subheader(
            "📚 Syllabus Completion"
        )

        st.progress(
            average_completion / 100
        )

        st.success(
            f"{average_completion}% Completed"
        )

    st.divider()

    # ==================================
    # SUBJECT PROGRESS GRAPH
    # ==================================

    st.subheader(
        "📈 Subject-wise Progress"
    )

    fig = px.bar(
        syllabus_df,
        x="subject_name",
        y="completion_percentage",
        text="completion_percentage"
    )

    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside"
    )

    fig.update_layout(
        height=500,
        yaxis_range=[0, 100],
        xaxis_title="Subject",
        yaxis_title="Completion %"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================
    # RECENT ANNOUNCEMENTS
    # ==================================

    st.subheader(
        "📢 Recent Announcements"
    )

    announcements_df = pd.read_sql_query(
        """
        SELECT
            title,
            creator_role,
            announcement_date
        FROM announcements
        ORDER BY announcement_id DESC
        LIMIT 5
        """,
        conn
    )

    if announcements_df.empty:

        st.info(
            "No announcements available."
        )

    else:

        st.dataframe(
            announcements_df,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # ==================================
    # LOW PROGRESS SUBJECTS
    # ==================================

    st.subheader(
        "⚠️ Subjects Requiring Attention"
    )

    low_progress = syllabus_df[
        syllabus_df[
            "completion_percentage"
        ] < 60
    ]

    if low_progress.empty:

        st.success(
            "All subjects are progressing well."
        )

    else:

        st.dataframe(
            low_progress,
            use_container_width=True,
            hide_index=True
        )

    conn.close()