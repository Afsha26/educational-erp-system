import streamlit as st

from database.db import get_connection

from modules.teacher.dashboard import  teacher_dashboard
from modules.teacher.attendance import teacher_attendance
from modules.teacher.syllabus import teacher_syllabus
from modules.teacher.announcements import teacher_announcements
from modules.teacher.queries import teacher_queries


def teacher_panel():

    # ==================================
    # SESSION STATE
    # ==================================

    if "teacher_page" not in st.session_state:
        st.session_state.teacher_page = "Dashboard"

    full_name = st.session_state.get("full_name", "Teacher")
    department = st.session_state.get("department", "-")
    designation = st.session_state.get("designation", "-")
    email = st.session_state.get("email", "-")
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
        padding:8px 15px 6px;
        margin-bottom:0;
    }

    .sidebar-header h1{
        margin:0;
        font-size:32px;
        line-height:1.1;
    }

    .sidebar-title{
        color:white;
        font-size:24px;
        font-weight:bold;
        margin:0;
    }

    .sidebar-subtitle{
        color:#F3EEF1;
        font-size:14px;
        margin:0;
    }

    .profile-card{
        background:rgba(255,255,255,0.12);
        border:1px solid rgba(255,255,255,0.2);
        padding:15px;
        border-radius:15px;
        margin-bottom:15px;
        color:white;
    }

    .profile-name{
        font-size:18px;
        font-weight:bold;
    }

    .profile-info{
        font-size:13px;
        opacity:0.9;
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
                Teacher Portal
            </div>

        </div>
        """)
        cols = st.columns([1, 2, 1])
        cols[1].image("assets/logo.png", width=180)
        st.html(f"""
        <div class="profile-card">

            <div class="profile-name">
                {full_name}
            </div>

            <div class="profile-info">
                {designation}
            </div>

            <div class="profile-info">
                {department} Department
            </div>

            <div class="profile-info">
                {email}
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
        # DASHBOARD
        # ==========================

        if st.button(
            " Dashboard",
            use_container_width=True
        ):
            st.session_state.teacher_page = "Dashboard"
            st.rerun()

        # ==========================
        # ATTENDANCE
        # ==========================

        if st.button(
            " Attendance",
            use_container_width=True
        ):
            st.session_state.teacher_page = "Attendance"
            st.rerun()

        # ==========================
        # SYLLABUS
        # ==========================

        if st.button(
            " Syllabus",
            use_container_width=True
        ):
            st.session_state.teacher_page = "Syllabus"
            st.rerun()

        # ==========================
        # ANNOUNCEMENTS
        # ==========================

        if st.button(
            " Announcements",
            use_container_width=True
        ):
            st.session_state.teacher_page = "Announcements"
            st.rerun()

        # ==========================
        # QUERIES
        # ==========================

        if st.button(
            " Student Queries",
            use_container_width=True
        ):
            st.session_state.teacher_page = "Queries"
            st.rerun()

        st.markdown("---")

        if st.button(
            " Logout",
            use_container_width=True
        ):
            st.session_state.clear()
            st.rerun()

    # ==================================
    # PAGE ROUTING
    # ==================================

    page = st.session_state.teacher_page

    if page == "Dashboard":

        teacher_dashboard()

    elif page == "Attendance":

        teacher_attendance(
            st.session_state.user_id
        )

    elif page == "Syllabus":

        teacher_syllabus(
            st.session_state.user_id
        )

    elif page == "Announcements":

        teacher_announcements(
            st.session_state.user_id
        )

    elif page == "Queries":

        teacher_queries(
            st.session_state.user_id
        )