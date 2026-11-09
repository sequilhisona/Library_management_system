import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import init_db
from src.auth import register_user, login_user
from src.books import add_book, search_books, list_all_books

def show_main_menu():
    print("\n=================================")
    print("    LIBRARY MANAGEMENT SYSTEM    ")
    print("=================================")
    print("1. Register Account")
    print("2. Login")
    print("3. Exit")
    return input("Select an option (1-3): ").strip()
