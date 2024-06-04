import pandas as pd
import socket
import threading

# csv 초기화하는 함수
def init():
    df = pd.DataFrame([], columns=['user_id'])
    df['ip_addr'] = []
    df['port_num'] = []
    df.to_csv("user_list.csv", index=False)

# csv에 user 추가(행 추가)
def add(user_id, ip_addr, port_num):

    global user_list
    print(user_list)

    user_list.loc[len(user_list)] = [user_id, ip_addr, port_num]
    user_list.to_csv("user_list.csv", index=False)

    print(user_list)

# id로 csv에서 port번호 찾기
def find(user_id):
    global user_list

    port = user_list.loc[user_list['user_id'] == user_id, ['port_num']]
    if port.empty == True:
        return -1
    else:
        return int(port.iloc[0, 0])

# 추가로 만든 기능 : 특정 user_id가 연결 종료 시 user_list에서 정보 삭제하는 함수
def delete(user_id):
    global user_list

    inx = user_list[user_list['user_id'] == user_id].index
    user_list.drop(inx, inplace=True)
    user_list.reset_index(drop=True, inplace=True)
    user_list.to_csv("user_list.csv", index=False)

# user 존재 여부 확인
def detect_duplic_id(user_id):
    global user_list

    port = user_list.loc[user_list['user_id'] == user_id]
    if port.empty:
        return "not exist"
    else:
        return "exist"

def detect_duplic_port(port_num):
    global user_list

    port = user_list.loc[user_list['port_num'] == port_num]
    if port.empty:
        return "not exist"
    else:
        return "exist"

def make_user_list():
    global user_list

    list = ""
    user_id_list = user_list['user_id']

    for i in range(len(user_id_list)):
        list += f"{user_id_list[i]}\n"

    return list

# user가 강제종료 했을 때 어떻게 해야 csv에서 파일을 잘 처리할 수 있을까? -> 그냥 이전 코드 참고함
# 1. 연결 종료된 것을 확인해야함!!(이게 문제) -> 이전 코드에서 server에서 계속 data.recv() 하다가, try - except 문으로 처리함
# 주기적으로 로그인 서버에 연결해서 메시지를 보내게 해야 하는건가?
# 2. 연결 종료된 클라이언트 id를 가져옴
# 3. delete 해도 되고...
def handle(connect, addr):
    global user_list

    # ip주소, 포트 번호 분리
    ip_addr, port_num = addr

    # id 중복이면 다시 입력받게 하고, 중복이 아니면 추가하고 break
    while True:
        user_id = connect.recv(1024).decode()

        if detect_duplic_id(user_id) == "exist":
            connect.send("새로운 아이디를 설정해주세요\n********************************************************".encode())
        else:
            connect.send("성공".encode())
            break

    # 사용자 목록 전송
    connect.send(f"online user\n{make_user_list()}".encode())

    # 메시지를 받는데, 못 받았으면 except로 강제종료했다는 판단하에 user_id csv에서 제거
    while True:
        try:
            message = connect.recv(1024).decode()
        except:
            delete(user_id)
            break

# init()
user_list = pd.read_csv("user_list.csv")

if __name__ == '__main__':

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8000))
    server_socket.listen(5)
    print("server : 127.0.0.1:8000")

    while True:
        connect, addr = server_socket.accept()
        threading.Thread(target=handle, args=(connect, addr)).start()

# 여기부터는 그냥 테스트 코드입니다
# csv 파일 초기화
# init()
#
# # csv 파일 열기
# user_list = pd.read_csv("user_list.csv")
#
# # connection, addr = socket.accept() 이렇게 하면, addr에는 (IP주소, 포트번호) 와 같이 튜플로 온다.
# # client_id = connection.recv(1024).decode() 이런식으로 하면 id를 받을 수 있다.
# # 예시, id : test1, (ip, port) : (127.0.0.1, 7900)
# user_id = "test1"
# ip_addr, port_num = ("127.0.0.1", 7900)
#
# # user 추가
# add(user_id, ip_addr, port_num)
#
# # 반복문으로 add 테스트
# for i in range(2, 11):
#     add(f"test{i}", "127.0.0.1", (i + 1) * 500)
#
# # add한 결과
# print(user_list)
# print("=====================")
#
# # find 테스트
# want_port = find(user_id)
# if want_port == -1:
#     print("이 id를 가진 user가 없습니다.")
# else:
#     print(f"{user_id}'s port : {want_port}")
#
# # 반복문으로 find 테스트
# for i in range(2, 11):
#     want_port = find(f"test{i}")
#     if want_port == -1:
#         print("이 id를 가진 user가 없습니다.")
#     else:
#         print(f"test{i}'s port : {want_port}")
#
# # 없는 user에 대한 find 테스트
# want_port = find("test100")
# if want_port == -1:
#     print("이 id를 가진 user가 없습니다.")
# else:
#     print(f"test100's port : {want_port}")
#
# print("=====================")
#
# # 아마 클라이언트가 나가는 상황에서 삭제하는 코드도 있어야 할듯...
# # test1 유저 삭제
# delete(user_id)
#
# # 없는 user를 삭제하는데 오류 발생 X
# delete("test100")
#
# # delete 결과
# print(user_list)
#
# print("=====================")
# # user 중복 여부
# print(detect_duplic("test1"))
# print(detect_duplic("test3"))
#
# print("=====================")
# print(make_user_list())

