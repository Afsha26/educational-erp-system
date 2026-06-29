import sqlite3

import streamlit as st
import pandas as pd
import plotly.express as px


def teacher_attendance(teacher_id):

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
        <h2>📊 Attendance Management</h2>

        <p>
            Manage student attendance,
            monitor attendance trends and
            generate attendance insights.
        </p>
    </div>
    """)

    # ==================================
    # DATABASE CONNECT
    # ==================================

    conn = sqlite3.connect("database/erp.db")

    attendance_df = pd.read_sql_query(
        """
        SELECT
            a.status,
            a.student_id,
            s.roll_no,
            s.full_name AS student_name,
            l.lecture_date,
            sub.subject_name,
            sub.subject_id,
            s.division
        FROM attendance a
        JOIN lectures l
            ON a.lecture_id = l.lecture_id
        JOIN subjects sub
            ON l.subject_id = sub.subject_id
        JOIN students s
            ON a.student_id = s.student_id
        WHERE l.teacher_id = ?
        """,
        conn,
        params=(teacher_id,)
    )

    total_students = (
        attendance_df["student_id"].nunique()
        if not attendance_df.empty else 0
    )

    present_count = (
        (attendance_df["status"] == "Present").sum()
        if not attendance_df.empty else 0
    )

    absent_count = (
        (attendance_df["status"] == "Absent").sum()
        if not attendance_df.empty else 0
    )

    total_records = len(attendance_df)
    attendance_percentage = (
        round((present_count / total_records) * 100, 1)
        if total_records > 0 else 0
    )

    # ==================================
    # QUICK STATS
    # ==================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Students",
            total_students
        )

    with col2:
        st.metric(
            "Present",
            present_count
        )

    with col3:
        st.metric(
            "Absent",
            absent_count
        )

    with col4:
        st.metric(
            "Attendance %",
            f"{attendance_percentage}%"
        )

    st.divider()

    # ==================================
    # MARK ATTENDANCE
    # ==================================

    st.subheader("✅ Mark Attendance")

    subjects_df = pd.read_sql_query(
        """
        SELECT
            subject_id,
            subject_name,
            department,
            semester
        FROM subjects
        WHERE teacher_id = ?
        """,
        conn,
        params=(teacher_id,)
    )

    if subjects_df.empty:
        st.warning("No subjects found for this teacher.")
        conn.close()
        return

    subject_options = subjects_df["subject_name"].tolist()
    subject_map = dict(
        zip(subjects_df["subject_name"], subjects_df["subject_id"])
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        subject = st.selectbox(
            "Subject",
            subject_options
        )

    subject_row = subjects_df[
        subjects_df["subject_name"] == subject
    ].iloc[0]

    divisions_df = pd.read_sql_query(
        """
        SELECT DISTINCT division
        FROM students
        WHERE department = ?
          AND semester = ?
        ORDER BY division
        """,
        conn,
        params=(
            subject_row["department"],
            subject_row["semester"]
        )
    )

    with col2:
        division = st.selectbox(
            "Division",
            divisions_df["division"].tolist()
            if not divisions_df.empty else ["A"]
        )

    with col3:
        lecture_date = st.date_input("Lecture Date")

    st.info(
        f"Attendance Sheet : {subject} | Division {division}"
    )

    students_df = pd.read_sql_query(
        """
        SELECT
            student_id,
            roll_no,
            full_name
        FROM students
        WHERE department = ?
          AND semester = ?
          AND division = ?
        ORDER BY roll_no
        """,
        conn,
        params=(
            subject_row["department"],
            subject_row["semester"],
            division
        )
    )

    lecture_df = pd.read_sql_query(
        """
        SELECT lecture_id
        FROM lectures
        WHERE subject_id = ?
          AND teacher_id = ?
          AND lecture_date = ?
        """,
        conn,
        params=(
            subject_map[subject],
            teacher_id,
            lecture_date.isoformat()
        )
    )

    lecture_id = (
        lecture_df["lecture_id"].iloc[0]
        if not lecture_df.empty else None
    )

    attendance_history = {}
    if lecture_id is not None:
        history_df = pd.read_sql_query(
            """
            SELECT student_id, status
            FROM attendance
            WHERE lecture_id = ?
            """,
            conn,
            params=(lecture_id,)
        )
        attendance_history = dict(
            zip(history_df["student_id"], history_df["status"])
        )

    attendance_sheet_df = pd.DataFrame([
        {
            "student_id": row["student_id"],
            "Roll No": row["roll_no"],
            "Student Name": row["full_name"],
            "Status": attendance_history.get(
                row["student_id"], "Present"
            )
        }
        for _, row in students_df.iterrows()
    ]).set_index("student_id")

    edited_df = st.data_editor(
        attendance_sheet_df,
        use_container_width=True,
        hide_index=True
    )

    if st.button(
        "💾 Save Attendance",
        use_container_width=True
    ):
        save_conn = sqlite3.connect("database/erp.db")
        save_cursor = save_conn.cursor()

        existing_lecture = save_cursor.execute(
            "SELECT lecture_id FROM lectures WHERE subject_id = ? AND teacher_id = ? AND lecture_date = ?",
            (
                subject_map[subject],
                teacher_id,
                lecture_date.isoformat()
            )
        ).fetchone()

        if existing_lecture:
            lecture_id = existing_lecture[0]
        else:
            save_cursor.execute(
                "INSERT INTO lectures(subject_id, teacher_id, lecture_date) VALUES (?, ?, ?)",
                (
                    subject_map[subject],
                    teacher_id,
                    lecture_date.isoformat()
                )
            )
            lecture_id = save_cursor.lastrowid

        for student_id, row in edited_df.iterrows():
            status_value = row["Status"]
            status_text = (
                "Present"
                if str(status_value).strip().lower() in (
                    "present", "true", "1", "yes", "y"
                )
                else "Absent"
            )

            existing_record = save_cursor.execute(
                "SELECT attendance_id FROM attendance WHERE lecture_id = ? AND student_id = ?",
                (lecture_id, student_id)
            ).fetchone()

            if existing_record:
                save_cursor.execute(
                    "UPDATE attendance SET status = ? WHERE attendance_id = ?",
                    (status_text, existing_record[0])
                )
            else:
                save_cursor.execute(
                    "INSERT INTO attendance(lecture_id, student_id, status) VALUES (?, ?, ?)",
                    (lecture_id, student_id, status_text)
                )

        save_conn.commit()
        save_conn.close()
        st.success("Attendance saved successfully.")

    st.divider()

    # ==================================
    # SUBJECT ATTENDANCE ANALYTICS
    # ==================================

    st.subheader("📈 Subject Attendance Analytics")

    analytics_df = pd.read_sql_query(
        """
        SELECT
            sub.subject_name AS Subject,
            ROUND(
                AVG(CASE WHEN a.status = 'Present' THEN 1.0 ELSE 0.0 END) * 100,
                1
            ) AS Attendance
        FROM attendance a
        JOIN lectures l
            ON a.lecture_id = l.lecture_id
        JOIN subjects sub
            ON l.subject_id = sub.subject_id
        WHERE l.teacher_id = ?
        GROUP BY sub.subject_name
        ORDER BY Attendance DESC
        """,
        conn,
        params=(teacher_id,)
    )

    if analytics_df.empty:
        st.info("No attendance analytics available yet.")
    else:
        fig = px.bar(
            analytics_df,
            x="Subject",
            y="Attendance",
            text="Attendance",
            title="Average Attendance by Subject"
        )

        fig.update_traces(
            texttemplate="%{text}%",
            textposition="outside"
        )

        fig.update_layout(
            yaxis_range=[0, 100],
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ==================================
    # ATTENDANCE TREND
    # ==================================

    st.subheader("📅 Monthly Attendance Trend")

    trend_df = pd.read_sql_query(
        """
        SELECT
            strftime('%b %Y', l.lecture_date) AS Month,
            ROUND(
                AVG(CASE WHEN a.status = 'Present' THEN 1.0 ELSE 0.0 END) * 100,
                1
            ) AS Attendance
        FROM attendance a
        JOIN lectures l
            ON a.lecture_id = l.lecture_id
        WHERE l.teacher_id = ?
        GROUP BY strftime('%Y-%m', l.lecture_date)
        ORDER BY strftime('%Y-%m', l.lecture_date)
        """,
        conn,
        params=(teacher_id,)
    )

    if trend_df.empty:
        st.info("No attendance trend available yet.")
    else:
        trend_fig = px.line(
            trend_df,
            x="Month",
            y="Attendance",
            markers=True
        )

        trend_fig.update_layout(
            yaxis_range=[0,100],
            height=400
        )

        st.plotly_chart(
            trend_fig,
            use_container_width=True
        )

    st.divider()

    # ==================================
    # LOW ATTENDANCE STUDENTS
    # ==================================

    st.subheader("⚠️ Low Attendance Students")

    low_df = pd.read_sql_query(
        """
        SELECT
            s.roll_no AS "Roll No",
            s.full_name AS "Student Name",
            ROUND(
                AVG(CASE WHEN a.status = 'Present' THEN 1.0 ELSE 0.0 END) * 100,
                1
            ) AS "Attendance %"
        FROM attendance a
        JOIN lectures l
            ON a.lecture_id = l.lecture_id
        JOIN students s
            ON a.student_id = s.student_id
        WHERE l.teacher_id = ?
        GROUP BY s.student_id
        HAVING AVG(CASE WHEN a.status = 'Present' THEN 1.0 ELSE 0.0 END) * 100 < 75
        ORDER BY "Attendance %" ASC
        """,
        conn,
        params=(teacher_id,)
    )

    if low_df.empty:
        st.info("No low attendance students found.")
    else:
        st.dataframe(
            low_df,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # ==================================
    # RECENT ATTENDANCE
    # ==================================

    st.subheader("📖 Recent Attendance Sessions")

    sessions_df = pd.read_sql_query(
        """
        SELECT
            l.lecture_date AS "Date",
            sub.subject_name AS "Subject",
            s.division AS "Division",
            ROUND(
                AVG(CASE WHEN a.status = 'Present' THEN 1.0 ELSE 0.0 END) * 100,
                1
            ) AS "Attendance %"
        FROM attendance a
        JOIN lectures l
            ON a.lecture_id = l.lecture_id
        JOIN subjects sub
            ON l.subject_id = sub.subject_id
        JOIN students s
            ON a.student_id = s.student_id
        WHERE l.teacher_id = ?
        GROUP BY l.lecture_id
        ORDER BY l.lecture_date DESC
        LIMIT 5
        """,
        conn,
        params=(teacher_id,)
    )

    if sessions_df.empty:
        st.info("No recent attendance sessions found.")
    else:
        st.dataframe(
            sessions_df,
            use_container_width=True,
            hide_index=True
        )

    conn.close()