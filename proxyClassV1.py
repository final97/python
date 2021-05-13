# -*- coding: utf-8 -*-

import os
import json
import sys
import datetime
import random
import requests
import configLoader
import browserUserAgent as bua
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone


class ProxyClassV1:
    def __init__(self):
        self.targetUrl = configLoader.ConfigLoader.Loader.Proxy.PROXY_URL
        self.proxyPath = configLoader.ConfigLoader.Loader.Proxy.PROXY_PATH
        
    def isProxy(self):
        if os.path.isfile(self.proxyPath) :
            KST = timezone(timedelta(hours=9))
            nowTime = datetime.now(KST)
            fileTime = datetime.fromtimestamp(os.path.getmtime(self.proxyPath), KST)
            ## 24시간이 지나면 false
            if nowTime - fileTime < timedelta(hours=24):
                return True
        
        return False
    
    def loadProxy(self):
        with open(self.proxyPath) as f1:
            return json.load(f1)

    def getURLProxyData(self):
        agent = bua.BrowserUserAgent()
        browser = agent.getDriver()

        browser.get(self.targetUrl)
        browser.implicitly_wait(5)
        bs4 = BeautifulSoup(browser.page_source, "lxml")
        tables = bs4.select("body > table:nth-child(3) > tbody > tr:nth-child(4) > td > table > tbody")

        proxyList = []

        for tr in tables[0].children:
            # 하위태그가 없을 경우 for 문을 중단한다.
            try:
                tds = tr.children
                td = list(tds)
            except Exception as e:
                # print(e)
                break
      
            # 헤더 2칸 스킵
            if len(td) < 9:
                continue
            
            ip_port = td[0].text
            proxy_type = td[1].text
            country = td[3].text
            times = td[8].text.split(" ")

            map = {"ip_port": ip_port, "proxy_type": proxy_type, "country": country, "time": times[0] + " " + times[1]}
            proxyList.append(map)

        proxyJson = json.dumps(proxyList)      
        with open(self.proxyPath, "w") as f1:
            json.dump(proxyJson, f1)

        return proxyJson
    
    # json 타입으로 리턴한다.
    def getProxys(self):
        if self.isProxy() :
            return self.loadProxy()
        else :
            return self.getURLProxyData()
        
    # json 타입으로 리턴한다.
    def getProxy(self):
        proxylist = self.getProxys()
        return proxylist[random.randrange(0,len(proxylist))]
        
if __name__ == "__main__":
    proxy = ProxyClass()
    # j = json.loads(proxy.getProxys())
    print(proxy.getProxy())

    # for row in j:
    #     print(row)