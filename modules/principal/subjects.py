import streamlit as st
import pandas as pd
from database.db import get_connection

def principal_subjects():
    st.markdown("""
    <style>

    /* Section headings */
    h3{
        color:#58339C;
    }

    /* Metric Cards */
    div[data-testid="stMetric"]{
        background:white;
        border-left:6px solid #9043B7;
        border-radius:15px;
        padding:15px;
        box-shadow:0px 2px 10px rgba(88,51,156,0.12);
    }

    /* Forms */
    div[data-testid="stForm"]{
        background:#FFFFFF;
        border:2px solid #E0D4F0;
        border-radius:15px;
        padding:20px;
    }

    /* Text Inputs */
    div[data-baseweb="input"]{
        border-radius:10px;
    }

    /* Select Boxes */
    div[data-baseweb="select"]{
        border-radius:10px;
    }

    /* DataFrame */
    div[data-testid="stDataFrame"]{
        border:2px solid #E0D4F0;
        border-radius:15px;
        overflow:hidden;
    }

    /* Buttons */
    div.stButton > button{
        background:#58339C;
        color:white;
        border:none;
        border-radius:10px;
        font-weight:bold;
        height:45px;
    }

    div.stButton > button:hover{
        background:#9043B7;
        color:white;
    }

    /* Caption */
    div[data-testid="stCaptionContainer"]{
        color:#58339C;
        font-weight:600;
    }

    </style>
    """, unsafe_allow_html=True)

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
    # FILTERS
    # ==================================

    st.subheader("🔍 Search & Filter Subjects")

    col1, col2, col3 = st.columns(3)

    with col1:
        search = st.text_input(
            "Search Subject"
        )

    with col2:
        department_filter = st.selectbox(
            "Department",
            [
                "All",
                "Computer",
                "Information Technology",
                "Electronics",
                "Mechanical",
                "Civil"
            ]
        )

    with col3:
        semester_filter = st.selectbox(
            "Semester",
            [
                "All",
                1,2,3,4,5,6,7,8
            ]
        )

    # ==================================
    # LOAD SUBJECTS
    # ==================================

    df = pd.read_sql_query("""
    SELECT
        subject_id,
        subject_name,
        department,
        semester,
        completion_percentage
    FROM subjects
    ORDER BY department, semester, subject_name
    """, conn)

    # ==================================
    # APPLY FILTERS
    # ==================================

    filtered_df = df.copy()

    if search.strip():

        filtered_df = filtered_df[
            filtered_df["subject_name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if department_filter != "All":

        filtered_df = filtered_df[
            filtered_df["department"] == department_filter
        ]

    if semester_filter != "All":

        filtered_df = filtered_df[
            filtered_df["semester"] == semester_filter
        ]

    # ==================================
    # SUBJECT TABLE
    # ==================================

    st.subheader("📋 Subject List")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        f"Showing {len(filtered_df)} of {len(df)} subjects"
    )

    st.divider()

    # ==================================
    # DELETE SUBJECT
    # ==================================

    st.subheader("🗑 Delete Subject")

    if filtered_df.empty:

        st.info(
            "No subjects available for the selected filters."
        )

    else:

        subject_options = {
            f"{row.subject_name} | {row.department} | Semester {row.semester}":
            row.subject_id
            for _, row in filtered_df.iterrows()
        }

        selected_subject = st.selectbox(
            "Select Subject",
            list(subject_options.keys())
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
                subject_options[selected_subject],
            ))

            conn.commit()

            st.success(
                "Subject deleted successfully."
            )

            st.rerun()

    conn.close()