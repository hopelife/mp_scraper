import requests
from bs4 import BeautifulSoup
import json
import os

BASE_DIR = '/Volumes/data/dev/projects/crawl/python/test'
#BASE_DIR = 'c:/moon/test'

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
		#url = "http://www.g2b.go.kr:8340/link.do?kwd=%B3%BB%C1%F8%20%BC%BA%B4%C9%C6%F2%B0%A1&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo="
		#add = "&val1=" + param[0] + "&val2=" + param[1] + "&val3=" + param[2] + "&seq=" + param[3] + "&type=" + param[4] +  "&div=" + param[5] + "&target=%BF%EB%BF%AA"
		url = "http://www.g2b.go.kr:8101/ep/result/serviceBidResultDtl.do?"
		add = "bidno=" + param[0] + "&bidseq=" + param[1] +"&whereAreYouFrom=piser"

	elif js == "showGcLinkView":
		url = "http://www.g2b.go.kr:8340/link.do?kwd=%B3%BB%C1%F8%20%BC%BA%B4%C9%C6%F2%B0%A1&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo="
		add = "&val1=" + param[0] + "&val2=" + param[1] + "&val3=" + param[2] + "&seq=" + param[3] + "&type=" + param[4] + "&target=%BF%EB%BF%AA"

	return url + add


'''
http://www.g2b.go.kr:8340/link.do?kwd=내진 성능평가&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=&
val1=20070516090&val2=01&val3=&seq=1&type=1&div=1&target=%BF%EB%BF%AA

http://www.g2b.go.kr:8340/link.do?kwd=내진 성능평가&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=&val1=20070516090&val2=01&val3=&seq=1&type=1&div=1&target=%BF%EB%BF%AA

http://www.g2b.go.kr:8340/link.do?kwd=\ub0b4\uc9c4 \uc131\ub2a5\ud3c9\uac00&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=
&val1=20070516090&val2=01&val3=&seq=1&type=1&div=1&target=\uc6a9\uc5ed




http://www.g2b.go.kr:8340/link.do?kwd=%B3%BB%C1%F8%20%BC%BA%B4%C9%C6%F2%B0%A1&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=
&val1=20070516090&val2=01&val3=&seq=1&type=1&div=1&target=%BF%EB%BF%AA
'''
#data = {'key':[], 'val':[]}


## 개찰결과 목록
#gc_list.html
#url = "http://www.g2b.go.kr/pt/menu/selectSubFrame.do?framesrc=http://www.g2b.go.kr:8340/search.do?category=GC&kwd=%B3%BB%C1%F8%20%BC%BA%B4%C9%C6%F2%B0%A1"

#gc_list.html
#url = "http://www.g2b.go.kr:8340/search.do?category=GC&kwd=%B3%BB%C1%F8%20%BC%BA%B4%C9%C6%F2%B0%A1"

#gc_list3.html
#url = "http://www.g2b.go.kr:8340/body.do?kwd=내진 성능평가&category=GC"
url = "http://www.g2b.go.kr:8340/body.do?kwd=%B3%BB%C1%F8%20%BC%BA%B4%C9%C6%F2%B0%A1&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&startDate2=&endDate2=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=&preKwd=&preKwds=&body=yes"

#gc_list3.html
#showGcLinkView( val1, val2, val3, seq, type, target)


## 용역 개찰결과 상세조회
#gc_list3.html
#showGcPostLinkView( val1, val2, val3, seq, div, type, target)


#data = {"num":"", "js":"", "url":"", "name":"", "org":""}
arr = []


## 용역 개찰결과 상세조회 content
#http://www.g2b.go.kr:8101/ep/result/serviceBidResultDtl.do?bidno=20070704413&bidseq=00&whereAreYouFrom=piser

