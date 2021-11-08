import os, sys
import math
import copy
import time
# import re
# import requests
import urllib
import lxml.html as ht
# import lxml.etree as et

##------------------------------------------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), '../_public')) ## Note: 현재 디렉토리 기준 상대 경로 설정
# sys.path.append(os.path.join(os.path.abspath('../../_public'))) ## Note: 현재 디렉토리 기준 상대 경로 설정
from utils_basic import (
    _create_folder, 
    _read_file, 
    _file_to_json, 
    _json_to_file, 
    _to_lists, 
    _to_dicts,
    _fn
)
from utils_scraping import (
    _root,
    _pages_by_pagination, 
    _scrape_list_pages, 
    _extract_values,
    _scrape_detail_page,
    _scrape_full_html
)

# from scrap_selenium import (go_selenium, _wait_xpath)

# base_path = '../../../../__references/_python/sats/_scrap/tistory/igotit/source/'  ## .ipynb
base_path = '../../../__references/_python/sats/_scrap/tistory/igotit/source/'  ## .py
base_url = 'https://igotit.tistory.com/'
url = 'https://igotit.tistory.com/'

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
        'title': './/h1[@class="page-subject"]',
        'date': './/div[@class="muted text-right"]',
        'content': './/div[contains(@class, "page-content")]',
    }, 

    dels = [  # content에서 제거할 요소 xpath
        # './/blockquote[last()]'
    ],
    # pres = [  ## NOTE: 여백, 줄바꿈 유지
    #     './/pre'
    # ],
    full = False, 
    files = {
        'fig' : {
            'xpath': './/img',
            'url': {
                # 'xpath': 'span',
                'target': 'src',
            },
            'path': {
                # 'xpath': './/img',
                # 'target': 'data-filename',
                # 'body': callback,
                'prefix': 'images/',
                'suffix': ''
            },
            # 'swap': {  # element를 치환하는 경우에만 사용
            #     'tag': 'img',  #
            #     'attrs': [  # 원래 element에서 복사할 attribute 요소
            #         'src',
            #         'data-origin-width',
            #         'data-origin-height',
            #     ]    
            # }
        }
    }
)

# _scrape_full_html(title='intro', url=base_url, base_url=base_url, base_path=f"{base_path}/_tpls/", files=defaults['files'])
# time.sleep(5)

## NOTE: 리스트 페이지 추출
# NOTE: paginations
# paginations = []

# path = f"{base_path}/_tpls/intro.html"
# root = _root(path, encoding='utf-8')
# root = root.xpath('.//table[@id="treeComponent"]//td')[0]

# ## NOTE: main category
# values = {
#     # 'title': {
#     #     'xpath': './table//table//td[@class="branch3"]/div',
#     #     'target': 'text'
#     # },
#     'href': {
#         'xpath': './table//table//td[@class="branch3"]',
#         'target': 'onclick',
#         '_replace_basic': {"'": "", "window.location.href=": ""}
#     },
#     'count': {
#         'xpath': './table//table//td[@class="branch3"]/div/span',
#         'target': 'text',
#         '_replace_basic':{"(": "", ")": ""}
#     },
# }

# vals = _extract_values(root, values, _zip=None)
# vals['href'] = [urllib.parse.unquote(href) for href in vals['href']]  ## NOTE: unqoute

# category1 = _to_dicts(vals)

# ## NOTE: sub category
# values = {
#     # 'title': {
#     #     # 'xpath': './div[contains(@id, "_children")]/table//td[@class="branch3"]/div',
#     #     'xpath': './div/table//td[@class="branch3"]/div',
#     #     'target': 'text'
#     # },
#     'href': {
#         'xpath': './div/table//table',
#         'target': 'onclick',
#         '_replace_basic': {"'": "", "window.location.href=": ""}
#     },
#     'count': {
#         'xpath': './div/table//td[@class="branch3"]/div/span',
#         'target': 'text',
#         '_replace_basic':{"(": "", ")": ""}
#     },
# }

# vals = _extract_values(root, values, _zip=None)
# vals['href'] = [urllib.parse.unquote(href) for href in vals['href']]  ## NOTE: unqoute

# categories = category1 + _to_dicts(vals)

# paginations = []
# for category in categories:
#     title = category['href'].split('category/')[-1]
#     count = category['count']
#     paginations.append({'title': title, 'f_url': "{base_url}category/{title}?page={page_no}", 'range': (1, math.ceil(int(count)/30)+1)})

# _json_to_file(paginations, f'{base_path}_json/paginations.json')
# time.sleep(5)


# NOTE: paginations -> list pages
# paginations = _file_to_json(f'{base_path}_json/paginations.json')
# list_pages = _pages_by_pagination(base_url, paginations)

# _json_to_file(list_pages, f'{base_path}_json/list_pages.json')
# time.sleep(3)


# ## NOTE: list pages -> detail pages
# list_pages = _file_to_json(f'{base_path}_json/list_pages.json')

# xpath = './/div[@id="searchList"]'  # title, url을 추출할 base element의 xpath

# values = {
#     'title': {
#         'xpath': './ol/li/a',
#         'target': 'text'
#     },
#     'url': {
#         'xpath': './ol/li/a',
#         'target': 'href'
#     },
# }

# # root = _root("https://igotit.tistory.com/category/VisualStudio.C++.C#?page=1")
# # root = root.xpath(xpath)[0]
# # print(f"root: {ht.tostring(root, encoding=str)}")


# ## NOTE: 한꺼번에 하면 memory Error가 발생할 수 있으므로, 끊어서
# i = 0
# for category, pages in list_pages.items():
#     i += 1
#     if i == 1:  ## 전체 카테고리는 skip
#         continue
#     ## BUG! url에 'C#'은 안되고 'C%23'는 됨
#     # pages = [urllib.parse.quote(page) for page in pages]
#     print(f"pages: {pages}")
#     detail_pages = _scrape_list_pages(pages, xpath, values)
#     # category = category.replace('.', '_')

#     _json_to_file({category: detail_pages}, f'{base_path}_json/detail_pages{i}.json')

# time.sleep(5)


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
        # 'date': './/div[@class="article"]',
        'content': './/div[@class="article"]',
    }, 
    dels = [  # content에서 제거할 요소 xpath
        ".//p[text()='\u00A0']",
        # ".//div[@class='revenue_unit_wrap ']",
        # "(.//p)[1]",  ## 확인 필요
        # "(.//figure)[1]",  ## 확인 필요
        # "//figure[contains(@id, 'og_')]",
        './/div[contains(@class,"container_postbtn")]/following-sibling::*',
        './/div[contains(@class,"container_postbtn")]',
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


# ## NOTE: test
# url = 'https://igotit.tistory.com/entry/Visual-C-사용자-정의-매크로-만들기?category=807192'
# title = 'Visual-C-사용자-정의-매크로-만들기'

# detail_options = dict(defaults, **dict(title=title, url=url, base_path=base_path))
# _scrape_detail_page(**detail_options)


# ## NOTE: scrape category 
# Data.Math.Phys	5
# Trading	6
# Trading/메타트레이더 코딩	12
# Trading/암호화폐	13
# scraps = [5, 6, 12, 13]
scraps = [5, 6]

for i in scraps:
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
