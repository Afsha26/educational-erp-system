import streamlit as st

from auth.login import login_page

# Student
from modules.student.student_panel import student_panel
from modules.student.student_panel import student_panel

# Teacher
from modules.teacher.teacher_panel import teacher_panel

# HOD
from modules.hod.dashboard import hod_dashboard

# Principal
from modules.principal.dashboard import principal_dashboard
from modules.teacher.teacher_panel import teacher_panel

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    login_page()

else:

    role = st.session_state.role

    if role == "Student":
        student_panel()

    elif role == "Teacher":
        teacher_panel()

    elif role == "HOD":
        hod_dashboard()

    elif role == "Principal":
        principal_dashboard()