for title in spider(url, 'li'):
	data = {}
	num = title.find("span", {"class":"num"})

	if num:
		data["num"] = num.string
		data["js"] = title.find("strong", {"class":"tit"}).find("a").get("href")
		data["name"] = title.find("strong", {"class":"tit"}).text.replace(data["num"],'').replace('\n','').replace('\t','')
		data["org"] = title.find("span", {"class":"date"}).text.replace("수요기관", "").replace('\n','').replace('\t','')
		data["url"] = get_url(js2arr(data["js"]))

		#print(arr)
		arr.append(data)

with open(os.path.join(BASE_DIR, 'gc_arr.json'), 'w+') as json_file:
	json.dump(arr, json_file)


'''
for title in spider(url, 'tr'):

	if title.find(string="배정예산"):
		print(title.find('p', text="배정예산").parent.next_sibling.next_sibling.string)
		data['key'].append(title.find(text="배정예산"))

with open(os.path.join(BASE_DIR, 'result2.json'), 'w+') as json_file:
	json.dump(data, json_file)


for title in spider(url, '.tit a'):
	data['num'].append(title.find('span').string)
	data['href'].append(title.get('href'))
with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
	json.dump(data, json_file)
'''

'''
## 목록 페이지


/link.do? url + "&val1=" + val1 + "&val2=" + val2 + "&val3=" + val3 + "&seq=" + seq + "&type=" + type + "&target=" + target


## 상세 페이지
http://www.g2b.go.kr:8340/link.do?
kwd=%B3%BB%C1%F8&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=
&val1=20180506430&val2=00&val3=0&seq=1&type=1&target=%B9%B0%C7%B0



http://www.g2b.go.kr:8340/link.do?
kwd=%B3%BB%C1%F8&category=GC&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=
&val1=20180518200&val2=00&val3=0&seq=1&type=1&target=%B9%B0%C7%B0

## 입찰공고

javascript:showTgongLinkView('20180518200','00','1','%EC%9A%A9%EC%97%AD');

http://www.g2b.go.kr:8340/link.do?
kwd=%B3%BB%C1%F8&category=TGONG&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=&val1=20180517316&val2=00&type=1&target=%EC%9A%A9%EC%97%AD

javascript:showTgongLinkView('20180517316','00','1','%EC%9A%A9%EC%97%AD');

javascript:showTgongLinkView('20180517798','00','1','%EC%9A%A9%EC%97%AD');
http://www.g2b.go.kr:8340/link.do?kwd=%B3%BB%C1%F8&category=TGONG&subCategory=ALL&detailSearch=false&sort=R&reSrchFlag=false&pageNum=1&srchFd=ALL&date=&startDate=&endDate=&orgType=balju&orgName=&orgCode=&swFlag=Y&dateType=&area=&gonggoNo=&val1=20180517798&val2=00&type=1&target=%BF%EB%BF%AA

function showTgongLinkView( val1, val2, type, target) {
	var url = "kwd=³»Áø";
	url += "&category=TGONG";
	url += "&subCategory=ALL";
	url += "&detailSearch=false";
	url += "&sort=R";
	url += "&reSrchFlag=false";
	url += "&pageNum=1";
	url += "&srchFd=ALL";
	url += "&date=";
	url += "&startDate=";
	url += "&endDate=";
	url += "&orgType=balju";
	url += "&orgName=";
	url += "&orgCode=";
	url += "&swFlag=Y";
	url += "&dateType=";
	url += "&area=";
	url += "&gonggoNo=";

	location.href="/link.do?" + url + "&val1=" + val1 + "&val2=" + val2 + "&type=" + type + "&target=" + target;
}


javascript:showGcLinkView('20180506430','00','0','1','1','물품')">


function showGcLinkView( val1, val2, val3, seq, type, target) {
	var url = "kwd=³»Áø";
	url += "&category=GC";
	url += "&subCategory=ALL";
	url += "&detailSearch=false";
	url += "&sort=R";
	url += "&reSrchFlag=false";
	url += "&pageNum=1";
	url += "&srchFd=ALL";
	url += "&date=";
	url += "&startDate=";
	url += "&endDate=";
	url += "&orgType=balju";
	url += "&orgName=";
	url += "&orgCode=";
	url += "&swFlag=Y";
	url += "&dateType=";
	url += "&area=";
	url += "&gonggoNo=";

	location.href="/link.do?" + url + "&val1=" + val1 + "&val2=" + val2 + "&val3=" + val3 + "&seq=" + seq + "&type=" + type + "&target=" + target;
}

## 입찰 공고

 공고 찜하기
입찰집행 부가정보

PQ심사결과조회
  TP심사결과조회
  지명경쟁자료조회
  실적경쟁자료조회
  과업설명참가조회
신청서/입찰서 제출

PQ심사신청
  실적심사신청
  적격심사신청
  과업설명참가신청
  공동수급협정서관리
 지문투찰
[공고일반 ]
공고종류

실공고
게시일시

2018/05/15 13:44
입찰공고번호

20180518200 - 00
참조번호

강원도철원교육지원청 공고 제2018-53호
공고명

장흥초 외 3교(오덕초,묘장초,토성초) 내진성능평가용역
본 공고는 지문인식 전자입찰제도가 적용되오니 미리 지문보안토큰에 지문정보를 등록하여야 합니다.
btSafety 본 공고는 "나라장터 안전 입찰서비스"를 이용하여야만 전자입찰서를 제출 할 수 있습니다. 유의사항 안내
공고기관

강원도교육청 강원도철원교육지원청
수요기관

강원도교육청 강원도철원교육지원청
입찰방식

전자입찰
낙찰방법

공고서 참조
계약방법

제한경쟁
국제입찰구분

국내입찰
용역구분

기술용역
발주계획번호

5-1-2018-7931000-000008
재입찰

재입찰 허용
(재입찰시 예비가격을 다시 생성하여 예정가격이 산정됩니다.)
국내/국제 입찰사유

국제입찰 비대상(고시금액 이하 또는 대상기관아님)
WTO품목번호

입찰자격

공고서 참조
관련공고

[입찰집행 및 진행 정보 ]
집행관

권현옥
최초입회관(담당자)

권현옥
입찰개시일시

2018/05/19 10:00
입찰마감일시

2018/05/23 10:00
개찰(입찰)일시

2018/05/23 11:00
개찰장소

국가종합전자조달시스템(나라장터)
입찰참가자격등록
마감일시

2018/05/22 18:00
조달청 입찰참가등록 가능시간은 평일 09:00~18:00 이며, 토요일, 일요일 및 공휴일은 업무처리가 불가합니다.
본 입찰에 참여하는 업체는 입찰참가자격등록마감일시까지 나라장터에 경쟁입찰참가자격등록을 해야 합니다.
보증서접수마감일시


보증서 접수마감일시를 입력하지 않은 경우에는, 입찰서 접수마감일 전일 18시까지 제출이 가능합니다.
(단, 입찰보증금지급각서로 대체하는 경우 보증금이 면제됩니다.)
공동수급협정서
접수여부

방식: 공고서참조 공동수급불허
공동수급협정서
마감일시

마감: 공고서 참조
PQ심사신청서

방식: 없음
PQ심사신청서
신청기한

TP심사신청서

없음
TP심사신청서
신청기한

실적심사신청서

방식: 없음
실적심사신청서
신청기한

과업설명장소

과업설명일시

동가입찰 낙찰자
자동추첨프로그램

사용
[입찰참가수수료 및 입찰보증금 납부정보 ]
입찰참가수수료 납부

방식: 공고서참조
입찰참가수수료금액

원
입찰보증금납부

채권자명

강원도철원교육지원청 채권관리관
[예정가격 결정 및 입찰금액 정보]
예가방법

복수예가 : 4 (추첨예가) / 15 (총예가)
추첨번호공개여부

비공개
배정예산

66,768,000원
추정가격

60,698,182원
[투찰제한 - 일반 ]
지역제한

투찰제한
참가가능지역

[강원도]
지사투찰허용여부

지사투찰불허
업종제한

투찰제한
업종사항제한

[ 안전진단전문기관(건축)(1397) ]업종 또는
[ 안전진단전문기관(종합)(4963) ]업종을 등록한 업체

※업종명을 클릭시 관련 근거법령을 조회하실수 있습니다.
※[]안의 업종제한은 시스템상에 입력된 제한사항으로 공고서와 상이할 수도 있습니다.
   입찰에 참여하시기 전에 반드시 공고서를 숙지하여 정확한 제한 업종을 확인하시기 바랍니다.

※아래는 제한된 업종에 대해 투찰가능한 허용업종 상황을 보여줍니다. 확인하시기 바랍니다.
No.	투찰가능한업종	허용업종
1	안전진단전문기관(건축)(1397)	안전진단전문기관(종합)(4963)
과업설명 제한여부

참가제한안함
공동수급체 구성원 지역제한적용여부

공고서에 의함
[ 기초금액 공개 ]
기초금액	비고1	비고2	상세보기
자료없음[첨부 파일 ]
No.	문서구분	파일명
1	공고서
20180518200-00_1526359393153_[공고문] 장흥초 외 3교(오덕초,묘장초,토성초) 내진성능평가용여.hwp
2	과업지시서
20180518200-00_1526359393163_학교시설 내진성능평가 과업지지서.hwp
-	안내사항	안전입찰 유의사항 안내.html



## 개찰 결과



## 최종 낙찰자
http://www.g2b.go.kr:8101/ep/co/selectCompInfo.do?bizRegNo=2208125905&tbidno=20180509384&bidseq=00&rebidno=0


javascript:openbider('2208125905','20180509384','00','0','bider')

상호명

(주)도화구조
영문상호명

Dohwa Structural Engineers Co., Let.
대표자명

이재훈
주소

서울특별시 강남구 역삼로9길 13, 3층 (역삼동, 한신빌딩)
전화번호

02-539-0305
홈페이지


## 발주계획


## 사전규격


## 계약진행현황


## 전자서고

'''



