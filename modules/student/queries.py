from numpy import nan
import streamlit as st
from database.db import get_connection
from datetime import datetime
import pandas as pd

def ask_query(student_id):

    # ==================================
    # CSS
    # ==================================

    st.html("""
    <style>

    .query-header{
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

    .info-card{
        background:white;
        padding:18px;
        border-radius:15px;
        border-left:6px solid #9043B7;
        box-shadow:0px 2px 10px rgba(0,0,0,0.08);
        margin-bottom:15px;
    }

    .info-title{
        color:#58339C;
        font-weight:bold;
        font-size:18px;
        margin-bottom:10px;
    }

    </style>
    """)

    # ==================================
    # HEADER
    # ==================================

    st.html("""
    <div class="query-header">

        <h2>💬 Student Query Portal</h2>

        <p>
            Communicate directly with your teachers and
            receive guidance regarding academics,
            attendance, syllabus and assignments.
        </p>

    </div>
    """)

    # ==================================
    # LAYOUT
    # ==================================

    left, right = st.columns([2, 1])

    # ==================================
    # QUERY FORM
    # ==================================

    with left:

        st.subheader("✍️ Submit New Query")

        category = st.selectbox(
            "Query Category",
            [
                "Attendance",
                "Syllabus",
                "Assignment",
                "Examination",
                "Subject Doubt",
                "Other"
            ]
        )

        priority = st.selectbox(
            "Priority",
            [
                "Low",
                "Medium",
                "High"
            ]
        )

        query_text = st.text_area(
            "Describe your query",
            height=180,
            placeholder="""
Example:
I was marked absent for the DBMS lecture
conducted on 10-06-2026 although I attended
the session.
            """
        )

        st.caption(
            f"Characters: {len(query_text)}"
        )

        if st.button(
            "📨 Submit Query",
            use_container_width=True
        ):

            if not query_text.strip():

                st.warning(
                    "Please enter your query."
                )

            else:

                conn = get_connection()

                cursor = conn.cursor()

                cursor.execute("""
                INSERT INTO student_queries
                (
                    student_id,
                    query_message,
                    created_at
                )
                VALUES (?,?,?)
                """,
                (
                    student_id,
                    query_text,
                    datetime.now()
                ))

                conn.commit()
                conn.close()

                st.success(
                    "✅ Query submitted successfully."
                )

    # ==================================
    # HELP SECTION
    # ==================================

    with right:

        st.html("""
        <div class="info-card">

            <div class="info-title">
                📌 Guidelines
            </div>

            <ul>
                <li>Be clear and specific.</li>
                <li>Mention subject name.</li>
                <li>Include dates if relevant.</li>
                <li>Avoid duplicate queries.</li>
            </ul>

        </div>
        """)

        st.html("""
        <div class="info-card">

            <div class="info-title">
                ⏱ Expected Response
            </div>

            Teachers generally respond
            within 24–48 hours.

        </div>
        """)

        st.html("""
        <div class="info-card">

            <div class="info-title">
                📚 Common Categories
            </div>

            • Attendance Issues<br>
            • Assignment Queries<br>
            • Exam Related Doubts<br>
            • Syllabus Questions<br>
            • Subject Clarifications

        </div>
        """)

        # ==================================
        # MY QUERIES
        # ==================================

    st.divider()

    st.subheader("📨 My Submitted Queries")

    conn = get_connection()

    query_df = pd.read_sql_query("""
        SELECT
            query_id,
            query_message,
            teacher_reply,
            created_at
            FROM student_queries
            WHERE student_id = ?
            ORDER BY created_at DESC
            """,
            conn,
            params=(student_id,)
        )

    conn.close()

    if query_df.empty:

        st.info(
            "You have not submitted any queries yet."
        )

    else:

        for _, row in query_df.iterrows():

            query_message = row["query_message"]

            teacher_reply = row["teacher_reply"]

            created_at = row["created_at"]

            with st.expander(
                    f"📅 {created_at}"
            ):

                st.markdown(
                    f"**Your Query:**\n\n{query_message}"
                )

                st.markdown("---")

                if teacher_reply and teacher_reply not in [nan, None, ""]:

                    st.success(
                        f"Teacher Reply:\n\n{teacher_reply}"
                        )
                else:
                    st.warning(
                        "Awaiting teacher response."
                        )