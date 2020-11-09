# xml 파일을 parsing하기 위해 import
from xml.etree import ElementTree

# xml 데이터를 받고 무결성 검사를 하기 위해
# 어떤 엣지인지? 어떤 신호등인지? 확인하기 위한 함수
# 리턴값은 엣지넘버, 신호등번호, 시간을 리스트로 반환
def parsing_XML():
    tree = ElementTree.parse('./realtime_data_xml/realtime.xml')
    root = tree.getroot()
    # root에서 나머지 세부 문자 추출
    edgeNo = root.findtext("edgeNo")
    traffic_light = root.findtext("traffic_light")
    time = root.findtext("time")
    return [edgeNo, traffic_light, time]

# pip install pymysql
import pymysql

# 솔트값을 얻기 위한 함수
def get_salt_value(edgeNo, traffic_light):
    table = str()
    if edgeNo == '1':
        table = 'E1_salt'
    elif edgeNo == '2':
        table = 'E2_salt'
    # MySQL Connection 연결
    conn = pymysql.connect(host='database-1.ckkbkqdct7py.ap-northeast-2.rds.amazonaws.com', user='admin', password='kshieldjr', db='Raspberry_Communication', charset='utf8')
    # Connection으로부터 Cursor 생성
    curs = conn.cursor()
    # SQL문 실행
    sql = "select salt from " + table + " where id = '" + traffic_light + "'"
    curs.execute(sql)
    # 데이터 Fetch
    rows = curs.fetchall()
    # connection 닫기
    conn.close()
    return rows[0][0]

# pip install pycryptodomex
from Cryptodome.Hash import SHA256 as SHA

# 첫번째 매개변수는 str 타입의 파일이름
# 두번째 매개변수는 str 타입의 솔트값
def make_hash(filename, salt_value):
    # 파일을 바이너리 읽기 모드로 열기
    f = open(filename, mode = "rb")
    tmp_binary = f.read()
    # print(tmp_binary)
    tmp = bytes(salt_value, encoding="utf-8")
    # print(tmp)
    tmp_binary += tmp
    # print(tmp_binary)
    # SHA256 객체 생성
    hash = SHA.new()
    # hashing
    hash.update(tmp_binary)
    return hash.hexdigest()

# json 파일을 생성하기 위해 import
import json
from collections import OrderedDict

# Json 파일 만들기
def make_Json_file(edgeNO, traffic_light, time, file_path):
    file_data = OrderedDict()
    file_data["edgeNo"] = edgeNO
    file_data["traffic_light"] = traffic_light
    file_data["time"] = time
    print(json.dumps(file_data, ensure_ascii=False, indent="\t"))
    with open(file_path, 'w', encoding='utf-8') as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, indent="\t")


import os
# 무결성 검사
def integrity_check(hash_value, Raspberry_hash_value):
    # 생성한 해쉬 값과 받은 해쉬 값이 같으면 파일 전송
    if hash_value == Raspberry_hash_value:
        os.system('scp -i "/home/ubuntu/EC2_python_realtime/socket_programming.pem" ./realtime_data_json/realtime.json ubuntu@ec2-13-209-12-175.ap-northeast-2.compute.amazonaws.com:/home/ubuntu/project/realtime_data_json/')
        return True
    # 생성한 해쉬 값과 받은 해쉬 값이 다르면 전송하지 않고
    # 로그 기록!!!!!!!!!!!! <= 이거 만들기
    else:
        return False
