# [파이썬 크롤러 만들기](https://jione-e.tistory.com/28)
# [Source Code for Package lxml.html](https://lxml.de/api/lxml.html-pysrc.html)

import os, sys
import json
import time
import re

import requests
import lxml.html as etree
import lxml.etree as et
import chardet
from urllib import parse



sys.path.append('../_public') ## Note: 현재 디렉토리 기준 상대 경로 설정
# from scrap_requests import (_root_tree, _fn)
# from scrap_selenium import (go_selenium, _wait_xpath)
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
    punc = r'[\\/:*?"<>|]'  ## NOTE: 파일이름에 사용할 수 없는 문자
    # punc = '[!"#$%&\'()*+,-./:;<=>?[\]^_`{|}~“”·]'
    return re.sub(punc, '_', s)
    # return re.sub(punc, '_', s).encode('utf-8', 'ignore').decode('utf-8', 'ignore') 


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
    root = etree.fromstring(page.content.decode('utf-8', 'ignore'))

    # enc = parse.quote(text)
    # dec = parse.unquote(enc)
    return {
        _remove_punc(el.xpath('./span[@class="title"]')[0].text.replace('.', '').strip()): parse.unquote(el.get('href').strip())
        for el in root.xpath(xpath)
    }
    # return {
    #     _remove_punc(etree.tostring(el.xpath('./span[@class="title"]')[0], encoding=str)): el.get('href').strip()
    #     for el in root.xpath(xpath)
    # }

    # for menu in meus:
    #     title = menu.xpath('./span[@class="title"]')
    #     href = menu.attrib['href']


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
    root = etree.fromstring(requests.get(url).content.decode('utf-8', 'ignore'))

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
    styles = root.xpath("//style[@type='text/css']")
    # n = len(styles)
    # print(f"styles: {n}")
    for style in styles:
        n = len(head.xpath('.//style'))
        # print(f"{etree.tostring(style)}")
        head.insert(n+1, style)  ## NOTE: meta, 앞의 style 뒤에 추가

    _title = root.xpath('.//article[@id="content"]//div[@class="post-cover"]//h1')[0]
    _author = root.xpath('.//article[@id="content"]//div[@class="post-cover"]//span[@class="author"]')[0]
    _date = root.xpath('.//article[@id="content"]//div[@class="post-cover"]//span[@class="date"]')[0]

    # root = root.xpath('.//article[contains(@class, "post__holder")]')[0]
    root = root.xpath('.//article[@id="content"]//div[@class="entry-content"]/div')[0]

    figs = root.xpath('.//figure')
    
    # for fig in figs:
    #     print(f"figure: {etree.tostring(fig)}")

    root.make_links_absolute(base_url)  # TODO: url들을 절대 주소로 변환
# <span data-url=
# "https://blog.kakaocdn.net/dn/M6YCK/btrdjdNKSJs/P0QXLncXH37CeB3gNK4KSK/img.png"
#  data-lightbox="lightbox" data-alt="&amp;lt;코스피 20일 이평선 마켓 타이밍&amp;gt;"><img src="images/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&amp;fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FM6YCK%2FbtrdjdNKSJs%2FP0QXLncXH37CeB3gNK4KSK%2Fimg.png" data-origin-width="1166" data-origin-height="820" data-ke-mobilestyle="widthOrigin"></span>
    for fig in figs:
        try:    #  KeyError: 'data-filename'
            url = fig.xpath('span')[0].attrib['data-url']
            _url = url.split('/')
            path = f"images/{_url[-2]}.{_url[-1].split('.')[-1]}"
            _save_file_by_url(f'{base_path }/{path}', url)  # NOTE: image 파일 저장
            time.sleep(0.1)
            ## NOTE: figure element -> img element
            img = et.Element("img")
            img.set('src', path)
            fig.getparent().replace(fig, img)  ## NOTE: element 치환(figure -> img) 
        except:
            print(f"fig: {etree.tostring(fig)}")
            pass

    ## TODO: figs2: <span data-url="https://t1.daumcdn.net/cfile/tistory/995FB0435FAE3D8B06?download" data-lightbox="lightbox"><img src="https://t1.daumcdn.net/cfile/tistory/995FB0435FAE3D8B06" style="cursor: pointer;max-width:100%;height:auto" width="600" height="406" filename="4.PNG" filemime="image/jpeg"></span>

    # figs = root.xpath('.//img')

    # root.make_links_absolute(base_url)  # TODO: url들을 절대 주소로 변환

    # for fig in figs:
    #     try:    #  KeyError: 'data-filename'
    #         path = f'images/' + fig.attrib['src'].lower().split('/')[-1]
    #         url = fig.attrib['src']
    #         _save_file_by_url(f'{base_path}/{path}', url)  # NOTE: image 파일 저장
    #         time.sleep(0.1)
    #         ## NOTE: figure element -> img element
    #         fig.set('src', path)
    #     except:
    #         print(f"fig: {etree.tostring(fig)}")
    #         pass


    ## NOTE: 제거
    els = root.xpath('.//p[text()="\u00A0"]')  ## NOTE: &nbsp; 삭제
