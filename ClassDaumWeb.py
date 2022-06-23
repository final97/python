import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # SSL 인증 Warning 스킵


class ClassDaumWeb:
    def __init__(self, header, query, url):
        self.header = header
        self.query = query
        self.url = url
        # print("self.header = {}".format(self.header))
        # print("self.hequeryader = {}".format(self.query))
        # print("self.url = {}".format(self.url))

    def get(self):
        self.response = requests.get(self.url, headers=self.header, params=self.query, verify=False)  # verify false 옵션 SSL 인증 오류 회피
        self.jsonObjects = self.response.json()

    def printCheck(self):
        print("status_code : {}".format(self.response.status_code))
        # for header in self.response.headers:
        #     print("{}: {}".format(header, self.response.headers[header]))

    def printMata(self):
        if self.response.status_code == 200:
            jsonObjects = self.jsonObjects["meta"]
            for jsonObject in jsonObjects:
                print("{}: {}".format(jsonObject, jsonObjects[jsonObject]))

    def printDocument(self):
        if self.response.status_code == 200:
            jsonObjects = self.jsonObjects["documents"]
            for jsonObject in jsonObjects:
                # print("{}".format(jsonObject))
                for doc in jsonObject:
                    print("{}: {}".format(doc, jsonObject[doc]))


    def getDocumentList(self):
        documentsList = []
        if self.response.status_code == 200:
            jsonObjects = self.jsonObjects["documents"]
            for jsonObject in jsonObjects:
                # print("{}".format(jsonObject))
                documentsList.append(jsonObject)
        return documentsList
            

if __name__ == '__main__':
    header = {'Content-Type': 'application/soap+xml', 'charset': 'utf-8', 'Authorization':'KakaoAK 954fff1b8a0e2e72236268052d9125ff'} 
    query = {'query': '이효리', 'sort': 'recency'}
    url = "https://dapi.kakao.com/v2/search/web"


    daumWeb = ClassDaumWeb(header, query, url)
    daumWeb.get()
    daumWeb.printCheck()
    daumWeb.printMata()
    # daumWeb.printDocument()
    documentList = daumWeb.getDocumentList()

    for list in documentList:
        print("{}".format(list["contents"]))
