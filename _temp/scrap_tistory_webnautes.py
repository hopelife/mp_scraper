# [파이썬 크롤러 만들기](https://jione-e.tistory.com/28)
# [Source Code for Package lxml.html](https://lxml.de/api/lxml.html-pysrc.html)

import os, sys
import json
import time
import re

from urllib import parse
import requests
import lxml.html as etree
import lxml.etree as et

sys.path.append('../_public') ## Note: 현재 디렉토리 기준 상대 경로 설정
from scrap_requests import (_root_tree, _fn)
from utils_basic import (_read_file, _create_folder, _write_file, _fn)

# url = 'https://jmoney77.tistory.com/notice/682'
# requests.get(url).source

def _normalize_spaces(s):
    """연결된 공백을 하나의 공백으로 변경
    """
    return re.sub(r'\s+', ' ', s).strip()


def _remove_punc(s):
    """ 특수문자 제거

    Args:
        s (str): 입력 문자열
    """
    punc = r'[\\/:*?"<>|]'  ## NOTE: 파일이름에 사용할 수 없는 문자
    # punc = '[!"#$%&\'()*+,-./:;<=>?[\]^_`{|}~“”·]'
    return re.sub(punc, '_', s)


def _remove_el(root, xpath):
    for el in root.xpath(xpath):
        try:
            el.getparent().remove(el)
        except:
            pass


def _save_file_by_url(path, url):
    """해당 url의 파일(이미지 포함)을 path에 저장
    """
    _create_folder('/'.join(path.split('/')[:-1]))
    r = requests.get(url)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            f.write(r.content)


def _paging_list(section, next, before):
    pass


def _extract_detail_pages_2(url, xpath):
    """상세 페이지 title, url 추출
    """
    ## NOTE: 파일 이름 변경(제목(파일이름)이 계층형으로 구분되지 않은 경우)
    ## 파일 이름 중복 / 파일 순서 혼란 야기
    # 1. 목차(좌측) 페이지 download
    # 2. xpath: './/a[contains(@class, "list-group-item")]'
    # els = root.xpath(xpath)
    page = requests.get(url)
    root = etree.fromstring(page.content)
    pages = {}

    prefixs = ['', '']
    for el in root.xpath(xpath):
        try:
            span = el.xpath('./span/span')[0]
        except:
            print("책 제목")
            pass
        else:
            style = span.attrib['style']
            title = _remove_punc(span.text.strip())

            url = el.get('href')
            if 'javascript' in url:  # NOTE: 책 제목 외에는 모두 해당
                url = f"/{url.split('(')[-1][:-1]}"
                # url = f"/book/{url.split('(')[-1][:-1]}"

            if ':0px' in style:
                prefixs[0] = f"{title.split(' ')[0][:-1]}-"
            elif ':20px' in style:
                title = prefixs[0] + title
                prefixs[1] = f"{title.split(' ')[0][:-1]}-"
            elif ':40px' in style:
                title = prefixs[1] + title

            pages[title.replace('.', '')] = url

    return pages


def _extract_detail_pages(url, xpath):
    """상세 페이지 title, url 추출
    """
    page = requests.get(url)
    root = etree.fromstring(page.content)
    pages = {}
    for el in root.xpath(xpath):
        title = el.xpath('.//h2[@class="post_title"]//text()')[0]
        url = el.get('href')
        pages[title] = url

    return pages


def scrape_list_pages(pages, xpath, callback):
    """스크랩할 page 리스트
    TODO: response = session.get(url)  # Session / yield 사용
    """
    _pages = {}
    if type(pages) == list:
        for url in pages:
            _pages = dict(_pages, **callback(url, xpath))
    elif type(pages) == dict:  # dict
        for sub, url in pages.items():
            _pages[sub] = {}
            _pages[sub] = dict(_pages[sub], **callback(url, xpath))

    return _pages


