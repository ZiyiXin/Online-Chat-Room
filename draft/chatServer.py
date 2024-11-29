import socket
import select
import time

# Set up server details
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Arbitrary port for connection

# List of sockets for select
sockets_list = []
# Dictionary to store client sockets and their assigned client names
clients = {}

# Counter for assigning unique client IDs
client_id_counter = 1

def start_server(host, port):
    """
    Start the server, set up the socket, and begin listening for connections.
    """
    global sockets_list
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    sockets_list.append(server_socket)
    print(f"Server listening on {host}:{port}")

    return server_socket

def accept_new_connection(server_socket):
    """
    Accept a new connection from a client and assign a unique name.
    """
    global client_id_counter

    client_socket, client_address = server_socket.accept()
    sockets_list.append(client_socket)

    # Assign a unique client name (Client1, Client2, etc.)
    client_name = f"Client{client_id_counter}"
    clients[client_socket] = client_name
    client_id_counter += 1

    print(f"Accepted new connection from {client_address} as {client_name}")

def handle_client_message(notified_socket):
    """
    Handle a message received from a client and broadcast it to other clients.
    """
    try:
        message = notified_socket.recv(1024)

        if not message:
            # If message is empty, client disconnected
            print(f"Closed connection from {clients[notified_socket]}")
            sockets_list.remove(notified_socket)
            del clients[notified_socket]
        else:
            # Format the message with client name and timestamp
            formatted_message = format_message(clients[notified_socket], message)
            print(f"Received message from {clients[notified_socket]}: {message.decode('utf-8')}")

            # Broadcast the formatted message to other clients
            broadcast_message(notified_socket, formatted_message)

    except Exception as e:
        # Handle client disconnection
        print(f"Error: {e}")
        sockets_list.remove(notified_socket)
        del clients[notified_socket]

def broadcast_message(sender_socket, message):
    """
    Send the received message to all clients except the sender, along with 
    the client's unique identifier and the time the message was sent.
    """
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except:
                # If the sending fails (client disconnected), remove it from the list
                client_socket.close()
                sockets_list.remove(client_socket)
                del clients[client_socket]

def format_message(client_name, message):
    """
    Format the message to include the client's unique identifier and the time the message was sent.
    """
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    formatted_message = f"[{current_time}] {client_name}: {message.decode('utf-8')}"
    return formatted_message.encode('utf-8')

def run_server():
    """
    The main loop of the server, handling client connections and messages.
    """
    server_socket = start_server(HOST, PORT)

    while True:
        # Use select to handle multiple client connections
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                accept_new_connection(server_socket)
            else:
                handle_client_message(notified_socket)

        # Handle exceptions
        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]

# Entry point for the script
if __name__ == "__main__":
    run_server()