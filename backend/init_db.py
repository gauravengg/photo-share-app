#!/usr/bin/env python3
"""
Database initialization script
Run this to create all tables
"""

from models import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("✅ Database setup complete!")
    print("\nYou can now run the server with: python main.py")
