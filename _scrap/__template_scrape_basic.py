import os, sys
# import re
# import requests

# import lxml.html as ht
# import lxml.etree as et

##------------------------------------------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), '.')) ## Note: 현재 디렉토리 기준 상대 경로 설정
from utils_basic import (_create_folder, _read_file, _file_to_json, _json_to_file, _to_lists, _fn)
from utils_scrapping import (
    _pages_by_pagination, 
    _scrape_list_pages, 
    _extract_values,
    _scrape_detail_page
)
# from scrap_selenium import (go_selenium, _wait_xpath)

## @@ scrapping process
##------------------------------------------------------------
## 0. basic settings
base_path = 'otexts_com/fppkr/'
base_url = 'https://otexts.com/fppkr/'

## 1. scrape list pages

## 1-1 paginations
## NOTE: pagination이 있는 경우
paginations = [
    {
        'title': '투자의 기초(필독)', 
        'f_url': "{base_url}category/{title}?page={page_no}", 'range': (1, 5)
    },
    {
        'title': '실전 투자 기법', 
        'f_url': "{base_url}category/{title}?page={page_no}", 'range': (1, 3)
    },
]

list_pages = _pages_by_pagination(base_url, paginations)

_json_to_file(list_pages, f"{base_path}list_pages.json")  ## 설정 저장


## 1-1 list_pages -> detail_pages

pages = {
    'fppkr': 'https://otexts.com/fppkr/', 
    # 'fpp3': 'https://otexts.com/fpp3/'
}

xpath = './/nav/ul'  # title, url을 추출할 base element(menus)의 xpath

values_chapter = {
    'title': {
        'target': 'content',
        'xpath': './li/a',
#         '_filter': _filter,  # filtering callback
#         '_replace_basic': _replace_basic1, # replace callback
#         '_replace_regex': _replace_regex1, # replace callback
    },
    'url': {
        'target': 'href',
        'xpath': './li/a'
    },

}


detail_pages = _scrape_list_pages(pages, xpath, values_chapter, callback=_extract_values)  # NOTE: 장chapter
_json_to_file(detail_pages, f"{base_path}detail_pages.json")  ## 설정 저장


## 2. scrape detail pages

defaults = dict(
    base_url = base_url,
    base_path = base_path, 
    head = {
        'create': {
            'meta': {
                'charset': 'utf-8'
            }
        },
        'copy': {
            "//style[@type='text/css']"
        },
        # 'files': ['js', 'css']
    },
    body = {
        'title': './/div[@id="data-methods"]//h2',
        # 'author': '',
        'content': './/section[@id="section-"]',
    }, 
    dels = [  # content에서 제거할 요소 xpath
    ], 
    full = False, 
    files = {
        'fig' : {
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
            # 'swap': {  # element를 치환하는 경우에만 사용
            #     'tag': 'img',  #
            #     'attrs': [  # 원래 element에서 복사할 attribute 요소
            #         'src',
            #         # 'width',
            #         # 'height',
            #     ]    
            # }
        }
    }
)

# detail_options = dict(defaults, **dict(title='1-4 예측 데이터와 기법', url='https://otexts.com/fppkr/data-methods.html'))


for title, url in detail_pages.items():
    detail_options = dict(defaults, **dict(title=title, url=url))
    _scrape_detail_page(**detail_options)