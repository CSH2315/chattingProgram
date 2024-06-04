import login_list
import port

print("********************************************************")
print("채팅 프로그램에 오신 것을 환영합니다")
print("채팅을 위해서는 사용하실 아이디를 입력해주세요")
print("********************************************************")

id_test = ""

while id_test == "":
    print("사용하실 아이디를 입력하세요 : ")
    temp_id = input()
    id_x = login_list.detect_duplic_id(temp_id)
    if id_x == "not exist":
        print("아이디 설정이 완료되었습니다")
        print("********************************************************")
        id_test = "good"
    elif id_x == "exist":
        print("새로운 아이디를 설정해주세요")
        print("********************************************************")
    

port_test = ""
while port_test == "":
    print("사용하실 포트 번호를 입력하세요 : ")
    temp_port = input()
    id_x = login_list.detect_duplic_port(temp_port)
    if id_x == "not exist":
        print("포트 설정이 완료되었습니다")
        print("********************************************************")
        port_test = "good"
    elif id_x == "exist":
        print("새로운 포트를 설정해주세요")
        print("********************************************************")
    

login_list.add(temp_id, '127.0.0.1', temp_port)


print("채팅을 시작하길 바라신다면 '/채팅시작'을 입력해주세요")
oh_my = input()

# 원래 채팅 시작 전 아이디를 검증하는 코드
# # chat_test = ""
# # if oh_my == "/채팅시작":
# #     while chat_test == "":
# #         print("채팅할 사람의 아이디를 입력해 주세요")
# #         temp_input = input()
# #         # id_y = login_list.detect_duplic_id(temp_input)

# #         if id_y == "exist":
# #             port.socket_chatting(temp_id, '127.0.0.1', temp_port, temp_input)
# #             chat_test = "good"
# #         elif id_y == "not exist":
# #             print("아이디를 다시 확인해주세요")

if oh_my == "/채팅시작":
    print("채팅할 사람의 아이디를 입력해주세요")
    dumb = input()
    print("채팅할 사람의 포트를 입력해주세요")
    chat_port = input()
else:
    pass

port.socket_chatting(temp_id, "127.0.0.1", int(temp_port), int(chat_port))