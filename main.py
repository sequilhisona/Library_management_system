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

def show_user_menu(user):
    while True:
        print(f"\n--- Welcome, {user['username']} ({user['role'].capitalize()}) ---")
        print("1. View All Books")
        print("2. Search Books")
        if user['role'].lower() == 'admin':
            print("3. Add New Book")
        print("0. Logout")
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            books = list_all_books()
            print(f"\n--- Catalog ({len(books)} Books) ---")
            for b in books:
                print(f"[{b['book_id']}] {b['title']} by {b['author']} | Genre: {b['genre']} | Available: {b['available_copies']}/{b['total_copies']}")
        elif choice == '2':
            keyword = input("Enter title, author, or genre to search: ").strip()
            results = search_books(keyword)
            print(f"\n--- Search Results ({len(results)} Found) ---")
            for b in results:
                print(f"[{b['book_id']}] {b['title']} by {b['author']} | Genre: {b['genre']} | Available: {b['available_copies']}/{b['total_copies']}")
        elif choice == '3' and user['role'].lower() == 'admin':
            title = input("Book Title: ").strip()
            author = input("Author: ").strip()
            genre = input("Genre: ").strip()
            copies = int(input("Total Copies: ").strip() or 1)
            add_book(title, author, genre, copies)
        elif choice == '0':
            print("Logging out...")
            break
        else:
            print("Invalid option. Please try again.")

def main():
    # Ensure database tables exist
    init_db()
    
    while True:
        choice = show_main_menu()
        
        if choice == '1':
            print("\n--- Register User ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            role = input("Role (student/admin) [default: student]: ").strip() or "student"
            register_user(username, password, role)
        elif choice == '2':
            print("\n--- User Login ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user = login_user(username, password)
            if user:
                show_user_menu(user)
        elif choice == '3':
            print("Thank you for using the Library Management System. Goodbye!")
            sys.exit()
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