def scrape_detail_page(title, url, base_url, base_path):
    """스크랩할 page 리스트
    url: 스크랩할 페이지
    base_url: 스크랩할 site url
    base_path: 저장할 폴더
    TODO: response = session.get(url)  # Session / yield 사용
    """
    root = etree.fromstring(requests.get(url).content)
    # root = root.xpath('//*[@id="load_content"]/div[contains(@class, "page-content")]')[0]  # 확인 필요

    ## HTML wraper
    html = et.Element("html")
    # head = et.Element("head")
    body = et.Element("body")

    # html.insert(0, head)
    html.insert(0, body)

    # ## meta(encoding)
    # meta = et.Element("meta")
    # meta.set('charset', 'utf-8')
    # head.insert(0, meta)

    # # style
    # styles = root.xpath(".//style[@type='text/css']")
    # for style in styles:
    #     n = len(head.xpath('.//style'))
    #     head.insert(n+1, style)  ## NOTE: meta, 앞의 style 뒤에 추가

    ## body
    # print(f"root: {root}")
    _title1 = et.Element("h1")
    _title1.text = root.xpath('.//*[@id="content"]//header/div/h1/a/text()')[0]
    _title2 = root.xpath('.//*[@id="content"]//header/div/div[@class="sub-info"]//abbr[contains(@class, "dt-published")]')[0]

    root = root.xpath('.//*[@id="content"]/section/div/div[contains(@class, "e-content")]/div[contains(@class, "contents_style")]')[0]
    # tail = root.xpath('./following-sibling::div')[0]

    figs = root.xpath('.//img')

    root.make_links_absolute(base_url)  # TODO: url들을 절대 주소로 변환

    for fig in figs:
        try:    #  KeyError: 'data-filename'
            path = f'images/{fig.attrib["src"].lower().split("/")[-2]}.png'
            url = fig.attrib['src']
            # _save_file_by_url(f'{base_path}/{path}', url)  # NOTE: image 파일 저장
            time.sleep(0.1)
            ## NOTE: figure element -> img element
            fig.set('src', path)
            del fig.attrib["srcset"]

        except:
            print(f"fig: {etree.tostring(fig)}")
            pass

    body.insert(0, _title1)
    body.insert(1, _title2)
    body.insert(2, root)

    ## NOTE: 삭제
    xpaths = ['./head', './/div[contains(@class, "revenue_unit_wrap")]', './/ins', './/iframe', './body/div/div[last()]']
    # xpaths = ['./head', './/div[contains(@class, "revenue_unit_wrap")]', './/ins', './/iframe', './body/div/div[last()]', './body/a[last()]']

    for xpath in xpaths:
        _remove_el(html, xpath)

    _create_folder(base_path)  ## NOTE: 이미지 저장시 폴더 생성됨
    title = _remove_punc(title)  # TODO: 파일 이름에 사용할 수 없는 특수문자 제거
    open(f'{base_path }/{title}.html', 'w', encoding="utf-8").write(_normalize_spaces(etree.tostring(html, encoding=str))) ## NOTE: html 저장, endcoding=str, spaces 정리  ## html 저장


def _modify_html(path, xpaths):
    """html 파일 수정

    Args:
        path ([type]): [description]
    """

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"content: {content}")
        root = etree.fromstring(content)
        for xpath in xpaths:
            _remove_el(root, xpath)
        f.close()

        with open(path, 'w', encoding='utf-8') as f:
            f.write(etree.tostring(root, encoding=str))
            f.close()


def modify_html(path):
    """html 파일 일괄 수정

    Args:
        path ([type]): [description]
    """
    pass


