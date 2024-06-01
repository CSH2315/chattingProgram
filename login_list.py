import pandas as pd

# csv 초기화하는 함수
def init():
    df = pd.DataFrame([], columns=['user_id'])
    df['ip_addr'] = []
    df['port_num'] = []
    df.to_csv("user_list.csv", index=False)

# csv에 user 추가(행 추가)
def add(user_list, user_id, ip_addr, port_num):
    user_list.loc[len(user_list)] = [user_id, ip_addr, port_num]
    user_list.to_csv("user_list.csv", index=False)


# id로 csv에서 port번호 찾기
def find(user_list, user_id):
    port = user_list.loc[user_list['user_id'] == user_id, ['port_num']]

    if port.empty == True:
        return -1
    else:
        return int(port.iloc[0, 0])

# 추가로 만든 기능 : 특정 user_id가 연결 종료 시 user_list에서 정보 삭제하는 함수
def delete(user_list, user_id):
    inx = user_list[user_list['user_id'] == user_id].index
    user_list.drop(inx, inplace=True)
    user_list.reset_index(drop=True, inplace=True)
    user_list.to_csv("user_list.csv", index=False)

# csv 파일 초기화
init()

# csv 파일 열기
user_list = pd.read_csv("user_list.csv")

# connection, addr = socket.accept() 이렇게 하면, addr에는 (IP주소, 포트번호) 와 같이 튜플로 온다.
# client_id = connection.recv(1024).decode() 이런식으로 하면 id를 받을 수 있다.
# 예시, id : test1, (ip, port) : (127.0.0.1, 7900)
user_id = "test1"
ip_addr, port_num = ("127.0.0.1", 7900)

# user 추가
add(user_list, user_id, ip_addr, port_num)

# 반복문으로 add 테스트
for i in range(2, 11):
    add(user_list, f"test{i}", "127.0.0.1", (i + 1) * 500)

# add한 결과
print(user_list)
print("=====================")

# find 테스트
want_port = find(user_list, user_id)
if want_port == -1:
    print("이 id를 가진 user가 없습니다.")
else:
    print(f"{user_id}'s port : {want_port}")

# 반복문으로 find 테스트
for i in range(2, 11):
    want_port = find(user_list, f"test{i}")
    if want_port == -1:
        print("이 id를 가진 user가 없습니다.")
    else:
        print(f"test{i}'s port : {want_port}")

# 없는 user에 대한 find 테스트
want_port = find(user_list, "test100")
if want_port == -1:
    print("이 id를 가진 user가 없습니다.")
else:
    print(f"test100's port : {want_port}")

print("=====================")

# 아마 클라이언트가 나가는 상황에서 삭제하는 코드도 있어야 할듯...
# test1 유저 삭제
delete(user_list, user_id)

# 없는 user를 삭제하는데 오류 발생 X
delete(user_list, "test100")

# delete 결과
print(user_list)