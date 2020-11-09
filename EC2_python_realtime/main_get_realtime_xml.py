from parsing import *


tmp_list = parsing_XML()
# 반환된 리스트의 첫번째 값은 엣지넘버
# 반환된 리스트의 두번째 값은 신호등 번호
print("realtime.xml 에서 parsing한 값")
print("edgeNO : " + tmp_list[0])
print("traffic_light : " + tmp_list[1])

# 첫번째 매개변수는 str 타입의 edgeNo
# 두번째 매개변수는 str 타입의 traffic_light
salt_value = get_salt_value(tmp_list[0], tmp_list[1])
# 반환된 값은 str타입의 salt_value
print("salt_value : " + salt_value)

# 첫번째 매개변수는 str 타입의 파일이름
# 두번째 매개변수는 str 타입의 솔트값
hash_value = make_hash("./realtime_data_xml/realtime.xml", salt_value)
# 반환된 값은 str 타입의 hash 값
print("hash_value : " + hash_value)

# 라파로부터 받은 hash값이라고 가정
Raspberry_hash_value = "a9f4f854cf913efcc645a1398df79ce92487ab3c9f458ae007c06c902ec525da"
integrity_check(hash_value, Raspberry_hash_value)

# json 파일 만들기
make_Json_file(tmp_list[0], tmp_list[1], tmp_list[2])

# 무결성 검사 후 EC2(라파통신) => EC2(관리자페이지) 파일 넘기기
result = integrity_check(hash_value, Raspberry_hash_value)
print(result)
