# import time, datetime

# import requests
# import urllib.request
# import lxml.html as etree
# import re
import os, sys

sys.path.append(os.path.join(os.path.abspath('../staff')))
from ScrapBySelenium import ScrapBySelenium
from function_basic import convert_to_digit, write_file, read_file, create_folder

import time
import math
import json
import lxml.html as etree
from urllib import parse

## 전역 상수
BASE_URL = "https://cafe.daum.net/poordoctor"
BASE_PATH = "../_scrap/_poordoctor"

### NOTE: 로그인

# 카카오계정 로그인 페이지 
# url = "https://accounts.kakao.com/login?continue=https%3A%2F%2Flogins.daum.net%2Faccounts%2Fksso.do%3Frescue%3D"
url = "https://accounts.kakao.com/login?continue=https%3A%2F%2Flogins.daum.net%2Faccounts%2Fksso.do%3Frescue%3Dtrue%26url%3Dhttps%253A%252F%252Fcafe.daum.net%252F_c21_%252Fhome%253Fgrpid%253DfjM0"

s = ScrapBySelenium(url=url, browser='chrome', headless=False)

## 아이디, 비밀번호 입력
id = 'monwater@naver.com'
pw = 'Mo5221on!'

s.driver.find_element_by_id('id_email_2').send_keys(id)  # 아이디
s.driver.find_element_by_id('id_password_3').send_keys(pw)  # 비밀번호
s.driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
time.sleep(3)


### NOTE: 리스트(검색)
# ## 검색 버튼 클릭
# # frame 이동
# iframe = s.driver.find_element_by_id('down')  
# s.driver.switch_to.frame(iframe)

# # 검색어 입력
# word = '붉은나비'
# s.driver.find_element_by_xpath('.//input[@name="search_left_query"]').send_keys(word)
# s.driver.find_element_by_xpath('//a[@class="btnSearch btn_search"]').click()

# ## 상세 검색 영역
# s.driver.find_element_by_xpath('.//select[@name="item"]/option[@value="writer"]').click() # 검색범위 변경(글쓴이)
# s.driver.find_element_by_id("suggest_search0").click()  # 검색 버튼 클릭

# ## 검색 결과 페이지
# # 검색 결과 개수 확인
# total = int(s.driver.find_element_by_xpath('.//em[@class="txt_point"]').text)
# # print(f"total: {total}")

# # 출력 개수 변경
# s.driver.find_element_by_id("viewListBtn").click()
# s.driver.find_element_by_xpath('.//div[@id="viewListLayer"]/ul/li[5]').click()   # '50개'씩 출력

# paging_unit=50

# pages = math.ceil(total/paging_unit)
# print(f"pages: {pages}")


# # <tr class="list_row_info">
# #            		                 <td class="search_num" nowrap="nowrap">284244</td>
# #                 <td class="subject searchpreview_subject">
                	                	          			
# #                 	                    							                        <a href="/_c21_/bbs_nsread?grpid=fjM0&amp;fldid=Ohux&amp;contentval=01Bwazzzzzzzzzzzzzzzzzzzzzzzzz&amp;datanum=284244&amp;searchlist_uri=%2F_c21_%2Fcafesearch&amp;search_ctx=LrpNuZSucOsx.YncUoV2ej_tRpHqkOL1hFNwnK7pMwx2pUU9oYvq-CADq-lzJK_p_TYbLZznvSbg3qy8mowcMO7gTMK.A-9bjR6jw34nhIZ6qoOzMYq3mJOi_wh-dGxW6b222STVKsMwppYeW4jilln59w2YK_RtOY9ScNo3tPAaLxCFUYyGDtTRUr.CwIL2jQ9M1PxyBh1Faxvb_iISdO1vNLm-gQg1NfXVFIlm4ZDwFTcR2uAegQU9gi3UhRayafGnbzf1lQ.m7Ea5ktTeZz9nQQrblUXI_R2zWn69R3Bm1E7Sq_8AoOGAZPJuW9MmeiE13Y_F5-JywWIcf7Ao_g00"><b>붉은</b><b>나비</b>원장님 책 구합니다.</a>
                                                                                                                                                																								
