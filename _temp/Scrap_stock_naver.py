from ScrapBySelenium import ScrapBySelenium
import time, datetime
# import re

_base_url = 'https://m.stock.naver.com'

def today():
    """
    오늘 날짜
    """
    return datetime.datetime.now().strftime("%Y%m%d")


def scrap_naver_total(shcode='336370'):
    """
    shcode의 종목에 대한 '종합/투자자별 매매동향/...' 데이터 scrap
    """
    url = f"https://m.stock.naver.com/item/main.nhn#/stocks/{shcode}/total"
    print(f"shcode: {shcode}")
    s = ScrapBySelenium(url=url)
    wait_xpath = '//div[@class="total_more"][1]/a'

    if s.wait(wait_xpath) == -1:  # NOTE: 페이지가 없는 것으로 간주
        print('page not found!!')
        return False
    
    s.click(xpath=wait_xpath)
    wait_xpath = "//ul[@class='total_list']/li[16]/span"
    s.wait(wait_xpath)
    time.sleep(0.1)  # NOTE: 혹시 몰라서 ;;

    ## N증권 / 국내증시 / 종합
    # els = ["전일", "시가", "고가", "저가", "거래량", "대금", "시총", "외인소진율", "52주최고", "52주최저", "PER", "EPS", "추정PER", "추정EPS", "PBR", "BPS", "배당수익률", "주당배당금"]
    # 52주 최고: 원주가 기준 81,000 84,500 / 52주 최저: 원주가 기준 43,826 45,800
    output = {'종목코드': shcode, '날짜': today()}
    ##
    xpath = f'//ul[@class="total_list"]/li'
    elements = s.find_elements(xpath)
    for element in elements:
        key = s.sub_element_text(element=element, xpath='./div[1]')
        txt = s.sub_element_text(element=element, xpath='./span[1]')
## BUG
# Traceback (most recent call last):
#   File "tasks_after.py", line 96, in <module>
#     # time.sleep(3)
#   File "tasks_after.py", line 91, in update_krx_items
#     upsert_docs(keys=['업종번호'], docs=scrap_naver_upjong(), collection='naver.stock.upjong')
#   File "tasks_after.py", line 62, in update_krx_items_naver
#     """
#   File "C:\Dev\docMoon\projects\SATS\source3\extra\Scrap_stock_naver.py", line 41, in scrap_naver_total
#     txt = s.sub_element_text(element=element, xpath='./span[1]')
#   File "C:\Dev\docMoon\projects\SATS\source3\extra\ScrapBySelenium.py", line 124, in sub_element_text
#     return element.find_element_by_xpath(xpath).text.split("\n")[0]
#   File "C:\ProgramData\Miniconda3\envs\sats\lib\site-packages\selenium\webdriver\remote\webelement.py", line 351, in find_element_by_xpath
#     return self.find_element(by=By.XPATH, value=xpath)
#   File "C:\ProgramData\Miniconda3\envs\sats\lib\site-packages\selenium\webdriver\remote\webelement.py", line 658, in find_element
#     return self._execute(Command.FIND_CHILD_ELEMENT,
#   File "C:\ProgramData\Miniconda3\envs\sats\lib\site-packages\selenium\webdriver\remote\webelement.py", line 633, in _execute
#     return self._parent.execute(command, params)
#   File "C:\ProgramData\Miniconda3\envs\sats\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 321, in 
# execute
#     self.error_handler.check_response(response)
#   File "C:\ProgramData\Miniconda3\envs\sats\lib\site-packages\selenium\webdriver\remote\errorhandler.py", line 242, 
# in check_response
#     raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: element is not attached to the page document
#   (Session info: headless chrome=90.0.4430.93)


        output[key] = s._convert_to_float(txt)
        # print(f"txt: {txt}")

    # for i, key in enumerate(els):
    #     xpath = f'//ul[@class="total_list"]/li[{i+1}]/span[1]'
    #     # element = s.find_element(xpath)
    #     output[key] = s._convert_to_float(s.find_element_text(xpath))
    #     if key == '52주최고':
    #         print(f"{output[key]}")

    ## N증권 / 국내증시 / 투자자별 매매동향
    trends = []
    # trend = {'종목코드': shcode, '날짜': today()}
    for i in range(0, 5):
        date = s.attribute_value(f'//tbody[@class="_date_wrapper"]/tr[{i+1}]', "data-date")
        trends.append({'종목코드': shcode, '날짜': date})

    # els = ['외국인', '보유율', '기관', '개인', '종가', '전일비', '거래량']

    els = []
    elements = s.find_elements('//table[contains(@class, "trend_tb")]/thead//th')  # NOTE: tr(행)
    for element in elements:
        els.append(s.sub_element_text(element=element, xpath='./span[1]'))
    
    # print(f"els: {els[1:]}")

    for i, trend in enumerate(trends):
        for j, key in enumerate(els[1:]):  # NOTE: els 첫번째 요소 '날짜' 제외 
            xpath = f'//tbody[@class="_list"]/tr[{i+1}]/td[{j+1}]/span[last()]'
            element = s.find_element(xpath)
            trends[i][key] = s._convert_to_float(element.text)

    output['투자동향'] = trends

    ## 동일 업종 비교
    xpath = '//div[contains(@class, "compare")]/a'
    if s.wait(xpath, max_wait=3) != -1: # '동일 업종 비교'가 있는 경우
        upjong = s.attribute_value(xpath, "href").split('=')[-1]
        output['업종번호'] = upjong

    ## 컨센서스
    xpath = '//span[contains(@class, "data_lyr")]'
    if s.check_element(xpath): # NOTE: 컨센서스가 있는 경우
        trade_weight = s._convert_to_float(s.find_element(xpath).text)  # NOTE: 매수.매도 점수
        goal_price = s._convert_to_float(s.find_element('//span[@class="goal_stock"]/em').text)  # NOTE: 목표가
        output['매매추천'] = trade_weight
        output['목표주가'] = goal_price


    s.close()  # NOTE: selenium browser close
    return output


