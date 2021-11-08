# [파이썬 크롤러 만들기](https://jione-e.tistory.com/28)
# [Source Code for Package lxml.html](https://lxml.de/api/lxml.html-pysrc.html)

import os, sys
import json
import time
import re
import csv

import requests
import lxml.html as etree
import lxml.etree as et

sys.path.append('../_public') ## Note: 현재 디렉토리 기준 상대 경로 설정
from scrap_selenium import (go_selenium, _wait_xpath)
from utils_basic import (_read_file, _create_folder, _dicts_to_lists, _write_file, _fn)


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
    return re.sub(punc, '', s)


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
    pages = {}
    for el in root.xpath(xpath):
        title = el.xpath('./span')[0].get('title').replace('.', '')
        url = el.get('href')
        if 'javascript' in url:
            url = f"/book/{url.split('(')[-1][:-1]}"
        pages[title] = url

    return pages


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
    # root = root.xpath('//*[@id="load_content"]/div[contains(@class, "page-content")]')[0]  # 확인 필요

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

    # style
    styles = root.xpath(".//style[@type='text/css']")
    for style in styles:
        n = len(head.xpath('.//style'))
        head.insert(n+1, style)  ## NOTE: meta, 앞의 style 뒤에 추가

    ## body
    # print(f"root: {root}")
    _title = root.xpath('.//div[@id="load_content"]//h1')[0]
    root = root.xpath('.//div[@id="load_content"]//div[contains(@class, "page-content")]')[0]
    tail = root.xpath('./following-sibling::div')[0]

    figs = root.xpath('.//img')

    root.make_links_absolute(base_url)  # TODO: url들을 절대 주소로 변환

    for fig in figs:
        try:    #  KeyError: 'data-filename'
            path = f'images/' + fig.attrib['src'].lower().split('/')[-1].split('?')[0]
            url = fig.attrib['src']
            # _save_file_by_url(f'{base_path}/{path}', url)  # NOTE: image 파일 저장
            time.sleep(0.1)
            ## NOTE: figure element -> img element
            fig.set('src', path)
        except:
            print(f"fig: {etree.tostring(fig)}")
            pass

    body.insert(0, _title)
    body.insert(1, root)
    body.insert(2, tail)

    _create_folder(base_path)  ## NOTE: 이미지 저장시 폴더 생성됨
    title = _remove_punc(title)  # TODO: 파일 이름에 사용할 수 없는 특수문자 제거
    open(f'{base_path }/{title}.html', 'w', encoding="utf-8").write(_normalize_spaces(etree.tostring(html, encoding=str))) ## NOTE: html 저장, endcoding=str, spaces 정리  ## html 저장


if __name__ == '__main__':

    url = 'https://candlestickchart.com/glossary/listing'
    xpath = './/div[@class="card-body"]//a[@class="indicator_data"]'

    brower = go_selenium(url=url, headless=True, implicitly_wait=5)
    els = brower.find_elements_by_xpath(xpath)

    indicators = []

    for el in els:
        time.sleep(1)
        try:
            el.click()
        except:
            print("click error")
            pass
        else:
            _root = _wait_xpath(xpath='.//div[@id="indicator_view_modal"]', max_wait=5, driver=brower)

            root = etree.fromstring(_root.get_attribute('innerHTML'))
            name = root.xpath('.//h4[@id="exampleModalLabel"]/text()')
            pattern = root.xpath('.//div[@class="modal-body"]/div/div/p[1]/text()')
            trend = root.xpath('.//div[@class="modal-body"]/div/div/p[2]/text()')
            reliability = root.xpath('.//div[@class="modal-body"]/div/div/p[3]/text()')
            identification = root.xpath('.//div[@class="modal-body"]/div[@class="mb-3"]//li/text()')
            meaning = root.xpath('.//div[@class="modal-body"]/div[3]//p/text()')
            src = root.xpath('.//img')[0].attrib['src']

            print(f"src: {src}")
            indicators.append(dict(
                name = name[0],
                pattern = pattern[0].split(':')[-1].strip(),
                trend = trend[0].split(':')[-1].strip(),
                reliability = reliability[0].split(':')[-1].strip(),
                identification = ''.join(identification).strip(),
                meaning = meaning[0].split(':')[-1].strip(),
                src = src
            ))

            button = _wait_xpath(xpath='.//button[@aria-label="Close"]', max_wait=5, driver=brower)

            button.click()


    ## NOTE: 이미지 다운로드
    base_path = 'candlestickchart_com'
    for indicator in indicators:
        url = indicator['src']
        path = '/'.join(url.split('/')[-3:])
        _save_file_by_url(f'{base_path}/{path}', url)

    ## NOTE: indicators dicts 저장(csv)
    path = f"{base_path}/{'GLOSSARY OF CANDLESTICK INDICATORS'.lower()}.csv"
    with open(path, 'w', newline='', encoding='utf-8') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerows(_dicts_to_lists(indicators))

    ## NOTE: 문자 치환
    path = f"{base_path}/{'GLOSSARY OF CANDLESTICK INDICATORS'.lower()}.csv"
    with open(path, 'r', encoding='utf-8') as f:
        contents = f.read()
        contents = contents.replace('�', '’')
        f.close()

        with open(path, 'w', encoding='utf-8') as f:
            f.write(contents)
            f.close()