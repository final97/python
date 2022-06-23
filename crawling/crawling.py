# -*- coding: utf-8 -*-

import os
import requests
import re
import time
import random
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
        self.confLoad = configLoader.ConfigLoader.Loader
        self.chmoader = chromeLoader.ChromeLoader()
    
    def __del__(self):
        del self.chmoader
    
    # 중복값 제거
    def dup_remove(self, linklist):
        return list(set(linklist)) #list로 변환

    # 페이지 정보 추출
    def getPageData(self):

        browser = self.chmoader.getBrower()
        try:
 
            browser.get("https://search.shopping.naver.com/search/all?vertical=style&query=닥스")
            browser.implicitly_wait(10)

            ## 페이지로딩
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div[2]/div[3]/div[1]/ul/div')))

            ## 필요값 찾기
            bs4 = BeautifulSoup(browser.page_source, "lxml")
            totelement = bs4.select_one("#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > div.seller_filter_area > ul > li.active > a > span.subFilter_num__2x0jq")
            totalArticle = int(totelement.strip().replace(",",""))
            print("totalcnt=={}".format(totalArticle))


            # element = bs4.select_one("#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div")
            
        except TimeoutException as te:
            print("TimeoutException == {}".format(te))
        except Exception as e:
            print("Exception : \n")
            print("\t\t\tType : {}".format(type(e)))    # the exception instance
            print("\t\t\tArgs : {}".format(e.args))     # arguments stored in .args
            print("\t\t\tFullText : {}".format(e))
        finally :
            browser.close()

    def timesleep(self, interval):
        time.sleep(interval * random.random())


if __name__ == "__main__":

    naver = Crawling()
    naver.getPageData()


    # naver.search()

    # del naver