# -*- coding: utf-8 -*-

WORK_PATH = "/Users/final97/apps/workspace-python/my_project"

class Config:

    DEFAULT_PATH = WORK_PATH

    class ChromeDriver:
        DRIVER_PATH = "/Users/final97/apps/pkg/webdriver/chromedriver"

    class Proxy:
        PROXY_URL = "https://spys.one/en/free-proxy-list/"
        PROXY_PATH = WORK_PATH + "/proxy_list"
        PROXY_SELECTOR = "body > table:nth-child(3) > tbody > tr:nth-child(4) > td > table > tbody"


if __name__ == "__main__":
    print(Config.Proxy.PROXY_PATH)