# #                                                     <img src="//t1.daumcdn.net/cafe_image/cf_img2/img_blank2.gif" width="8" height="12" alt="새글" class="icon_new">
                                                
# #                                     </td>
# #                 <td class="search_nick" nowrap="nowrap">
# #                                 											<img src="//t1.daumcdn.net/cafe_image/cf_img2/bbs2/roleicon/2/r_level_30.gif">
# # 					                    <a href="#" onclick="showSideView(this, '5Fd_qdfn._g0', '\uAFC8 \uC548\uAFB8\uB294 \uC790\uC758 \uCD5C\uD6C4'); return false;">꿈 안꾸는 자의 최후</a>
# # 				                </td>
# #                 <td class="date" nowrap="nowrap">11:34</td>
# #                 <td class="count search_count" nowrap="nowrap">13</td>
# #             </tr>

# # <a class="txt_point num  " href="#" onclick="viewShortComment('OHl4', 163065); return false;">[4]</a>

# page_list = []

# def scrap_page_list(page_list=[]):
#     trs = s.driver.find_elements_by_xpath('.//tr[@class="list_row_info"]')
#     for tr in trs:
#         info = {}

#         # TODO: board_num element가 없는 경우가 있음
# #         board_num = tr.find_element_by_xpath('./td[contains(@class, "subject")]/a[2]').get_attribute("onclick")
#         try:
#             board_num_el = tr.find_element_by_xpath('./td[contains(@class, "subject")]/a[2]')
#         except:
#             continue

#         board_num = board_num_el.get_attribute("onclick")
#         print(f"board_num: {board_num}")
#         info['board'] = board_num.split("'")[1]
#         info['num'] = board_num.split(',')[1].split(')')[0].strip()
# #         info['num'] = tr.find_element_by_xpath('./td[@class="search_num"]').text
#         info['title'] = tr.find_element_by_xpath('./td[contains(@class, "subject")]/a[1]').text
#         info['writer'] = tr.find_element_by_xpath('./td[@class="search_nick"]/a').text
#         info['date'] = tr.find_element_by_xpath('./td[@class="date"]').text
#         page_list.append(info)
#         time.sleep(1)

#     return page_list


# ## 페이지 1
# page_list = scrap_page_list([])
# print(f"page_list: {page_list}")

# # 페이지 2 ~ 페이지 total
# # for page in range(0, pages - 1):
# #     s.driver.find_element_by_xpath(f'.//a[@class="num_box" and text() = "{page + 2}"]')

# # for page in range(0, pages - 1):
# for page in range(0, 2):
#     print(f"page: {page}")
# #     s.driver.find_element_by_xpath(f'.//a[@class="num_box" and text() = "{page + 2}"]').click()
# #     s.driver.find_element_by_xpath(f'.//a[text() = "{page + 2}"]').click()
#     s.driver.find_element_by_xpath(f'.//div[contains(@class, "paging")]//a[text() = "{page + 2}"]').click()
#     time.sleep(2)
#     page_list = scrap_page_list(page_list=page_list)

# print(f"page_list: {page_list}")

# write_file('poor_doctor_page_list1.json', json.dumps(page_list, indent=4, ensure_ascii=False))

# # time.sleep(2)


### NOTE: 페이지 내용

def scrap_page_content(page={}):
    url = f"{BASE_URL}/{page['board']}/{page['num']}"
    url = s.goto_page(url)
    title = page['title'].replace('.', '').replace(' ', '_').strip()
    time.sleep(1)

    # frame 이동
    iframe = s.driver.find_element_by_id('down')  
    s.driver.switch_to.frame(iframe)
    time.sleep(1)

    ## 본문
    root = s.driver.find_element_by_id("user_contents")
    source = s.element_source(root)
    
    create_folder(BASE_PATH)
    write_file(f"{BASE_PATH}/{title}.html", source)
    lxml_root = etree.fromstring(source)
    
    ## 이미지 다운로드
    
    ## 파일 다운로드

