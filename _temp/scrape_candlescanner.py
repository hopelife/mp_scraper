# [파이썬 크롤러 만들기](https://jione-e.tistory.com/28)
# [Source Code for Package lxml.html](https://lxml.de/api/lxml.html-pysrc.html)

import os, sys
import json
import time
import re

import requests
import lxml.html as etree
import lxml.etree as et

sys.path.append('../_public') ## Note: 현재 디렉토리 기준 상대 경로 설정
from scrap_requests import (_root_tree, _fn)
from scrap_selenium import (go_selenium, _wait_xpath)
from utils_basic import (_read_file, _create_folder, _json_to_file, _file_to_json, _write_file, _fn)

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
    punc = '[!"#$%&\'()*+,-./:;<=>?[\]^_`{|}~“”·]'
    return re.sub(punc, '', s)


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


def _extract_detail_pages(url, xpath):
    """상세 페이지 title, url 추출
    """
    page = requests.get(url)
    root = etree.fromstring(page.content)
    return {
        el.xpath('.//h3/text()')[0].replace('#', '').replace('.', '').replace(' (', '('): el.xpath('./a')[0].get('href')
        for el in root.xpath(xpath)
    }


def scrape_list_pages(pages, xpath):
    """스크랩할 page 리스트
    TODO: response = session.get(url)  # Session / yield 사용
    """
    _pages = {}
    if type(pages) == list:
        for url in pages:
            _pages = dict(_pages, **_extract_detail_pages(url, xpath))
    elif type(pages) == dict:  # dict
        for sub, url in pages.items():
            _pages[sub] = {}
            _pages[sub] = dict(_pages[sub], **_extract_detail_pages(url, xpath))

    return _pages


def scrape_detail_page(title, url, base_url, base_path):
    """스크랩할 page 리스트
    url: 스크랩할 페이지
    base_url: 스크랩할 site url
    base_path: 저장할 폴더
    TODO: response = session.get(url)  # Session / yield 사용
    """
    root = etree.fromstring(requests.get(url).content)

    ## HTML wraper
    html = et.Element("html")
    head = et.Element("head")
    body = et.Element("body")

    html.insert(0, head)
    html.insert(1, body)

    ## meta(encoding)
    meta = et.Element("meta")
    meta.set('charset', 'utf-8')
    head.insert(0, meta)

    ## style
    # styles = root.xpath(".//style[@type='text/css']")
    # for style in styles:
    #     n = len(head.xpath('.//style'))
    #     head.insert(n+1, style)  ## NOTE: meta, 앞의 style 뒤에 추가

    ## title
    # _title = root.xpath(".//div[@class='research-article-header__text']")[0]
    _title = root.xpath('.//h1[@class="title-header"]')[0]

    # root = root.xpath('.//article[contains(@class, "post__holder")]')[0]
    root = root.xpath('.//div[@class="post_content"]')[0]

    # youtube
    # root.xpath('.//figure')

    figs = root.xpath('.//img')

    root.make_links_absolute(base_url)  # TODO: url들을 절대 주소로 변환

    for fig in figs:
        try:    #  KeyError: 'data-filename'
            path = f'images/' + fig.attrib['src'].lower().split('/')[-1]
            url = fig.attrib['src']
            _save_file_by_url(f'{base_path}/{path}', url)  # NOTE: image 파일 저장
            time.sleep(0.1)
            ## NOTE: figure element -> img element
            fig.set('src', path)
        except:
            print(f"fig: {etree.tostring(fig)}")
            pass

    ## 제거
    _remove_el(root, './/blockquote')

    body.insert(0, _title)
    body.insert(1, root)

    open(f'{base_path }/{title}.html', 'w', encoding="utf-8").write(_normalize_spaces(etree.tostring(html, encoding=str))) ## NOTE: html 저장, endcoding=str, spaces 정리  ## html 저장


if __name__ == '__main__':
    print("scrape_candlescanner.py")
    base_url = 'https://www.candlescanner.com/'
    base_path = 'candlescanner_com'

    # url = 'https://www.candlescanner.com/patterns-dictionary/'

    # root = etree.fromstring(requests.get(url).content)
    # root = root.xpath('.//div[@class="tab-content"]/div[contains(@class, "tab-pane")]')[0]
    
    # ## NOTE: selenium
    # # driver = go_selenium(url=url, frame=None, browser='chrome', headless=False, implicitly_wait=10)
    # # body = _wait_xpath(xpath='.//*[@id="tab-1-80113659"]', max_wait=20, driver=driver)
    # # body = _wait_xpath(xpath='.//div[@class="tab-content"]/div[contains(@class, "tab-pane")]', max_wait=20, driver=driver)
    # # root = etree.fromstring(body.get_attribute('innerHTML'))
    
    # _types = root.xpath('./ul/li')

    # print(f"_types: {len(_types)}")

    # detail_pages = {}
    # for _type in _types:
    #     type_name = _type.xpath('.//strong')[0].text_content().split('(')[0].replace('candles', '').replace('patterns', '').strip()
    #     for candle in _type.xpath('.//td//a'):
    #         print(f"candle: {candle}")
    #         detail_pages[f"{type_name}_{candle.text_content().strip().replace(' ', '-').replace('/', '+')}"] = candle.attrib['href'].strip()

    # _create_folder(base_path)
    # _json_to_file(data=detail_pages, path=f"{base_path}/detail_pages.json")

    # detail_pages = {
    #     "Basic_Black Candle": "https://www.candlescanner.com/candlestick-patterns/black-candle/"
    # }

    detail_pages = _file_to_json(f"{base_path}/detail_pages.json")
    for title, url in detail_pages.items():
        scrape_detail_page(title, url, base_url, base_path)
        time.sleep(0.5)
    # for title in titles:
    #     url = f'https://www.forex.com/en/market-analysis/latest-research/{title}'
    #     scrape_detail_page(title, url, base_url, base_path)
    #     time.sleep(0.1)


    # name
    # figure
    # Japanese name
    # Forecast
    # Trend prior to the pattern
    # Opposite candlestick
    # Construction
    # description