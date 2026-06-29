import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px


def teacher_syllabus(user_id: int):

    conn = sqlite3.connect("database/erp.db")

    # ==================================
    # GET TEACHER ID
    # ==================================

    
    teacher_id=st.session_state.teacher_id
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
        <h2>📚 Syllabus Tracker</h2>

        <p>
            Monitor subject completion,
            update syllabus progress and
            track academic coverage.
        </p>
    </div>
    """)

    # ==================================
    # ASSIGNED SUBJECTS
    # ==================================

    subjects_df = pd.read_sql_query(
        """
        SELECT
        subject_id,
        subject_name,
        semester,
        completion_percentage
        FROM subjects
        WHERE teacher_id=?
        ORDER BY semester
        """,
        conn,
        params=(teacher_id,)
    )

    if subjects_df.empty:

        st.warning(
            "No subjects assigned."
        )

        conn.close()
        return

    # ==================================
    # QUICK STATS
    # ==================================

    total_subjects = len(subjects_df)

    avg_completion = round(
        subjects_df[
            "completion_percentage"
        ].mean(),
        2
    )

    completed_subjects = len(
        subjects_df[
            subjects_df[
                "completion_percentage"
            ] >= 100
        ]
    )

    pending_subjects = total_subjects - completed_subjects

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Subjects",
            total_subjects
        )

    with col2:
        st.metric(
            "Average Progress",
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
    # UPDATE PROGRESS
    # ==================================

    st.subheader(
        "✏️ Update Syllabus Progress"
    )

    selected_subject = st.selectbox(
        "Select Subject",
        subjects_df["subject_name"]
    )

    current_progress = subjects_df[
        subjects_df["subject_name"]
        == selected_subject
    ].iloc[0]["completion_percentage"]

    progress = st.slider(
        "Completion Percentage",
        0,
        100,
        int(current_progress)
    )

    if st.button(
        "💾 Update Progress",
        use_container_width=True
    ):

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE subjects
            SET completion_percentage=?
            WHERE subject_name=?
            """,
            (
                progress,
                selected_subject
            )
        )

        conn.commit()

        st.success(
            "Progress Updated Successfully"
        )

        st.rerun()

    st.divider()

    # ==================================
    # SUBJECT TABLE
    # ==================================

    st.subheader(
        "📖 Assigned Subjects"
    )

    display_df = subjects_df.copy()

    display_df.rename(
        columns={
            "subject_name":"Subject",
            "semester":"Semester",
            "completion_percentage":"Completion %"
        },
        inplace=True
    )

    st.dataframe(
        display_df[
            [
                "Subject",
                "Semester",
                "Completion %"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================
    # ANALYTICS
    # ==================================

    st.subheader(
        "📈 Syllabus Completion Analytics"
    )

    analytics_df = pd.DataFrame({

        "Subject":
            subjects_df["subject_name"],

        "Completion":
            subjects_df[
                "completion_percentage"
            ]
    })

    fig = px.bar(
        analytics_df,
        x="Subject",
        y="Completion",
        text="Completion",
        title="Subject Completion Percentage"
    )

    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_range=[0,100],
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================
    # BEHIND SCHEDULE
    # ==================================

    st.subheader(
        "⚠️ Subjects Requiring Attention"
    )

    low_df = subjects_df[
        subjects_df[
            "completion_percentage"
        ] < 60
    ]

    if low_df.empty:

        st.success(
            "All subjects are progressing well."
        )

    else:

        st.dataframe(
            low_df[
                [
                    "subject_name",
                    "semester",
                    "completion_percentage"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    conn.close()