'''
# web crawling for bid http://www.g2b.go.kr(나라장터 입찰)
## urls
* BASE: http://www.g2b.go.kr

* list(개찰결과 목록): http://www.g2b.go.kr:8340/body.do?kwd=%B3%BB%C1%F8%20%BC%BA%B4%C9%C6%F2%B0%A1&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&startDate2=&endDate2=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=&preKwd=&preKwds=&body=yes

* detail(물품 개찰결과 상세조회): http://www.g2b.go.kr:8340/body.do?kwd=%B3%BB%C1%F8%20%BC%BA%B4%C9%C6%F2%B0%A1&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&startDate2=&endDate2=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=&preKwd=&preKwds=&body=yes

* http://www.g2b.go.kr:8101/ep/result/serviceBidResultDtl.do?bidno=param[0]&bidseq=param[1]&whereAreYouFrom=piser

* 예비가격 산정결과: http://www.g2b.go.kr:8101/ep/open/pdamtCalcResultDtl.do?bidno=20070516090&bidseq=01&bidcate=0

### keyword: 내진(%B3%BB%C1%F8), 정밀(%C1%A4%B9%D0)
### 지역: 충청남도, 지역제한 없음(전국)

### 기관명 찾기@@@


'''

import requests
from bs4 import BeautifulSoup
import json
import os

BASE_DIR = '/Volumes/data/dev/projects/crawl/python/test'
#BASE_DIR = 'c:/moon/test'
MAX_PAGE = 20

def spider(url, tag):
	url = url
	source_code = requests.get(url)
	#source_code.encoding=None   # None 으로 설정
	source_code.encoding='euc-kr'  # 한글 인코딩
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, 'lxml')

	f = open(BASE_DIR + '/gc_list3.html', 'w')
	f.write(plain_text)
	f.close()

	return soup.select(tag)

def js2arr(js_str):
	js_str = js_str.replace('javascript:','').replace(')','').replace("'",'')
	arr1 = js_str.split('(')
	arr2 = arr1[1].split(',')
	return (arr1[0], arr2)



def get_url(tpl):
	js = tpl[0]
	param = tpl[1]

	if js == "showGcPostLinkView":
		url = "http://www.g2b.go.kr:8101/ep/result/serviceBidResultDtl.do?"
		add = "bidno=" + param[0] + "&bidseq=" + param[1] +"&whereAreYouFrom=piser"

	elif js == "showGcLinkView":
		url = "http://www.g2b.go.kr:8340/link.do?kwd=%B3%BB%C1%F8%20%BC%BA%B4%C9%C6%F2%B0%A1&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo="
		add = "&val1=" + param[0] + "&val2=" + param[1] + "&val3=" + param[2] + "&seq=" + param[3] + "&type=" + param[4] + "&target=%BF%EB%BF%AA"

	return url + add


url_head = "http://www.g2b.go.kr:8340/body.do?kwd=%B3%BB%C1%F8%20%BC%BA%B4%C9%C6%F2%B0%A1&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum="

url_tail = "&srchFd=ALL&date=&startDate=&endDate=&startDate2=&endDate2=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=&preKwd=&preKwds=&body=yes"

arr = []
page = 1

# MAX_PAGE까지 page 증가하면서 반복
while (page < MAX_PAGE):
	url = url_head + str(page) + url_tail

	for title in spider(url, 'li'):
		data = {}
		num = title.find("span", {"class":"num"})

		if num:
			data["num"] = num.string
			#data["js"] = title.find("strong", {"class":"tit"}).find("a").get("href")
			js = title.find("strong", {"class":"tit"}).find("a").get("href")
			#data["name"] = title.find("strong", {"class":"tit"}).text.replace(data["num"],'').replace('\n','').replace('\t','')
			#data["org"] = title.find("span", {"class":"date"}).text.replace("수요기관", "").replace('\n','').replace('\t','')
			data["org"] = title.find("span", {"class":"date"}).text.replace("수요기관", "").strip()
			data["url"] = get_url(js2arr(js))

			arr.append(data)

	page += 1


with open(os.path.join(BASE_DIR, 'gc_arr.json'), 'w+') as json_file:
	json.dump(arr, json_file)
