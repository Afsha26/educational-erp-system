import io
import datetime

import pandas as pd
import streamlit as st

from database.db import get_connection


def principal_teachers():
    # =====================================
    # PAGE CSS
    # =====================================

    st.markdown(
        """
        <style>
        h3 {
            color: #58339C;
        }

        div[data-testid="stMetric"] {
            background: white;
            border-left: 6px solid #9043B7;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0px 2px 10px rgba(88, 51, 156, 0.12);
        }

        div[data-testid="stForm"] {
            background: #FFFFFF;
            border: 2px solid #E0D4F0;
            border-radius: 15px;
            padding: 20px;
        }

        div[data-baseweb="input"] {
            border-radius: 10px;
        }

        div[data-baseweb="select"] {
            border-radius: 10px;
        }

        div[data-testid="stDataFrame"] {
            border: 2px solid #E0D4F0;
            border-radius: 15px;
            overflow: hidden;
        }

        div.stButton > button {
            background: #58339C;
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            height: 45px;
        }

        div.stButton > button:hover {
            background: #9043B7;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            background:linear-gradient(135deg,#58339C,#9043B7);
            padding:25px;
            border-radius:15px;
            color:white;
            margin-bottom:20px;
        ">
            <h2>👨‍🏫 Teacher Management</h2>
            <p>Manage institution teachers across all departments.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================
    # SUMMARY SECTION
    # =====================================

    cursor.execute("SELECT COUNT(*) FROM teachers")
    total_teachers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT department) FROM teachers")
    total_departments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT designation) FROM teachers")
    total_designations = cursor.fetchone()[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Teachers", total_teachers)
    col2.metric("Departments", total_departments)
    col3.metric("Designations", total_designations)

    st.divider()

    # =====================================
    # ADD TEACHER
    # =====================================

    st.subheader("➕ Add Teacher")

    cursor.execute("""
    SELECT DISTINCT department
    FROM subjects
    ORDER BY department
    """)
    subject_departments = [row[0] for row in cursor.fetchall() if row[0]]

    if not subject_departments:
        subject_departments = [
            "Computer",
            "Information Technology",
            "Electronics",
            "Mechanical",
            "Civil",
        ]

    with st.form("add_teacher"):
        full_name = st.text_input("Full Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        department = st.selectbox("Department", subject_departments)
        designation = st.selectbox(
            "Designation",
            [
                "Assistant Professor",
                "Associate Professor",
                "Professor",
                "Lab Assistant",
            ],
        )
        email = st.text_input("Email")

        submitted = st.form_submit_button("Add Teacher")

        if submitted:
            if not full_name.strip() or not username.strip() or not password.strip() or not email.strip():
                st.warning("Please fill all fields.")
            else:
                cursor.execute("SELECT * FROM users WHERE username=?", (username.strip(),))
                if cursor.fetchone():
                    st.error("Username already exists.")
                else:
                    cursor.execute(
                        """
                        INSERT INTO users (username, password, role)
                        VALUES (?, ?, ?)
                        """,
                        (username.strip(), password, "Teacher"),
                    )
                    user_id = cursor.lastrowid

                    cursor.execute(
                        """
                        INSERT INTO teachers (user_id, full_name, department, designation, email)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (user_id, full_name.strip(), department, designation, email.strip()),
                    )

                    conn.commit()
                    st.success("Teacher added successfully.")
                    st.rerun()

    st.divider()

    # =====================================
    # SEARCH & FILTERS
    # =====================================

    st.subheader("🔍 Search & Filter Teachers")

    teacher_df = pd.read_sql_query(
        """
        SELECT
            t.teacher_id,
            t.full_name,
            t.department,
            t.designation,
            t.email,
            u.username,
            t.user_id
        FROM teachers t
        JOIN users u ON t.user_id = u.user_id
        ORDER BY t.department, t.full_name
        """,
        conn,
    )

    if teacher_df.empty:
        st.info("📂 No teachers found.")
    else:
        department_filter_options = ["All"] + sorted(
            teacher_df["department"].dropna().astype(str).unique().tolist()
        )
        designation_filter_options = ["All"] + sorted(
            teacher_df["designation"].dropna().astype(str).unique().tolist()
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            search_term = st.text_input("Search Teacher")

        with col2:
            department_filter = st.selectbox("Department", department_filter_options)

        with col3:
            designation_filter = st.selectbox("Designation", designation_filter_options)

        filtered_df = teacher_df.copy()

        if search_term.strip():
            filtered_df = filtered_df[
                filtered_df["full_name"].astype(str).str.contains(search_term, case=False, na=False)
                | filtered_df["department"].astype(str).str.contains(search_term, case=False, na=False)
                | filtered_df["email"].astype(str).str.contains(search_term, case=False, na=False)
            ]

        if department_filter != "All":
            filtered_df = filtered_df[filtered_df["department"].astype(str) == department_filter]

        if designation_filter != "All":
            filtered_df = filtered_df[filtered_df["designation"].astype(str) == designation_filter]

        if filtered_df.empty:
            st.info("🔍 No teacher matches your search.")
        else:
            st.dataframe(filtered_df[["teacher_id", "full_name", "department", "designation", "email", "username"]], use_container_width=True, hide_index=True)

            st.caption(f"Showing {len(filtered_df)} of {len(teacher_df)} Teachers")

    st.divider()

    # =====================================
    # EXPORT
    # =====================================

    st.subheader("📤 Export Teacher List")

    export_df = teacher_df.copy()
    if not teacher_df.empty:
        export_df = export_df[["teacher_id", "full_name", "department", "designation", "email", "username"]]

    if not export_df.empty:
        today = datetime.date.today().strftime("%Y-%m-%d")
        csv_buffer = io.BytesIO()
        export_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            export_df.to_excel(writer, index=False, sheet_name="Teachers")
        excel_buffer.seek(0)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇ Download CSV",
                data=csv_buffer,
                file_name=f"Teacher_List_{today}.csv",
                mime="text/csv",
            )
        with col2:
            st.download_button(
                "⬇ Download Excel",
                data=excel_buffer,
                file_name=f"Teacher_List_{today}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    else:
        st.info("No teacher data available to export.")

    st.divider()

    # =====================================
    # DELETE TEACHER
    # =====================================

    st.subheader("🗑 Delete Teacher")

    if not teacher_df.empty and not filtered_df.empty:
        delete_options = [
            f"{row['full_name']} | {row['department']}"
            for _, row in filtered_df.iterrows()
        ]
        selected_teacher = st.selectbox("Select Teacher", delete_options)

        if st.button("Delete Selected Teacher"):
            selected_row = filtered_df[filtered_df["full_name"].astype(str) + " | " + filtered_df["department"].astype(str) == selected_teacher]
            if not selected_row.empty:
                user_id = int(selected_row.iloc[0]["user_id"])
                cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
                conn.commit()
                st.success("Teacher deleted successfully.")
                st.rerun()
    elif teacher_df.empty:
        st.info("No teacher available to delete.")
    else:
        st.info("No teacher matches your current filters.")

    try:
        conn.close()
    except Exception:
        pass