def scrap_naver_upjong():
    """
    업종 상승률
    """
    url = "https://m.stock.naver.com/sise/siseList.nhn?menu=upjong"
    s = ScrapBySelenium(url=url)
    # wait_xpath = '//span[@class="u_pg_area"]/span[contains(@class, "u_pg_txt")]'
    wait_xpath = '//span[@class="u_pg_total"]'
    s.wait(wait_xpath)
    total = s._convert_to_float(s.find_element_text(wait_xpath))
    wait_xpath = '//span[@class="u_pg_area"]/span[contains(@class, "u_pg_txt")]'
    s.click(xpath=wait_xpath)  # 버튼 펼치기

    output = []
    for i in range(0, total):
        gap_xpath = f'//ul[contains(@class, "dmst_type_lst")]/li[{i+1}]//span[1]'
        name_xpath = f'//ul[contains(@class, "dmst_type_lst")]/li[{i+1}]//strong[@class="stock_item"]'
        no_xpath = f'//ul[contains(@class, "dmst_type_lst")]/li[{i+1}]//a[1]'
        # <a href="/sise/siseGroupDetail.nhn?menu=upjong&amp;no=218" class="btn_detail" onclick="nclk(this, 'mil.cat', '', '');">상세 목록 보기</a>
        name = s.find_element(name_xpath).text
        no = s.attribute_value(no_xpath, 'href').split('=')[-1]
        gap = s._convert_to_float(s.find_element(gap_xpath).text)
        print(f"{name}, {no}, {gap}")
        output.append({'업종명': name, '업종번호': no, '업종상승률': gap})
    
    s.close()

    return output


# https://m.stock.naver.com/sise/siseGroupDetail.nhn?menu=upjong&no=218

if __name__ == '__main__':
    ## shcode의 종목에 대한 '종합/투자자별 매매동향/업종번호/'
    # t = scrap_naver_total(shcode='336370')
    # t = scrap_naver_total(shcode='336370')
    # print(f"{t}")

    ## naver 상승률
    u = scrap_naver_upjong()
    print(f"{u}")

    ## naver 업종 코드(page serial)

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
