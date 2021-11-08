import requests
from bs4 import BeautifulSoup
import json
import os

BASE_DIR = '/Volumes/data/dev/projects/crawl/python/test'

def spider(url, tag):
	url = url
	source_code = requests.get(url)

	source_code.encoding=None   # None 으로 설정
	#print("encoding:", source_code.encoding)
	#source_code.encoding='euc-kr'  # 한글 인코딩

	plain_text = source_code.text

	soup = BeautifulSoup(plain_text, 'lxml')
	#print(soup)

	return soup.select(tag)

data = {'num':[], 'href':[]}

url = "http://www.g2b.go.kr:8340/body.do?kwd=%B3%BB%C1%F8&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&startDate2=&endDate2=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=&preKwd=&preKwds=&body=yes"

#print(spider(url, '.tit'))

for title in spider(url, '.tit a'):
	data['num'].append(title.find('span').string)
	data['href'].append(title.get('href'))

with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
  json.dump(data, json_file)

'''
for title in my_titles:
    data[title.text] = title.get('href')


with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
    json.dump(data, json_file)
'''
