import os, sys
import math
import copy
import time
from datetime import datetime
import re
# import requests
import urllib
import lxml.html as ht
# import lxml.etree as et


##------------------------------------------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), '../_public')) ## Note: 현재 디렉토리 기준 상대 경로 설정
from utils_basic import (
    _create_folder, 
    _read_file, 
    _file_to_json, 
    _json_to_file, 
    _to_lists, 
    _to_digit,
    _divide_list,
    _fn
)
from utils_scraping import (
    _root,
    _remove_punc,
    _pages_by_pagination, 
    _scrape_list_pages, 
    _extract_values,
    _scrape_detail_page,
    _scrape_full_html
)
from scrap_selenium import (
    _selenium,
    _source,
    _wait,
    _login,
)

# sys.path.append(os.path.join(os.path.abspath('../staff')))
# from ScrapBySelenium import ScrapBySelenium

_base_url = 'https://m.stock.naver.com'

TODAY = datetime.now().strftime("%Y%m%d")

##
##----------------------------------------------------------

def scrap_naver_total(shcode='336370'):
    """
    shcode의 종목에 대한 '종합/투자자별 매매동향/...' 데이터 scrap
    """
    # url = f"https://m.stock.naver.com/item/main.nhn#/stocks/{shcode}/total"
    url = f"https://m.stock.naver.com/index.html#/domestic/stock/{shcode}/total"
    browser = _selenium(url=url, headless=False)
    button = _wait(xpath='.//*[@id="content"]//div[@class="VStockInfo_article__3dWiQ"]/a', driver=browser)
    
    if not button:
        print(f"페이지 로딩 실패")
        return False
    
    button.click()  ## 종목 정보 더보기

    html = _source(driver=browser, xpath='.//*[@id="content"]')
    root = _root(html)

    # ## NOTE: N증권 / 국내증시 / 종합
    # info = root.xpath('.//ul[@class="VStockInfo_list__1Hfnb"]')[0]

    # values = {
    #     'keys': {
    #         'xpath': './/li[contains(@class, "VStockInfo_item__1jFNs")]/div/strong',
    #         'target': 'text',
    #     },
    #     'vals': {
    #         'xpath': './/li[contains(@class, "VStockInfo_item__1jFNs")]/div/span',
    #         'target': 'text',
    #     },
    # }
    
    # r = _extract_values(info, values, _zip=None)
    # print({key: _to_digit(val) for key, val in zip(r['keys'], r['vals'])})

    ## NOTE: N증권 / 국내증시 / 투자자별 매매동향
    button = _wait(xpath='.//*[@id="content"]//div[@class="VTableTrend_boxMore__1EVMo"]/a[1]', driver=browser)
    
    if not button:
        print(f"페이지 로딩 실패")
        return False
    
    button.click()  ## 매매동향 더보기
    info = root.xpath('.//div[@class="VTableTrend_inner__1Crkx"]')[0]

    values = {
        'keys': {
            'xpath': './table/thead/tr/th',
            'target': 'text'
        },
        'vals': {
            'xpath': './table/tbody/tr/td',
            'target': 'content'
        }
    }
    
    r = _extract_values(info, values, _zip=None)
    n = len(r['keys'])  ## NOTE: 열column 수
    vals = [val if i%n == 0 else _to_digit(val[:len(val)//2]) if i%n==n-2 else _to_digit(val) for i, val in enumerate(r['vals'])]
    rows = [r['keys']] + _divide_list(vals, n)
    print(f"투자동향: {rows}")

#     ## NOTE: 동일 업종 비교
#     xpath = '//div[contains(@class, "compare")]/a'
#     if s.wait(xpath, max_wait=3) != -1: # '동일 업종 비교'가 있는 경우
#         upjong = s.attribute_value(xpath, "href").split('=')[-1]
#         output['업종번호'] = upjong

#     ## 컨센서스
#     xpath = '//span[contains(@class, "data_lyr")]'
#     if s.check_element(xpath): # NOTE: 컨센서스가 있는 경우
#         trade_weight = s._convert_to_float(s.find_element(xpath).text)  # NOTE: 매수.매도 점수
#         goal_price = s._convert_to_float(s.find_element('//span[@class="goal_stock"]/em').text)  # NOTE: 목표가
#         output['매매추천'] = trade_weight
#         output['목표주가'] = goal_price


#     s.close()  # NOTE: selenium browser close
#     return output


# def scrap_naver_upjong():
#     """
#     업종 상승률
#     """
#     url = "https://m.stock.naver.com/sise/siseList.nhn?menu=upjong"
#     s = ScrapBySelenium(url=url)
#     # wait_xpath = '//span[@class="u_pg_area"]/span[contains(@class, "u_pg_txt")]'
#     wait_xpath = '//span[@class="u_pg_total"]'
#     s.wait(wait_xpath)
#     total = s._convert_to_float(s.find_element_text(wait_xpath))
#     wait_xpath = '//span[@class="u_pg_area"]/span[contains(@class, "u_pg_txt")]'
#     s.click(xpath=wait_xpath)  # 버튼 펼치기

#     output = []
#     for i in range(0, total):
#         gap_xpath = f'//ul[contains(@class, "dmst_type_lst")]/li[{i+1}]//span[1]'
#         name_xpath = f'//ul[contains(@class, "dmst_type_lst")]/li[{i+1}]//strong[@class="stock_item"]'
#         no_xpath = f'//ul[contains(@class, "dmst_type_lst")]/li[{i+1}]//a[1]'
#         # <a href="/sise/siseGroupDetail.nhn?menu=upjong&amp;no=218" class="btn_detail" onclick="nclk(this, 'mil.cat', '', '');">상세 목록 보기</a>
#         name = s.find_element(name_xpath).text
#         no = s.attribute_value(no_xpath, 'href').split('=')[-1]
#         gap = s._convert_to_float(s.find_element(gap_xpath).text)
#         print(f"{name}, {no}, {gap}")
#         output.append({'업종명': name, '업종번호': no, '업종상승률': gap})
    
#     s.close()

#     return output


if __name__ == '__main__':
    ## NOTE: 테스트
    scrap_naver_total(shcode='336370')

    ## NOTE: shcode의 종목에 대한 '종합/투자자별 매매동향/업종번호/'
    # t = scrap_naver_total(shcode='336370')
    # print(f"{t}")

    ## NOTE: 업종별 업종명/업종번호/상승률
    # u = scrap_naver_upjong()
    # print(f"{u}")

    ## NOTE: file
    # path = './naver_sise_rise_table_bak.html'
    # path = './naver_sise_rise_table.html'
    # root = _tree_from_file(path=path)
    # # text = _text_by_xpath(root, xpath='.//div[@class="choice_lt"]/div')
    # # text = _text_by_xpath(root, xpath='.//th')
    # result = []
    # for i in range(3, 13):
    #     texts = _texts_by_xpath(root, xpath=f'.//table[@class="type_2"]/tbody/tr[{i}]/td')
    #     if len(texts) > 2:
    #         result.append(texts)

    # print(f"result: {result}")
    # # print(f"{[el.text for el in root.findall('.//country//rank')]}")

    # ## NOTE: naver_stock_m_domestic_upper_kospi
    # path = './naver_stock_m_domestic_upper_kospi.html'
    # root = _tree_from_file(path=path)

    # result = []
    # for i in range(1, 10):
    #     texts = _texts_by_xpath(root, xpath=f'.//table/tbody//tr[{i}]/td')
    #     if len(texts) > 2:
    #         result.append(texts)

    # print(f"result: {result}")


    ## TODO:
    ## naver 업종 코드(page serial)
    # https://m.stock.naver.com/sise/siseGroupDetail.nhn?menu=upjong&no=218

    # # 네이버
    # N증권 > 국내증시


    # ### 종합
    # - https://m.stock.naver.com/item/main.nhn#/stocks/336370/total
    # 전일
    # 시가
    # 고가
    # 저가
    # 거래량
    # 대금
    # 시총
    # 외인소진율
    # 52주최고
    # 52주최저
    # PER
    # EPS
    # BPS
    # 배당수익률
    # 주당배당금

    # ### 토론
    # - https://m.stock.naver.com/item/main.nhn#/stocks/336370/discuss


    # ### 뉴스.공시

    # #### 종목뉴스
    # https://m.stock.naver.com/item/main.nhn#/stocks/336370/news

    # #### 공시정보
    # https://m.stock.naver.com/item/main.nhn#/stocks/336370/notice

    # #### IR정보
    # https://m.stock.naver.com/item/main.nhn#/stocks/336370/ir

    # ### 시세.호가

    # #### 일별시세
    # https://m.stock.naver.com/item/main.nhn#/stocks/336370/price

    # #### 5단계 호가
    # https://m.stock.naver.com/item/main.nhn#/stocks/336370/ask


    # ### 재무
    # #### 연간실적
    # https://m.stock.naver.com/item/main.nhn#/stocks/336370/annual

    # #### 분기실적
    # https://m.stock.naver.com/item/main.nhn#/stocks/336370/quarter

    # #### 비재무정보
    # https://m.stock.naver.com/item/main.nhn#/stocks/336370/nonfinance



    # ## 홈
    # ### 관심종목

    # ### 트렌드 랭킹

    # ## 시장지표

    # ### 주요

    # ### 환율

    # ### 에너지

    # ### 금속

    # ### 금리

    # ### 농축산물



    # ## 국내

    # ### 시가총액

    # ### 업종

    # ### 테마

    # ### 그룹

    # ### 인기검색

    # ### 배당

    # ### 거래상위

    # ### 상한가

    # ### 


    # 컨센서스

    # 컨센서스



    # 업종
    # 테마
    # 그룹


    # 거래상위
    # https://m.stock.naver.com/sise/siseList.nhn?menu=quant&sosok=0


    # 상한가

    # 상승

    # 하락

    # 관리
