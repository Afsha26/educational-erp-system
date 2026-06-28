import streamlit as st
import pandas as pd
import io
import datetime
import matplotlib.pyplot as plt
from database.db import get_connection


def principal_reports():
    # =====================================
    # HEADER
    # =====================================

    st.markdown(
        f"""
    <div style="background:linear-gradient(135deg,#58339C,#9043B7);padding:20px;border-radius:12px;color:white;margin-bottom:12px;">
        <h2>📄 Institution Reports</h2>
        <p>Generate, preview and export institutional reports.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # =====================================
    # HELPERS
    # =====================================

    def load_departments(conn):
        q = "SELECT DISTINCT department FROM students WHERE department IS NOT NULL ORDER BY department"
        try:
            df = pd.read_sql_query(q, conn)
            return ["All"] + df["department"].dropna().astype(str).tolist()
        except Exception:
            return ["All"]

    def load_report(report_type, conn):
        if report_type == "Student Report":
            q = """
                SELECT student_id, roll_no, full_name, department, semester, division, email
                FROM students
            """
        elif report_type == "Teacher Report":
            q = """
                SELECT teacher_id, full_name, department, designation, email
                FROM teachers
            """
        elif report_type == "HOD Report":
            q = """
                SELECT hod_id, full_name, department, email
                FROM hods
            """
        elif report_type == "Subject Report":
            q = """
                SELECT subject_id, subject_name, department, semester, completion_percentage
                FROM subjects
            """
        elif report_type == "Announcement Report":
            q = """
                SELECT announcement_id, title, message, announcement_date, creator_role
                FROM announcements
                ORDER BY announcement_date DESC
            """
        else:  # Attendance
            q = """
                SELECT a.attendance_id, st.student_id, st.full_name AS student_name, st.roll_no,
                       st.department, st.semester, s.subject_name, l.lecture_date, a.status
                FROM attendance a
                JOIN lectures l ON a.lecture_id = l.lecture_id
                JOIN subjects s ON l.subject_id = s.subject_id
                JOIN students st ON a.student_id = st.student_id
                ORDER BY l.lecture_date DESC
            """
        return pd.read_sql_query(q, conn)

    def apply_filters(df, department, semester):
        if df is None or df.empty:
            return df
        if "department" in df.columns and department and department != "All":
            df = df[df["department"].astype(str) == str(department)]
        if "semester" in df.columns and semester and semester != "All":
            df = df[df["semester"].astype(str) == str(semester)]
        return df

    def show_summary(report_type, df):
        # summary metrics per report
        if df is None:
            df = pd.DataFrame()
        if report_type == "Student Report":
            total = len(df)
            departments = df["department"].nunique() if "department" in df.columns else 0
            semesters = df["semester"].nunique() if "semester" in df.columns else 0
            return {"Total Students": total, "Departments": departments, "Semesters": semesters}
        if report_type == "Teacher Report":
            total = len(df)
            departments = df["department"].nunique() if "department" in df.columns else 0
            designations = df["designation"].nunique() if "designation" in df.columns else 0
            return {"Total Teachers": total, "Departments": departments, "Designations": designations}
        if report_type == "HOD Report":
            total = len(df)
            departments = df["department"].nunique() if "department" in df.columns else 0
            return {"Total HODs": total, "Departments": departments}
        if report_type == "Subject Report":
            total = len(df)
            avg_completion = round(df["completion_percentage"].mean(), 2) if "completion_percentage" in df.columns and not df.empty else 0
            return {"Total Subjects": total, "Average Completion %": avg_completion}
        if report_type == "Attendance Report":
            total = len(df)
            present = len(df[df["status"] == "Present"]) if "status" in df.columns else 0
            absent = len(df[df["status"] == "Absent"]) if "status" in df.columns else 0
            attendance_pct = round((present / total) * 100, 2) if total > 0 else 0
            return {"Attendance %": attendance_pct, "Present Records": present, "Absent Records": absent}
        if report_type == "Announcement Report":
            total = len(df)
            principal = len(df[df.get("creator_role", "").astype(str) == "Principal"]) if "creator_role" in df.columns else 0
            hod = len(df[df.get("creator_role", "").astype(str) == "HOD"]) if "creator_role" in df.columns else 0
            return {"Total Announcements": total, "Principal Announcements": principal, "HOD Announcements": hod}
        return {}

    def draw_chart(report_type, df):
        if df is None or df.empty:
            return
        try:
            if report_type == "Student Report" and "department" in df.columns:
                data = df["department"].value_counts()
                fig, ax = plt.subplots()
                ax.bar(data.index.astype(str), data.values, color="#58339C")
                ax.set_title("Students by Department")
                ax.set_ylabel("Count")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            if report_type == "Teacher Report" and "department" in df.columns:
                data = df["department"].value_counts()
                fig, ax = plt.subplots()
                ax.bar(data.index.astype(str), data.values, color="#9043B7")
                ax.set_title("Teachers by Department")
                ax.set_ylabel("Count")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            if report_type == "Subject Report" and "department" in df.columns:
                data = df["department"].value_counts()
                fig, ax = plt.subplots()
                ax.bar(data.index.astype(str), data.values, color="#58339C")
                ax.set_title("Subjects by Department")
                ax.set_ylabel("Count")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            if report_type == "Attendance Report" and "status" in df.columns:
                data = df["status"].value_counts()
                fig, ax = plt.subplots()
                ax.pie(data.values, labels=data.index.astype(str), autopct="%1.1f%%", colors=["#58339C", "#9043B7"])
                ax.set_title("Attendance Distribution")
                ax.axis("equal")
                st.pyplot(fig)

            if report_type == "Announcement Report" and "creator_role" in df.columns:
                data = df["creator_role"].value_counts()
                fig, ax = plt.subplots()
                ax.bar(data.index.astype(str), data.values, color="#9043B7")
                ax.set_title("Announcements by Creator Role")
                ax.set_ylabel("Count")
                plt.xticks(rotation=45)
                st.pyplot(fig)
        except Exception:
            pass

    def export_report(df, report_type):
        today = datetime.date.today().isoformat()
        safe_name = report_type.replace(" ", "_")
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        towrite = io.BytesIO()
        with pd.ExcelWriter(towrite, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Report")
        towrite.seek(0)
        excel_bytes = towrite.read()
        return csv_bytes, excel_bytes, safe_name, today

    # =====================================
    # DYNAMIC FILTERS (loaded once)
    # =====================================

    conn = get_connection()
    try:
        departments = load_departments(conn)
    finally:
        conn.close()

    # =====================================
    # FILTERS
    # =====================================

    report_type = st.selectbox(
        "Report Type",
        [
            "Student Report",
            "Teacher Report",
            "HOD Report",
            "Subject Report",
            "Attendance Report",
            "Announcement Report",
        ],
    )

    department = st.selectbox("Department", departments)
    semester_options = ["All"] + [str(i) for i in range(1, 9)]
    semester = st.selectbox("Semester", semester_options)

    generate = st.button("Generate Report")

    display_df = pd.DataFrame()
    gen_on = ""

    # =====================================
    # LOAD DATA / QUERIES
    # =====================================

    if generate:

        conn = get_connection()

        # Load data once for the selected report
        df = load_report(report_type, conn)

        # Apply filters using pandas
        df = apply_filters(df, department, semester)

        # =====================================
        # SUMMARY METRICS
        # =====================================

        total_records = len(df)
        departments_included = df["department"].dropna().unique().tolist() if "department" in df.columns else []

        # =====================================
        # DISPLAY SUMMARY + METADATA
        # =====================================

        summary = show_summary(report_type, df)
        cols = st.columns(len(summary) if len(summary) > 0 else 1)
        for i, (k, v) in enumerate(summary.items()):
            try:
                cols[i].metric(k, v)
            except Exception:
                pass

        gen_by = st.session_state.get("user_fullname", "Principal")
        gen_on = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        s1, s2, s3 = st.columns(3)
        s1.write(f"**Generated By:** {gen_by}")
        s2.write(f"**Generated On:** {gen_on}")
        s3.write(f"**Record Count:** {total_records}")

        st.divider()

        # =====================================
        # PREVIEW DATAFRAME
        # =====================================

        display_df = df.copy()

        # Rename columns to user friendly
        display_df.rename(columns=lambda x: x.replace("_", " ").title(), inplace=True)

        if display_df.empty:
            st.info("📂 No data available.\n\nTry changing filters or adding records.")
            return

        # Format date columns
        for col in display_df.columns:
            if "date" in col.lower():
                try:
                    display_df[col] = pd.to_datetime(display_df[col]).dt.strftime("%Y-%m-%d")
                except Exception:
                    pass

        # Search
        search_term = st.text_input("Search within report")
        if search_term:
            mask = pd.Series(False, index=display_df.index)
            for col in display_df.select_dtypes(include=[object]).columns:
                mask = mask | display_df[col].astype(str).str.contains(search_term, case=False, na=False)
            display_df = display_df[mask]

        # Sorting
        sort_cols = display_df.columns.tolist()
        sort_by = st.selectbox("Sort By", ["None"] + sort_cols)
        sort_dir = st.radio("Order", ["Ascending", "Descending"], horizontal=True)
        if sort_by and sort_by != "None":
            display_df = display_df.sort_values(by=sort_by, ascending=(sort_dir == "Ascending"))

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # =====================================
        # CHARTS
        # =====================================

        draw_chart(report_type, df)

    st.divider()

    # =====================================
    # EXPORT SECTION
    # =====================================

    st.subheader("📤 Export Report")

    if not display_df.empty:
        csv_bytes, excel_bytes, safe_name, today = export_report(display_df, report_type)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button(
                "⬇ Download CSV",
                data=csv_bytes,
                file_name=f"{safe_name}_{today}.csv",
                mime="text/csv",
            )
        with c2:
            st.download_button(
                "⬇ Download Excel",
                data=excel_bytes,
                file_name=f"{safe_name}_{today}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        with c3:
            try:
                from reportlab.lib import colors
                from reportlab.lib.pagesizes import letter
                from reportlab.lib.styles import getSampleStyleSheet
                from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate, Table, TableStyle

                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter)
                elements = []
                styles = getSampleStyleSheet()

                elements.append(Paragraph(f"Generated On: {gen_on or 'N/A'}", styles["Normal"]))
                elements.append(Spacer(1, 12))

                table_data = [list(display_df.columns)] + display_df.head(200).astype(str).values.tolist()
                tbl = Table(table_data, repeatRows=1)
                tbl.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#58339C")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                        ]
                    )
                )

                elements.append(tbl)
                doc.build(elements)
                buffer.seek(0)
                pdf_bytes = buffer.read()

                st.download_button(
                    "Download PDF",
                    data=pdf_bytes,
                    file_name=f"{safe_name}_{today}.pdf",
                    mime="application/pdf",
                )
            except Exception:
                st.info("PDF export requires 'reportlab'. Install with: pip install reportlab")
    else:
        st.info("Generate a report first to export it.")

    try:
        conn.close()
    except Exception:
        pass

