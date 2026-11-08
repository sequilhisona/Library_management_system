import hashlib
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import get_connection

def hash_password(password):
    """Hash a plaintext password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, role="student"):
    """Register a new user into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pwd = hash_password(password)
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_pwd, role)
        )
        conn.commit()
        print(f"User '{username}' registered successfully as {role}!")
        return True
    except Exception:
        print("Error registering user: Username might already exist.")
        return False
    finally:
        conn.close()

def login_user(username, password):
    """Authenticate credentials against database records."""
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pwd = hash_password(password)
    
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hashed_pwd)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user:
        print(f"Login successful! Welcome, {user['username']} ({user['role']}).")
        return dict(user)
    else:
        print("Invalid username or password.")
        return None

if __name__ == "__main__":
    print("--- Testing Auth System ---")
    register_user("admin", "admin123", role="admin")
    login_user("admin", "admin123")
