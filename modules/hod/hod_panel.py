import streamlit as st

from modules.hod.hod_dashboard import hod_dashboard
# from modules.hod.teachers import hod_teachers
# from modules.hod.syllabus import hod_syllabus
# from modules.hod.attendance import hod_attendance
from modules.hod.announcements import hod_announcements
from modules.hod.hod_queries import hod_queries


def hod_panel():

    # ==================================
    # SESSION STATE
    # ==================================

    if "hod_page" not in st.session_state:
        st.session_state.hod_page = "Dashboard"

    full_name = st.session_state.get(
        "full_name",
        "HOD"
    )

    department = st.session_state.get(
        "department",
        "Computer"
    )

    email = st.session_state.get(
        "email",
        "-"
    )

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
        padding:15px;
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
        font-size:18px;
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
                Head of Department Portal
            </div>

        </div>
        """)

        st.html(f"""
        <div class="profile-card">

            <div class="profile-name">
                {full_name}
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

        # ======================
        # DASHBOARD
        # ======================

        if st.button(
            " Dashboard",
            use_container_width=True
        ):
            st.session_state.hod_page = "Dashboard"
            st.rerun()

        # ======================
        # TEACHERS
        # ======================

        if st.button(
            " Teachers",
            use_container_width=True
        ):
            st.session_state.hod_page = "Teachers"
            st.rerun()

        # ======================
        # SYLLABUS
        # ======================

        if st.button(
            " Syllabus",
            use_container_width=True
        ):
            st.session_state.hod_page = "Syllabus"
            st.rerun()

        # ======================
        # ATTENDANCE
        # ======================

        if st.button(
            " Attendance Analytics",
            use_container_width=True
        ):
            st.session_state.hod_page = "Attendance"
            st.rerun()

        # ======================
        # ANNOUNCEMENTS
        # ======================

        if st.button(
            " Announcements",
            use_container_width=True
        ):
            st.session_state.hod_page = "Announcements"
            st.rerun()

        # ======================
        # QUERIES
        # ======================

        if st.button(
            " Student Queries",
            use_container_width=True
        ):
            st.session_state.hod_page = "Queries"
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

    page = st.session_state.hod_page

    if page == "Dashboard":

        hod_dashboard(st.session_state.user_id)

    # elif page == "Teachers":

    #     hod_teachers()

    # elif page == "Syllabus":

    #     hod_syllabus()

    # elif page == "Attendance":

    #     hod_attendance()

    elif page == "Announcements":

        hod_announcements(st.session_state.user_id)

    elif page == "Queries":

        hod_queries(st.session_state.user_id)