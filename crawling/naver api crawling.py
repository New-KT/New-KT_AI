# -*- coding: utf-8 -*-
import urllib.request
import datetime
import time
import json
import re

#발급받은 api 입력
client_id = ''
client_secret = ''

# 요청형식 만들기
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

# getRequestUrl에 보낼 url제작
def getNaverSearch(node, srcText, start, display,sort):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s&sort=%s" % (urllib.parse.quote(srcText), start, display, sort)

    url = base + node + parameters
    responseDecode = getRequestUrl(url)  # [CODE 1]

    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)


# 결과 저장
def getPostData(post, jsonResult, cnt):
    title = post['title']
    title = re.sub("<.*?>", "", title)

    description = post['description']
    description = re.sub("<.*?>", "", description)

    org_link = post['link']

    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({'cnt': cnt, 'title': title, 'description': description,'link': org_link, 'pDate': pDate})
    return None

# [CODE 0]
def main():
    node = 'news'  # 크롤링 할 대상
    srcText = input('검색어를 입력하세요: ')
    sort='sim'   # 관련도순
    cnt = 0
    jsonResult = []
    url_list=[]

    jsonResponse = getNaverSearch(node, srcText, 1, 5, sort)  # [CODE 2] 5개의 기사를 가져옴
    total = jsonResponse['total']

    for post in jsonResponse['items']:
      cnt+=1
      getPostData(post,jsonResult,cnt)
    print('전체 검색 : %d 건' % total)

    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(jsonFile)

    print("가져온 데이터 : %d 건" % (cnt))
    print('%s_naver_%s.json SAVED' % (srcText, node))

if __name__ == '__main__':
    main()


