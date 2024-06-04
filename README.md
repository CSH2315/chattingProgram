# chattingProgram
# login_list.py 함수 정리
## init()  
init은 현재 온라인인 user를 관리하는 **user_list.csv** 파일을 초기화하는 함수이다.  
## add(user_id, ip_addr, port_num)  
매개변수에서 **user_id, ip_addr, port_num** 은 각각 id, ip주소, port 번호이다. **user_list.csv** 에 입력받은 **user_id, ip_addr, port_num** 를 **user_list.csv** 에 추가한다.  
## find(user_id)  
매개변수에서 **user_id**는 id를 의미한다. 입력받은 id를 user_list.csv에서 찾는다. port 번호가 존재하면 그 port 번호를 return 하고, 없으면 -1(그 user가 없다는 뜻) 를 return 한다.  
## delect(user_id)  
매개변수에서 **user_id**는 id를 의미한다. user_list.csv 에서 입력받은 user_id를 찾아서 제거한다.  
## detect_duplic_id(user_id)  
매개변수에서 **user_id**는 id를 의미한다. user_list.csv에서 이미 이 id를 가진 user가 있는지 확인한다. 이미 존재하면 "exist"를 return 하고, 존재하지 않으면 "not exist"를 return 한다.  
## detect_duplic_port(port_num)  
매개변수에서 **port_num**는 port 번호를 의미한다. user_list.csv에서 이미 이 port 번호를 가진 user가 있는지 확인한다. 이미 존재하면 "exist"를 return 하고, 존재하지 않으면 "not exist"를 return 한다.  
## make_user_list()  
로그인 서버에서 클라이언트로 user 목록을 보낼 때, user들의 이름을 개행을 기준으로 문자열을 만들어서 return 한다.  
## handle(connect, addr)  
매개변수에서 **connect**는 연결한 클라이언트의 소켓 객체이다. **addr**는 **(ip주소, port 번호)** 형태의 튜플을 가지고 있다. 먼저 addr을 ip_addr, port_num으로 분리한다. 그리고 id를 입력받아서 이미 존재하는 id인지 확인해서 다시 입력받게 하거나 user를 추가함. 다음에 user 목록을 전송하고, 무한반복문으로 message를 받고 클라이언트가 강제종료했을 때를 대비해서 except로 가면 강제종료한 user를 제거한다.  
