# -*- coding: utf-8 -*-

import os
import requests
import re
import time
import configLoader
import chromeLoader
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from multiprocessing import Pool

class Crawling:
    
    def __init__(self):
        self.loader = chromeLoader.ChromeLoader()
    
    def __del__(self):
        del self.loader
    
    # 중복값 제거
    def dup_remove(self, linklist):
        return list(set(linklist)) #list로 변환

    # 매안검색, 해당 키워드 검색 페이지로 이동
    # def search(self):

    #     browser = self.loader.getBrower()
    #     try:
 
    #         browser.get(self.conn_url.format(self.pageid, self.keyword))
    #         browser.implicitly_wait(10)
    #         WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/ui-view/div/main/div/div/section/div[1]/div[2]/span/span/em')))

            
    #         bs4 = BeautifulSoup(browser.page_source, "lxml")
    #         element = bs4.select_one("em.search_number").text
    #         totalArticle = int(element.strip("건").replace(",",""))
    #         print("{}, totalcnt=={}, pageid={}, article=={}".format(self.keyword, totalArticle, self.pageid, article))

              

    #     except TimeoutException as te:
    #         print("TimeoutException == {}".format(te))
    #     except Exception as e:
    #         print("Exception == {}".format(e))
    #     finally :
    #         browser.close()

    def timesleep(self, interval):
        time.sleep(interval * random.random())


if __name__ == "__main__":

    naver = Crawling()

    # naver.search()

    # del naver