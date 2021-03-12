import requests
import re
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def get_cal(element, s):
    idx = 0
    for e in element :
        if s == e.text : 
            break
        else :
            idx += 1
    return idx

def set_element(xpathclick, xpathlist, xpathenter):
    browser.find_element_by_xpath(xpathclick).click()
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpathlist)))
    browser.find_element_by_xpath(xpathenter).send_keys(Keys.ENTER)



yes = datetime.today() - timedelta(1)

url = "https://datalab.naver.com/shoppingInsight/sCategory.naver"
browser = webdriver.Chrome(executable_path=r'/Users/final97/apps/pkg/webdriver/chromedriver')
browser.get(url)
browser.implicitly_wait(time_to_wait=5)

idx_year = 0
idx_month = 0
idx_day = 0

soup = BeautifulSoup(browser.page_source, "lxml")
el_period = soup.select_one('div.set_period_target > span:nth-child(1)')
e1 = el_period.select('div.select')

idx_year = get_cal(e1[0].select('ul > li'), '{:04d}'.format(yes.year)) + 1
idx_month = get_cal(e1[1].select('ul > li'), '{:02d}'.format(yes.month)) + 1
idx_day = get_cal(e1[2].select('ul > li'), '{:02d}'.format(yes.day)) + 1

# year 선택
set_element(
        '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[1]/span'
        , '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[1]/ul'
        , '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[1]/ul/li[' + str(idx_year) + ']/a'
        )
time.sleep(1)
# month 선택
set_element(
        '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[2]/span'
        , '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[2]/ul'
        , '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[2]/ul/li[' + str(idx_month) + ']/a'
        )
time.sleep(1)
# day 선택
set_element(
        '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[3]/span'
        , '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[3]/ul'
        , '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div[2]/span[1]/div[3]/ul/li[' + str(idx_day) + ']/a'
        )


el = soup.find('ul', class_='select_list scroll_cst')
el_li = el.find_all("li")
el_li_cnt = len(el_li)

for i in range(1, el_li_cnt):
    set_element(
        '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div[1]/span'
        , '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul'
        , '/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div[1]/ul/li[' + str(i) + ']/a'
        )
    time.sleep(0.5)
    browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div/a').click()
    time.sleep(2)

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/ul')))

    top100area = BeautifulSoup(browser.page_source, "lxml")
    top100 = top100area.select_one('div.rank_top1000_scroll > ul')
    browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]').click()
    time.sleep(1)

    top100area = BeautifulSoup(browser.page_source, "lxml")
    top100.extend(top100area.select_one('div.rank_top1000_scroll > ul'))

    # print(el_li[i-1].select_one('a')['data-cid'])

    for e in top100 :
        print('{} - {}, {} 번 {} 키워드'.format(el_li[i-1].text, el_li[i-1].find('a')['data-cid'], e.select_one('a > span').text.strip(), e.select_one('a').text.strip()))

    # /html/body/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div/a[2]




time.sleep(3)
browser.close()
