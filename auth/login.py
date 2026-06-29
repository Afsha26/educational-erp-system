import sqlite3

import streamlit as st
from auth.auth_service import authenticate


def login_page():

    # =====================================
    # PAGE CONFIG
    # =====================================

    st.html("""
    <style>

    .stApp{
        background-color:#F3EEF1;
    }

    .main-title{
        color:#58339C;
        font-size:42px;
        font-weight:bold;
        margin-bottom:5px;
    }

    .subtitle{
        color:#9043B7;
        font-size:18px;
        margin-bottom:5px;
    }

    .hero-title{
        color:#58339C;
        font-size:36px;
        font-weight:bold;
        margin-bottom:10px;
    }

    .feature-card{
        background:white;
        padding:20px;
        border-radius:15px;
        border-left:6px solid #9043B7;
        box-shadow:0px 3px 10px rgba(0,0,0,0.08);
        margin-bottom:15px;
    }

    .feature-title{
        color:#58339C;
        font-size:18px;
        font-weight:bold;
        margin-bottom:5px;
    }

    .feature-text{
        color:#555;
        font-size:14px;
    }

    .login-title{
        color:#58339C;
        text-align:center;
        margin-bottom:5px;
    }

    .login-subtitle{
        text-align:center;
        color:#666;
        margin-bottom:20px;
    }

    div.stButton > button{
        width:100%;
        background:#58339C;
        padding:20px;
        color:white;
        border:none;
        border-radius:10px;
        height:50px;
        font-size:18px;
        font-weight:bold;
    }

    div.stButton > button:hover{
        background:#9043B7;
        color:white;
    }

    </style>
    """)

    # =====================================
    # HEADER
    # =====================================

    col_logo, col_title = st.columns([1, 8])

    with col_logo:
        st.html("<h1>🎓</h1>")

    with col_title:
        st.html("""
        <div class='main-title'>
            Educational ERP
        </div>

        <div class='subtitle'>
            Smart Academic Management Platform
        </div>
        """)

    st.divider()

    # =====================================
    # MAIN BODY
    # =====================================

    left, right = st.columns([1.5, 1])

    # =====================================
    # LEFT PANEL
    # =====================================

    with left:

        st.html("""
        <div class='hero-title'>
            Manage Your Institution Efficiently
        </div>
        """)

        st.write("""
        Streamline attendance tracking, syllabus monitoring,
        academic reporting, announcements and communication
        through one centralized ERP platform.
        """)

        st.write("")

        # =====================================
        # LIVE METRICS
        # =====================================

        students_count = 0
        teachers_count = 0
        subjects_count = 0

        try:
            conn = sqlite3.connect("database/erp.db")
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM students")
            students_count = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM teachers")
            teachers_count = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM subjects")
            subjects_count = cursor.fetchone()[0] or 0

        except sqlite3.Error:
            students_count = 0
            teachers_count = 0
            subjects_count = 0

        finally:
            if "conn" in locals():
                conn.close()

        metric1, metric2, metric3 = st.columns(3)

        with metric1:
            st.metric("Students", f"{students_count}")

        with metric2:
            st.metric("Teachers", f"{teachers_count}")

        with metric3:
            st.metric("Subjects", f"{subjects_count}")

        st.write("")

        st.html("""
        <div class='feature-card'>
            <div class='feature-title'>
                📊 Attendance Analytics
            </div>
            <div class='feature-text'>
                Real-time attendance reports and insights.
            </div>
        </div>
        """)

        st.html("""
        <div class='feature-card'>
            <div class='feature-title'>
                📚 Syllabus Tracking
            </div>
            <div class='feature-text'>
                Monitor lecture coverage and subject completion.
            </div>
        </div>
        """)

        st.html("""
        <div class='feature-card'>
            <div class='feature-title'>
                📢 Announcements
            </div>
            <div class='feature-text'>
                Share notices and academic updates instantly.
            </div>
        </div>
        """)

        st.html("""
        <div class='feature-card'>
            <div class='feature-title'>
                💬 Communication Portal
            </div>
            <div class='feature-text'>
                Direct interaction between teachers and students.
            </div>
        </div>
        """)

    # =====================================
    # RIGHT PANEL (LOGIN)
    # =====================================

    with right:

        st.html("""
        <h2 class='login-title'>🔐 Login</h2>
        <p class='login-subtitle'>
            Access your ERP Dashboard
        </p>
        """)

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        if st.button("Login"):

            user = authenticate(username, password)

            if user:

                # Basic Session Data
                st.session_state.logged_in = True
                st.session_state.user_id = user["user_id"]
                st.session_state.username = user["username"]
                st.session_state.role = user["role"]

                # Student Data
                if "student_id" in user:
                    st.session_state.student_id = user["student_id"]

                if "full_name" in user:
                    st.session_state.full_name = user["full_name"]

                if "roll_no" in user:
                    st.session_state.roll_no = user["roll_no"]

                if "division" in user:
                    st.session_state.division = user["division"]
                
                if "semester" in user:
                    st.session_state.semester = user["semester"]
                    
                if "teacher_id" in user:
                    st.session_state.teacher_id = user["teacher_id"]

                if "department" in user:
                    st.session_state.department = user["department"]

                if "designation" in user:
                    st.session_state.designation = user["designation"]

                if "email" in user:
                    st.session_state.email = user["email"]
                    
                if "hod_id" in user:
                    st.session_state.hod_id = user["hod_id"]

                if "principal_id" in user:
                    st.session_state.principal_id = user["principal_id"]
                    
                st.success(
                    f"Welcome {user.get('full_name', user['username'])} 🎉"
                )
                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

    st.divider()

    st.caption(
        "Educational ERP • Attendance • Syllabus • Analytics • Communication"
    )