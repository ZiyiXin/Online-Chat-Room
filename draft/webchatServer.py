import asyncio
import websockets
import json
import time

connected_clients = {}
client_counter = 1  # 记录客户端的数量，分配唯一ID

async def handle_client(websocket, path):
    global client_counter

    # 为每个客户端分配一个唯一的 ID
    client_id = client_counter
    client_counter += 1

    # 获取客户端的 IP 地址并作为用户名
    client_name = f"Client{client_id}"
    connected_clients[websocket] = client_name

    # 发送 clientId 给客户端
    await websocket.send(json.dumps({'type': 'clientId', 'clientId': client_id}))

    # 向所有客户端广播新的用户列表
    await broadcast_user_list()

    try:
        async for message in websocket:
            # 当收到消息时，将消息发送给所有连接的客户端
            data = json.loads(message)
            if data['type'] == 'message':
                # 获取当前时间，并格式化成可读的时间格式
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                formatted_message = f"{client_name}: {data['message']}"
                await broadcast_message(formatted_message, data['clientId'], timestamp)
    finally:
        # 客户端断开连接时，移除客户端并更新用户列表
        del connected_clients[websocket]
        await broadcast_user_list()

async def broadcast_message(message, sender_client_id, timestamp):
    if connected_clients:
        # 将时间戳和消息一起发送
        data = json.dumps({'type': 'message', 'message': message, 'timestamp': timestamp, 'clientId': sender_client_id})
        await asyncio.gather(*[client.send(data) for client in connected_clients])

async def broadcast_user_list():
    users = list(connected_clients.values())
    if connected_clients:
        data = json.dumps({'type': 'users', 'users': users})
        await asyncio.gather(*[client.send(data) for client in connected_clients])

async def main():
    # 启动 WebSocket 服务器
    server = await websockets.serve(handle_client, "localhost", 8080)
    print("WebSocket server is running on ws://localhost:8080")
    # 运行事件循环，直到服务器关闭
    await server.wait_closed()

if __name__ == "__main__":
    # 使用 asyncio 启动事件循环
    asyncio.run(main())