## NOTE: requests, lxml.html로 불가한 경우에만 사용!!
## 설치된 chrome version == _bin/chromedriver.exe 버전이 같아야 함
## chrome version 확인: chrome > 설정 > chrome 정보(좌측 하단)
## chromedriver 다운로드: https://chromedriver.chromium.org/downloads

## [Python 의 selenium 을 이용해서 스크롤 하기](https://hello-bryan.tistory.com/194)

import os, re
import platform
import time

import requests
import lxml.html as etree

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains  # ActionChains 사용, 페이지 scroll down

from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge


def _set_driver(browser='chrome', headless=True, implicitly_wait=10):
    """selenium driver 설정

    Args:
        browser (str, optional): [description]. Defaults to 'chrome'.
        headless (bool, optional): [description]. Defaults to True.
        implicitly_wait (int, optional): [description]. Defaults to 10.
    """
    if browser=='chrome':
        ## chromedriver 경로
        if 'Windows' in platform.system():
            CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__), './_bin/chromedriver.exe')
        else:
            CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__), './_bin/chromedriver')

        chrome_options = Options()
        if headless:
            chrome_options.add_argument('headless')
        chrome_options.add_argument('window-size=1920x1080')
        chrome_options.add_argument("disable-gpu")
        # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

    elif browser=='edge':
        edge_options = EdgeOptions()
        edge_options.use_chromium = True  # if we miss this line, we can't make Edge headless
        # A little different from Chrome cause we don't need two lines before 'headless' and 'disable-gpu'
        if headless:
            edge_options.add_argument('headless')
        edge_options.add_argument('window-size=1920x1080')
        edge_options.add_argument('disable-gpu')
        driver = Edge(executable_path='_bin/msedgedriver.exe', options=edge_options)

    return driver


def _wait(xpath='', max_wait=20, driver=None):
    """
    xpath의 element가 click 가능할 때까지 기다림, max_wait = 20
    """
    try:
        WebDriverWait(driver,  max_wait).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return driver.find_element_by_xpath(xpath)
    except:
        # 실패 시에는 에러메시지로 Time Out 출력
        print('Time Out')
        return False  # NOTE: False 리턴, 페이지가 없는 것으로 간주


# selenium login 
def _login(xpath='', keys={}, driver=None): # TODO: login process
    _wait(xpath=xpath, max_wait=20, driver=driver)
    driver.find_element_by_xpath(xpath['id']).send_keys(keys['id'])
    driver.find_element_by_xpath(xpath['pw']).send_keys(keys['pw'])
    driver.find_element_by_xpath(xpath['submit']).click()
    time.sleep(2)


def _scroll(xpath, driver):
    """
    xpath의 element가 있는 곳까지 scroll down
    """
    el = driver.find_element_by_xpath(xpath)
    action = ActionChains(driver)
    action.move_to_element(el).perform()


