import socket
import threading
import time

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

host='127.0.0.1'
ID = input("Enter ID: ").strip().upper()
listen_port = int(input("Enter your listening port: "))
connect_port = int(input("Enter the port number for connecting to the peer: "))

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
    s_connect.connect((host, connect_port))
    print(f'Client {ID} connected to {host}:{connect_port}')
except ConnectionRefusedError:
    print(f'Failed to connect to {host}:{connect_port}')
    exit(1)

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