# # https://joycecoder.tistory.com/107
# import json
# import requests
# # from bs4 import BeautifulSoup as bs

# url = 'https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20210619&endTime=20210720&timeframe=week'
# headers = {
#     'Referer': 'http://finance.naver.com',
#     'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127'
# }
# response = requests.get(url, headers=headers)
# print(response.content)
# # print(response.json()['data'])


from urllib import parse 
from ast import literal_eval 
import requests 

def get_sise(code, start_time, end_time, time_from='day'): 
    get_param = { 
        'symbol': code, 
        'requestType': 1, 
        'startTime': start_time, 
        'endTime': end_time, 
        'timeframe': time_from 
    } 
    get_param = parse.urlencode(get_param) 
    url = f"https://api.finance.naver.com/siseJson.naver?{get_param}"
    response = requests.get(url) 
    
    return literal_eval(response.text.strip())

print(get_sise('005930', '20210601', '20210605', 'day'))