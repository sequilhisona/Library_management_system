import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import get_connection

def add_book(title, author, genre, total_copies):
    """Add a new book record to the library catalog."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO books (title, author, genre, total_copies, available_copies)
               VALUES (?, ?, ?, ?, ?)""",
            (title, author, genre, total_copies, total_copies)
        )
        conn.commit()
        print(f"Book '{title}' added successfully!")
        return True
    except Exception as e:
        print(f"Error adding book: {e}")
        return False
    finally:
        conn.close()

def search_books(keyword):
    """Search books by title, author, or genre."""
    conn = get_connection()
    cursor = conn.cursor()
    query = "%" + keyword + "%"
    cursor.execute(
        """SELECT * FROM books 
           WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?""",
        (query, query, query)
    )
    books = cursor.fetchall()
    conn.close()
    return [dict(b) for b in books]

def list_all_books():
    """Retrieve all books currently in inventory."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return [dict(b) for b in books]

if __name__ == "__main__":
    print("--- Testing Book Management ---")
    add_book("Clean Code", "Robert C. Martin", "Programming", 5)
    add_book("The Pragmatic Programmer", "Andrew Hunt", "Programming", 3)
    
    print("\nAll Books:")
    for b in list_all_books():
        print(f"[{b['book_id']}] {b['title']} by {b['author']} (Available: {b['available_copies']}/{b['total_copies']})")
