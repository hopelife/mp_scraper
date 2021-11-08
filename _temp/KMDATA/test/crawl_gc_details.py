import requests
from bs4 import BeautifulSoup
import json
import os
import re

BASE_DIR = '/Volumes/data/dev/projects/crawl/python/test'
#BASE_DIR = 'c:/moon/test'
JSON_FILE = 'gc_arr.json'


def spider(url, tag, file_name):
	url = url
	source_code = requests.get(url)
	source_code.encoding=None   # None 으로 설정
	#source_code.encoding='euc-kr'  # 한글 인코딩
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, 'lxml')

	f = open(BASE_DIR + '/' + file_name, 'w')
	f.write(plain_text)
	f.close()

	return soup.select(tag)



f = open(BASE_DIR + '/' + JSON_FILE, 'r')
jsn = json.loads(f.read())
f.close()

'''
#data
#{"num":"","name":"","bid":[{"no":"", "bn"]}

"num": 입찰공고번호
"name": 공고명
"norg": 공고기관
"dorg": 수요기관
"rdate": 실제개찰일시

"bid": 개찰 내역
"no": 순위
"bn": 사업자등록번호(biz number)
"bname": 상호명
"cname": 대표자명
"bprice": 입찰금액
"brate": 투찰률
"rn": 추첨번호(raffle number)
"bdate": 투찰일시
'''

arr = []

for item in jsn:
	tail = item["num"][1:-1] + ".html"
	file_name = "gc_detail_" + tail
	soup = spider(item["url"], "tbody tr", file_name)
	data = {"num": item["num"][1:-1], "content":[]}
	for cont in soup:
		for i in cont.find_all('td'):
			t = re.sub('\n|\r|\t', '', i.text)
			t = re.sub('^ +| +$', '', t)
			#t = re.sub('\n|\t|^ +| +$', '', t)
			data["content"].append(t)
			#print(re.sub('\n|\t|^ +| +$', '', i.text))
			#print(i.text.replace('\n','').replace('\t',''))
	arr.append(data)

with open(os.path.join(BASE_DIR, 'gc_detail_arr.json'), 'w+') as json_file:
	json.dump(arr, json_file)




#예비가격 산정결과
#http://www.g2b.go.kr:8101/ep/open/pdamtCalcResultDtl.do?bidno=20070516090&bidseq=01&bidcate=0
