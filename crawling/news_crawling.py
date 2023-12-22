import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import urllib.request
import re
import datetime
import os
from dotenv import load_dotenv

load_dotenv('.env')

#발급받은 api 입력
client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")

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

# 네이버 검색 API를 통해 뉴스 검색
def getNaverSearch(node, srcText, start, display, sort):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s&sort=%s" % (urllib.parse.quote(srcText), start, display, sort)

    url = base + node + parameters
    responseDecode = getRequestUrl(url)

    if responseDecode == None:
        return None
    else:
        return json.loads(responseDecode)

# 뉴스 기사에서 텍스트 추출
def get_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        article_text = soup.find('article').get_text(separator='\n', strip=True)
        return article_text

    except Exception as e:
        print(f"Error while fetching article from {url}: {e}")
        return None

# 결과 저장
def getPostData(post, jsonResult, cnt):
    title = post['title']
    title = re.sub("<.*?>", "", title)

    description = post['description']
    description = re.sub("<.*?>", "", description)

    org_link = post['link']
    
    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')  # 수정된 부분
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({'cnt': cnt, 'title': title, 'description': description,
                       'link': org_link, 'pDate': pDate})
    return None

# 메인 함수
def main():
    node = 'news'  # 크롤링 할 대상
    srcText = input('검색어를 입력하세요: ')
    sort = 'sim'   # 관련도순
    cnt = 0
    jsonResult = []
    url_list = []
    article_texts = []  # 기사 텍스트를 저장할 리스트 추가

    jsonResponse = getNaverSearch(node, srcText, 1, 5, sort)
    total = jsonResponse['total']

    for post in jsonResponse['items']:
        cnt += 1
        getPostData(post, jsonResult, cnt)

    print('전체 검색 : %d 건' % total)

    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(jsonFile)

    print("가져온 데이터 : %d 건" % (cnt))
    print('%s_naver_%s.json SAVED' % (srcText, node))

    # 각 기사 URL에 대해 기사 텍스트를 가져오기
    for item in jsonResult:
        url = item['link']
        # 네이버 뉴스를 가져올 경우에만 크롤링
        if url.startswith('https://n.news.naver.com/mnews/'):
            article_text = get_article_text(url)
            if article_text:
                article_texts.append(article_text)  # 텍스트를 리스트에 추가
                print(f"\n{article_text}")

    # 기사 텍스트를 파일에 저장
    with open('%s_naver_%s_texts.txt' % (srcText, node), 'w', encoding='utf-8') as textfile:
        for text in article_texts:
            textfile.write(text + '\n')

if __name__ == '__main__':
        main()
        