# -*- coding: utf-8 -*-

import os
import requests
import re
import time
import yaml
import random
import remotedbModule
import ProxyClass as PC
import BrowerUserAgent as BUA
import unicodedata
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from multiprocessing import Pool

class NaverblogCrawlingHashTagClass:

    workpath = os.getcwd() + '/apps/workspace-python/my_project/'
    # workpath = "/root/app-test/crawling"

    # 설정파일 읽기
    with open(workpath + "config.yaml") as f:
        configs = yaml.load(f, Loader=yaml.FullLoader)
    
    
    def __init__(self):
        self.isuseProxy = False
        self.isuseAgent = True
        self.noheader = True
        self.chromepath = NaverblogCrawlingHashTagClass.configs['chromedrive']['chrome_path']
      
    def getBrower(self):
        chrome_options = webdriver.ChromeOptions()

        if self.isuseProxy :
            proxy = PC.ProxyClass()
            chrome_options.add_argument('--proxy-server={}'.format(proxy.getProxy()))
        if self.isuseAgent :
            agent = BUA.BrowerUserAgent()
            chrome_options.add_argument(agent.getBrowerUserAgent())
        
        if self.noheader :
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

        browser = webdriver.Chrome(executable_path=self.chromepath, chrome_options=chrome_options)
        return browser


    # 검색 결과 목록 가져오기
    def getlinklist(self) :
        os.putenv("NLS_LANG", ".AL32UTF8")
        remote_db_class = remotedbModule.Remote_Database()

        try :
            sql = """
                    SELECT *
                    FROM (
                        SELECT PLATFORM, KEYWORD, LINKURL FROM CRAWLING_TARGET_URL CTU
                        WHERE PLATFORM = 'naverblog'
                        and NOT EXISTS (SELECT 1 FROM CRAWLING_TARGET_URL_HASHTAGS CTUH
                                            WHERE CTU.PLATFORM = CTUH.PLATFORM
                                            AND CTU.KEYWORD = CTUH.KEYWORD
                                            AND CTU.LINKURL = CTUH.LINKURL
                                        )
                        ORDER BY REGDT
                    )
                    WHERE ROWNUM < 1000
                """
 
            pageList = remote_db_class.executeAll(sql)
        except Exception as e:
            print("Exception == {}".format(e))
        finally :
            remote_db_class.close()
        
        return pageList

    def getHashtags(self, browser, row):
        link = row[2]
        hashtags = []
        
        try : 
            browser.get(link)
            browser.implicitly_wait(5)

            browser.switch_to.frame("mainFrame")
            
            bs4 = BeautifulSoup(browser.page_source, "lxml")
            tagList = bs4.find(id=re.compile("tagList_.*"))
            elements = None

            if tagList != None :
                elements = tagList.select("a > span.ell")
                for e in elements :
                    hashtags.append(e.text.strip())

            # print(hashtags)
        except Exception as e :
            print("exception==={}".format(e))
        return self.dup_remove(hashtags)

    # 중복값 제거
    def dup_remove(self, linklist):
        return list(set(linklist)) #list로 변환


    def timesleep(self, interval):
        time.sleep(interval * random.random())

    def insertHashTag(self):
        remote_db_class = remotedbModule.Remote_Database()
        browser = self.getBrower()
        idx = 0
        while True :
            # 조회목록 가져오기
            rows = self.getlinklist()
            if len(rows) == 0:
                break

            for row in rows :
                platform = row[0]
                keyword = row[1]
                link = row[2]

                # hashtag 가져오기
                hashtags = self.getHashtags(browser, row)
                print("keyword={}, hashtags = {}".format(keyword, hashtags))
                
                # insert hashtag
                if hashtags != None and len(hashtags) > 0 :
                    for hashtag in hashtags:
                        sql = "insert into CRAWLING_TARGET_URL_HASHTAGS (platform, keyword, linkurl, hashtag) values ('{}', '{}', '{}', '{}')".format(platform, keyword, link, unicodedata.normalize("NFC", hashtag))
                        remote_db_class.execute(sql)
                        remote_db_class.commit()
                else :
                    sql = "insert into CRAWLING_TARGET_URL_HASHTAGS (platform, keyword, linkurl, hashtag) values ('{}', '{}', '{}', '{}')".format(platform, keyword, link, "-")
                    remote_db_class.execute(sql)
                    remote_db_class.commit()

                if idx != 0 and idx % 500 == 0 :
                    browser.close()
                    browser = self.getBrower()

                idx += 1

        remote_db_class.close()
        browser.close()




if __name__ == "__main__":
    # 검색 URL 가져오기
    naver = NaverblogCrawlingHashTagClass()
    naver.insertHashTag()

