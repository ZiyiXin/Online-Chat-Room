from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

connected_users = {}  # Store WebSocket: username mappings


@app.get("/")
async def login_page():
    """Serve the login page."""
    return templates.TemplateResponse("login.html", {"request": {}})


@app.get("/chat")
async def chat_page():
    """Serve the chat room page."""
    return templates.TemplateResponse("chat.html", {"request": {}})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    username = None

    try:
        while True:
            data = await websocket.receive_json()

            # Set username
            if data.get("type") == "set_username":
                username = data["username"]
                connected_users[websocket] = username
                await broadcast_user_list()
                await broadcast_message(f"{username} joined the chat room")

            # Handle message
            elif data.get("type") == "message":
                message = data["message"]
                to_user = data.get("to", "Public Room")
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if to_user == "Public Room":
                    await broadcast_message(f"[{timestamp}] {username}: {message}")
                else:
                    await send_private_message(to_user, f"[{timestamp}] {username} -> {to_user}: {message}")

    except WebSocketDisconnect:
        if websocket in connected_users:
            del connected_users[websocket]
            await broadcast_user_list()

# Helper Functions
async def broadcast_user_list():
    """Send updated user list to all clients."""
    user_list = list(connected_users.values())
    await broadcast({"type": "user_list", "users": user_list})


async def broadcast_message(message):
    """Broadcast message to all clients."""
    await broadcast({"type": "message", "message": message})


async def broadcast(data):
    """Send a message to all connected clients."""
    for ws in list(connected_users.keys()):
        try:
            await ws.send_json(data)
        except:
            del connected_users[ws]


async def send_private_message(to_user, message):
    """Send a private message to a specific user."""
    for ws, user in connected_users.items():
        if user == to_user:
            await ws.send_json({"type": "message", "message": message})