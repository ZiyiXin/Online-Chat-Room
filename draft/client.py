import socket
import threading

# 服务器信息
HOST = '127.0.0.1'
PORT = 12345

# 接收消息的线程
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            print("与服务器断开连接")
            client_socket.close()
            break

# 主函数
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # 启动接收消息的线程
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    print("已连接到聊天室！输入消息并按 Enter 发送")

    while True:
        try:
            # 用户输入消息
            message = input()
            client_socket.send(message.encode('utf-8'))
        except:
            print("与服务器断开连接")
            client_socket.close()
            break

if __name__ == "__main__":
    main()