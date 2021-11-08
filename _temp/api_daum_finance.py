# https://souljit2.tistory.com/7

import requests
# from bs4 import BeautifulSoup as bs

url = 'https://finance.daum.net/api/search/ranks?limit=10'
headers = {
    'Referer': 'http://finance.daum.net',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127'
}
response = requests.get(url, headers=headers)
print(response.json()['data'])
# jsonObjs = response.json()
# dataList = jsonObjs['data']
# for data in dataList :
#     print(data['name'])