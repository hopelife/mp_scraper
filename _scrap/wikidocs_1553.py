import os, sys
import math
import copy
import re
# import requests
import urllib
import lxml.html as ht
# import lxml.etree as et
from markdownify import markdownify
# import markdown

##------------------------------------------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), '../_public')) ## Note: 현재 디렉토리 기준 상대 경로 설정
from utils_basic import (_create_folder, _read_file, _file_to_json, _json_to_file, _to_lists, _fn)
from utils_scraping import (
    _root,
    _remove_punc,
    _pages_by_pagination, 
    _scrape_list_pages, 
    _extract_values,
    _scrape_detail_page,
    _scrape_full_html
)

# from scrap_selenium import (go_selenium, _wait_xpath)

base_path = '../../../__references/_python/sats/_scrap/wikidocs/1553_파이썬 - 기본을 갈고 닦자!/source/'  ## 'https://wikidocs.net/book/1553'
base_url = 'https://wikidocs.net/'
url = 'https://wikidocs.net/book/1553'

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
        'title': './/h1[@class="page-subject"]',
        'date': './/div[@class="muted text-right"]',
        'content': './/div[contains(@class, "page-content")]',
    }, 

    dels = [  # content에서 제거할 요소 xpath
        './/blockquote[last()]'
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

# _scrape_full_html(title='intro', url=url, base_url=base_url, base_path=base_path, files=defaults['files'])

## NOTE: detail pages
# path = f'{base_path}intro.html'
# # root = _root(path, encoding='utf-8')
# root = _root(path)
# root = root.xpath('.//div[contains(@class, "list-group-toc")]')[0]
# print(ht.tostring(root, encoding=str))

# detail_pages = {}
# for el in root.xpath('.//a[contains(@class, "list-group-item")]'):
#     url = el.get('href')
#     if 'javascript' in url:  # NOTE: 책 제목 외에는 모두 해당
#         url = f"/{url.split('(')[-1][:-1]}"
#         title = el.xpath('./span/span')[0].text.strip()
#         detail_pages[title] = url
# _json_to_file(detail_pages, f'{base_path}_json/detail_pages.json')
        



# title = "40. itertools 모듈과 iterable에 유용한 내장함수"
# url = "/16070"
# url = f"{base_url}{url[1:]}"
# detail_options = dict(defaults, **dict(title=title, url=url, base_path=base_path))

# _scrape_detail_page(**detail_options)

## NOTE: scrape category 
detail_pages = _file_to_json(f'{base_path}_json/detail_pages.json')
for title, url in detail_pages.items():
    _defaults = copy.deepcopy(defaults)  ## NOTE: 깊은 복사
    url = f"{base_url}{url[1:]}"
    detail_options = dict(_defaults, **dict(title=title, url=url, base_path=base_path))
    _scrape_detail_page(**detail_options)


## NOTE: html -> markdown

# path = "_scrap/wikidocs/1553_파이썬 - 기본을 갈고 닦자!/40. itertools 모듈과 iterable에 유용한 내장함수.html"


# content = open(path, "r", encoding="utf-8").read()
# md = markdownify(content, heading_style="ATX")
# md = re.sub(r'^\s+', r'', md)
# md = re.sub(r'\s+$', r'', md)
# md = re.sub(r'\n{3,}', r'\n\n', md)
# md = re.sub(r'```\n+((.+\n)+)\n*?```', r'```\n\1```', md)  ## 수정
# path = '.'.join(path.split('.')[:-1]) + '.md'
# file = open(path, "w", encoding="utf-8").write(md)
# print(md)

# path = "C:/Dev/docMoon/_sources/_python/scraping/_scrap/wikidocs/1553_파이썬 - 기본을 갈고 닦자!/40. itertools 모듈과 iterable에 유용한 내장함수.md"
# code = open(path, "r", encoding="utf-8").read()

# md = markdown.Markdown(extensions=['pretty'])
# print(md.convert(code))
# _path = "C:/Dev/docMoon/_sources/_python/scraping/_scrap/wikidocs/1553_파이썬 - 기본을 갈고 닦자!/40. itertools 모듈과 iterable에 유용한 내장함수_.md"
# file = open(_path, "w", encoding="utf-8").write(md.convert(code))

# ## NOTE: scrape category 
# # 키움증권 자료실/키움증권 수식관리자	detail_pages13.json	
# # 키움증권 자료실/키움증권 조건검색기	detail_pages14.json
# for i in range(13, 15):
#     detail_pages = _file_to_json(f'{base_path}_json/detail_pages{i}.json')
#     for _path, pages in detail_pages.items():
#         _base_path = f"{base_path}{_path}/"
#         for title, url in pages.items():
#             # _defaults = defaults.copy()
#             _defaults = copy.deepcopy(defaults)  ## NOTE: 깊은 복사
#             print(f"_defaults['body']: {_defaults['body']}")
#             url = f'{base_url}{url[1:]}'
#             detail_options = dict(_defaults, **dict(title=title, url=url, base_path=_base_path))
#             _scrape_detail_page(**detail_options)


# detail_options = dict(defaults, **dict(title=title, url=url, base_path=base_path))

# _scrape_detail_page(**detail_options)


