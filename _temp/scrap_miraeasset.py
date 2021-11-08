## 증권용어사전 저장
import os, sys
import time, datetime

sys.path.append(os.path.join(os.path.abspath('../staff')))
from ScrapBySelenium import ScrapBySelenium

## 증권용어사전
def scrap_miraeasset_glossary():
    """
    증권용어사전 저장
    """
    # url = f'https://www.miraeassetdaewoo.com/hki/hki3028/r01.do'
    url = f'https://securities.miraeasset.com/hki/hki3028/r01.do#seq_5'
    s = ScrapBySelenium(url=url)
    xpath = '//div[@class="scrollbox"]/ul[@class="result"]/li/a'

    if s.wait(xpath) == -1:  # NOTE: 페이지가 없는 것으로 간주
        print('page not found!!')
        return False
    
    elements = s.find_elements(xpath)

    scripts = []
    for element in elements:
        script = element.get_attribute("href")
        scripts.append(script)

    words = []
    for script in scripts:
        # print(f"script: {script}")
        s.do_script(script)
        # s.click_element(element=element)
        # time.sleep(1)
        xpath = '//div[@class="scrollbox"]/div[@class="result-inboxtxt"]'
        if s.wait(xpath) == -1:  # NOTE: 페이지가 없는 것으로 간주
            print('page not found!!')
            continue

        txts = s.find_element(xpath).text.split("\n")

        key = txts[0]
        if key.count('(') > 1: # NOTE: 페이지 오류, 2번 중복되어서 나오는 '(abc...)' 제거
            key = "(".join(txts[0].split(" (")[:-1])
        
        words.append({key: "\n".join(txts[1:]).replace("\u3000", " ").replace("  ", " ")})


    # print(f"words: {words}")
    with open('../../_backup/glossary_miraeasset.json', 'w', encoding='utf-8') as f:
        f.write(f"{words}")
        f.close()
   
    s.close()


if __name__ == '__main__':
    # pass
    scrap_miraeasset_glossary()
