import streamlit as st
import pandas as pd
from database.db import get_connection


def show_announcements(user_id):

    # ==================================
    # CSS
    # ==================================

    st.html("""
    <style>

    .announcement-header{
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

    .announcement-card{
        background:white;
        padding:20px;
        border-radius:15px;
        border-left:6px solid #9043B7;
        box-shadow:0px 2px 10px rgba(0,0,0,0.08);
        margin-bottom:15px;
    }

    .announcement-title{
        color:#58339C;
        font-size:20px;
        font-weight:bold;
        margin-bottom:8px;
    }

    .announcement-meta{
        color:#777;
        font-size:13px;
        margin-bottom:10px;
    }

    .announcement-message{
        color:#444;
        font-size:15px;
    }

    </style>
    """)

    # ==================================
    # HEADER
    # ==================================

    st.html("""
    <div class="announcement-header">

        <h2>📢 Announcements</h2>

        <p>
        Stay updated with important academic notices,
        events, examinations and institutional updates.
        </p>

    </div>
    """)

    # ==================================
    # DATABASE
    # ==================================

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM announcements
        ORDER BY announcement_date DESC
        """,
        conn
    )

    conn.close()

    # ==================================
    # SEARCH
    # ==================================

    search = st.text_input(
        "🔍 Search Announcement",
        placeholder="Search by title e.g. Announcement 2..."
    )

    if search:

        df = df[
            df["title"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # ==================================
    # SUMMARY
    # ==================================

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Announcements",
            len(df)
        )

    with col2:
        st.metric(
            "Unread",
            len(df)
        )

    st.divider()

    # ==================================
    # ANNOUNCEMENT CARDS
    # ==================================

    if df.empty:

        st.info(
            "No announcements found."
        )

    else:

        for _, row in df.iterrows():

            title = row.get(
                "title",
                "Announcement"
            )

            message = row.get(
                "message",
                ""
            )

            date = row.get(
                "announcement_date",
                ""
            )

            teacher = row.get(
                "teacher_name",
                "Faculty"
            )

            st.html(f"""
            <div class="announcement-card">

                <div class="announcement-title">
                    📌 {title}
                </div>

                <div class="announcement-meta">
                    👨‍🏫 {teacher} • 📅 {date}
                </div>

                <div class="announcement-message">
                    {message}
                </div>

            </div>
            """)