#  from urllib import parse
# >>> parse.quote('한글')                          // URL 인코딩
# '%ED%95%9C%EA%B8%80'
# >>> parse.unquote('(%EA%B5%AC)%EA%B0%80%EC%9E%85%EC%9E%90%EB%B2%88%ED%98%B8')  // URL 디코딩
# '(구)가입자번호'  
    
    
page = {
    "board": "AE8I",
    "num": "91244",
    "title": "제가 좋아하는 약대 94편 - 설진2.",
    "writer": "붉은나비",
    "date": "21.06.26"
}

scrap_page_content(page=page)
    

# _item = {
#     'title': '임상질문&자료&컨퍼런스',
#     'content': {
#         '제목': {
#             'outer': '//div[@id="primaryContent"]/div[@class="bbs_read_tit"]',
#             'sub_items': {
#                 '제목': 'strong/text()',
#             }
#         },
#         '정보': {
#             'outer': '//div[@id="primaryContent"]//div[@class="bbs_read_tit"]/div[@class="info_desc"]/div[@class="cover_info"]',
#             'sub_items': {
#                 '글쓴이': 'a/text()',
#                 '추천': 'span[1]/text()',
#                 '조회': 'span[2]/text()',
#                 '시간': 'span[3]/text()',
#                 '댓글': 'span[4]/text()',
#             }
#         },
#         '내용': {
#             'outer': '//div[@id="primaryContent"]/div[@id="bbs_contents"]',
#             'sub_items': {
#                 '본문': '//div[@id="user_contents"]/node()',
#             }
#         },
#         # '댓글': {
#         #     'outer': '//*[@id="comment_view"]',
#         #     'sub_items': {
#         #         'DB공개일자': 'tbody/tr[1]/td/text()',
#         #         'TKOI': 'tbody/tr[2]/td/text()',
#         #         'DOI': 'tbody/tr[3]/td/text()'
#         #     }
#         # },
#     }

# }

## 이미지
# <div class="figure-img" data-ke-type="image" data-ke-style="alignCenter" data-ke-mobilestyle="widthOrigin"><img src="https://t1.daumcdn.net/cafeattach/fjM0/acbd428ba0fd89730adaa3900ab149c67d1d73a7" class="txc-image" data-img-src="https://t1.daumcdn.net/cafeattach/fjM0/acbd428ba0fd89730adaa3900ab149c67d1d73a7" data-origin-width="1080" data-origin-height="1406" tabindex="0"></div>


# ## 파일
# <ul id="AFList" style="display: block;">
# 	<li>
# 		<a href="javascript:checkVirus('grpid%3DfjM0%26fldid%3DAE8I%26dataid%3D91245%26fileid%3D1%26regdt%3D20210626151705&amp;url=https%3A%2F%2Ft1.daumcdn.net%2Fcafeattach%2FfjM0%2F9e091be57ca93baba9c2eb203bc4f895ac63f46b');" class="AFFileName" id="fileExt0" style="background: url(&quot;//t1.daumcdn.net/cafe_image/cf_img2/bbs2/p_hwp_s.gif&quot;) no-repeat;">항미생물한약.hwp (48kB)</a>
# 		<a href="javascript:checkVirus('grpid%3DfjM0%26fldid%3DAE8I%26dataid%3D91245%26fileid%3D1%26regdt%3D20210626151705&amp;url=https%3A%2F%2Ft1.daumcdn.net%2Fcafeattach%2FfjM0%2F9e091be57ca93baba9c2eb203bc4f895ac63f46b');" class="txt_sub p11">다운로드</a>
# 			<span class="bar2 p11">|</span>
# 		<a href="javascript:fileFilterViewer(&quot;https://t1.daumcdn.net/cafeattach/fjM0/9e091be57ca93baba9c2eb203bc4f895ac63f46b?download&quot;, &quot;/cafeattach/fjM0/9e091be57ca93baba9c2eb203bc4f895ac63f46b&quot;, &quot;항미생물한약.hwp&quot;, &quot;grpid%3DfjM0%26fldid%3DAE8I%26dataid%3D91245%26fileid%3D1%26regdt%3D20210626151705&amp;url=https%3A%2F%2Ft1.daumcdn.net%2Fcafeattach%2FfjM0%2F9e091be57ca93baba9c2eb203bc4f895ac63f46b&quot;);" class="txt_sub p11">미리보기</a>
# 			<script type="text/javascript" language="javascript">
# 								setFileTypeImg("항미생물한약.hwp", 0);
# 							</script>
# 						</li>
# 												</ul>

