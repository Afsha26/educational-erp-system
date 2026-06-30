import streamlit as st

from auth.login import login_page

# Student
from modules.principal.principal_panel import principal_panel
from modules.student.student_panel import student_panel

# Teacher
from modules.teacher.teacher_panel import teacher_panel

# HOD
from modules.hod.hod_panel import hod_panel

# Principal
from modules.principal.dashboard import principal_dashboard
from modules.teacher.teacher_panel import teacher_panel

from database.admin_rec import create_default_principal
from database.init_db import init_db
from database.sample_data import sample_data


if "db_setup_completed" not in st.session_state:
    st.session_state.db_setup_completed = False

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    if not st.session_state.db_setup_completed:
        if "db_setup_choice" not in st.session_state:
            st.session_state.db_setup_choice = "Create empty database with default principal"

        setup_choice = st.sidebar.radio(
            "Database setup",
            [
                "Create empty database with default principal",
                "Load sample ERP system",
            ],
            key="db_setup_choice",
        )

        if st.sidebar.button("Initialize database"):
            init_db()

            if setup_choice == "Create empty database with default principal":
                create_default_principal()
            else:
                sample_data()

            st.session_state.db_setup_completed = True

    login_page()

else:

    role = st.session_state.role

    if role == "Student":
        student_panel()

    elif role == "Teacher":
        teacher_panel()

    elif role == "HOD":
        hod_panel()

    elif role == "Principal":
        principal_panel()