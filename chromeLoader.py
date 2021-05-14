# -*- coding: utf-8 -*-

import os
import proxyClassV1 as pc
import browserUserAgent as bua

class ChromeLoader:

    def __init__(self):
         self.browser = None

    def __del__(self):
        self.close()

    def getBrower(self):
        proxy = pc.ProxyClassV1()
        agent = bua.BrowserUserAgent()
        print("proxy.getProxy()...{}".format(proxy.getProxy()))
        self.browser = agent.getDriver(proxy.getProxy())

        return self.browser

    def close(self):
        if self.browser != None and not self.browser :
            self.browser.close()


if __name__ == "__main__":
    # 검색 URL 가져오기
    loader = ChromeLoader()
    loader.getBrower()
    del loader

