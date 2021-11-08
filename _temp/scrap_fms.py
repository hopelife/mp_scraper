    # ## NOTE: chrome
    # s = ScrapBySelenium(browser='chrome', url='https://www.selenium.dev/documentation/ko/getting_started_with_webdriver/browsers/')

    # ## NOTE: edge
    # ## 로그인
    # url = 'http://www.fms.or.kr/'
    # s = ScrapBySelenium(browser='edge', url=url)
    # time.sleep(3)
    # s.close_all_popups()

    # xpath = {
    #     'id': '//*[@id="user_id"]',
    #     'pw': '//*[@id="pswd"]',
    #     'submit': '//*[@id="loginForm"]/div/div[2]/button'
    # }
    # keys = {
    #     'id': 'sdcelltrion2',
    #     'pw': 'sdcelltrion2!!'
    # }

    # s.login(xpath, keys)
    # s.close_all_popups()
    # time.sleep(2)

    # # s.escape()
    # s.close_alert()
    # time.sleep(2)
    # s.close_all_popups()

    # ## 시설물관리대장 click
    # xpath = '//div[@class="main-center-link"]/a[1]'
    # s.click(xpath=xpath)
    # # s.goto_page(url)
    # time.sleep(3)

    # s.goto_iframe('mainFrame')

    # ## NOTE: html 저장 
    # s.save_html(path='시설물관리대장.html', xpath='//div[@id="divListData"]', encoding='utf-8')
    # time.sleep(1)


    # D:/moon/dev/projects/SATS/source4/staff/시설물관리대장.html
    url = 'D:/moon/dev/projects/SATS/source4/staff/시설물관리대장.html'
    s = ScrapBySelenium(browser='edge', url=url)

    ## 시설물관리대장
    xpath = '//tr/td[@class="t-left"][1]'
    els = s.find_elements(xpath)

    ## TODO: 시설물 목록
    for el in els:
        # print(f'el: {el.get_attribute("outerHTML")}')
        title = s.sub_element_text(xpath='a', element=el)
        print(f"시설물명: {title}")

        # if title in titles:  # 시설물 목록에 있으면
        #     pass
        #     crawl_시설물관리대장()

        # s.sub_element(xpath='/a', element=el).click()

    # # xpath = '//td[@class="t-left"][1]/a'
    # xpath = '//tr/td[@class="t-left"][1]/a'
    # s.click(xpath=xpath)
    # time.sleep(3)
    # s.save_html(path='기본현황.html', encoding='utf-8')
    # # el = s.find_elements(xpath=xpath)
    # # print(f"el: {el}")

    # ### 기본현황
    # s.goto_iframe('ifrm')
    # time.sleep(1)
    # s.save_html(path='기본현황_table.html', xpath='//table', encoding='utf-8')

    # ## 이미지 저장
    # xpath = '//table//td/a/img[1]'
    # path = 'test_screenshot.png'
    # s.save_screenshot(xpath, path)

    # # xpath = '//table//td/a/img[1]'
    # path = 'test_file.png'
    # s.save_file(xpath, path)
    # time.sleep(2)

    # #### combobox
    # xpath = '//select[@name="bk_no"]'
    # s.goto_combobox(xpath=xpath, value='1')  ## NOTE: value selected, '1', '0' -> TODO: option 갯수에 따라 for loop
    # time.sleep(2)
    # s.save_html(path='기본현황_table2.html', xpath='//table', encoding='utf-8')

    ### 상제제원

    ### 부재구성

    ### 설계도서/보고서

    ### 점검진단도래시기

    ### 안전등급추이

    ### 위치정보


    ## 유지관리계획

    ### 유지관리계획(총괄)

    ### 점검진단계획

    ### 보수보강계획


    ## NOTE: 로그아웃
    # s.goto_iframe('mainFrame')

    ## 로그아웃 버튼 show click
    # xpath = '//span[contains(@class, "username")]'
    # s.click(xpath=xpath)
    # time.sleep(1)

    # ## 로그아웃 click
    # xpath = '//a[contains(@class, "btn-logout")]'
    # s.click(xpath=xpath)

    ## 팝업 닫기

    ## NOTE: 종료
    s.close()