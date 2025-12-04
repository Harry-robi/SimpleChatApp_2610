#!/usr/bin/env python3
"""
Demonstration script showing the complete message storage and retrieval flow.
This simulates what happens when users join, chat, and leave.
"""
import os
import time

# Remove existing database for fresh demo
if os.path.exists('messages.sqlite'):
    os.remove('messages.sqlite')
    print("🗑️  Cleared existing database\n")

# Import the functions we implemented
from web_server import init_database, save_message, get_message_history

print("=" * 70)
print("DEMONSTRATION: Message Storage and Retrieval Flow")
print("=" * 70)

# Step 1: Initialize Database
print("\n📦 STEP 1: Initialize Database")
print("-" * 40)
init_database()

# Step 2: Simulate User Session
print("\n👥 STEP 2: Simulating Chat Session")
print("-" * 40)

# Alice joins
print("\n  [Alice connects]")
save_message("Alice joined the chat!", nickname="Alice", message_type="system_join")
print("  ✓ Saved: system_join - 'Alice joined the chat!'")
time.sleep(0.1)  # Small delay for different timestamps

# Bob joins
print("\n  [Bob connects]")
save_message("Bob joined the chat!", nickname="Bob", message_type="system_join")
print("  ✓ Saved: system_join - 'Bob joined the chat!'")
time.sleep(0.1)

# Chat messages
print("\n  [Chat conversation]")
messages = [
    ("Hello everyone!", "Alice"),
    ("Hey Alice! How are you?", "Bob"),
    ("I'm doing great, thanks!", "Alice"),
    ("Anyone else joining today?", "Bob"),
]

for content, nickname in messages:
    save_message(content, nickname=nickname, message_type="regular")
    print(f"  ✓ Saved: regular - {nickname}: '{content}'")
    time.sleep(0.1)

# Charlie joins (new user who will see history)
print("\n  [Charlie connects]")
save_message("Charlie joined the chat!", nickname="Charlie", message_type="system_join")
print("  ✓ Saved: system_join - 'Charlie joined the chat!'")
time.sleep(0.1)

# More messages
save_message("Welcome Charlie!", "Alice", "regular")
print("  ✓ Saved: regular - Alice: 'Welcome Charlie!'")
time.sleep(0.1)

save_message("Thanks! What did I miss?", "Charlie", "regular")
print("  ✓ Saved: regular - Charlie: 'Thanks! What did I miss?'")
time.sleep(0.1)

# Bob leaves
print("\n  [Bob disconnects]")
save_message("Bob left the chat!", nickname="Bob", message_type="system_leave")
print("  ✓ Saved: system_leave - 'Bob left the chat!'")

# Step 3: Retrieve Message History
print("\n\n📜 STEP 3: Retrieve Message History (as new user would see it)")
print("-" * 40)

history = get_message_history(limit=100)
print(f"\n  Retrieved {len(history)} messages:\n")

print("  ┌" + "─" * 68 + "┐")
print(f"  │ {'TYPE':<12} │ {'NICKNAME':<10} │ {'CONTENT':<38} │")
print("  ├" + "─" * 68 + "┤")

for content, nickname, timestamp, msg_type in history:
    # Truncate content if too long
    display_content = content[:38] if len(content) <= 38 else content[:35] + "..."
    print(f"  │ {msg_type:<12} │ {nickname or 'System':<10} │ {display_content:<38} │")

print("  └" + "─" * 68 + "┘")

# Step 4: Show how frontend would format these
print("\n\n🖥️  STEP 4: How Frontend Displays Messages")
print("-" * 40)
print("\n  Formatted for display:\n")

for content, nickname, timestamp, msg_type in history:
    # Parse timestamp for display
    time_part = timestamp.split('T')[1][:5]  # Get HH:MM
    hour = int(time_part.split(':')[0])
    minute = time_part.split(':')[1]
    ampm = 'PM' if hour >= 12 else 'AM'
    hour = hour % 12 or 12
    formatted_time = f"{hour}:{minute}{ampm}"
    
    if msg_type in ('system_join', 'system_leave'):
        # System messages shown in yellow/italic style
        print(f"  [{formatted_time}] 🔔 {content}")
    else:
        # Regular messages show nickname: content
        print(f"  [{formatted_time}] {nickname}: {content}")

# Step 5: Verify Database Contents
print("\n\n🔍 STEP 5: Direct Database Verification")
print("-" * 40)

import sqlite3
conn = sqlite3.connect('messages.sqlite')
cursor = conn.cursor()

# Count by type
cursor.execute("SELECT message_type, COUNT(*) FROM messages GROUP BY message_type")
counts = cursor.fetchall()
print("\n  Message counts by type:")
for msg_type, count in counts:
    print(f"    • {msg_type}: {count}")

# Verify index exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_timestamp'")
index = cursor.fetchone()
print(f"\n  Timestamp index exists: {'✓ Yes' if index else '✗ No'}")

conn.close()

print("\n" + "=" * 70)
print("✅ DEMONSTRATION COMPLETE")
print("=" * 70)
print("""
Summary:
  • Database initialized with correct schema
  • Messages saved with proper types (regular, system_join, system_leave)
  • Message history retrieved in chronological order
  • Timestamps stored in ISO format, displayed in 12-hour format
  • System messages visually distinguished from regular messages
""")
