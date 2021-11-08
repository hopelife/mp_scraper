import os, sys, time
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

base_path = '../../../__references/_python/sats/_scrap/wikidocs/486_시스템 트레이딩을 위한 데이터 사이언스 (파이썬 활용편)/source/'  ## 'https://wikidocs.net/book/486'
base_url = 'https://wikidocs.net/'
url = 'https://wikidocs.net/book/486'
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


# ## NOTE: 책 제목 페이지
# _scrape_full_html(title='intro', url=url, base_url=base_url, base_path=base_path, files=defaults['files'])

# time.sleep(5)


## NOTE: detail pages from 제목 페이지

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
#         prefix = title.split(' ')[0].replace('.', '-')
#         if prefix[-1] == '-':
#             prefix = prefix[:-1]
#         body = ' '.join(title.split(' ')[1:])
#         title = f"{prefix} {body}".strip()
#         if title[0] == 'I' or title[0] == 'V':
#             title = f'Appendix {title}'
#         detail_pages[title] = url
# _json_to_file(detail_pages, f'{base_path}_json/detail_pages.json')
# time.sleep(5)    


## NOTE: scrape detail pages
detail_pages = _file_to_json(f'{base_path}_json/detail_pages.json')
for title, url in detail_pages.items():
    _defaults = copy.deepcopy(defaults)  ## NOTE: 깊은 복사
    url = f"{base_url}{url[1:]}"
    detail_options = dict(_defaults, **dict(title=title, url=url, base_path=base_path))
    _scrape_detail_page(**detail_options)


## NOTE: html -> markdown
