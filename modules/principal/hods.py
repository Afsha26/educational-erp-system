import streamlit as st
import pandas as pd
from database.db import get_connection


def principal_hods():

    st.markdown("""
    <div style="
        background:linear-gradient(135deg,#58339C,#9043B7);
        padding:25px;
        border-radius:15px;
        color:white;
        margin-bottom:20px;
    ">
        <h2>👨‍💼 HOD Management</h2>
        <p>Manage Heads of Departments.</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()
    cursor = conn.cursor()

    # ==================================
    # STATISTICS
    # ==================================

    cursor.execute("SELECT COUNT(*) FROM hods")
    total_hods = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(DISTINCT department)
    FROM hods
    """)
    total_departments = cursor.fetchone()[0]

    col1, col2 = st.columns(2)

    col1.metric(
        "Total HODs",
        total_hods
    )

    col2.metric(
        "Departments",
        total_departments
    )

    st.divider()

    # ==================================
    # ADD HOD
    # ==================================

    st.subheader("➕ Add HOD")

    with st.form("add_hod"):

        full_name = st.text_input("Full Name")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
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

        email = st.text_input("Email")

        submitted = st.form_submit_button(
            "Add HOD"
        )

        if submitted:

            if (
                full_name == "" or
                username == "" or
                password == "" or
                email == ""
            ):

                st.warning(
                    "Please fill all fields."
                )

            else:

                cursor.execute("""
                SELECT *
                FROM users
                WHERE username=?
                """, (username,))

                if cursor.fetchone():

                    st.error(
                        "Username already exists."
                    )

                else:

                    cursor.execute("""
                    INSERT INTO users
                    (
                        username,
                        password,
                        role
                    )
                    VALUES
                    (
                        ?, ?, ?
                    )
                    """,
                    (
                        username,
                        password,
                        "HOD"
                    ))

                    user_id = cursor.lastrowid

                    cursor.execute("""
                    INSERT INTO hods
                    (
                        user_id,
                        full_name,
                        department,
                        email
                    )
                    VALUES
                    (
                        ?, ?, ?, ?
                    )
                    """,
                    (
                        user_id,
                        full_name,
                        department,
                        email
                    ))

                    conn.commit()

                    st.success(
                        "HOD added successfully."
                    )

                    st.rerun()

    st.divider()

    # ==================================
    # VIEW HODS
    # ==================================

    st.subheader("📋 HOD List")

    hod_df = pd.read_sql_query("""

    SELECT

        h.hod_id,
        h.full_name,
        h.department,
        h.email,
        u.username

    FROM hods h

    JOIN users u

    ON h.user_id=u.user_id

    ORDER BY h.department

    """, conn)

    st.dataframe(
        hod_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================
    # DELETE HOD
    # ==================================

    st.subheader("🗑 Delete HOD")

    if not hod_df.empty:

        hod_options = {

            f"{row.full_name} ({row.department})":
            row.user_id

            for _, row in pd.read_sql_query("""

            SELECT
                h.full_name,
                h.department,
                h.user_id

            FROM hods h

            """, conn).iterrows()

        }

        selected = st.selectbox(
            "Select HOD",
            list(hod_options.keys())
        )

        if st.button(
            "Delete HOD",
            type="primary"
        ):

            cursor.execute("""
            DELETE FROM users
            WHERE user_id=?
            """,
            (
                hod_options[selected],
            ))

            conn.commit()

            st.success(
                "HOD deleted successfully."
            )

            st.rerun()

    conn.close()