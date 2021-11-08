import requests
import json

#json header에 있는 json url 주소
json_url = 'https://askdjango.github.io/lv2/data.json'

#받아온 json을 텍스트로 변환
json_string = requests.get(json_url).text

#json모듈을 사용해서 로드
data_list = json.loads(json_string)

print(data_list)
