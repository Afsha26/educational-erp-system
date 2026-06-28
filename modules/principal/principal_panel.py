import streamlit as st

from .dashboard import principal_dashboard
from .subjects import principal_subjects
from .hods import principal_hods
from .announcements import principal_announcements
from .analytics import principal_analytics
from .reports import principal_reports


def principal_panel():

    # ==================================
    # SESSION STATE
    # ==================================

    if "principal_page" not in st.session_state:
        st.session_state.principal_page = "Dashboard"

    full_name = st.session_state.get(
        "full_name",
        "Principal"
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

            <h1>🏛️</h1>

            <div class="sidebar-title">
                Educational ERP
            </div>

            <div class="sidebar-subtitle">
                Principal Portal
            </div>

        </div>
        """)

        st.html(f"""
        <div class="profile-card">

            <div class="profile-name">
                {full_name}
            </div>

            <div class="profile-info">
                Principal
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
            st.session_state.principal_page = "Dashboard"
            st.rerun()

        # ======================
        # SUBJECTS
        # ======================

        if st.button(
            " Subjects",
            use_container_width=True
        ):
            st.session_state.principal_page = "Subjects"
            st.rerun()
        # ======================
        # teachers
        # ======================
        if st.button(
            " Teachers",   
            use_container_width=True
        ):
            st.session_state.principal_page = "Teachers"
            st.rerun()
        # ======================
        # HODS
        # ======================

        if st.button(
            " HOD Management",
            use_container_width=True
        ):
            st.session_state.principal_page = "HODs"
            st.rerun()

        # ======================
        # ANNOUNCEMENTS
        # ======================

        if st.button(
            " Announcements",
            use_container_width=True
        ):
            st.session_state.principal_page = "Announcements"
            st.rerun()

        # ======================
        # ANALYTICS
        # ======================

        if st.button(
            " Analytics",
            use_container_width=True
        ):
            st.session_state.principal_page = "Analytics"
            st.rerun()

        # ======================
        # REPORTS
        # ======================

        if st.button(
            " Reports",
            use_container_width=True
        ):
            st.session_state.principal_page = "Reports"
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

    page = st.session_state.principal_page

    if page == "Dashboard":

        principal_dashboard()

    elif page == "Subjects":

        principal_subjects()

    elif page == "HODs":

        principal_hods()

    elif page == "Announcements":

        principal_announcements()

    elif page == "Analytics":

        principal_analytics()

    elif page == "Reports":

        principal_reports()