# -*- coding: utf-8 -*-

import os
import configLoader
import proxyClassV1 as pc
import browserUserAgent as bua

class ChromeLoader:

    def __init__(self):
         self.agent = None

    def __del__(self):
        # self.close()
        pass

    def getBrower(self):
        proxy = pc.ProxyClassV1()
        self.agent = bua.BrowserUserAgent()
        browser = self.agent.getDriver(proxy.getProxy())

        return browser

    def close(self):
        print("self.browser")
        self.agent.close()


if __name__ == "__main__":
    # 검색 URL 가져오기
    loader = ChromeLoader()
    loader.getBrower()
    del loader

