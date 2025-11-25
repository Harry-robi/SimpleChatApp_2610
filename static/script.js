// Wait for page to load before setting up
document.addEventListener('DOMContentLoaded', function() {
    initializeChat();
});

function initializeChat() {
    // Connect to the server
    const socket = io();

    // Debug: Log connection events
    console.log('Attempting to connect to server...');

    // Get HTML elements
    const statusDiv = document.getElementById('status');
    const nicknameSection = document.getElementById('nickname-section');
    const chatSection = document.getElementById('chat-section');
    const nicknameInput = document.getElementById('nickname-input');
    const nicknameSubmit = document.getElementById('nickname-submit');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');

    let currentNickname = null;

// When connected to server
socket.on('connect', () => {
    console.log('Connected to server!');
    statusDiv.textContent = 'Status: Connected';
    statusDiv.className = 'connected';
});

// Handle connection errors
socket.on('connect_error', (error) => {
    console.error('Connection error:', error);
    statusDiv.textContent = 'Status: Connection Error';
    statusDiv.className = '';
});

// When disconnected from server
socket.on('disconnect', () => {
    statusDiv.textContent = 'Status: Disconnected';
    statusDiv.className = '';
    addMessage('Disconnected from server', true);
});

// When server sends a status message
socket.on('status', (data) => {
    addMessage(data.msg, true);
});

// When server sends a chat message
socket.on('message', (data) => {
    const messageText = data.msg;
    addMessage(messageText, false);
});

// When nickname is successfully set
socket.on('nickname_set', (data) => {
    console.log('Nickname set successfully:', data.nickname);
    currentNickname = data.nickname;
    
    // Show existing users if any
    if (data.existing_users && data.existing_users.length > 0) {
        const usersList = data.existing_users.join(', ');
        addMessage(`Users already in chat: ${usersList}`, true);
    }
    
    nicknameSection.style.display = 'none';
    chatSection.style.display = 'block';
    messageInput.disabled = false;
    sendButton.disabled = false;
    messageInput.focus();
});

// TODO: Handle message history from the server
// When the server sends message history (after a user sets their nickname),
// you need to display all the historical messages in the chat
socket.on('message_history', (data) => {
    // TODO: Implement message history display
    // Steps:
    // 1. Log the number of messages received (for debugging)
    // 2. Clear any existing messages in the chatMessages div
    // 3. Loop through data.messages array
    // 4. For each message, destructure: [content, nickname, timestamp, messageType]
    // 5. Determine if it's a system message (messageType === 'system_join' || 'system_leave')
    // 6. For regular messages, reconstruct the display format: `${nickname}: ${content}`
    //    For system messages, use the content as-is
    // 7. Call addMessageWithTimestamp() with the display text, isSystem flag, and timestamp
    // 
    // Example structure:
    // console.log('Loading message history:', data.messages.length, 'messages');
    // chatMessages.innerHTML = '';
    // if (data.messages && data.messages.length > 0) {
    //     data.messages.forEach((msg) => {
    //         const [content, nickname, timestamp, messageType] = msg;
    //         // ... (add your code here)
    //     });
    // }
});

// When there's an error
socket.on('error', (data) => {
    addMessage('Error: ' + data.msg, true);
});

// Function to get current time in 12-hour format (e.g., 4:14PM)
function getTimestamp() {
    const now = new Date();
    let hours = now.getHours();
    const minutes = now.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    
    hours = hours % 12;
    hours = hours ? hours : 12; // 0 should be 12
    
    const minutesStr = minutes < 10 ? '0' + minutes : minutes;
    return `${hours}:${minutesStr}${ampm}`;
}

// TODO: Implement function to format ISO timestamp to 12-hour format
// This function converts an ISO timestamp string (from the database) to a readable 12-hour format
// Parameters:
//   - isoString: ISO format timestamp string (e.g., "2024-01-15T14:30:00.123456")
// Returns:
//   - Formatted string in 12-hour format (e.g., "2:30PM")
//
// Steps:
// 1. If isoString is empty/null, return getTimestamp() for current time
// 2. Try to create a Date object from the ISO string
// 3. Extract hours and minutes from the date
// 4. Determine AM/PM based on hours (>= 12 is PM, else AM)
// 5. Convert to 12-hour format (0-11 for hours, with 0 becoming 12)
// 6. Format minutes with leading zero if needed
// 7. Return formatted string: `${hours}:${minutesStr}${ampm}`
// 8. If there's an error, return getTimestamp() as fallback
//
// Example structure:
// function formatTimestamp(isoString) {
//     if (!isoString) return getTimestamp();
//     try {
//         const date = new Date(isoString);
//         // ... (add your code here)
//     } catch (e) {
//         return getTimestamp();
//     }
// }
function formatTimestamp(isoString) {
    // TODO: Implement this function
    // Hint: Use new Date(isoString) to parse the ISO timestamp
    // Hint: Use date.getHours() and date.getMinutes() to extract time components
    return getTimestamp(); // Placeholder - replace with your implementation
}

// Function to add a message to the chat
function addMessage(text, isSystem) {
    addMessageWithTimestamp(text, isSystem, null);
}

// TODO: Implement function to add a message with a specific timestamp
// This function creates and displays a message in the chat with a given timestamp
// Parameters:
//   - text: The message text to display
//   - isSystem: Boolean indicating if this is a system message
//   - timestamp: ISO timestamp string (optional, null for current time)
//
// Steps:
// 1. Create a new div element for the message
// 2. Set its className to 'message'
// 3. Determine the timestamp string:
//    - If timestamp is provided, use formatTimestamp(timestamp)
//    - Otherwise, use getTimestamp() for current time
// 4. Check if it's a system message (isSystem is true OR text contains 'joined', 'left', 'Connected', 'Disconnected')
//    If so, add 'system' class to messageDiv
// 5. Create a span element for the timestamp with className 'timestamp'
// 6. Set the timestamp text content (timestamp + space)
// 7. Create a span element for the message text
// 8. Set the message text content
// 9. Append timestamp span and message text span to messageDiv
// 10. Append messageDiv to chatMessages container
// 11. Scroll to bottom: chatMessages.scrollTop = chatMessages.scrollHeight
//
// Example structure:
// function addMessageWithTimestamp(text, isSystem, timestamp) {
//     const messageDiv = document.createElement('div');
//     messageDiv.className = 'message';
//     // ... (add your code here)
// }
function addMessageWithTimestamp(text, isSystem, timestamp) {
    // TODO: Implement this function
    // Hint: Use document.createElement() to create DOM elements
    // Hint: Use element.appendChild() to add elements to the DOM
    // Hint: Use formatTimestamp() to format the timestamp if provided
}

// When user clicks "Join Chat" button
nicknameSubmit.addEventListener('click', () => {
    const nickname = nicknameInput.value.trim();
    console.log('Join Chat clicked, nickname:', nickname);
    console.log('Socket connected:', socket.connected);
    
    if (nickname) {
        if (socket.connected) {
            console.log('Sending set_nickname event');
            socket.emit('set_nickname', { nickname: nickname });
        } else {
            alert('Not connected to server. Please wait for connection.');
            console.error('Socket not connected!');
        }
    } else {
        alert('Please enter a nickname');
    }
});

// When user presses Enter in nickname field
nicknameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        nicknameSubmit.click();
    }
});

// When user clicks "Send" button
sendButton.addEventListener('click', sendMessage);

// When user presses Enter in message field
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Function to send a message
function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        socket.emit('message', { message: message });
        // Don't play sound for own messages - they're already displayed immediately
        messageInput.value = '';
    }
}

    // When page is closing, disconnect from server
    window.addEventListener('beforeunload', () => {
        socket.disconnect();
    });
}