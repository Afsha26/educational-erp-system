import streamlit as st
import sqlite3
import pandas as pd


def teacher_queries(user_id):

    conn = sqlite3.connect("database/erp.db")

    # ==================================
    # HEADER
    # ==================================

    st.html("""
    <div style="
        background:linear-gradient(135deg,#58339C,#9043B7);
        color:white;
        padding:25px;
        border-radius:20px;
        margin-bottom:20px;
    ">
        <h2>💬 Student Queries</h2>

        <p>
            View and respond to student
            questions and concerns.
        </p>
    </div>
    """)

    # ==================================
    # LOAD QUERIES
    # ==================================

    queries_df = pd.read_sql_query(
        """
        SELECT
            q.query_id,
            s.roll_no,
            s.full_name,
            q.query_message,
            q.teacher_reply,
            q.created_at
        FROM student_queries q

        JOIN students s
            ON q.student_id = s.student_id

        ORDER BY q.query_id DESC
        """,
        conn
    )

    # ==================================
    # STATISTICS
    # ==================================

    total_queries = len(queries_df)

    pending_queries = len(
        queries_df[
            queries_df["teacher_reply"].isna()
        ]
    )

    replied_queries = (
        total_queries - pending_queries
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Queries",
            total_queries
        )

    with col2:
        st.metric(
            "Pending",
            pending_queries
        )

    with col3:
        st.metric(
            "Replied",
            replied_queries
        )

    st.divider()

    # ==================================
    # NO DATA
    # ==================================

    if queries_df.empty:

        st.info(
            "No student queries available."
        )

        conn.close()
        return

    # ==================================
    # QUERY LIST
    # ==================================

    st.subheader(
        "📨 Student Questions"
    )

    for _, row in queries_df.iterrows():

        replied = (
            pd.notna(row["teacher_reply"])
            and
            row["teacher_reply"] != ""
        )

        status_color = (
            "#28A745"
            if replied
            else "#F39C12"
        )

        status_text = (
            "Answered"
            if replied
            else "Pending"
        )

        st.html(f"""
        <div style="
            background:white;
            border-left:6px solid {status_color};
            padding:18px;
            border-radius:15px;
            margin-bottom:15px;
            box-shadow:0px 2px 8px rgba(0,0,0,0.08);
        ">

            <h4 style="
                color:#58339C;
                margin-bottom:8px;
            ">
                👤 {row['full_name']}
            </h4>

            <p>
                <b>Roll No:</b>
                {row['roll_no']}
            </p>

            <p>
                <b>Query:</b><br>
                {row['query_message']}
            </p>

            <p>
                <b>Date:</b>
                {row['created_at']}
            </p>

            <span style="
                background:{status_color};
                color:white;
                padding:4px 10px;
                border-radius:10px;
                font-size:12px;
            ">
                {status_text}
            </span>

        </div>
        """)

        # ==========================
        # REPLY SECTION
        # ==========================

        if replied:

            st.success(
                f"Reply: {row['teacher_reply']}"
            )

        else:

            reply = st.text_area(
                "Reply",
                key=f"reply_{row['query_id']}"
            )

            if st.button(
                "📤 Send Reply",
                key=f"send_{row['query_id']}"
            ):

                if reply.strip() == "":

                    st.warning(
                        "Please enter a reply."
                    )

                else:

                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        UPDATE student_queries
                        SET teacher_reply=?
                        WHERE query_id=?
                        """,
                        (
                            reply,
                            row["query_id"]
                        )
                    )

                    conn.commit()

                    st.success(
                        "Reply sent successfully."
                    )

                    st.rerun()

        st.divider()

    conn.close()