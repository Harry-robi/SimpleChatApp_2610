#!/usr/bin/env python3
"""
Starter code for the Web server
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, disconnect
import socket
import urllib.request
import sys
# TODO: Import necessary modules for database operations
# You will need: sqlite3 and datetime
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here' # You dont need to change this. 
socketio = SocketIO(app, cors_allowed_origins="*")

# Store WebSocket clients
websocket_clients = {}  # {socket_id: nickname}

# TODO: Database configuration
# Define the database filename (should be 'messages.sqlite')
# Example: DB_NAME = 'messages.sqlite'
DB_NAME = 'messages.sqlite'

def init_database():
    """
    TODO: Initialize the SQLite database and create tables if they don't exist
    
    This function should:
    1. Connect to the SQLite database (use check_same_thread=False for Flask-SocketIO)
    2. Create a 'messages' table with the following columns:
       - id: INTEGER PRIMARY KEY AUTOINCREMENT
       - content: TEXT NOT NULL (the message text)
       - nickname: TEXT (the sender's nickname, can be NULL for system messages)
       - timestamp: TEXT NOT NULL (ISO format timestamp)
       - message_type: TEXT NOT NULL (values: 'regular', 'system_join', 'system_leave')
    3. Create an index on the timestamp column for faster queries
    4. Commit the changes and close the connection
    5. Print a confirmation message
    
    Hint: Use CREATE TABLE IF NOT EXISTS to avoid errors if table already exists
    """
    # TODO: Implement database initialization
    # Example structure:
    # conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    # cursor = conn.cursor()
    # cursor.execute('''CREATE TABLE IF NOT EXISTS ...''')
    # ... (add your code here)
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        nickname TEXT,
        timestamp TEXT NOT NULL,
        message_type TEXT NOT NULL
    )''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_timestamp ON messages(timestamp)''')
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def save_message(content, nickname=None, message_type='regular'):
    """
    TODO: Save a message to the database
    
    Parameters:
    - content: The message text to store
    - nickname: The sender's nickname (optional, can be None)
    - message_type: Type of message ('regular', 'system_join', or 'system_leave')
    
    This function should:
    1. Generate a timestamp using datetime.now().isoformat()
    2. Connect to the database (use check_same_thread=False for Flask-SocketIO)
    3. Insert the message into the messages table with all required fields
    4. Commit the transaction
    5. Close the connection
    
    Hint: Use parameterized queries (?) to prevent SQL injection
    """
    # TODO: Implement message saving
    # Example structure:
    # timestamp = datetime.now().isoformat()
    # conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    # cursor = conn.cursor()
    # cursor.execute('''INSERT INTO messages ...''')
    # ... (add your code here)
    timestamp = datetime.now().isoformat()
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO messages (content, nickname, timestamp, message_type) VALUES (?, ?, ?, ?)''', 
                   (content, nickname, timestamp, message_type))
    conn.commit()
    conn.close()

def get_message_history(limit=100):
    """
    TODO: Retrieve message history from the database
    
    Parameters:
    - limit: Maximum number of messages to retrieve (default: 100)
    
    Returns:
    - A list of tuples, each containing (content, nickname, timestamp, message_type)
      in chronological order (oldest first)
    
    This function should:
    1. Connect to the database (use check_same_thread=False for Flask-SocketIO)
    2. Query the messages table, ordering by timestamp DESC (newest first)
    3. Limit the results to the specified number
    4. Fetch all results
    5. Close the connection
    6. Reverse the list to get chronological order (oldest first)
    7. Return the list
    
    Hint: Use ORDER BY timestamp DESC LIMIT ? to get the most recent messages
    """
    # TODO: Implement message history retrieval
    # Example structure:
    # conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    # cursor = conn.cursor()
    # cursor.execute('''SELECT ... ORDER BY timestamp DESC LIMIT ?''', (limit,))
    # ... (add your code here)
    # return list(reversed(messages))  # Reverse to get chronological order
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''SELECT content, nickname, timestamp, message_type FROM messages ORDER BY timestamp DESC LIMIT ?''', (limit,))
    messages = cursor.fetchall()
    conn.close()
    return list(reversed(messages))

@app.route('/')
def index():
    """Serve the main chat page"""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f'Client connected: {request.sid}')
    emit('status', {'msg': 'Connected to server. Please enter your nickname.'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f'Client disconnected: {request.sid}')
    if request.sid in websocket_clients:
        nickname = websocket_clients[request.sid]
        broadcast_message = f"{nickname} left the chat!"
        
        # TODO: Save the leave notification to the database
        # Call save_message() with the broadcast_message, nickname, and message_type='system_leave'
        # Example: save_message(broadcast_message, nickname=nickname, message_type='system_leave')
        save_message(broadcast_message, nickname=nickname, message_type='system_leave')
        
        del websocket_clients[request.sid]
        socketio.emit('message', {'msg': broadcast_message})
        socketio.emit('users_list', {'users': list(websocket_clients.values())})

@socketio.on('set_nickname')
def handle_set_nickname(data):
    """Handle nickname setting"""
    nickname = data.get('nickname', '').strip()
    if nickname:
        # Get list of existing users before adding the new one
        existing_users = list(websocket_clients.values())
        
        websocket_clients[request.sid] = nickname
        broadcast_message = f"{nickname} joined the chat!"
        
        # TODO: Save the join notification to the database
        # Call save_message() with the broadcast_message, nickname, and message_type='system_join'
        # Example: save_message(broadcast_message, nickname=nickname, message_type='system_join')
        save_message(broadcast_message, nickname=nickname, message_type='system_join')
        
        # Broadcast join message
        socketio.emit('message', {'msg': broadcast_message})
        emit('status', {'msg': f'Welcome, {nickname}!'})
        
        # TODO: Load and send message history to the newly connected user
        # 1. Call get_message_history() with limit=100 to retrieve the last 100 messages
        # 2. Emit a 'message_history' event to this client with the history
        #    Format: emit('message_history', {'messages': history})
        # Example:
        # history = get_message_history(limit=100)
        # emit('message_history', {'messages': history})
        history = get_message_history(limit=100)
        emit('message_history', {'messages': history})
        
        emit('nickname_set', {'nickname': nickname, 'existing_users': existing_users})
        socketio.emit('users_list', {'users': list(websocket_clients.values())})
    else:
        emit('error', {'msg': 'Nickname cannot be empty'})

@socketio.on('message')
def handle_message(data):
    """Handle incoming chat messages"""
    if request.sid in websocket_clients:
        nickname = websocket_clients[request.sid]
        message = data.get('message', '').strip()
        if message:
            # Handle quit command
            if message.lower() == 'quit':
                broadcast_message = f"{nickname} left the chat!"
                
                # TODO: Save the leave notification to the database
                # Call save_message() with broadcast_message, nickname, and message_type='system_leave'
                # Example: save_message(broadcast_message, nickname=nickname, message_type='system_leave')
                save_message(broadcast_message, nickname=nickname, message_type='system_leave')
                
                socketio.emit('message', {'msg': broadcast_message})
                del websocket_clients[request.sid]
                socketio.emit('users_list', {'users': list(websocket_clients.values())})
                disconnect()
            else:
                broadcast_message = f"{nickname}: {message}"
                
                # TODO: Save the regular message to the database
                # IMPORTANT: Save only the message content (not the "nickname: message" format)
                # Call save_message() with the message content, nickname, and message_type='regular'
                # Example: save_message(message, nickname=nickname, message_type='regular')
                save_message(message, nickname=nickname, message_type='regular')
                
                socketio.emit('message', {'msg': broadcast_message})
    else:
        emit('error', {'msg': 'Please set your nickname first'})

@socketio.on('get_users')
def handle_get_users():
    """Send list of connected users"""
    emit('users_list', {'users': list(websocket_clients.values())})

if __name__ == '__main__':
    # TODO: Initialize the database when the server starts
    # Call init_database() here
    # Example: init_database()
    init_database()
    
    # Get port number from command line argument
    port = 5001  # Default port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if port < 1 or port > 65535:
                print("Error: Port must be between 1 and 65535")
                print("Usage: python web_server.py [port]")
                sys.exit(1)
        except ValueError:
            print("Error: Port must be a number")
            print("Usage: python web_server.py [port]")
            sys.exit(1)
    
    # Get server info
    local_ip = socket.gethostbyname(socket.gethostname())
    try:
        with urllib.request.urlopen('https://api.ipify.org', timeout=5) as response:
            public_ip = response.read().decode('utf-8').strip()
    except Exception:
        public_ip = None
    
    print("=" * 50)
    print("Multi-Client Chat Web Server")
    print("=" * 50)
    print(f"Database: {DB_NAME}")
    print(f"Starting web server on http://localhost:{port}")
    print(f"Local IP: http://{local_ip}:{port}")
    if public_ip:
        print(f"Public IP: http://{public_ip}:{port}")
    print("Open your browser and navigate to the URL above")
    print("=" * 50)
    
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
