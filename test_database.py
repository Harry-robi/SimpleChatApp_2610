#!/usr/bin/env python3
"""
Test script to verify database storage and retrieval functionality
"""
import sqlite3
import os

# Import the database functions from web_server
from web_server import DB_NAME, init_database, save_message, get_message_history

def test_database():
    print("=" * 50)
    print("Database Storage & Retrieval Test")
    print("=" * 50)
    
    # Step 1: Initialize the database
    print("\n1. Initializing database...")
    init_database()
    
    # Verify the database file was created
    if os.path.exists(DB_NAME):
        print(f"   ✓ Database file '{DB_NAME}' created successfully")
    else:
        print(f"   ✗ ERROR: Database file '{DB_NAME}' was not created")
        return
    
    # Step 2: Test saving messages
    print("\n2. Testing message storage...")
    
    # Save different types of messages
    test_messages = [
        ("Hello, everyone!", "Alice", "regular"),
        ("Bob joined the chat!", "Bob", "system_join"),
        ("How are you?", "Bob", "regular"),
        ("I'm doing great!", "Alice", "regular"),
        ("Charlie joined the chat!", "Charlie", "system_join"),
        ("Bob left the chat!", "Bob", "system_leave"),
    ]
    
    for content, nickname, msg_type in test_messages:
        save_message(content, nickname=nickname, message_type=msg_type)
        print(f"   ✓ Saved: [{msg_type}] {nickname}: {content}")
    
    # Step 3: Retrieve and display messages
    print("\n3. Testing message retrieval...")
    history = get_message_history(limit=100)
    
    print(f"   Retrieved {len(history)} messages from database:\n")
    print("   " + "-" * 60)
    for content, nickname, timestamp, msg_type in history:
        print(f"   [{msg_type:12}] {nickname or 'System':10} | {content}")
    print("   " + "-" * 60)
    
    # Step 4: Verify data directly in SQLite
    print("\n4. Direct database verification...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check table structure
    cursor.execute("PRAGMA table_info(messages)")
    columns = cursor.fetchall()
    print("   Table structure:")
    for col in columns:
        print(f"      - {col[1]} ({col[2]})")
    
    # Count messages
    cursor.execute("SELECT COUNT(*) FROM messages")
    count = cursor.fetchone()[0]
    print(f"\n   Total messages in database: {count}")
    
    # Count by message type
    cursor.execute("SELECT message_type, COUNT(*) FROM messages GROUP BY message_type")
    type_counts = cursor.fetchall()
    print("   Messages by type:")
    for msg_type, cnt in type_counts:
        print(f"      - {msg_type}: {cnt}")
    
    conn.close()
    
    print("\n" + "=" * 50)
    print("✓ All database tests completed successfully!")
    print("=" * 50)

def view_all_messages():
    """View all messages currently in the database"""
    if not os.path.exists(DB_NAME):
        print(f"Database '{DB_NAME}' does not exist. Run test_database() first or start the server.")
        return
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, nickname, timestamp, message_type FROM messages ORDER BY timestamp")
    messages = cursor.fetchall()
    conn.close()
    
    print(f"\nAll messages in '{DB_NAME}':")
    print("-" * 80)
    print(f"{'ID':4} | {'Type':12} | {'Nickname':12} | {'Content':30} | {'Timestamp'}")
    print("-" * 80)
    for msg_id, content, nickname, timestamp, msg_type in messages:
        print(f"{msg_id:4} | {msg_type:12} | {nickname or 'System':12} | {content[:30]:30} | {timestamp}")
    print("-" * 80)
    print(f"Total: {len(messages)} messages")

def clear_database():
    """Clear all messages from the database (for testing)"""
    if os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages")
        conn.commit()
        conn.close()
        print(f"Cleared all messages from '{DB_NAME}'")
    else:
        print(f"Database '{DB_NAME}' does not exist")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "view":
            view_all_messages()
        elif command == "clear":
            clear_database()
        elif command == "test":
            test_database()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python test_database.py [test|view|clear]")
    else:
        # Default: run the full test
        test_database()
