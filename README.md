# Library Management System

A modular command-line Library Management System built with Python and SQLite.

## Project Structure
- `main.py` — Interactive CLI menu and user session loop.
- `src/database.py` — SQLite connection and core schema initialization.
- `src/auth.py` — User registration and login with SHA-256 password hashing and role-based access (`student` / `admin`).
- `src/books.py` — Book catalog management (add, list, and keyword search).
- `src/transactions.py` — Book borrowing, returning, stock updates, and user transaction history.

## How to Run
```bash
python3 main.py
