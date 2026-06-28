import streamlit as st
import pandas as pd
from datetime import datetime
from database.db import get_connection


def principal_announcements():
# ==================================
# PAGE CSS
# ==================================

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
        <h2>📢 Announcements</h2>
        <p>Create and manage institute-wide announcements.</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()
    cursor = conn.cursor()

    # ==================================
    # STATISTICS
    # ==================================

    cursor.execute("SELECT COUNT(*) FROM announcements")
    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM announcements
    WHERE creator_role='Principal'
    """)
    principal_posts = cursor.fetchone()[0]

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Announcements",
        total
    )

    col2.metric(
        "Posted by Principal",
        principal_posts
    )

    st.divider()

    # ==================================
    # CREATE ANNOUNCEMENT
    # ==================================

    st.subheader("➕ Create Announcement")

    with st.form("announcement_form"):

        title = st.text_input("Title")

        message = st.text_area(
            "Message",
            height=150
        )

        submitted = st.form_submit_button(
            "Publish Announcement"
        )

        if submitted:

            if title.strip() == "" or message.strip() == "":

                st.warning(
                    "Please fill all fields."
                )

            else:

                cursor.execute("""
                INSERT INTO announcements
                (
                    title,
                    message,
                    announcement_date,
                    created_by,
                    creator_role
                )
                VALUES
                (
                    ?, ?, ?, ?, ?
                )
                """,
                (
                    title,
                    message,
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    st.session_state.principal_id,
                    "Principal"
                ))

                conn.commit()

                st.success(
                    "Announcement published successfully."
                )

                st.rerun()

    st.divider()

    # ==================================
    # VIEW ANNOUNCEMENTS
    # ==================================

    st.subheader("📋 Announcement History")

    df = pd.read_sql_query("""

    SELECT

        announcement_id,
        title,
        message,
        announcement_date,
        creator_role

    FROM announcements

    ORDER BY announcement_date DESC

    """, conn)

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No announcements available."
        )

    st.divider()

    # ==================================
    # DELETE
    # ==================================

    st.subheader("🗑 Delete Announcement")

    if not df.empty:

        options = {
            f"{row.title} ({row.announcement_date})":
            row.announcement_id
            for _, row in df.iterrows()
        }

        selected = st.selectbox(
            "Select Announcement",
            list(options.keys())
        )

        if st.button(
            "Delete Announcement",
            type="primary"
        ):

            cursor.execute("""
            DELETE FROM announcements
            WHERE announcement_id=?
            """,
            (
                options[selected],
            ))

            conn.commit()

            st.success(
                "Announcement deleted successfully."
            )

            st.rerun()

    conn.close()