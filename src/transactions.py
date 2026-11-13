import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import get_connection

def init_transactions_table():
    """Create the transactions table if it does not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            borrow_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT DEFAULT 'borrowed',
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
    """)
    conn.commit()
    conn.close()

def borrow_book(user_id, book_id):
    """Borrow an available book and decrement available_copies."""
    init_transactions_table()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT title, available_copies FROM books WHERE book_id = ?", (book_id,))
    book = cursor.fetchone()
    
    if not book:
        print("Book ID not found.")
        conn.close()
        return False
    if book["available_copies"] <= 0:
        print(f"Sorry, '{book['title']}' is currently out of stock.")
        conn.close()
        return False
        
    borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO transactions (user_id, book_id, borrow_date, status) VALUES (?, ?, ?, 'borrowed')",
        (user_id, book_id, borrow_date)
    )
    cursor.execute(
        "UPDATE books SET available_copies = available_copies - 1 WHERE book_id = ?",
        (book_id,)
    )
    conn.commit()
    conn.close()
    print(f"Successfully borrowed '{book['title']}'!")
    return True

def return_book(transaction_id):
    """Return a borrowed book and increment available_copies."""
    init_transactions_table()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT book_id, status FROM transactions WHERE transaction_id = ?",
        (transaction_id,)
    )
    tx = cursor.fetchone()
    
    if not tx:
        print("Transaction ID not found.")
        conn.close()
        return False
    if tx["status"] == "returned":
        print("This book has already been returned.")
        conn.close()
        return False
        
    return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "UPDATE transactions SET return_date = ?, status = 'returned' WHERE transaction_id = ?",
        (return_date, transaction_id)
    )
    cursor.execute(
        "UPDATE books SET available_copies = available_copies + 1 WHERE book_id = ?",
        (tx["book_id"],)
    )
    conn.commit()
    conn.close()
    print("Book returned successfully!")
    return True

def list_user_transactions(user_id):
    """List all active and past transactions for a user."""
    init_transactions_table()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.transaction_id, b.title, t.borrow_date, t.return_date, t.status
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        WHERE t.user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
