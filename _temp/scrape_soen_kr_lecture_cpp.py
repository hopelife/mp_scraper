# [파이썬 크롤러 만들기](https://jione-e.tistory.com/28)
# [Source Code for Package lxml.html](https://lxml.de/api/lxml.html-pysrc.html)

import os, sys
import json
import time
import re

import requests
import lxml.html as etree
import lxml.etree as et
from requests_html import HTMLSession  ## NOTE: wait page loading

sys.path.append('../_public') ## Note: 현재 디렉토리 기준 상대 경로 설정
from scrap_requests import (_root_tree, _fn)
from scrap_selenium import (go_selenium, _wait_xpath)
from utils_basic import (_read_file, _create_folder, _file_to_json, _json_to_file, _write_file, _fn)

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


def scrape_list_pages(url, base_path):
    """스크랩할 page 리스트
    TODO: response = session.get(url)  # Session / yield 사용
    """
    url = 'http://www.soen.kr/lecture/ccpp/menu.htm'

    root = etree.fromstring(requests.get(url).content.decode(encoding='euc-kr'))
    titles = [a.text.split('.')[-1] for a in root.xpath('.//a')]
    hrefs = [a.attrib['href'] for a in root.xpath('.//a')]

    list_pages = {title: href for (title, href) in zip(titles, hrefs)}

    detail_pages = {}
    for title, href in list_pages.items():
        _detail_pages = {}
        url = 'http://www.soen.kr/lecture/ccpp/' + href

        root = etree.fromstring(requests.get(url).content.decode(encoding='euc-kr'))
        title2s = root.xpath('.//td[@bgcolor="eeffee"]')
        elements = []
        
        for title2 in title2s:
            _title2s = title2.xpath('./p')
            if len(_title2s) > 0:
                elements += _title2s
            else:
                elements += title2s
            # for title3 in title2.xpath('./following-sibling::p'):
            #     print("")
            #     elements.append(title3)

        print(len(elements))

        for element in elements:
            for el in element.xpath('./*'):
                if el.tag == 'font':
                    if el.text != None:
                        _title2 = re.sub(r'제\s*(\d+)\s*장 ', r'\1_', el.text).replace('.', '_').strip()
                elif el.tag == 'b':
                    _title3 = ''.join(el.xpath('./text()')).strip()

                    if _title3 != '':
                        _title3 = re.sub(r'(\d+)-(\d+)\.', lambda m: _title2 + '-' + m.group(2) + '_', _title3).replace('.', '_')
                    # print(f"title: {_title3}")

                elif el.tag == 'a':
                    if el.text != None:
                        _detail_pages[f"{_title3}-{el.text.replace('.', '_')}"] = el.attrib['href']

        if _detail_pages != {}:
            detail_pages[title] = _detail_pages
        else:
            detail_pages[title] = url  ## NOTE: url 

    # detail pages 저장
    base_path = '_cpp/soen_kr'
    _create_folder(base_path)
    _json_to_file(data=detail_pages, path=f"{base_path}/detail_pages.json")

    return detail_pages


def scrape_detail_page(title, url, base_url, base_path):
    """스크랩할 page 리스트
    url: 스크랩할 페이지
    base_url: 스크랩할 site url
    base_path: 저장할 폴더
    TODO: response = session.get(url)  # Session / yield 사용
    """
    ## NOTE: requests 사용
    # content = requests.get(url).content
    # content = requests.get(url, timeout=(3.05, 27)).content
    # time.sleep(2)
    # root = etree.fromstring(content)
    # root = root.xpath('.//body')[0]
    # print(f"root: {etree.tostring(root)}")

    ## NOTE: requests_html 사용
    # s  = HTMLSession()
    # response = s.get(url)
    # response.html.render()
    # # response.text.encode(encoding='utf-8')
    # body = response.html.find('body', first=True)
    # # root = etree.fromstring(body.text.encode(encoding='utf-8').decode('utf-8'))
    # root = etree.fromstring(body.text)
    # print(response.full_text)
    # root = root.xpath('.//body')[0]

    ## NOTE: selenium 사용
    driver = go_selenium(url=url, frame=None, browser='chrome', headless=True, implicitly_wait=10)
    body = _wait_xpath(xpath='.//body', max_wait=20, driver=driver)
    source = body.get_attribute('innerHTML')
    root = etree.fromstring(source)
    # print(f"root: {etree.tostring(root)}")

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

    # ## style
    # # styles = root.xpath(".//style[@type='text/css']")
    # # for style in styles:
    # #     n = len(head.xpath('.//style'))
    # #     head.insert(n+1, style)  ## NOTE: meta, 앞의 style 뒤에 추가

    # ## title
    # # _title = root.xpath(".//div[@class='research-article-header__text']")[0]

    # # root = root.xpath(".//div")[0]  # 확인 필요

    figs = root.xpath('.//img')

    # print(f"base_url: {base_url}")
    root.make_links_absolute(base_url)  # TODO: url들을 절대 주소로 변환

    for fig in figs:
        try:    #  KeyError: 'data-filename'
            path = f'images/' + '/'.join(fig.attrib['src'].split('/')[-2:]).replace('.files/image', '_')
            url = fig.attrib['src']
            # print(f"image url: {url}")
            # http://www.soen.kr/lecture/ccpp/cpp1/1-1-1.files/image002.gif

            _save_file_by_url(f'{base_path}/{path}', url)  # NOTE: image 파일 저장
            time.sleep(0.1)
            ## NOTE: figure element -> img element
            fig.set('src', path)
        except:
            print(f"fig: {etree.tostring(fig)}")
            pass

    body.insert(0, root)
    driver.close()
    _create_folder(base_path)  ## NOTE: 이미지 저장시 폴더 생성됨
    title = _remove_punc(title)  # TODO: 파일 이름에 사용할 수 없는 특수문자 제거
    open(f'{base_path }/{title}.html', 'w', encoding="utf-8").write(_normalize_spaces(etree.tostring(html, encoding=str))) ## NOTE: html 저장, endcoding=str, spaces 정리  ## html 저장