#     els += root.xpath(".//p[not(normalize-space())]")  ## NOTE: empty p 삭제, BUG! figure tag도 전부 없어짐!!!
    els += root.xpath('.//div[@class="revenue_unit_wrap "]')
    
    els += root.xpath('.//div[contains(@class, "container_postbtn")]/following-sibling::*')  # following-sibling
    els += root.xpath('.//div[contains(@class, "container_postbtn")]') # 자기 자신
    els += root.xpath('.//div[@class="txc-textbox"][last()]')  ## TODO: 마지막 txc-textbox => 모두 광고인지 확인 필요
    ## TODO <p data-ke-size="size16">다음 포스팅에서 살펴보겠습니다.</p> 뒷부분 제거

    for el in els:
        try:
            el.getparent().remove(el)
        except:
            pass

    body.insert(0, _title)
    body.insert(1, _author)
    body.insert(2, _date)
    body.insert(3, root)

    _create_folder(base_path)  ## NOTE: 이미지 저장시 폴더 생성됨
    title = _remove_punc(title)  # TODO: 파일 이름에 사용할 수 없는 특수문자 제거
    open(f'{base_path }/{title}.html', 'w', encoding="utf-8").write(_normalize_spaces(etree.tostring(html, encoding=str))) ## NOTE: html 저장, endcoding=str, spaces 정리  ## html 저장