'''
입찰분류	재입찰번호	수요기관	세부품명	최저입찰자 또는
낙찰예정자	투찰금액(원)	투찰률(%)	진행상황
1	0	부산광역시 연제구	교량받침	(주)리더스산업	125,107,540	84.335	개찰완료
'''


'''
개찰결과 -> 낙찰 패턴 예측 (입찰가, )

입찰분류, 투찰금액, 투찰액

투찰 상세내역



http://www.g2b.go.kr:8101/ep/open/pdamtCalcResultDtl.do


예비가격 산정결과
입찰공고번호	20180325452-00	참조번호	부산광역시 연제구 공고 제2018-298호
입찰분류	1	재입찰번호	0
공고명	연산교 내진보강 및 보수보강 공사 관련 교량받침 제조구매
낙찰자선정적용기준	행정자치부 기준	실제 개찰일시	2018-03-22 15:24
예가범위	-3% ~ +3%	기초금액기준	7
		상위갯수
정렬기준	Random 저장	복수예비가격	2018-03-22 9:15
		작성시각
구분	금액	추첨횟수	구분	금액	추첨횟수
추첨가격 1	145,316,600	2	추첨가격 2	145,937,700	1
추첨가격 3	150,003,500	3	추첨가격 4	147,002,800	2
추첨가격 5	146,738,700	2	추첨가격 6	150,123,000	0
추첨가격 7	143,985,900	1	추첨가격 8	147,920,400	2
추첨가격 9	144,959,600	2	추첨가격 10	148,649,200	3
추첨가격 11	144,412,300	2	추첨가격 12	149,410,400	3
추첨가격 13	151,801,800	2	추첨가격 14	151,273,700	1
추첨가격 15	143,423,900	2
예정가격	148,344,925	기초금액	147,525,000



입찰공고 -> 입찰가 결정 -> 입찰

게시일
입찰고고번호
공고명
공고기관
입찰방식
계약방법

발주계획번호

배정예산
추정가격

첨부파일


'''
