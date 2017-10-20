from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re


def get_cookies(driver):
    cookies = {}
    with open('cookies', 'r') as f:
        datas = f.read().split(';')
        for item in datas:
            name, value = item.split('=', 1)
            driver.add_cookie({'name':name, 'value':value})
        f.close()

def down_page(driver, times):
    for i in range(0, times+1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)


def parse_one_page(html):
    '''进行正则匹配'''
    pattern = re.compile('.*?<a class="UserLink-link.*?data-za-detail-view-element_name="User">(.*?)</a></div>'  #用户姓名
                         +'.*?</span></span>.*?>(.*?)<.*?</span>' #用户操作
                         +'.*?<h2 class="ContentItem-title">.*?target="_blank".*?>(.*?)</a>' #推荐内容
                         +'.*?分享', re.S)
    items = re.findall(pattern, html)
    print(items)

    for item in items:
        yield {
            'ActiveUser': item[0],
            'Active': item[1],
            'Title': item[2],
        }


def main():
    url = 'https://www.zhihu.com'
    driver = webdriver.Edge()
    driver.get(url)
    down_page(driver, 10)
    html = driver.page_source
    with open('html.txt', 'w', encoding='utf-8') as f:
        f.write(html)
    parse_one_page(html)

    with open('result.txt', 'w', encoding='utf-8') as fo:
        for i in parse_one_page(html):
            fo.write(str(i) + '\n')
        fo.close()


if __name__ == '__main__':
    main()
