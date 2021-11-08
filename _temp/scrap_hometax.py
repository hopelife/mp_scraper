# import time, datetime

# import requests
# import urllib.request
# import lxml.html as etree
# import re
import os, sys

sys.path.append(os.path.join(os.path.abspath('../staff')))
from ScrapBySelenium import ScrapBySelenium
from function_basic import convert_to_digit, write_file, read_file, create_folder

# 공동인증서 로그인

import time

## 홈텍스로 이동 
# url = "https://www.hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index.xml"
url = "https://www.hometax.go.kr/"

s = ScrapBySelenium(url=url, browser='chrome', headless=False)

## 로그인 버튼 클릭
s.driver.find_element_by_id('group88615548').click()

time.sleep(2)

## 본문영역(iframe)
iframe = s.driver.find_element_by_id('txppIframe')
s.driver.switch_to.frame(iframe)

time.sleep(2)


## 로그인 버튼
s.driver.find_element_by_id('anchor22').click() 

time.sleep(2)

## 공인인증서 영역
iframe = s.driver.find_element_by_id('dscert')
s.driver.switch_to.frame(iframe)

time.sleep(2)

# 두번째 공인인증서 선택
# driver.find_element_by_xpath('//*[@title="파이낸스 데이터(20607)0003029201709191518042"]').click()
s.driver.find_element_by_xpath('//*[@title="증권/보험용"]').click()

time.sleep(2)

# 인증서 비밀번호 입력
passwd = 'moon5221!!'
s.driver.find_element_by_id('input_cert_pw').send_keys(passwd)
s.driver.find_element_by_id('btn_confirm_iframe').click()

time.sleep(2)

# 상위 프레임으로 이동
s.driver.switch_to_default_content()
s.driver.close()

    
