import requests
import chardet
from bs4 import BeautifulSoup

def spider(max_pages):
	#page = 1
	#while page < max_pages:
		#url = 'http://creativeworks.tistory.com/' + str(page)
		url = "http://www.g2b.go.kr:8340/body.do?kwd=%B3%BB%C1%F8&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&startDate2=&endDate2=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=&preKwd=&preKwds=&body=yes"
		source_code = requests.get(url)

		source_code.encoding=None   # None 으로 설정
		#print("encoding:", source_code.encoding)
		#source_code.encoding='euc-kr'  # 한글 인코딩

		plain_text = source_code.text

		soup = BeautifulSoup(plain_text, 'lxml')
		print(soup)


		for link in soup.select('.tit'):
			href = link.select('a')
			title = link.select('.num')
			print(href)
			#print(title)

		#page += 1

spider(2)
