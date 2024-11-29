const socket = new WebSocket('ws://localhost:8000'); // 连接到 WebSocket 服务器

const messageDisplay = document.getElementById('message-display');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const userList = document.getElementById('user-list'); // 用户列表

let clientId = null; // 记录客户端的唯一ID

// 监听来自服务器的消息
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    // 处理消息类型
    if (data.type === 'message') {
        // 只有在消息不是自己发送的情况下才显示
        if (data.clientId !== clientId) {
            const newMessage = document.createElement('p');
            newMessage.textContent = `${data.timestamp} - ${data.message}`;
            messageDisplay.appendChild(newMessage);
        }
    } else if (data.type === 'users') {
        // 如果是用户列表更新，更新用户列表显示
        updateUserList(data.users);
    } else if (data.type === 'clientId') {
        // 设置客户端的唯一ID
        clientId = data.clientId;
    }
};

// 发送聊天消息
sendButton.addEventListener('click', () => {
    const message = messageInput.value;

    // 本地显示消息并附带时间戳
    const timestamp = new Date().toLocaleString();
    const localMessage = document.createElement('p');
    localMessage.textContent = `${timestamp} - You: ${message}`;
    messageDisplay.appendChild(localMessage);

    // 发送消息给服务器，并附带上自己的 clientId
    socket.send(JSON.stringify({ type: 'message', message: message, clientId: clientId }));

    // 清空输入框
    messageInput.value = '';
});

// 更新用户列表显示
function updateUserList(users) {
    userList.innerHTML = ''; // 清空用户列表
    users.forEach(user => {
        const listItem = document.createElement('li');
        listItem.textContent = user;
        userList.appendChild(listItem);
    });
}