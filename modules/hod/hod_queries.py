import streamlit as st
import pandas as pd
from database.db import get_connection

def queries(user_id):

    st.markdown("""
    <div style="
        background:linear-gradient(135deg,#6A11CB,#2575FC);
        padding:25px;
        border-radius:15px;
        color:white;
        margin-bottom:20px;
    ">
        <h2>💬 Department Queries Monitoring</h2>
        <p>Monitor student queries and teacher responses across the department.</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()

    query = """
    SELECT
        sq.query_id,
        s.roll_no,
        s.full_name,
        sq.query_message,
        sq.teacher_reply,
        sq.created_at
    FROM student_queries sq
    JOIN students s
        ON sq.student_id = s.student_id
    ORDER BY sq.created_at DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    # ==================================
    # STATISTICS
    # ==================================

    total_queries = len(df)

    replied_queries = len(
        df[
            df["teacher_reply"].notna() &
            (df["teacher_reply"] != "")
        ]
    )

    pending_queries = total_queries - replied_queries

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Queries",
            total_queries
        )

    with col2:
        st.metric(
            "Replied Queries",
            replied_queries
        )

    with col3:
        st.metric(
            "Pending Queries",
            pending_queries
        )

    st.divider()

    # ==================================
    # PENDING QUERIES
    # ==================================

    st.subheader("⚠ Pending Queries")

    pending_df = df[
        df["teacher_reply"].isna() |
        (df["teacher_reply"] == "")
    ]

    if not pending_df.empty:

        st.dataframe(
            pending_df[
                [
                    "query_id",
                    "roll_no",
                    "full_name",
                    "query_message",
                    "created_at"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success(
            "All queries have been replied to."
        )

    st.divider()

    # ==================================
    # QUERY ANALYTICS
    # ==================================

    st.subheader("📊 Query Analytics")

    analytics_df = pd.DataFrame({
        "Category": [
            "Replied",
            "Pending"
        ],
        "Count": [
            replied_queries,
            pending_queries
        ]
    })

    st.bar_chart(
        analytics_df.set_index("Category")
    )

    st.divider()

    # ==================================
    # SEARCH
    # ==================================

    st.subheader("🔍 Search Queries")

    search_text = st.text_input(
        "Search by Student Name or Roll Number"
    )

    filtered_df = df.copy()

    if search_text:

        filtered_df = df[
            df["full_name"].str.contains(
                search_text,
                case=False,
                na=False
            )
            |
            df["roll_no"].str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    # ==================================
    # ALL QUERIES
    # ==================================

    st.subheader("📋 All Student Queries")

    display_df = filtered_df.copy()

    display_df["Status"] = display_df[
        "teacher_reply"
    ].apply(
        lambda x:
        "✅ Replied"
        if pd.notna(x) and x != ""
        else "⏳ Pending"
    )

    st.dataframe(
        display_df[
            [
                "query_id",
                "roll_no",
                "full_name",
                "query_message",
                "teacher_reply",
                "Status",
                "created_at"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================
    # QUERY DETAILS
    # ==================================

    st.subheader("👁 View Query Details")

    if not df.empty:

        selected_query = st.selectbox(
            "Select Query ID",
            df["query_id"]
        )

        record = df[
            df["query_id"] == selected_query
        ].iloc[0]

        st.info(
            f"Student : {record['full_name']} ({record['roll_no']})"
        )

        st.markdown("### Query")

        st.write(
            record["query_message"]
        )

        st.markdown("### Teacher Reply")

        if (
            pd.notna(record["teacher_reply"])
            and
            record["teacher_reply"] != ""
        ):
            st.success(
                record["teacher_reply"]
            )
        else:
            st.warning(
                "Reply Pending"
            )