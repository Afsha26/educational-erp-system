import streamlit as st

from modules.student.dashboard import show_dashboard
from modules.student.attendance import show_attendance
from modules.student.announcements import show_announcements
from modules.student.queries import ask_query


def student_panel():

    # ==================================
    # SESSION STATE
    # ==================================

    if "student_page" not in st.session_state:
        st.session_state.student_page = "Dashboard"

    # ==================================
    # CSS
    # ==================================

    st.html("""
    <style>

    section[data-testid="stSidebar"]{
        background:linear-gradient(
            180deg,
            #58339C 0%,
            #9043B7 100%
        );
    }

    .sidebar-header{
        text-align:center;
    }

    .sidebar-title{
        color:white;
        font-size:24px;
        font-weight:bold;
    }

    .sidebar-subtitle{
        color:#F3EEF1;
        font-size:14px;
    }

    section[data-testid="stSidebar"] div.stButton > button{
        background:white;
        color:#58339C;
        border-left:6px solid #9043B7;
        border:1px solid #E0D4F0;
        border-radius:12px;
        font-weight:bold;
        height:48px;
        width:100%;
        margin-bottom:8px;
        text-align:center;
        font-size:20px;
    }

    section[data-testid="stSidebar"] div.stButton > button:hover{
        background:#F3EEF1;
        color:#58339C;
    }

    </style>
    """)

    # ==================================
    # USER INFO
    # ==================================

    student_name = st.session_state.get(
        "full_name",
        "Student"
    )
    student_rollno = st.session_state.get(
        "roll_no",
        "Student"
    )
    student_id = st.session_state.get(
        "student_id",
        "-"
    )
    student_department = st.session_state.get(
        "department",
        "-"
    )
    student_semester = st.session_state.get(
        "semester",
        "-"
    )
    student_division = st.session_state.get(
        "division",
        "-"
    )
    student_email = st.session_state.get(
        "email",
        "-"
    )

    # ==================================
    # SIDEBAR
    # ==================================

    with st.sidebar:

        st.html("""
        <div class="sidebar-header">

            <h1>🎓</h1>

            <div class="sidebar-title">
                Educational ERP
            </div>

            <div class="sidebar-subtitle">
                Student Portal
            </div>

        </div>
        """)

        st.markdown("---")

        st.html(f"""
        <div style="
        background:rgba(255,255,255,0.15);
        padding:15px;
        border-radius:12px;
        margin-bottom:10px;
        ">

        <div style="
            color:white;
            font-size:18px;
            font-weight:bold;
        ">
            {student_name}
        </div>

        <div style="
            color:#E8DDF5;
            font-size:14px;
            margin-top:6px;
        ">
            Roll No: {student_rollno}
        </div>

        <div style="
            color:#E8DDF5;
            font-size:13px;
            margin-top:4px;
        ">
            Student ID: {student_id}
        </div>

        <div style="
            color:#E8DDF5;
            font-size:13px;
            margin-top:2px;
        ">
            Department: {student_department}
        </div>

        <div style="
            color:#E8DDF5;
            font-size:13px;
            margin-top:2px;
        ">
            Semester: {student_semester}
        </div>

        <div style="
            color:#E8DDF5;
            font-size:13px;
            margin-top:2px;
        ">
            Division: {student_division}
        </div>

        <div style="
            color:#E8DDF5;
            font-size:13px;
            margin-top:2px;
        ">
            Email: {student_email}
        </div>

        </div>
        """)

        st.html("""
        <div style="
            color:white;
            font-size:18px;
            font-weight:bold;
            margin-bottom:10px;
        ">
            Navigation
        </div>
        """)

        # ==========================
        # Navigation Buttons
        # ==========================

        if st.button(
            "Dashboard",
            use_container_width=True
        ):
            st.session_state.student_page = "Dashboard"
            st.rerun()

        if st.button(
            "Attendance",
            use_container_width=True
        ):
            st.session_state.student_page = "Attendance"
            st.rerun()

        if st.button(
            "Announcements",
            use_container_width=True
        ):
            st.session_state.student_page = "Announcements"
            st.rerun()

        if st.button(
            "Queries",
            use_container_width=True
        ):
            st.session_state.student_page = "Queries"
            st.rerun()

        st.markdown("---")

        # ==========================
        # Logout
        # ==========================

        if st.button(
            "Logout",
            use_container_width=True
        ):
            st.session_state.clear()
            st.rerun()

    # ==================================
    # ROUTING
    # ==================================

    page = st.session_state.student_page

    if page == "Dashboard":
        show_dashboard()

    elif page == "Attendance":
        show_attendance(
            st.session_state.user_id
        )

    elif page == "Announcements":
        show_announcements(
            st.session_state.user_id
        )

    elif page == "Queries":
        ask_query(
            st.session_state.user_id
        )