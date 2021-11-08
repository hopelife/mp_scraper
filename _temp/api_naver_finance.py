# https://joycecoder.tistory.com/107

import requests
# from bs4 import BeautifulSoup as bs

url = 'https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20210619&endTime=20210720&timeframe=week'
headers = {
    'Referer': 'http://finance.naver.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127'
}
response = requests.get(url, headers=headers)
print(response.json()['data'])
# jsonObjs = response.json()
# dataList = jsonObjs['data']
# for data in dataList :
#     print(data['name'])