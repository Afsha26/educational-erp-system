import sqlite3
import os

DATABASE_PATH = "database/erp.db"

DEFAULT_USERNAME = "principal"
DEFAULT_PASSWORD = "principal123"  # Change after first login
DEFAULT_ROLE = "Principal"
DEFAULT_NAME = "System Principal"
DEFAULT_EMAIL = "principal@erp.com"


def create_default_principal():
    # Ensure database folder exists
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Check whether principal user already exists
    cursor.execute(
        "SELECT user_id FROM users WHERE username = ?",
        (DEFAULT_USERNAME,)
    )

    user = cursor.fetchone()

    if user:
        print("Default Principal already exists.")
    else:
        # Insert into users table
        cursor.execute("""
            INSERT INTO users(username, password, role)
            VALUES (?, ?, ?)
        """, (
            DEFAULT_USERNAME,
            DEFAULT_PASSWORD,
            DEFAULT_ROLE
        ))

        user_id = cursor.lastrowid

        # Insert into principals table
        cursor.execute("""
            INSERT INTO principals(user_id, full_name, email)
            VALUES (?, ?, ?)
        """, (
            user_id,
            DEFAULT_NAME,
            DEFAULT_EMAIL
        ))

        conn.commit()
        print("Default Principal created successfully.")

        print("\n========== DEFAULT LOGIN ==========")
        print(f"Username : {DEFAULT_USERNAME}")
        print(f"Password : {DEFAULT_PASSWORD}")
        print("===================================\n")

    conn.close()


if __name__ == "__main__":
    create_default_principal()