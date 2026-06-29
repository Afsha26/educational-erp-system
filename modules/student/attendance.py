import math
import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px


def show_attendance(student_id):

    # =====================
    # LOAD DATA
    # =====================

    conn = sqlite3.connect("database/erp.db")

    attendance_df = pd.read_sql_query(
        """
        SELECT
            l.lecture_date,
            s.subject_name AS subject,
            a.status
        FROM attendance a

        JOIN lectures l
            ON a.lecture_id = l.lecture_id

        JOIN subjects s
            ON l.subject_id = s.subject_id

        WHERE a.student_id = ?

        ORDER BY l.lecture_date DESC
        """,
        conn,
        params=(student_id,)
    )

    conn.close()
    st.title("📊 Attendance Management")

    # =====================
    # NO DATA CHECK
    # =====================

    if attendance_df.empty:

        st.warning("No attendance records found.")

        return

    # =====================
    # CALCULATIONS
    # =====================

    total_lectures = len(attendance_df)

    present_lectures = len(
        attendance_df[
            attendance_df["status"] == "Present"
        ]
    )

    absent_lectures = len(
        attendance_df[
            attendance_df["status"] == "Absent"
        ]
    )

    attendance_percentage = math.floor(
        (present_lectures / total_lectures) * 100
    )

    # =====================
    # SUMMARY CARDS
    # =====================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Attendance %",
            f"{attendance_percentage}%"
        )

    with col2:
        st.metric(
            "Present Lectures",
            present_lectures
        )

    with col3:
        st.metric(
            "Absent Lectures",
            absent_lectures
        )

    with col4:
        st.metric(
            "Total Lectures",
            total_lectures
        )

    st.divider()

    # =====================
    # ATTENDANCE PROGRESS
    # =====================

    st.subheader("📈 Attendance Progress")

    st.progress(
        attendance_percentage / 100
    )

    st.success(
        f"Current Attendance : {attendance_percentage}%"
    )

    if attendance_percentage >= 75:
        st.success("✅ Eligible")
    else:
        st.error("❌ Defaulter")

    st.divider()

    # =====================
    # SUBJECT-WISE ATTENDANCE
    # =====================

    st.subheader(
        "📚 Subject-wise Attendance"
    )

    subject_df = (
        attendance_df
        .groupby("subject")
        .apply(
            lambda x: round(
                (
                    (x["status"] == "Present").sum()
                    / len(x)
                ) * 100,
                2
            )
        )
        .reset_index(name="Attendance")
    )

    subject_df.rename(
        columns={
            "subject": "Subject"
        },
        inplace=True
    )

    fig = px.bar(
        subject_df,
        x="Subject",
        y="Attendance",
        text="Attendance",
        title="Attendance Percentage by Subject"
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

    # =====================
    # MONTHLY TREND
    # =====================

    st.subheader(
        "📅 Monthly Attendance Trend"
    )

    attendance_df["lecture_date"] = pd.to_datetime(
        attendance_df["lecture_date"]
    )

    monthly_df = (
    attendance_df
    .groupby(
        attendance_df["lecture_date"]
        .dt.strftime("%Y-%m")
    )
        .apply(
            lambda x: round(
                (
                    (x["status"] == "Present").sum()
                    / len(x)
                ) * 100,
                2
            )
        )
        .reset_index(name="Attendance")
    )

    monthly_df.rename(
        columns={
            "lecture_date": "Month"
        },
        inplace=True
    )

    trend_fig = px.line(
        monthly_df,
        x="Month",
        y="Attendance",
        markers=True
    )

    trend_fig.update_layout(
        yaxis_range=[0, 100],
        height=400
    )

    st.plotly_chart(
        trend_fig,
        use_container_width=True
    )

    st.divider()

    # =====================
    # ATTENDANCE RECORDS
    # =====================

    st.subheader(
        "📖 Attendance Records"
    )

    records_df = attendance_df.copy()

    records_df.rename(
        columns={
            "lecture_date": "Date",
            "subject": "Subject",
            "status": "Status"
        },
        inplace=True
    )

    records_df["Date"] = records_df["Date"].dt.strftime(
        "%d-%m-%Y"
    )

    st.dataframe(
        records_df,
        use_container_width=True,
        hide_index=True
    )