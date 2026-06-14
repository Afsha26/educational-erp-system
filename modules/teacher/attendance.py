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
    # QUICK STATS
    # ==================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Students",
            "120"
        )

    with col2:
        st.metric(
            "Present",
            "105"
        )

    with col3:
        st.metric(
            "Absent",
            "15"
        )

    with col4:
        st.metric(
            "Attendance %",
            "87.5%"
        )

    st.divider()

    # ==================================
    # MARK ATTENDANCE
    # ==================================

    st.subheader("✅ Mark Attendance")

    col1, col2, col3 = st.columns(3)

    with col1:

        subject = st.selectbox(
            "Subject",
            [
                "DBMS",
                "Operating System",
                "Computer Network",
                "Java",
                "Python"
            ]
        )

    with col2:

        division = st.selectbox(
            "Division",
            [
                "A",
                "B",
                "C"
            ]
        )

    with col3:

        lecture_date = st.date_input(
            "Lecture Date"
        )

    st.info(
        f"Attendance Sheet : {subject} | Division {division}"
    )

    attendance_df = pd.DataFrame({

        "Roll No": [
            "CE101",
            "CE102",
            "CE103",
            "CE104",
            "CE105"
        ],

        "Student Name": [
            "Afsha Shaikh",
            "Ayesha Khan",
            "Mohammed Ali",
            "Sara Khan",
            "Zain Sheikh"
        ],

        "Status": [
            True,
            True,
            False,
            True,
            True
        ]
    })

    edited_df = st.data_editor(
        attendance_df,
        use_container_width=True,
        hide_index=True
    )

    if st.button(
        "💾 Save Attendance",
        use_container_width=True
    ):
        st.success(
            "Attendance saved successfully."
        )

    st.divider()

    # ==================================
    # SUBJECT ATTENDANCE ANALYTICS
    # ==================================

    st.subheader(
        "📈 Subject Attendance Analytics"
    )

    analytics_df = pd.DataFrame({

        "Subject": [
            "DBMS",
            "OS",
            "CN",
            "Java",
            "Python"
        ],

        "Attendance": [
            90,
            84,
            78,
            92,
            87
        ]
    })

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
        yaxis_range=[0,100],
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

    st.subheader(
        "📅 Monthly Attendance Trend"
    )

    trend_df = pd.DataFrame({

        "Month": [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun"
        ],

        "Attendance": [
            82,
            84,
            86,
            88,
            85,
            87
        ]
    })

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

    st.subheader(
        "⚠️ Low Attendance Students"
    )

    low_df = pd.DataFrame({

        "Roll No": [
            "CE110",
            "CE114",
            "CE118"
        ],

        "Student Name": [
            "Student A",
            "Student B",
            "Student C"
        ],

        "Attendance %": [
            62,
            58,
            67
        ]
    })

    st.dataframe(
        low_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================
    # RECENT ATTENDANCE
    # ==================================

    st.subheader(
        "📖 Recent Attendance Sessions"
    )

    sessions_df = pd.DataFrame({

        "Date": [
            "10-06-2026",
            "09-06-2026",
            "08-06-2026"
        ],

        "Subject": [
            "DBMS",
            "OS",
            "Java"
        ],

        "Division": [
            "A",
            "A",
            "B"
        ],

        "Attendance %": [
            92,
            85,
            88
        ]
    })

    st.dataframe(
        sessions_df,
        use_container_width=True,
        hide_index=True
    )