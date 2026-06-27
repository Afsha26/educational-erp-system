import streamlit as st
import pandas as pd
from database.db import get_connection


def principal_subjects():

    st.markdown("""
    <div style="
        background:linear-gradient(135deg,#58339C,#9043B7);
        padding:25px;
        border-radius:15px;
        color:white;
        margin-bottom:20px;
    ">
        <h2>📚 Subject Management</h2>
        <p>Create and manage subjects for all departments.</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()
    cursor = conn.cursor()

    # ==================================
    # SUBJECT STATISTICS
    # ==================================

    cursor.execute("SELECT COUNT(*) FROM subjects")
    total_subjects = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(DISTINCT department)
    FROM subjects
    """)
    total_departments = cursor.fetchone()[0]

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Subjects",
        total_subjects
    )

    col2.metric(
        "Departments",
        total_departments
    )

    st.divider()

    # ==================================
    # ADD SUBJECT
    # ==================================

    st.subheader("➕ Add Subject")

    with st.form("add_subject"):

        subject_name = st.text_input(
            "Subject Name"
        )

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
            [1,2,3,4,5,6,7,8]
        )

        submitted = st.form_submit_button(
            "Add Subject"
        )

        if submitted:

            if subject_name.strip() == "":

                st.warning(
                    "Please enter subject name."
                )

            else:

                cursor.execute("""
                SELECT *
                FROM subjects
                WHERE subject_name=?
                AND department=?
                AND semester=?
                """,
                (
                    subject_name,
                    department,
                    semester
                ))

                if cursor.fetchone():

                    st.error(
                        "Subject already exists."
                    )

                else:

                    cursor.execute("""
                    INSERT INTO subjects
                    (
                        subject_name,
                        department,
                        semester
                    )
                    VALUES
                    (
                        ?,?,?
                    )
                    """,
                    (
                        subject_name,
                        department,
                        semester
                    ))

                    conn.commit()

                    st.success(
                        "Subject added successfully."
                    )

                    st.rerun()

    st.divider()

    # ==================================
    # SEARCH
    # ==================================

    search = st.text_input(
        "🔍 Search Subject"
    )

    query = """
    SELECT
        subject_id,
        subject_name,
        department,
        semester,
        completion_percentage
    FROM subjects
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    if search:

        df = df[
            df["subject_name"]
            .str.contains(
                search,
                case=False
            )
        ]

    st.subheader("📋 Subject List")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================
    # DELETE SUBJECT
    # ==================================

    st.subheader("🗑 Delete Subject")

    if not df.empty:

        subject_option = {
            f"{row.subject_name} (Sem {row.semester})":
            row.subject_id
            for _, row in df.iterrows()
        }

        selected_subject = st.selectbox(
            "Select Subject",
            list(subject_option.keys())
        )

        if st.button(
            "Delete Subject",
            type="primary"
        ):

            cursor.execute("""
            DELETE FROM subjects
            WHERE subject_id=?
            """,
            (
                subject_option[selected_subject],
            ))

            conn.commit()

            st.success(
                "Subject deleted successfully."
            )

            st.rerun()

    conn.close()