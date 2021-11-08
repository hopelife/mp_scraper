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
        el.text: el.get('href')
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
    try:
        _title1 = root.xpath('.//h1[@id="article-heading_3-0"]')[0]
    except:
        _title1 = et.Element("h1")  ## 요소가 없으면 title로 생성
        _title1.text = title

    try:
        _title2 = root.xpath('.//div[@id="displayed-date_2-0"]')[0]
    except:
        _title2 = et.Element("div")  ## 요소가 없으면 title로 생성
        _title2.text = 'No datetime data'

    try:
        root = root.xpath('.//div[@id="mntl-sc-page_1-0"]')[0]
    except:
        root = root.xpath('.//*[@id="article-content_1-0"]')[0]

    root.make_links_absolute(base_url)  # TODO: url들을 절대 주소로 변환

    figs = root.xpath('.//figure')
    print(f"figs: {len(figs)}")

    root.make_links_absolute(base_url)  # TODO: url들을 절대 주소로 변환

    for fig in figs:
        img = fig.xpath(".//img")[0]
        try:    #  KeyError: 'data-filename'
            path = f'images/' + img.attrib['data-src'].lower().split('/')[-1]
            url = img.attrib['data-src']
            _save_file_by_url(f'{base_path}/{path}', url)  # NOTE: image 파일 저장
            time.sleep(0.1)
            ## NOTE: figure element -> img element
            _img = et.Element("img")
            _img.set('src', path)
            _img.set('width', '800')  ## NOTE: 이미지 폭 강제 설정
            fig.getparent().replace(fig, _img)  ## NOTE: element 치환(figure -> img) 
        except:
            print(f"fig: {etree.tostring(fig)}")
            pass

    # 제외(마지막 div)
    el = root.xpath('./div[last()]')[0]
    el.getparent().remove(el)

    # insert
    body.insert(0, _title1)
    body.insert(1, _title2)
    body.insert(2, root)

    _create_folder(base_path)  ## NOTE: 이미지 저장시 폴더 생성됨
    title = _remove_punc(title)  # TODO: 파일 이름에 사용할 수 없는 특수문자 제거
    open(f'{base_path }/{title}.html', 'w', encoding="utf-8").write(_normalize_spaces(etree.tostring(html, encoding=str))) ## NOTE: html 저장, endcoding=str, spaces 정리  ## html 저장