if __name__ == '__main__':

    # detail_pages = scrape_list_pages(pages, xpath, _extract_detail_pages)  ## NOTE: 제목(파일이름 변경이 필요없는 경우)
    # 'WSL 2 ( Windows Subsystem for Linux ) 를 사용하여 Ubuntu 20.04 설치 하는 방법': 'https://webnautes.tistory.com/1170',
    base_url = 'https://webnautes.tistory.com'

    ### list(category)
    root = etree.fromstring(requests.get(base_url).content)
    menu = root.xpath('//*[@id="sidebar-category"]')[0]
    categories = menu.xpath('.//ul[@class="category_list"]//a[@class="link_item"]')
    # links = [el.attrib['href'] for el in menu.xpath('.//ul[@class="category_list"]//a[@class="link_item"]')]

    # category_pages = {c.text.strip(): l for (c, l) in zip(categories, links) if c.text.strip() != ''}
    category_pages = {c.text.strip(): [] for c in categories}

    # ### list(subcategory)
    for submenu in categories:
        try:
            category = submenu.text.strip()

            subcategories = submenu.xpath('following-sibling::ul//a')
            # links = [el.attrib['href'] for el in submenu.xpath('following-sibling::ul//a')]
            if len(subcategories) > 0:
                category_pages[category] = [c.text.strip() for c in subcategories]

            # if len(links) > 0:
            #     category_pages[category] = {c.text.strip(): l for (c, l) in zip(subcategories, links)}
            # print(f"category_pages[{category}]: {category_pages[category]}")
        except:
            print("not subcategory............")
            pass


    print(category_pages)
    # ### list(detail)

    category = '개발 환경'
    for subcategory in category_pages[category]:
        pass
    subcategory = 'C&C++'
    url = f'https://webnautes.tistory.com/category/{category}/{subcategory}'
    root = etree.fromstring(requests.get(url).content)

    # https://webnautes.tistory.com/category/개발 환경/Visual Studio 2017&2019

    items = root.xpath('.//div[@id="content"]/section[contains(@class, "entry")]')
    for item in items:
        title = item.xpath('.//a[@class="post_link"]//h2')[0]
        url = item.xpath('.//a[@class="post_link"]')[0].attrib['href']

    list_pages = {
        f'{category}_{subcategory}': f'https://webnautes.tistory.com/category/{category}/{subcategory}'
    }
    xpath = './/div[@id="content"]/section[contains(@class, "entry")]//a[@class="post_link"]'
    detail_pages = scrape_list_pages(list_pages, xpath, _extract_detail_pages)
    print(detail_pages)

    ### detail
    detail_pages = {
        '개발 환경_C&C++': {
            'Visual Studio Code에서 C/C++ 프로그래밍( Windows / Ubuntu)': '/1158?category=753663', 
            'GDB를 사용한 원격 디버깅': '/1469?category=753663', 
            'Visual Studio Code에서 C/C++ 프로그래밍 with Makefile ( Windows/Ubuntu)': '/1429?category=753663', 
            'Sublime Text 3와 MinGW를 사용하여 C/C++ 개발 환경 만들기': '/856?category=753663', 
            '윈도우용 gcc, g++ 컴파일러를 사용하기 위해  MinGW 설치하는 방법': '/1196?category=753663'
        }
    }

    base_url = 'https://webnautes.tistory.com'
    base_path = 'tistory_webnautes'
    for key, pages in detail_pages.items():
        base_path += f'/{key}'
        for title, url in pages.items():
            scrape_detail_page(title, f'{base_url}{url}', base_url, base_path)

    ## NOTE: html 수정
    # path = "./tistory_webnautes/개발 환경_C&C++/Visual Studio Code에서 C_C++ 프로그래밍( Windows _ Ubuntu).html"
    # xpaths = ['./head', './/div[contains(@class, "revenue_unit_wrap")]', './/ins', './/iframe', './body/div/div[last()]', './body/a[last()]']
    # _modify_html(path, xpaths)

    # _title1: './/*[@id="content"]//header/div/h1/a'  # 제목
    # _title2: './/*[@id="content"]//header/div/div[@class="sub-info"]//abbr[contains(@class, "dt-published")]'  # 작성일

    # body
    # //*[@id="content"]/section/div/div[contains(@class, "e-content")]/div[contains(@class, "contents_style")]


    # xpath = './/a[contains(@class, "list-group-item")]'
    # detail_pages = scrape_list_pages(pages, xpath, _extract_detail_pages_2)  ## NOTE: 제목(파일 이름 변경이 필요한 경우!!)
    # # detail_pages = scrape_list_pages(pages, xpath, _extract_detail_pages)  ## NOTE: 제목(파일이름 변경이 필요없는 경우)
    # print(detail_pages)
