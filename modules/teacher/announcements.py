import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime


def teacher_announcements(user_id):

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
        <h2>📢 Announcement Management</h2>

        <p>
            Create, manage and publish
            announcements for students.
        </p>
    </div>
    """)

    # ==================================
    # CREATE ANNOUNCEMENT
    # ==================================

    st.subheader(
        "➕ Create Announcement"
    )

    title = st.text_input(
        "Announcement Title"
    )

    message = st.text_area(
        "Announcement Message",
        height=150
    )

    if st.button(
        "📢 Publish Announcement",
        use_container_width=True
    ):

        if not title.strip() or not message.strip():

            st.warning(
                "Please fill all fields."
            )

        else:

            cursor = conn.cursor()

            cursor.execute(
                    """
                    INSERT INTO announcements
                    (
                        title,
                        message,
                        announcement_date,
                        created_by,
                        creator_role
                    )
                    VALUES (?,?,?,?,?)
                    """,
                    (
                        title,
                        message,
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        ),
                        user_id,
                        "Teacher"
                    )
            )
            conn.commit()

            st.success(
                "Announcement Published Successfully"
            )

            st.rerun()

    st.divider()

    # ==================================
    # STATISTICS
    # ==================================

    total_announcements = pd.read_sql_query(
        """
        SELECT COUNT(*) AS total
        FROM announcements
        """,
        conn
    ).iloc[0]["total"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Announcements",
            total_announcements
        )

    with col2:
        st.metric(
            "Published Today",
            pd.read_sql_query(
                """
                SELECT COUNT(*) AS total
                FROM announcements
                WHERE DATE(announcement_date)=DATE('now')
                """,
                conn
            ).iloc[0]["total"]
        )

    st.divider()

    # ==================================
    # VIEW ANNOUNCEMENTS
    # ==================================

    st.subheader(
        "📋 Published Announcements"
    )

    announcements_df = pd.read_sql_query(
        """
        SELECT
            announcement_id,
            title,
            message,
            announcement_date,
            creator_role,
            created_by
        FROM announcements
        ORDER BY announcement_id DESC
        """,
        conn
    )

    if announcements_df.empty:

        st.info(
            "No announcements available."
        )

    else:

        for _, row in announcements_df.iterrows():

            with st.container():

                st.html(f"""
                <div style="
                    background:white;
                    border-left:5px solid #C8A2C8;
                    border-radius:15px;
                    padding:18px;
                    margin-bottom:15px;
                    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
                ">

                    <h4 style="
                        color:#58339C;
                        margin-bottom:10px;
                    ">
                        📢 {row['title']}
                    </h4>

                    <p style="
                        color:#555;
                        margin-bottom:10px;
                    ">
                        {row['message']}
                    </p>
                    
                    <p style="
                        color:#9043B7;
                        font-weight:bold;
                    ">
                        Posted By:
                        {row['creator_role']}
                    </p>

                    <small style="
                        color:gray;
                    ">
                        Posted on:
                        {row['announcement_date']}
                    </small>

                </div>
                """)

                delete_col1, delete_col2 = st.columns(
                    [8, 1]
                )

                with delete_col2:

                    if st.button(
                        "🗑️",
                        key=f"delete_{row['announcement_id']}"
                    ):

                        cursor = conn.cursor()

                        cursor.execute(
                            """
                            DELETE FROM announcements
                            WHERE announcement_id=?
                            """,
                            (
                                row["announcement_id"],
                            )
                        )

                        conn.commit()

                        st.rerun()

    conn.close()