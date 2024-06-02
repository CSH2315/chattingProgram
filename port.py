import socket
import threading
import time

# ID와 Host, Port Number 저장할 Dictionary
peer_info = {}

def handle_receive(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode()}")
    conn.close()

def handle_send(conn):
    while True:
        message = input("Enter message to send: ")
        conn.sendall(message.encode())
        if message.lower() == "bye":
            break
    conn.close()

def start_peer(ID, listen_port, host='127.0.0.1'):
    print(peer_info)
    connect_ID = input("Enter the ID you want to connect to: ")
    connect_host, connect_port = peer_info.get(connect_ID, (None, None))
    if connect_host is None or connect_port is None:
        print("Invalid ID. Please try again.")
        return

    # Listen socket
    s_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_listen.bind((host, listen_port))
    s_listen.listen()
    print(f'Client {ID} listening on {host}:{listen_port}')

    # Ensure the other client has time to set up listening
    time.sleep(1)

    # Connect socket
    s_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s_connect.connect((connect_host, connect_port))
        print(f'Client {ID} connected to {connect_host}:{connect_port}')
    except ConnectionRefusedError:
        print(f'Failed to connect to {connect_host}:{connect_port}')
        return

    # Accept connection
    conn, addr = s_listen.accept()
    print(f'Client {ID} accepted connection from {addr}')

    # Start receiving and sending threads
    receive_thread = threading.Thread(target=handle_receive, args=(conn,))
    send_thread = threading.Thread(target=handle_send, args=(s_connect,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    # Update peer_info dictionary with new client information
    peer_info[ID] = (host, listen_port)

if __name__ == "__main__":
    ID = input("Enter ID: ").strip().upper()
    listen_port = int(input("Enter your listening port: "))
    peer_info[ID] = (None, None)
    start_peer(ID, listen_port)
