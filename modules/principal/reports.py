import streamlit as st

from modules.principal.dashboard import principal_dashboard
from modules.principal.subjects import principal_subjects
from modules.principal.hods import principal_hods
from modules.principal.announcements import principal_announcements
from modules.principal.analytics import principal_analytics
from modules.principal.reports import principal_reports


def principal_panel():

    # ==================================
    # SESSION STATE
    # ==================================

    if "principal_page" not in st.session_state:
        st.session_state.principal_page = "Dashboard"

    # ==================================
    # SIDEBAR
    # ==================================

    with st.sidebar:

        st.markdown("## 👨‍💼 Principal Panel")

        st.markdown("---")

        if st.button(
            "🏠 Dashboard",
            use_container_width=True
        ):
            st.session_state.principal_page = "Dashboard"

        if st.button(
            "📚 Subjects",
            use_container_width=True
        ):
            st.session_state.principal_page = "Subjects"

        if st.button(
            "👨‍💼 HODs",
            use_container_width=True
        ):
            st.session_state.principal_page = "HODs"

        if st.button(
            "📢 Announcements",
            use_container_width=True
        ):
            st.session_state.principal_page = "Announcements"

        if st.button(
            "📊 Analytics",
            use_container_width=True
        ):
            st.session_state.principal_page = "Analytics"

        if st.button(
            "📄 Reports",
            use_container_width=True
        ):
            st.session_state.principal_page = "Reports"

        st.markdown("---")

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()

    # ==================================
    # PAGE ROUTING
    # ==================================

    if st.session_state.principal_page == "Dashboard":
        principal_dashboard()

    elif st.session_state.principal_page == "Subjects":
        principal_subjects()

    elif st.session_state.principal_page == "HODs":
        principal_hods()

    elif st.session_state.principal_page == "Announcements":
        principal_announcements()

    elif st.session_state.principal_page == "Analytics":
        principal_analytics()

    elif st.session_state.principal_page == "Reports":
        principal_reports()