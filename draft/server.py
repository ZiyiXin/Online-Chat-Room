import socket
import threading
import time

# 服务器信息
HOST = '127.0.0.1'
PORT = 12345

# 维护所有连接的客户端
clients = {}
client_counter = 1  # 用于生成唯一的用户ID

# 广播消息给所有客户端
def broadcast(message, sender_socket=None):
    for client_socket in clients:
        if client_socket != sender_socket:  # 不发送给消息的发送者
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                # 如果发送失败，移除该客户端
                remove_client(client_socket)

# 处理每个客户端连接
def handle_client(client_socket):
    global client_counter

    # 分配唯一的用户ID
    user_id = f"User{client_counter}"
    client_counter += 1
    clients[client_socket] = user_id

    # 通知所有用户该用户已登录
    login_message = f"[{get_current_time()}] {user_id} 已登录"
    print(login_message)
    broadcast(login_message)

    try:
        while True:
            # 接收客户端消息
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            # 广播消息并附加时间
            timestamp = get_current_time()
            broadcast_message = f"[{timestamp}] {user_id}: {message}"
            print(broadcast_message)  # 在服务器端打印消息
            broadcast(broadcast_message, sender_socket=client_socket)
    except:
        pass
    finally:
        # 客户端断开连接
        logout_message = f"[{get_current_time()}] {user_id} 已退出"
        print(logout_message)
        broadcast(logout_message)
        remove_client(client_socket)

# 从客户端列表中移除断开的客户端
def remove_client(client_socket):
    if client_socket in clients:
        del clients[client_socket]
    client_socket.close()

# 获取当前时间
def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

# 主函数，启动服务器
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"服务器已启动，正在监听 {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"新连接：{client_address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()