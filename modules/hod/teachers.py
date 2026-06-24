import streamlit as st
import pandas as pd

from database.db import get_connection


def hod_teachers():

    st.markdown("""
    <div style="
        background:linear-gradient(135deg,#4A00E0,#8E2DE2);
        padding:25px;
        border-radius:15px;
        color:white;
        margin-bottom:20px;
    ">
        <h2>👨‍🏫 Teacher Management</h2>
        <p>Manage teachers and assign subjects.</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()
    cursor = conn.cursor()

    # ==================================
    # TEACHER STATISTICS
    # ==================================

    cursor.execute("""
    SELECT COUNT(*)
    FROM teachers
    """)

    total_teachers = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM subjects
    WHERE teacher_id IS NOT NULL
    """)

    assigned_subjects = cursor.fetchone()[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Teachers",
            total_teachers
        )

    with col2:
        st.metric(
            "Assigned Subjects",
            assigned_subjects
        )

    st.divider()

    # ==================================
    # ALL TEACHERS
    # ==================================

    st.subheader("👨‍🏫 Teacher Directory")

    teachers_df = pd.read_sql_query("""
    SELECT
        teacher_id,
        full_name,
        designation,
        department,
        email
    FROM teachers
    ORDER BY full_name
    """, conn)

    st.dataframe(
        teachers_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================
    # SUBJECT ASSIGNMENT
    # ==================================

    st.subheader("📚 Assign Subject")

    subjects_df = pd.read_sql_query("""
    SELECT
        subject_id,
        subject_name,
        semester
    FROM subjects
    ORDER BY semester, subject_name
    """, conn)

    teacher_options = {
        row["full_name"]: row["teacher_id"]
        for _, row in teachers_df.iterrows()
    }

    subject_options = {
        f"{row['subject_name']} (Sem {row['semester']})":
        row["subject_id"]
        for _, row in subjects_df.iterrows()
    }

    col1, col2 = st.columns(2)

    with col1:

        selected_subject = st.selectbox(
            "Select Subject",
            list(subject_options.keys())
        )

    with col2:

        selected_teacher = st.selectbox(
            "Assign Teacher",
            list(teacher_options.keys())
        )

    if st.button(
        "Assign Subject",
        use_container_width=True
    ):

        subject_id = subject_options[selected_subject]
        teacher_id = teacher_options[selected_teacher]

        cursor.execute("""
        UPDATE subjects
        SET teacher_id = ?
        WHERE subject_id = ?
        """, (teacher_id, subject_id))

        conn.commit()

        st.success(
            "Subject assigned successfully."
        )

        st.rerun()

    st.divider()

    # ==================================
    # CURRENT SUBJECT ALLOCATION
    # ==================================

    st.subheader("📋 Subject Allocation")

    allocation_df = pd.read_sql_query("""
    SELECT
        s.subject_id,
        s.subject_name,
        s.semester,
        t.full_name AS teacher_name,
        s.completion_percentage
    FROM subjects s

    LEFT JOIN teachers t
        ON s.teacher_id = t.teacher_id

    ORDER BY s.semester
    """, conn)

    st.dataframe(
        allocation_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================
    # TEACHER WORKLOAD
    # ==================================

    st.subheader("📊 Teacher Workload")

    workload_df = pd.read_sql_query("""
    SELECT

        t.full_name,

        COUNT(s.subject_id)
        AS total_subjects

    FROM teachers t

    LEFT JOIN subjects s
        ON t.teacher_id = s.teacher_id

    GROUP BY t.teacher_id

    ORDER BY total_subjects DESC
    """, conn)

    st.bar_chart(
        workload_df.set_index(
            "full_name"
        )
    )

    st.dataframe(
        workload_df,
        use_container_width=True,
        hide_index=True
    )

    conn.close()