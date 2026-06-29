import streamlit as st
from database.db import get_connection


def principal_profile():

    st.markdown("""
    <style>
    .profile-page{
        background: #FBF9FF;
        padding:16px;
    }

    .card{
        background:white;
        border-radius:12px;
        padding:18px;
        box-shadow:0 2px 8px rgba(88,51,156,0.08);
    }

    .btn-primary{
        background:linear-gradient(90deg,#6A3EA8,#8B4BBF);
        color:white;
        border:none;
        padding:8px 14px;
        border-radius:10px;
        font-weight:600;
    }

    .btn-primary:disabled{opacity:0.6}

    .field-label{font-weight:600;margin-bottom:6px}

    .muted{color:#6B6B6B;font-size:14px}

    </style>
    """, unsafe_allow_html=True)

    st.title(" Principal Profile")

    user_id = st.session_state.get("user_id")
    principal_id = st.session_state.get("principal_id")

    if not user_id or not principal_id:
        st.error("Unable to locate session information. Please log in again.")
        return

    # Fetch profile from DB using JOIN
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT u.user_id, u.username, u.password, u.role,
               p.principal_id, p.full_name, p.email
        FROM users u
        JOIN principals p ON u.user_id = p.user_id
        WHERE p.principal_id = ?
        """,
        (principal_id,)
    )

    row = cursor.fetchone()

    if not row:
        conn.close()
        st.error("Profile not found.")
        return

    # Convert sqlite3.Row to dict-like access
    profile = dict(row)

    # Profile card
    with st.container():
        st.markdown(f"""
        <div class="card">
            <h3 style='margin:0'>{profile.get('full_name')}</h3>
            <div class='muted'>{profile.get('role')}</div>
            <div style='margin-top:8px'>📧 {profile.get('email')}</div>
            <div style='margin-top:4px' class='muted'>ID: {profile.get('principal_id')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Edit profile form
    with st.container():
        st.subheader("Edit Profile")
        with st.form("edit_profile_form"):
            name = st.text_input("Full Name", value=profile.get("full_name", ""))
            username = st.text_input("Username", value=profile.get("username", ""))
            email = st.text_input("Email", value=profile.get("email", ""))

            submitted = st.form_submit_button("💾 Save Changes")

            if submitted:
                # Validation
                if not name.strip():
                    st.error("Full Name cannot be empty.")
                elif not username.strip():
                    st.error("Username cannot be empty.")
                elif not email.strip():
                    st.error("Email cannot be empty.")
                else:
                    # ensure username unique (exclude current user)
                    cursor.execute(
                        "SELECT user_id FROM users WHERE username = ? AND user_id != ?",
                        (username.strip(), user_id)
                    )
                    conflict = cursor.fetchone()
                    if conflict:
                        st.error("Username already taken. Please choose another username.")
                    else:
                        try:
                            cursor.execute(
                                "UPDATE principals SET full_name = ?, email = ? WHERE principal_id = ?",
                                (name.strip(), email.strip(), principal_id)
                            )
                            cursor.execute(
                                "UPDATE users SET username = ? WHERE user_id = ?",
                                (username.strip(), user_id)
                            )
                            conn.commit()

                            # Update session state
                            st.session_state["full_name"] = name.strip()
                            st.session_state["username"] = username.strip()
                            st.session_state["email"] = email.strip()

                            st.success("Profile Updated Successfully")
                        except Exception as e:
                            conn.rollback()
                            st.error(f"Failed to update profile: {e}")

    st.divider()

    # Change password section
    with st.container():
        st.subheader("🔑 Change Password")
        with st.form("change_password_form"):
            current_pwd = st.text_input("Current Password", type="password")
            new_pwd = st.text_input("New Password", type="password")
            confirm_pwd = st.text_input("Confirm Password", type="password")

            pwd_submitted = st.form_submit_button("🔒 Change Password")

            if pwd_submitted:
                # Fetch latest password from DB for verification
                cursor.execute("SELECT password FROM users WHERE user_id = ?", (user_id,))
                db_pwd_row = cursor.fetchone()
                db_pwd = db_pwd_row[0] if db_pwd_row else None

                if db_pwd is None:
                    st.error("Unable to verify current password.")
                elif current_pwd != db_pwd:
                    st.error("Current password is incorrect.")
                elif new_pwd != confirm_pwd:
                    st.error("New password and confirmation do not match.")
                elif len(new_pwd) < 6:
                    st.error("New password must be at least 6 characters long.")
                else:
                    try:
                        cursor.execute(
                            "UPDATE users SET password = ? WHERE user_id = ?",
                            (new_pwd, user_id)
                        )
                        conn.commit()
                        st.success("Password Changed Successfully")
                    except Exception as e:
                        conn.rollback()
                        st.error(f"Failed to change password: {e}")

    # Close connection
    conn.close()