if __name__ == '__main__':
    base_url = 'http://www.soen.kr/lecture/ccpp/'
    # base_url = 'http://www.soen.kr/lecture/ccpp/cpp1/'
    base_path = 'soen_kr/lecture/ccpp'

    # # menu_url = 'http://www.soen.kr/lecture/ccpp/menu.htm'
    # detail_pages = scrape_list_pages(menu_url, base_path)

    detail_pages = _file_to_json(f"{base_path}/detail_pages.json")

    _keys = list(dict(detail_pages).keys())

    for key, pages in detail_pages.items():
        _base_path = base_path + f'/{key}'
        print(f"base_path: {_base_path}")
        if type(pages) == str:
            scrape_detail_page(key, pages, base_url, base_path)
            pass
            time.sleep(0.1)
        else:
            for title, url in pages.items():
                _base_url = f'{base_url}cpp{_keys.index(key)}/'
                print(f"_base_url: {_base_url}")
                if url.split('.')[-1] == 'htm' or url.split('.')[-1] == 'html':  # html 문서이면
                    # print(f"url: {_base_url}{url}")
                    # print(f"base_url: {_base_url}")
                    title = title.replace('C/C++', 'C C++')
                    scrape_detail_page(title, f'{_base_url}{url}', _base_url, _base_path)
                    time.sleep(0.1)
                else:
                   title = title.replace('C/C++', 'C C++')
                   title = _remove_punc(title)
                   _save_file_by_url(f"{_base_path}/{title}.png", f'{_base_url}{url}') 
                   time.sleep(0.1)
                #    title = _remove_punc(title)
                #    print(f"path: {_base_path}/{title}.png")
                #    print(f"url: {_base_url}{url}")



    # title = '1_프로그래밍 입문-1_프로그래머-가_프로그램'
    # base_url = 'http://www.soen.kr/lecture/ccpp/cpp1/'
    # # base_url = 'http://www.soen.kr/lecture/ccpp/cpp1/'
    # base_path = 'soen_kr/lecture/ccpp'
    # url = 'http://www.soen.kr/lecture/ccpp/cpp1/1-1-1.htm'
    # scrape_detail_page(title, url, base_url, base_path)
    # content = requests.get(url).content
    # print(content)


    ## NOTE: requests wait for loading element
    ## https://stackoverflow.com/questions/45448994/wait-page-to-load-before-getting-data-with-requests-get-in-python-3
    # r = requests.get('https://github.com', timeout=(3.05, 27))
    # In this, timeout has two values, first one is to set session timeout and the second one is what you need. The second one decides after how much seconds the response is sent. You can calculate the time it takes to populate and then print the data out.


    # max_retries = # some int
    # retry_delay = # some int
    # n = 1
    # ready = 0
    # while n < max_retries:
    # try:
    #     response = requests.get('https://github.com')
    #     if response.ok:
    #         ready = 1
    #         break
    # except requests.exceptions.RequestException:
    #     print("Website not availabe...")
    # n += 1
    # time.sleep(retry_delay)

    # if ready != 1:
    # print("Problem")
    # else:
    # print("All good")



    # https://docs.python-requests.org/projects/requests-html/en/latest/
    # pip install requests-html

    # from requests_html import HTMLSession

    # s  = HTMLSession()
    # response = s.get(url)
    # response.html.render()

    # # print(response.html.links)
    # body = response.html.find('body', first=True)
    # # print(body.text.encode(encoding='utf-8').decode("iso-8859-1"))
    # print(body.text.encode(encoding="iso-8859-1").decode("utf-8"))
    # print(response.text.encode(encoding='utf-8'))

    # open(f'{base_path }/{title}.html', 'w', encoding="utf-8").write(response.text.encode(encoding='utf-8').decode("utf-8", "strict"))