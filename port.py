import socket
import threading

host='127.0.0.1'


def init(user_id, port, connect_id):
    user_id = user_id.strip()
    port = int(port)
    connect_id = str(connect_id) # 채팅을 보낼 상대 유저의 ID
    return user_id, port, connect_id

# def socket_chatting(user_id, host, listen_port): this is test code
def socket_chatting(user_id, host, listen_port, connect_id):
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

    # socket 연결 부분
    s_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_listen.bind((host, listen_port))
    s_listen.listen()
    print(f'Client {user_id} listening on {host}:{listen_port}')

    connect_port = int(find(user_list, connect_id)) # login_list.py에 있는 find 함수
    # connect_port = int(input("connect port: ")) this is test code.
    s_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s_connect.connect((host, connect_port))
        print(f'Client {user_id} connected to {host}:{connect_port}')
    except ConnectionRefusedError:
        print(f'Failed to connect to {host}:{connect_port}')
        return

    # thread 주고받는 부분
    conn, addr = s_listen.accept()
    print(f'client {user_id} accepted connection from {addr}')

    receive_thread = threading.Thread(target=handle_receive, args=(conn,))
    send_thread = threading.Thread(target=handle_send, args=(s_connect,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

'''
# this is test code 
user_id = input('username: ')
port = int(input('port: '))
connect_id = input('connect id: ')
user_id, port, connect_id = init(user_id, port, connect_id)
socket_chatting(user_id, host, port)
'''

'''

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
'''