if __name__ == '__main__':
    ## Forecasting: Principles and Practice

    base_path = 'tistory_com_stock79'
    base_url = 'https://stock79.tistory.com/'

    ## NOTE: list_pages
    categories = {
        '투자의 기초(필독)': [f"{base_url}category/투자의 기초(필독)?page={page_no}" for page_no in range(1, 5)],
        '실전 투자 기법': [f"{base_url}category/실전 투자 기법?page={page_no}" for page_no in range(1, 6)],
        '닥터퀀트의 젠포트 강좌': [f"{base_url}닥터퀀트의 젠포트 강좌?page={page_no}" for page_no in range(1, 2)],
        '주식 단기 매매 기법': [f"{base_url}주식 단기 매매 기법?page={page_no}" for page_no in range(1, 2)],
        '퀀트 투자 전략': [f"{base_url}category/퀀트 투자 전략?page={page_no}" for page_no in range(1, 2)],
        '모델 포트폴리오 공개': [f"{base_url}category/모델 포트폴리오 공개?page={page_no}" for page_no in range(1, 4)],
        '스크랩': [f"{base_url}category/스크랩?page={page_no}" for page_no in range(1, 5)],
        '주식투자 리스타트': [f"{base_url}category/주식투자 리스타트?page={page_no}" for page_no in range(1, 2)]
    }


    # list_pages = [f"{base_url}category/투자의%20기초%28필독%29?page={page_no}" for page_no in range(1, 5)]

    ## NOTE: get detail_pages
    # list_pages = [f"{base_url}category/투자의%20기초%28필독%29?page=1"]

    # detail_pages = {}
    # for category, list_pages in categories.items():
    #     xpath = './/div[@class="post-item"]/a'
    #     detail_pages[category] = scrape_list_pages(list_pages, xpath)
    #     time.sleep(0.5)

    # print(f"detail_pages: {detail_pages}")

    # _create_folder(base_path)
    # _json_to_file(data=detail_pages, path=f"{base_path}/detail_pages.json")

    # ## NOTE: scrape detail pages
    detail_pages = _file_to_json(f"{base_path}/detail_pages.json")

    detail_pages.pop('투자의 기초(필독)')
    # print(detail_pages)
    for key, details in detail_pages.items():
        _base_path = f"{base_path}/{key}"
        for title, url in details.items():
            title = _remove_punc(title.replace('.', '-'))
            scrape_detail_page(title, f"{base_url}{url[1:]}", base_url, _base_path)
            time.sleep(0.5)

    ## TODO: image element 다름!!!
    # 퀀트 투자 전략

    # <span class="imageblock" style="display:inline-block;width:526px;;height:auto;max-width:100%">
    # <img src="https://t1.daumcdn.net/cfile/tistory/99861D3359C7701D22" style="max-width:100%;height:auto" width="526" height="276" filename="1.PNG" filemime="image/jpeg">
    # </span>

    # 주식투자 리스타트
    # <div class="WACImageContainer SCX116252729" style="margin: 0px; padding: 0px; -webkit-user-select: text; -webkit-user-drag: none; -webkit-tap-highlight-color: transparent; position: relative; cursor: default; left: 0px; border: none; width: 482px; height: 289px;"><div id="{a5fd1fba-7822-48cc-b2e8-1e5408427c45}{130}" class="WACAltTextDescribedBy SCX116252729" aria-hidden="true" style="margin: 0px; padding: 0px; -webkit-user-select: text; -webkit-user-drag: none; -webkit-tap-highlight-color: transparent; position: absolute; visibility: hidden; z-index: -100;"></div><img class="WACImage SCX116252729" alt="이미지" src="data:image/gif;base64,R0lGODlh4gEhAXAAACH5BAEAAAAALAAAAADiASEBhwAAAAAAAAAAMwAAZgAAmQAAzAAA/wAzAAAzMwAzZgAzmQAzzAAz/wBmAABmMwBmZgBmmQBmzABm/wCZAACZMwCZZgCZmQCZzACZ/wDMAADMMwDMZgDMmQDMzADM/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/zMzADMzMzMzZjMzmTMzzDMz/zNmADNmMzNmZjNmmTNmzDNm/zOZADOZMzOZZjOZmTOZzDOZ/zPMADPMMzPMZjPMmTPMzDPM/zP/ADP/MzP/ZjP/mTP/zDP//2YAAGYAM2YAZmYAmWYAzGYA/2YzAGYzM2YzZmYzmWYzzGYz/2ZmAGZmM2ZmZmZmmWZmzGZm/2aZAGaZM2aZZmaZmWaZzGaZ/2bMAGbMM2bMZmbMmWbMzGbM/2b/AGb/M2b/Zmb/mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5kzAJkzM5kzZpkzmZkzzJkz/5lmAJlmM5lmZplmmZlmzJlm/5mZAJmZM5mZZpmZmZmZzJmZ/5nMAJnMM5nMZpnMmZnMzJnM/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswAmcwAzMwA/8wzAMwzM8wzZswzmcwzzMwz/8xmAMxmM8xmZsxmmcxmzMxm/8yZAMyZM8yZZsyZmcyZzMyZ/8zMAMzMM8zMZszMmczMzMzM/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8zAP8zM/8zZv8zmf8zzP8z//9mAP9mM/9mZv9mmf9mzP9m//+ZAP+ZM/+ZZv+Zmf+ZzP+Z///MAP/MM//MZv/Mmf/MzP/M////AP//M///Zv//mf//zP///wECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwECAwj/AAVdEUhwoMGCCA8qTMhwocOGEB9KjEhxosWKGC9qzMhxo8eOID+KDElypMmSKE+qLAlAUKuXMFthiwlzJk2ZN3HetEmTZ0yfNXMCfTlUZ0+hSHcmPaq0KdOnP5dGdToValCqV60SlZq1qteuYLdiFavV6FeyZ82GVYt2bdG3XNvKZUtXUEtsePPq3cu3r9+/gAMLHky4sOHDiBMrXsy4sePHkCNLnkyZ8JWBlTNr3sy5s+fPoEOLHh26laDTpFOrXs26tevXsGPrvXJXtu3buHPr3s37senavYMLH068uPHJlwUdX868ufPnt1sNVA69uvXr2LMnpk1du/fv4MMX///dXbz58+jTi06uvr379/ARm0Ydv779++6549/Pv7918oWZdoVe0rEQgEt5XcECCzL55+CDED7G3mCXLTjbdCwMiM2CAgXQYIQghigiX9LRJ9hLggTgVysqtsIgXpeNKOOMEepXmIJ+CYSNICwkqCGNQAYZH4CFpdhXiRv+eIWKK+YUk0s3QUmTlE/mRCVMV6Jo5ZZRcjmll1V2KeaXY4ZJ5plmpoklmGuW2Saab6qppZtzwllnT0LeiFmRPfJFH44w9tmkaU4WauihiCaq6KKMNuroo5BGKumklE6aZ4CnlSeYkQSaGCOMPwKm6aWkljqcjYTx2OmHMwn64ommxiwq625EBlaggTGymGGGAxaoYKiizirssLBNKNiCu/aKLLJ58TjqX6wSK+20nrGV+Oxo11Kr7bYSArdatNyGK658dmUbmrnjpqvuXsZ+u+678O41H7qf0RvvvdOi6i6+/Ipb62r29itwqe2qBu7ACMdqrWsBJ+ywjPoa/PDEpf6rWsMUZ+xfwakdrPHHEM7LMMgkixhxxyWn/KDFqWGs8svmcUyaxzDXnN7Crbls887XnTwzz0DfXO7IQRctnsyj0Wz00s6JnDPTUGPnc9JRV/0cy6TpbPXWsSEtmtJchx3/3XREi202b1N/ffbauWENWLQoymvipmzXbZvXe51mYV4uBrBggzz6DSy0dhfumtO2TsdkoK0qq5yL9mpt+OSRpd0XoHi9qqOqMNoLNuWgU+Z2jovz2CCL2HyauqAkzrSj6zjBLnvstM9ue+2436577rzv7nvvwP8ufPDED2988cgfr3zyvJfyieva4u2noJzOpCLmmJPoUqZvSul99+DX+b344RNK/vnmpz+++uWv73778KP/vvzxs0///fbnP7/+9btkyid0wIQpPkcqnKWqdK9Cneo4FxjJha46yqDDJ57HLcvxJXuaGxAD92SrB74HGpjABAW3NTrttYhxkGvcvo5e1UAPtica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" style="margin: 0px; padding: 0px; -webkit-user-select: text; -webkit-user-drag: none; -webkit-tap-highlight-color: transparent; border: none; width: 482px; height: 289px;"></div>



    # menus = root.xpath('.//div[@class="post-item"]/a')
    # for menu in meus:
    #     title = menu.xpath('./span[@class="title"]')
    #     href = menu.attrib['href']

    ## pagination
    # url_format = f"/category/투자의%20기초%28필독%29?page={page_no}"





    # menus = root.xpath('.//div[@class="post-item"]/a')
    # for menu in meus:
    #     title = menu.xpath('./span[@class="title"]')
    #     href = menu.attrib['href']

    # ## pagination
    # url_format = "/category/투자의%20기초%28필독%29?page={page_no)}"

    # for page_no in range(1, 5):
    # url = f"{url_format}"

    # paging = root.xpath('./div[@class="pagination"]')
    # prev = paging.xpath('./a[contains(@class, "prev")]')
    # pages = paging.xpath('./a')[1:-1]

    # hrefs = [page.attrib['href'] for page in pages]

    # for href in hrefs:
    #     pass
    #     ## _extract_detail_pages()

    # next = paging.xpath('./a[contains(@class, "next")]')