# javascript:checkVirus('grpid%3DfjM0%26fldid%3DAE8I%26dataid%3D91245%26fileid%3D1%26regdt%3D20210626151705&amp;url=https%3A%2F%2Ft1.daumcdn.net%2Fcafeattach%2FfjM0%2F9e091be57ca93baba9c2eb203bc4f895ac63f46b)
# javascript:checkVirus('grpid%3DfjM0%26fldid%3DAE8I%26dataid%3D91245%26fileid%3D1%26regdt%3D20210626151705&amp;url=
# https%3A%2F%2Ft1.daumcdn.net%2Fcafeattach%2FfjM0%2F9e091be57ca93baba9c2eb203bc4f895ac63f46b)
# https://t1.daumcdn.net/cafeattach/fjM0/9e091be57ca93baba9c2eb203bc4f895ac63f46b?download

#  from urllib import parse
# >>> parse.quote('한글')                          // URL 인코딩
# '%ED%95%9C%EA%B8%80'
# >>> parse.unquote('(%EA%B5%AC)%EA%B0%80%EC%9E%85%EC%9E%90%EB%B2%88%ED%98%B8')  // URL 디코딩
# '(구)가입자번호'    
    
## 팝업 scrap
# https://jamanbbo.tistory.com/51
# selenium의 swtich_to_window를 사용해서 새로운 창을 핸들링 할 수 있다.

# from selenium import webdriver
# driver = webdriver.Chrome('chromedirver')
# # 새로 띄워진 창을 핸들링함.
# ... (생략)
# driver.switch_to_window(driver.window_handles[1])  
# driver.get_window_position(driver.window_handles[1])
# 참고로 driver.window_handles[0]은 본래의 창을 의미한다.


## 다운로드 popup

# https://t1.daumcdn.net/cafeattach/fjM0/9e091be57ca93baba9c2eb203bc4f895ac63f46b?download

# <html lang="ko"><head>
# <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
# <title>Daum 카페</title>
# <link rel="stylesheet" type="text/css" href="//t1.daumcdn.net/cafe_cj/pcweb/build/css/2009/popup-a877b185d4.min.css">
# </head>

# <body cz-shortcut-listen="true">
# <div class="pop_title"><h2>바이러스 체크 후 파일받기</h2></div>
# <div class="pop_content">
# <!-- pop_content -->
# 	바이러스가 발견되지 않은 안전한 파일입니다.<br>
# 	파일을 받으시려면 파일받기 버튼을 클릭하세요.<br><br>
# 	<a href="https://t1.daumcdn.net/cafeattach/fjM0/9e091be57ca93baba9c2eb203bc4f895ac63f46b?download" class="b u">항미생물한약.hwp</a> <span class="txt_sub">(48kB)</span><br>
# <!-- pop_content end -->
# </div>

# <div class="pop_btn">
# 	<a href="https://t1.daumcdn.net/cafeattach/fjM0/9e091be57ca93baba9c2eb203bc4f895ac63f46b?download"><img src="//t1.daumcdn.net/cafe_image/top6/bbs/btn_filedown.gif" width="67" height="22" alt="파일받기"></a>
# 	<a href="javascript:close()"><img src="//t1.daumcdn.net/cafe_image/cf_img4/popup/btn_cancel_001.gif" width="40" height="23" alt="취소"></a>
# </div>
# <script>
# 	window.CAFEAPP = {};
# 	CAFEAPP.GRPID = 'fjM0';
# 	CAFEAPP.GRPCODE = 'poordoctor';
# 	CAFEAPP.GRPNAME = 'MD[DKM]';
# </script>
# <script src="//t1.daumcdn.net/tiara/js/v1/tiara.min.js"></script>
# <script src="//t1.daumcdn.net/cafe_cj/pcweb/build/js/util/cafe_tiara-d72676fb4d.js"></script>
# 	<script>
# 	CafeTiara.trackPage('pds_download', 'cafe');
# </script>


# </body></html>

