import streamlit as st
import sqlite3
import pandas as pd


def principal_reports():
    st.title("Principal Reports")
    st.write("Generate academic and administrative reports for the institution.")

    conn = sqlite3.connect("database/erp.db")

    total_students = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM students",
        conn
    )["total"][0]

    total_teachers = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM teachers",
        conn
    )["total"][0]

    average_attendance = pd.read_sql_query(
        "SELECT AVG(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) * 100 AS attendance_pct FROM attendance",
        conn
    )["attendance_pct"][0]

    passed_reports = pd.read_sql_query(
        "SELECT department, COUNT(*) AS subject_count FROM subjects GROUP BY department",
        conn
    )

    conn.close()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", total_students)
    col2.metric("Total Teachers", total_teachers)
    col3.metric("Average Attendance", f"{average_attendance:.2f}%")

    st.subheader("Subject Count by Department")
    st.dataframe(passed_reports)

    st.info("This is a sample report view. Extend it with custom filters and export options.")
