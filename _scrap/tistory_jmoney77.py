import os, sys
import math
import copy
# import re
# import requests
import urllib
import lxml.html as ht
# import lxml.etree as et

##------------------------------------------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), '../_public')) ## Note: 현재 디렉토리 기준 상대 경로 설정
from utils_basic import (_create_folder, _read_file, _file_to_json, _json_to_file, _to_lists, _fn)
from utils_scraping import (
    _root,
    _pages_by_pagination, 
    _scrape_list_pages, 
    _extract_values,
    _scrape_detail_page,
    _scrape_full_html
)

# from scrap_selenium import (go_selenium, _wait_xpath)

base_path = '_scrap/tistory/jmoney77/source/'
base_url = 'https://jmoney77.tistory.com/'
url = 'https://jmoney77.tistory.com/notice/682'

files = {
    'img': {
        'xpath': './/img',
        'url': {
            # 'xpath': '',
            'target': 'src',
        },
        'path': {
            # 'xpath': '',
            # 'target': '',
            'prefix': 'images/',
            'suffix': ''
        },
    }
}

# _scrape_full_html(title='intro', url=base_url, base_url=base_url, base_path=base_path, files=files)

## BUG: 한글깨짐
## <html lang="ko"> : lang 제거
## <meta encoding="utf-8" /> : encoding 삽입


## NOTE: 리스트 페이지 추출
## NOTE: paginations
# paginations = []

# path = f'{base_path}intro.html'
# # root = _root(path, encoding='euc-kr')
# root = _root(path, encoding='utf-8')
# root = root.xpath('.//ul[@class="category_list"]')[0]
# # print(ht.tostring(root))

# depth1s = root.xpath('./li/a')

# for depth1 in depth1s:
#     title = depth1.text.strip()  # title count new
#     # href = depth1.get("href")
#     href = urllib.parse.unquote(depth1.get("href"))
#     path = href.split('category/')[-1]
#     count = depth1.xpath('./span[@class="c_cnt"]')[0].text.strip()[1:-1]
#     depth2s = depth1.xpath('./following-sibling::ul/li/a')
#     # print(f"depth2s: {depth2s}")

#     if len(depth2s) > 0:
#         for depth2 in depth2s:
#             # title = depth2.text.strip()  # title count new
#             # href = depth1.get("href")
#             href = urllib.parse.unquote(depth2.get("href"))
#             path = href.split('category/')[-1]
#             count = depth2.xpath('./span[@class="c_cnt"]')[0].text.strip()[1:-1]
#             # paginations.append({'title': title, 'path': path, 'href': href, 'count': count})
#             paginations.append({'title': path, 'f_url': "{base_url}category/{title}?page_no={page_no}", 'range': (1, math.ceil(int(count)/30)+1)})
#             # print(f"title2: {title}\nhref2: {href}\ncount2: {count}")
#     else:
#         # print(f"title1: {title}\nhref1: {href}\ncount1: {count}")
#         # paginations.append({'path': path, 'href': href, 'count': count})
#         paginations.append({'title': path, 'f_url': "{base_url}category/{title}?page_no={page_no}", 'range': (1, math.ceil(int(count)/30)+1)})

# _json_to_file(paginations, f'{base_path}_json/paginations.json')
# print(paginations)

## NOTE: paginations -> list pages
# paginations = _file_to_json(f'{base_path}_json/paginations.json')
# list_pages = _pages_by_pagination(base_url, paginations)

# _json_to_file(list_pages, f'{base_path}_json/list_pages.json')


# ## NOTE: list pages -> detail pages
# list_pages = _file_to_json(f'{base_path}_json/list_pages.json')

# xpath = './/div[@id="contents"]'  # title, url을 추출할 base element의 xpath

# values = {
#     'title': {
#         'target': 'text',
#         'xpath': './/div[@class="index-inner-right"]//a[@class="link_post"]/h3[@class="tit_post"]',
# #         '_filter': _filter,  # filtering callback
# #         '_replace_basic': _replace_basic1, # replace callback
# #         '_replace_regex': _replace_regex1, # replace callback
#     },
#     'url': {
#         'target': 'href',
#         'xpath': './/div[@class="index-inner-right"]/a[@class="link_post"]'
#     },

# }

# ## NOTE: 한꺼번에 하면 memory Error가 발생할 수 있으므로, 끊어서
# i = 0
# for category, pages in list_pages.items():
#     i += 1
#     print(f"pages: {pages}")
#     detail_pages = _scrape_list_pages(pages, xpath, values)
#     _json_to_file({category: detail_pages}, f'{base_path}_json/detail_pages{i}.json')


## NOTE: scrape detail pages

defaults = dict(
    base_url = base_url,
    base_path = base_path, 
    head = {
        'create': {
            'meta': {
                'charset': 'utf-8'
            }
        },
        # 'copy': {
        #     "//style[@type='text/css']"
        # },
        # 'files': ['js', 'css']
    },
    body = {
        'title': './/div[@class="titleWrap"]/h2',
        'date': './/div[@class="titleWrap"]//div[@class="date"]',
        'content': './/div[@id="contents"]/div[@class="article"]/div',
    }, 
    dels = [  # content에서 제거할 요소 xpath
        ".//p[text()='\u00A0']",
        ".//div[@class='revenue_unit_wrap ']",
        "(.//p)[1]",  ## 확인 필요
        "(.//figure)[1]",  ## 확인 필요
        "//figure[contains(@id, 'og_')]",
        ".//div[contains(@class, 'rgyTextBox')]/following-sibling::*",
        ".//div[contains(@class, 'rgyTextBox')]",
        ".//p[@data-ke-size='size18']/following-sibling::*",
        ".//p[@data-ke-size='size18']",
    ], 
    full = False, 
    files = {
        'fig' : {
            'xpath': './/figure',
            'url': {
                'xpath': 'span',
                'target': 'data-url',
            },
            'path': {
                'xpath': './/img',
                'target': 'data-filename',
                # 'body': callback,
                'prefix': 'images/',
                'suffix': ''
            },
            'swap': {  # element를 치환하는 경우에만 사용
                'tag': 'img',  #
                'attrs': [  # 원래 element에서 복사할 attribute 요소
                    'src',
                    'data-origin-width',
                    'data-origin-height',
                ]    
            }
        }
    }
)

## NOTE: scrape category 
# 키움증권 자료실/키움증권 수식관리자	detail_pages13.json	
# 키움증권 자료실/키움증권 조건검색기	detail_pages14.json
for i in range(13, 15):
    detail_pages = _file_to_json(f'{base_path}_json/detail_pages{i}.json')
    for _path, pages in detail_pages.items():
        _base_path = f"{base_path}{_path}/"
        for title, url in pages.items():
            # _defaults = defaults.copy()
            _defaults = copy.deepcopy(defaults)  ## NOTE: 깊은 복사
            print(f"_defaults['body']: {_defaults['body']}")
            url = f'{base_url}{url[1:]}'
            detail_options = dict(_defaults, **dict(title=title, url=url, base_path=_base_path))
            _scrape_detail_page(**detail_options)


# root = root.xpath(".//div[@id='contents']/div[@class='article']/div")[0]  # 확인 필요

# title = "#18. 수식관리자 실전 응용(RSI지표 Signal선 추가하기)"
# url = "/714?category=944715"
# url = f'{base_url}{url[1:]}'
# _path = "키움증권 자료실/키움증권 수식관리자"
# base_path = f"{base_path}{_path}/"

# detail_options = dict(defaults, **dict(title=title, url=url, base_path=base_path))

# _scrape_detail_page(**detail_options)


