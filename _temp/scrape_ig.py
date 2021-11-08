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
    punc = '[!"#$%&\'()*+,-./:;<=>?[\]^_`{|}~“”·]'
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
    styles = root.xpath(".//style[@type='text/css']")
    for style in styles:
        n = len(head.xpath('.//style'))
        head.insert(n+1, style)  ## NOTE: meta, 앞의 style 뒤에 추가

    ## title
    _title1 = root.xpath(".//body/div[2]/div/div/div/div[3]/div/div/div/div/div[1]")[0]
    _title2 = root.xpath(".//body/div[2]/div/div/div/div[3]/div/div/div/div/div[2]")[0]
    # _title1 = root.xpath(".//div[@class='grid parsys']")[0]
    # _title1 = root.xpath(".//div[@class='grid parsys']")[0]
    # _title2 = root.xpath(".//body/div[1]/div/div/div/div[2]/div/div/div/div/div[1]")[0]
    # print(f"html: {etree.tostring(html)}")

    # root = root.xpath(".//body/div[2]/div/div/div/div[3]/div/div/div/div/div[3]")[0]  # 확인 필요
    root = root.xpath(".//body/div[2]/div/div/div/div[3]/div/div/div/div/div[3]/div")[0]
    # root = root.xpath(".//div[@class='grid__col__inner ']")[0]  # 확인 필요

    
    ## NOTE: 불필요한 div(앞으로 4개, 뒤로 4개) 제거
    l = len(root.xpath("./div/div/div/div"))
    for i, el in enumerate(root.xpath("./div/div/div/div")):  ## NOTE: 
        if i < 4 or i > l - 5:
            el.getparent().remove(el)

    root.make_links_absolute(base_url)  # TODO: url들을 절대 주소로 변환

    figs = root.xpath('.//igws-img')
    print(f"figs: {len(figs)}")

    root.make_links_absolute(base_url)  # TODO: url들을 절대 주소로 변환

    for fig in figs:
        try:    #  KeyError: 'data-filename'
            url = f"https://{fig.attrib['data-src']}"
            path = f'images/' + fig.attrib['data-src'].split('/')[-1].replace(' ', '_').lower()
            _save_file_by_url(f'{base_path }/{path}', url)  # NOTE: image 파일 저장
            time.sleep(0.1)
            ## NOTE: figure element -> img element
            img = et.Element("img")
            img.set('src', path)
            fig.getparent().replace(fig, img)  ## NOTE: element 치환(figure -> img) 
        except:
            print(f"fig: {etree.tostring(fig)}")
            pass

    ## NOTE: noscript 제거
    for el in root.xpath(".//noscript"):
        try:
            el.getparent().remove(el)
        except:
            pass   

    body.insert(0, _title1)
    body.insert(1, _title2)
    body.insert(2, root)

    _create_folder(base_path)  ## NOTE: 이미지 저장시 폴더 생성됨
    open(f'{base_path }/{title}.html', 'w', encoding="utf-8").write(_normalize_spaces(etree.tostring(html, encoding=str))) ## NOTE: html 저장, endcoding=str, spaces 정리  ## html 저장


if __name__ == '__main__':

    base_url = 'https://www.ig.com'
    base_path = 'ig_com'

    titles = [
        '16-candlestick-patterns-every-trader-should-know-180615',
        # 'how-to-trade-the-three-white-soldiers-pattern'
    ]
    
    for title in titles:
        url = f'https://www.ig.com/en/trading-strategies/{title}'
        scrape_detail_page(title, url, base_url, base_path)
        time.sleep(0.1)
