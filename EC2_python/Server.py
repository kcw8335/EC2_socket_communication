#!/usr/bin
# -*- coding: utf-8 -*-
'''
    For Server
    Client한테 제어 .xml 전송
    Client로부터 실시간 현황 수신
'''
import socket
import argparse
import threading
from os.path import exists
import hashlib
from function import *

# TODO 바꿔야할 설정들!!!
receive_directory = "/home/ubuntu/EC2_python_realtime/realtime_data_xml/"
send_directory = "/home/ubuntu/EC2_python_realtime/control_data_xml/"
host = ""
#send_port_ras1 = 8345
send_port_ras2 = 8343
rcv_port = 8342



def handle_receive(client_socket):
    while 1:
        # try:
        f_size = client_socket.recv(1024)
        f_size = f_size.decode()

        if f_size == "error":
            print("파일을 찾을 수 없습니다.")
            return

        msg = "ready"
        client_socket.sendall(msg.encode())
        file_name = client_socket.recv(1024)
        file_name = file_name.decode()
        msg1 = "real"
        client_socket.sendall(msg1.encode())
        #
        # 무결성 코드 작성하기
        #
        with open(receive_directory + file_name, 'w', encoding='utf-8') as f:
            # 파일 사이즈만큼 recv
            data = client_socket.recv(int(f_size))
            f.write(data.decode())

        hd = client_socket.recv(256)
        hd = hd.decode()
        # ====================================================================================================================================================================
        # 파일을 json으로 변환한 후 바로 전송하는 코드
        """tmp_list = parsing_XML(file_name, receive_directory)
        if tmp_list[0] == "1":
            file_path = "/home/ubuntu/EC2_python_realtime/realtime_data_json/realtime_1.json"
            make_Json_file(tmp_list[0], tmp_list[1], tmp_list[2], file_path)
            os.system('scp -i "/home/ubuntu/socket_programming.pem" /home/ubuntu/EC2_python_realtime/realtime_data_json/realtime_1.json ubuntu@ec2-13-209-12-175.ap-northeast-2.compute.amazonaws.com:/home/ubuntu/project4/realtime/')
        elif tmp_list[0] == "2":
            file_path = "/home/ubuntu/EC2_python_realtime/realtime_data_json/realtime_2.json"
            make_Json_file(tmp_list[0], tmp_list[1], tmp_list[2], file_path)
            os.system('scp -i "/home/ubuntu/socket_programming.pem" /home/ubuntu/EC2_python_realtime/realtime_data_json/realtime_2.json ubuntu@ec2-13-209-12-175.ap-northeast-2.compute.amazonaws.com:/home/ubuntu/project4/realtime/')"""
        # ====================================================================================================================================================================
        print(integrity_check_send(hd, file_name, receive_directory))
        # ====================================================================================================================================================================
        print("file name : " + file_name)
        print("size : " + f_size)
        print("hash digest : ", hd)
        """except:
            print("연결 끊김")
            client_socket.close()
            break
"""


def handle_send1(client_socket):
    while 1:
        if os.path.isfile(send_directory + "control_1.xml"):
            # XML_Data = parsing_XML("control_test.xml", send_directory)
            file_name = "control_ras1.xml"
            os.system("cp " + send_directory + "control_1.xml " + send_directory + file_name)
            # 해당 경로에 파일이 없으면 에러
            if not exists(send_directory + file_name):
                msg = "error"
                client_socket.sendall(msg.encode())
                client_socket.close()
                return

            client_socket.sendall(getFileSize(file_name, send_directory).encode())
            # client가 파일 내용을 받을 준비되었는지 확인
            ru_ready = client_socket.recv(1024)
            if ru_ready.decode() == "ready":
                client_socket.sendall(file_name.encode())
                real_ready = client_socket.recv(1024)
                if real_ready.decode() == "real":
                    client_socket.sendall(getFileData(file_name, send_directory).encode())
                    print("해시 결과 : ", hashing(file_name, send_directory))
                    client_socket.sendall(hashing(file_name, send_directory).encode())
            # 전송 후 파일 바로 삭제
            os.remove(send_directory + file_name)
            os.remove(send_directory + "control_1.xml")
    client_socket.close()


