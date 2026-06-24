import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database.db import get_connection


def hod_syllabus():

    st.markdown("""
    <div style="
        background:linear-gradient(
            135deg,
            #58339C,
            #9043B7
        );
        padding:25px;
        border-radius:15px;
        color:white;
        margin-bottom:20px;
    ">
        <h2>📚 Syllabus Monitoring</h2>
        <p>Track syllabus completion across the department</p>
    </div>
    """, unsafe_allow_html=True)

    conn = get_connection()

    # ==================================
    # SUBJECT DATA
    # ==================================

    query = """
    SELECT
        s.subject_name,
        s.semester,
        s.completion_percentage,
        t.full_name AS teacher_name
    FROM subjects s

    LEFT JOIN teachers t
        ON s.teacher_id = t.teacher_id

    ORDER BY s.semester
    """

    df = pd.read_sql_query(query, conn)

    # ==================================
    # KPI CARDS
    # ==================================

    total_subjects = len(df)

    avg_completion = round(
        df["completion_percentage"].mean(),
        2
    )

    completed_subjects = len(
        df[df["completion_percentage"] >= 100]
    )

    pending_subjects = len(
        df[df["completion_percentage"] < 100]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Subjects",
            total_subjects
        )

    with col2:
        st.metric(
            "Avg Completion",
            f"{avg_completion}%"
        )

    with col3:
        st.metric(
            "Completed",
            completed_subjects
        )

    with col4:
        st.metric(
            "Pending",
            pending_subjects
        )

    st.divider()

    # ==================================
    # OVERALL COMPLETION PIE CHART
    # ==================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📊 Completion Status")

        completed = len(
            df[df["completion_percentage"] >= 75]
        )

        lagging = len(
            df[df["completion_percentage"] < 75]
        )

        fig, ax = plt.subplots()

        ax.pie(
            [completed, lagging],
            labels=[
                "On Track",
                "Needs Attention"
            ],
            autopct="%1.1f%%"
        )

        st.pyplot(fig)

    # ==================================
    # SUBJECT WISE COMPLETION
    # ==================================

    with col2:

        st.subheader("📈 Subject Completion")

        chart_df = df[
            [
                "subject_name",
                "completion_percentage"
            ]
        ]

        st.bar_chart(
            chart_df.set_index(
                "subject_name"
            )
        )

    st.divider()

    # ==================================
    # LOW COMPLETION SUBJECTS
    # ==================================

    st.subheader(
        "⚠ Subjects Needing Attention"
    )

    low_df = df[
        df["completion_percentage"] < 75
    ]

    if not low_df.empty:

        st.dataframe(
            low_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "All subjects are progressing well."
        )

    st.divider()

    # ==================================
    # TEACHER WISE COMPLETION
    # ==================================

    st.subheader(
        "👨‍🏫 Teacher-wise Completion"
    )

    teacher_df = (
        df.groupby("teacher_name")
        ["completion_percentage"]
        .mean()
        .reset_index()
    )

    teacher_df.rename(
        columns={
            "completion_percentage":
            "average_completion"
        },
        inplace=True
    )

    st.bar_chart(
        teacher_df.set_index(
            "teacher_name"
        )
    )

    st.dataframe(
        teacher_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================
    # SEMESTER FILTER
    # ==================================

    st.subheader(
        "🔍 Semester-wise Monitoring"
    )

    semesters = sorted(
        df["semester"].unique()
    )

    selected_semester = st.selectbox(
        "Select Semester",
        semesters
    )

    semester_df = df[
        df["semester"] ==
        selected_semester
    ]

    st.dataframe(
        semester_df,
        use_container_width=True,
        hide_index=True
    )

    conn.close()