if __name__ == '__main__':

    base_url = 'https://www.investopedia.com'
    base_path = 'investopedia_com'

    # titles = [
    #     'best-ways-learn-technical-analysis',
    #     # 'how-to-trade-the-three-white-soldiers-pattern'
    # ]

    url = 'https://www.investopedia.com/trading/best-ways-learn-technical-analysis'
    xpath = '//*[@id="journey-nav__sublist_3-0"]/li/a'
    detail_pages = _extract_detail_pages(url, xpath)
    # print(detail_pages)

    ## NOTE: Guide to Technical Analysis
    detail_pages = {
        'KEY TECHNICAL ANALYSIS CONCEPTS': {
            'Overview': 'https://www.investopedia.com/terms/t/technical-analysis-of-stocks-and-trends.asp', 'Dow Theory': 'https://www.investopedia.com/terms/d/dowtheory.asp', 'Support and Resistance Basics': 'https://www.investopedia.com/trading/support-and-resistance-basics/', 'Support (Support Level)': 'https://www.investopedia.com/terms/s/support.asp', 'Resistance (Resistance Level)': 'https://www.investopedia.com/terms/r/resistance.asp', 'Trend': 'https://www.investopedia.com/terms/t/trend.asp', 'Pullback': 'https://www.investopedia.com/terms/p/pullback.asp', 'Breakout': 'https://www.investopedia.com/terms/b/breakout.asp', 'Reversal': 'https://www.investopedia.com/terms/r/reversal.asp', 'Overbought': 'https://www.investopedia.com/terms/o/overbought.asp', 'Oversold': 'https://www.investopedia.com/terms/o/oversold.asp', 'Relative Strength': 'https://www.investopedia.com/terms/r/relativestrength.asp', 'Candlestick': 'https://www.investopedia.com/terms/c/candlestick.asp', 'Volume': 'https://www.investopedia.com/terms/v/volume.asp', 'Gap': 'https://www.investopedia.com/terms/g/gap.asp'
        },

        ## NOTE: 스크래핑 제외
        # 'GETTING STARTED WITH TECHNICAL ANALYSIS': {
        #     'Best Ways to Learn Technical Analysis': 'https://www.investopedia.com/trading/best-ways-learn-technical-analysis/', 'Top 7 Books to Learn Technical Analysis': 'https://www.investopedia.com/articles/personal-finance/090916/top-5-books-learn-technical-analysis.asp', 'Top Technical Analysis Courses': 'https://www.investopedia.com/trading/top-technical-analysis-courses/', 'The Best Technical Analysis Trading Software': 'https://www.investopedia.com/articles/active-trading/121014/best-technical-analysis-trading-software.asp', 
        # },

        'ESSENTIAL TECHNICAL ANALYSIS STRATEGIES': {
            'Technical Analysis Strategies for Beginners': 'https://www.investopedia.com/articles/active-trading/102914/technical-analysis-strategies-beginners.asp', 'How to Use a Moving Average to Buy Stocks': 'https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp', 'How to Use Volume to Improve Your Trading': 'https://www.investopedia.com/articles/technical/02/010702.asp', 'The Anatomy of Trading Breakouts': 'https://www.investopedia.com/articles/trading/08/trading-breakouts.asp', 'Market Reversals and How to Spot Them': 'https://www.investopedia.com/investing/market-reversals-and-how-spot-them/',
        },

        'TECHNICAL ANALYSIS PATTERNS': {
            'Introduction to Technical Analysis Price Patterns': 'https://www.investopedia.com/articles/technical/112601.asp', '5 Most Powerful Candlestick Patterns': 'https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp', 'Continuation Pattern': 'https://www.investopedia.com/terms/c/continuationpattern.asp', 'Trendline': 'https://www.investopedia.com/terms/t/trendline.asp', 'Price Channel': 'https://www.investopedia.com/terms/p/price-channel.asp', 'Channeling: Charting a Path to Success': 'https://www.investopedia.com/trading/channeling-charting-path-to-success/', 'Playing the Gap': 'https://www.investopedia.com/articles/trading/05/playinggaps.asp', 'Double Tops and Bottoms': 'https://www.investopedia.com/terms/d/double-top-and-bottom.asp', 'Triple Tops and Bottoms': 'https://www.investopedia.com/articles/technical/02/012102.asp', 'Head And Shoulders Pattern': 'https://www.investopedia.com/terms/h/head-shoulders.asp', 'How to Trade the Head and Shoulders Pattern': 'https://www.investopedia.com/articles/technical/121201.asp', 'Flag': 'https://www.investopedia.com/terms/f/flag.asp', 'Pennant': 'https://www.investopedia.com/terms/p/pennant.asp', 'Triangle': 'https://www.investopedia.com/terms/t/triangle.asp', 'Wedge': 'https://www.investopedia.com/terms/w/wedge.asp', 'Cup and Handle Pattern': 'https://www.investopedia.com/terms/c/cupandhandle.asp', 'Trading Fibonacci Retracements': 'https://www.investopedia.com/articles/active-trading/091114/strategies-trading-fibonacci-retracements.asp', 'Elliott Wave Theory': 'https://www.investopedia.com/terms/e/elliottwavetheory.asp', "Trader's Guide to Using Fractals": 'https://www.investopedia.com/articles/trading/06/fractals.asp', 
        },
        
        'TECHNICAL ANALYSIS INDICATORS': {
            'Technical Indicator Definition': 'https://www.investopedia.com/terms/t/technicalindicator.asp', 'Moving Average (MA)': 'https://www.investopedia.com/terms/m/movingaverage.asp', 'Crossover': 'https://www.investopedia.com/terms/c/crossover.asp', 'Golden Cross vs. Death Cross': 'https://www.investopedia.com/ask/answers/121114/what-difference-between-golden-cross-and-death-cross-pattern.asp', 'Bollinger Band®': 'https://www.investopedia.com/terms/b/bollingerbands.asp', 'Oscillator': 'https://www.investopedia.com/terms/o/oscillator.asp', 'Moving Average Convergence Divergence (MACD)': 'https://www.investopedia.com/terms/m/macd.asp', 'Relative Strength Index (RSI)': 'https://www.investopedia.com/terms/r/rsi.asp', 'Stochastic Oscillator': 'https://www.investopedia.com/terms/s/stochasticoscillator.asp', 'Rate Of Change': 'https://www.investopedia.com/terms/p/pricerateofchange.asp', 'Money Flow Index (MFI)': 'https://www.investopedia.com/terms/m/mfi.asp', 'Divergence': 'https://www.investopedia.com/terms/d/divergence.asp'
        }
    }

    for key, pages in detail_pages.items():
        print(f"{key}")
        _base_path = base_path + f'/{key}'
        for title, url in pages.items():
            print(f"{title}")
            scrape_detail_page(title, f'{url}', base_url, _base_path)
