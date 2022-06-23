#-*- coding: utf-8 -*-
import os
import sys
import ssl
import json
import urllib.request
import yaml


# 설정파일 읽기
with open(os.getcwd() + '/apps/workspace-python/my_project/config.yaml') as f:
    configs = yaml.load(f, Loader=yaml.FullLoader)


client_id = configs['naveropenapi']['datalab']['search']['application']['client_id']
client_secret = configs['naveropenapi']['datalab']['search']['application']['client_secret']
url = configs['naveropenapi']['datalab']['search']['application']['application_url']
# body = '{"startDate": "2021-03-01","endDate": "2021-03-02","timeUnit": "date","keywordGroups": [{\"groupName": "한글","keywords": ["한글","korean"]}]}'

body = {
        "startDate": "2021-03-01",
        "endDate": "2021-03-02",
        "timeUnit": "date",
        "keywordGroups": [
            {
                "groupName": "쇼핑",
                "keywords": [
                    "닥스",
                    "korean"
                ]
            }
        ]
    }

# SSL: CERTIFICATE_VERIFY_FAILED 해결을 위한 의존성 추가
context = ssl._create_unverified_context()

# request = urllib.request.Request(url)
# request.add_header("X-Naver-Client-Id",client_id)
# request.add_header("X-Naver-Client-Secret",client_secret)
# request.add_header("Content-Type","application/json")
# # ensure_ascii가 참(기본값)이면, 출력에서 모든 비 ASCII 문자가 이스케이프 되도록 보장됩니다. ensure_ascii가 거짓이면, 그 문자들은 있는 그대로 출력됩니다.
# response = urllib.request.urlopen(request, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), context=context)
# rescode = response.getcode()
# if(rescode==200):
#     response_body = response.read()
#     print(response_body.decode('utf-8'))
# else:
#     print("Error Code:" + rescode)