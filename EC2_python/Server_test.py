#!/usr/bin
#-*- coding: utf-8 -*-
'''
    Client한테 .xml 보내는 코드
'''
import socket
import argparse
import threading
from os.path import exists
import os
import hashlib
from function import *

host = ""
#user_list = {}
notice_flag = 0

# 멀티스레드 코드
def handle_receive(client_socket, addr):
    receive_directory = "/home/ubuntu/EC2_python_realtime/realtime_data_xml"
    while 1:
        try:
            f_size = client_socket.recv(1024)
            f_size = f_size.decode()

            if f_size == "error":
                print("파일을 찾을 수 없습니다.")
                return

            msg = "ready"
            client_socket.sendall(msg.encode())
            file_name = client_socket.recv(1024)
            file_name = file_name.decode()
            # print(file_name)
            msg1 = "real"
            client_socket.sendall(msg1.encode())

            with open(receive_directory+"/"+file_name, 'w', encoding='utf-8') as f:
                # 파일 사이즈만큼 recv
                data = client_socket.recv(int(f_size))
                f.write(data.decode())
            hd = client_socket.recv(256)
            hd = hd.decode()

            print("file name : " + file_name)
            print("size : " + f_size)
            print("hash digest : ", hd)
        except:
            print("연결 끊김")
            client_socket.close()
            break

def handle_send(client_socket, addr):
    send_directory = "/home/ubuntu/EC2_python_realtime/control_data_xml"
    while 1:
        #print('to ',user,end=" ")
        if os.path.isfile(send_directory+"/control_test.xml"):
            os.system("cp "+send_directory+"/control_test.xml "+send_directory+"/control.xml")
            file_name = "control.xml"
            # 해당 경로에 파일이 없으면 에러
            #file_name = input()
            if not exists(send_directory + "/" + file_name):
                msg = "error"
                client_socket.sendall(msg.encode())
                client_socket.close()
                return

            client_socket.sendall(getFileSize(file_name, send_directory).encode())
            # client 가 파일 내용을 받을 준비 확인
            ru_ready = client_socket.recv(1024)
            if ru_ready.decode() == "ready":
                client_socket.sendall(file_name.encode())
                real_ready = client_socket.recv(1024)
                if real_ready.decode() == "real":
                    client_socket.sendall(getFileData(file_name, send_directory).encode())
                    print("해시 결과 : ", hashing(file_name, send_directory))
                    client_socket.sendall(hashing(file_name, send_directory).encode())
            os.remove("/home/ubuntu/EC2_python_realtime/control_data_xml/control_test.xml")
            os.remove("/home/ubuntu/EC2_python_realtime/control_data_xml/control.xml")
    client_socket.close()

def accept_func():
    #IPv4 체계, TCP 타입 소켓 객체를 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #포트를 사용 중 일때 에러를 해결하기 위한 구문
    #server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #ip주소와 port번호를 함께 socket에 바인드 한다.
    #포트의 범위는 1-65535 사이의 숫자를 사용할 수 있다.
    server_socket.bind((host, send_port))
    server_socket2.bind((host, port))
    #서버가 최대 5개의 클라이언트의 접속을 허용한다.
    server_socket.listen(4)
    server_socket2.listen(1)

    while 1:
        try:
            #클라이언트 함수가 접속하면 새로운 소켓을 반환한다.
            client_socket, addr = server_socket.accept()
            client_socket2, addr2 = server_socket2.accept()
            print("접속 완료")
        except KeyboardInterrupt:
            #for user, con in user_list:
            #    con.close()
            server_socket.close()
            server_socket2.close()
            print("Keyboard interrupt, Server 종료...")
        #user = client_socket.recv(1024)
        #user_list[user] = client_socket

        #accept()함수로 입력만 받아주고 이후 알고리즘은 핸들러에게 맡긴다.
        # notice_thread = threading.Thread(target=handle_notice, args=(client_socket, addr, user))
        # notice_thread.daemon = True
        # notice_thread.start()
        send_thread = threading.Thread(target=handle_send, args=(client_socket, addr))
        receive_thread = threading.Thread(target=handle_receive, args=(client_socket2, addr2))
        send_thread.daemon = True
        receive_thread.daemon = True
        send_thread.start()
        receive_thread.start()

# 파일의 크기를 반환하는 함수
def getFileSize(file_name, directory):
    file_size = os.path.getsize(directory + "/" + file_name)
    return str(file_size)

# 파일의 내용을 반환하는 함수
def getFileData(file_name, directory):
    with open(directory + "/" + file_name, 'r', encoding="UTF-8") as f:
        data = ""
        # 파일이 매번 각 라인을 읽어 리턴할 수 있기 때문에 라인마다 끊어서 저장
        for line in f:
            data += line
    return data

def hashing(file_name, directory):
    XML_control = parsing_XML_control(file_name, directory)
    f = open(directory + "/" + file_name, 'rb')
    data = f.read()
    f.close()
    data += get_salt_value(XML_control[0], XML_control[1]).encode('utf-8')
    hd = hashlib.sha256(data).hexdigest()
    return hd

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo server -sp send_port -p port")
    parser.add_argument('-sp', help="send_port_number", required=True)
    parser.add_argument('-p', help="port_number", required=True)


    args = parser.parse_args()
    try:
        port = int(args.p)
        send_port = int(args.sp)
    except:
        pass
    #file_exists = threading.Thread(target=file_exists, args=())
    accept_func()
