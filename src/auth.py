import hashlib
from src.database import get_connection

def hash_password(password):
    """Simple SHA-256 password hashing for coursework."""
    return hashlib.sha256(password.encode()).hexdigest()
