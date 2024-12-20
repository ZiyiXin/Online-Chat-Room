const username = localStorage.getItem('username');
const websocket = new WebSocket(`ws://${window.location.host}/ws`);
const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const userList = document.getElementById('user-list');
const chatTitle = document.getElementById('chat-title');

let selectedUser = "Public Room";

// WebSocket connection
websocket.onopen = () => {
    if (username) {
        websocket.send(JSON.stringify({ type: "set_username", username }));
    }
};

// WebSocket message handling
websocket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.type === "message") {
        displayMessage(data.message);
    } else if (data.type === "user_list") {
        updateUserList(data.users);
    }
};

function updateUserList(users) {
    userList.innerHTML = "";
    const publicRoom = document.createElement("li");
    publicRoom.textContent = "Public Room";
    publicRoom.onclick = () => selectUser("Public Room");
    userList.appendChild(publicRoom);

    users.forEach(user => {
        const userItem = document.createElement("li");
        userItem.textContent = user;
        userItem.onclick = () => selectUser(user);
        userList.appendChild(userItem);
    });
}

function selectUser(user) {
    selectedUser = user;
    chatTitle.textContent = user === "Public Room" ? "Public Room" : `Direct Message - ${user}`;
}

function displayMessage(message) {
    const messageElement = document.createElement("p");
    messageElement.textContent = message;
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

sendButton.addEventListener("click", () => {
    const message = messageInput.value.trim();
    if (message) {
        websocket.send(JSON.stringify({ type: "message", to: selectedUser, message }));
        messageInput.value = "";
    }
});