def handle_send2(client_socket):
    while 1:
        if os.path.isfile(send_directory + "control_2.xml"):
            # XML_Data = parsing_XML("control_test.xml", send_directory)
            file_name = "control_ras2.xml"
            os.system("cp " + send_directory + "control_2.xml " + send_directory + file_name)
            # 해당 경로에 파일이 없으면 에러
            if not exists(send_directory + file_name):
                msg = "error"
                client_socket.sendall(msg.encode())
                client_socket.close()
                return

            client_socket.sendall(getFileSize(file_name, send_directory).encode())
            # client가 파일 내용을 받을 준비되었는지 확인
            ru_ready = client_socket.recv(1024)
            if ru_ready.decode() == "ready":
                client_socket.sendall(file_name.encode())
                real_ready = client_socket.recv(1024)
                if real_ready.decode() == "real":
                    client_socket.sendall(getFileData(file_name, send_directory).encode())
                    print("해시 결과 : ", hashing(file_name, send_directory))
                    client_socket.sendall(hashing(file_name, send_directory).encode())
            # 전송 후 파일 바로 삭제
            os.remove(send_directory + file_name)
            os.remove(send_directory + "control_2.xml")
    client_socket.close()


def accept_func():
    
    '''
    send_port_ras1 = 8345
    rcv1_port = 8341
    edgeNo1 = '1'

    
    server_socket_rcv1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_rcv1.bind((host, rcv1_port))
    server_socket_rcv1.listen(1)


    server_socket_ras1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_ras1.bind((host, send_port_ras1))
    server_socket_ras1.listen(1)'''

    send_port_ras2 = 8343
    rcv2_port = 8342
    edgeNo2 = '2'

    server_socket_rcv2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_rcv2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket_rcv2.bind((host, rcv2_port))
    server_socket_rcv2.listen(1)

    server_socket_ras2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_ras2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket_ras2.bind((host, send_port_ras2))
    server_socket_ras2.listen(1)

    # 서버 소켓 rcv는 실시간 상황을 받는 소켓으로, 엣지 마다 소켓을 열며 소켓 당 최대 1개의 클라이언트의 접속을 허용한다.
    # 서버 소켓 ras는 제어를 보내는 소켓으로, 엣지 마다 소켓을 열며 소켓 당 최대 1개의 클라이언트의 접속을 허용한다.
    while 1:
        try:
            # 클라이언트 함수가 접속하면 새로운 소켓을 반환한다.
            #client_socket_rcv1, addr1 = server_socket_rcv1.accept()
            #client_socket_ras1, addr3 = server_socket_ras1.accept()
            
            client_socket_rcv2, addr2 = server_socket_rcv2.accept()
            client_socket_ras2, addr4 = server_socket_ras2.accept()
            print("접속 완료")
        except KeyboardInterrupt:
            #server_socket_rcv1.close()
            #server_socket_ras1.close()
            
            server_socket_rcv2.close()
            server_socket_ras2.close()
            print("Keyboard interrupt, Server 종료...")


        #send_ras1_thread = threading.Thread(target=handle_send1, args=(client_socket_ras1,))
        #rcv1_thread = threading.Thread(target=handle_receive, args=(client_socket_rcv1,))
        #send_ras1_thread.daemon = True
        #rcv1_thread.daemon = True
        #send_ras1_thread.start()
        #rcv1_thread.start()

        send_ras2_thread = threading.Thread(target=handle_send2, args=(client_socket_ras2,))
        rcv2_thread = threading.Thread(target=handle_receive, args=(client_socket_rcv2,))
        send_ras2_thread.daemon = True
        rcv2_thread.daemon = True
        send_ras2_thread.start()
        rcv2_thread.start()

if __name__ == '__main__':
    accept_func()