def _scroll_down(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height



def _selenium(url='', frame=None, browser='chrome', headless=True, implicitly_wait=10):
    """selenium driver를 초기화하고, url로 이동
    url page로 go
    """
    driver = _set_driver(browser=browser, headless=headless, implicitly_wait=implicitly_wait)
    driver.get(url=url)
    if not frame:
        driver.switch_to.frame(frame)
        driver.switch_to_default_content  #NOTE: 상위 프레임으로 전환
    return driver


def _source(driver=None, xpath=None):
    """selenium html source(str)

    Args:
        driver (obj, optional): [description]. Defaults to None.
        xpath (None, str, element, optional): [description]. Defaults to None.

    Returns:
        [str]: [description]
    """
    if xpath == None:  ## xpath가 없는 경우
        return driver.page_source
    elif type(xpath) == str:  ## xpath가 'str'으로 주어진 경우
        return driver.find_element_by_xpath(xpath).get_attribute('innerHTML')
    else:  ## xpath에 element가 입력된 경우
        return driver.element.get_attribute('innerHTML')


def _save_screenshot(xpath, path):
    with open(path, 'wb') as file:
        file.write(driver.find_element_by_xpath(xpath).screenshot_as_png)
        file.close()


def _close_all_popups(driver):
    """
    팝업 닫기
    """
    driver.window_handles
    for h in driver.window_handles[1:]:
        driver.switch_to_window(h)
        driver.close()
    driver.switch_to_window(driver.window_handles[0])


def _close_alert(driver):
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
        print("alert accepted")
    except TimeoutException:
        print("no alert")


if __name__ == '__main__':
    pass
    url = "https://www.hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index.xml"
    driver = go_selenium(url=url, frame=None, browser='chrome', headless=False, implicitly_wait=10)
    ## 홈텍스로 이동 
    # url = "https://www.hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index.xml"

    # _wait(xpath='.//', max_wait=20, driver=None)
    time.sleep(2)

    # source = driver.find_element_by_id('prcpMenuUl').get_attribute('innerHTML')
    source = driver.find_element_by_xpath("//ul[@id='prcpMenuUl']").get_attribute('innerHTML')
    print(etree.fromstring(source).xpath('//text()'))  ## NOTE: text 리스트
    print(etree.fromstring(source).text_content())  ## NOTE: text 전체를 한 문자열로


    # print(f"driver1: {driver}")
    # ## 로그인 버튼 클릭
    # driver.find_element_by_id('group88615548').click()

    # driver.find_element_by_id('group88615548').


    # time.sleep(2)
    # print(f"driver.find_element_by_id('group88615548'): {driver.find_element_by_id('group88615548')}")

    # ## 본문영역(iframe)
    # iframe = driver.find_element_by_id('txppIframe')
    # driver.switch_to.frame(iframe)

    # print(f"driver.find_element_by_id('txppIframe'): {driver.find_element_by_id('txppIframe')}")
    # time.sleep(2)

    # ## 로그인 버튼
    # driver.find_element_by_id('anchor22').click() 

    # time.sleep(2)

    # ## 공인인증서 영역
    # iframe = driver.find_element_by_id('dscert')
    # driver.switch_to.frame(iframe)

    # time.sleep(2)

    # # 두번째 공인인증서 선택
    # # driver.find_element_by_xpath('//*[@title="파이낸스 데이터(20607)0003029201709191518042"]').click()
    # driver.find_element_by_xpath('//*[@title="증권/보험용"]').click()

    # time.sleep(2)

    # # 인증서 비밀번호 입력
    # passwd = 'moon5221!!'
    # driver.find_element_by_id('input_cert_pw').send_keys(passwd)
    # driver.find_element_by_id('btn_confirm_iframe').click()

    # time.sleep(2)

    # # 상위 프레임으로 이동
    # driver.switch_to_default_content()
    # driver.close()


    ## NOTE: functions
    ##--------------------------------------------------------
    # - source: driver.page_source
    # - source2: element.get_attribute('innerHTML')
    # - find elements: driver(element).find_elements_by_xpath(xpath)
    # - find element: driver(element).find_element_by_xpath(xpath)
    # - exist element: True if len(driver.find_elements_by_xpath(xpath)) > 0 else False
    # - click: element.click()
    # - combobox: Select(driver.find_element_by_xpath(xpath)).select_by_value(value)
    # - combobox: Select(driver.find_element_by_xpath(xpath)).select_by_visible_text(option)
    # - text: element.find_element_by_xpath(xpath).text.split("\n")[0]
    # - text2: driver.find_elements_by_xpath(xpath)[0].text.split("\n")[0]
    # - attribute: driver.find_element_by_xpath(xpath).get_attribute(attr)
    # - script 실행: driver.execute_script(script)
    # - key press: driver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    # - close: driver.close()

    # def _save_html(path, xpath=None, encoding='utf-8'):
    #     """
    #     한글 깨지면 encoding='euc-kr'
    #     """
    #     if xpath == None:
    #         html = driver.page_source
    #     else:
    #         element = driver.find_element_by_xpath(xpath)
    #         # html = element.get_attribute('innerHTML')
    #         html = element.get_attribute('outerHTML')
    #     f = open(path, 'w', encoding=encoding)
    #     f.write(html)
    #     f.close()


    # def _save_file(xpath, path):
    #     """
    #     xpath: image xpath, ex) '//div[@id="recaptcha_image"]/img'
    #     path: image file path
    #     """
    #     # get the image source
    #     img = driver.find_element_by_xpath(xpath)
    #     src = img.get_attribute('src')

    #     # download the image
    #     # urllib.urlretrieve(src, path)
    #     urllib.request.urlretrieve(src, path)
