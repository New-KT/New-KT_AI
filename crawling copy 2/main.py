from news_crawling import * 
from news_summary import * 
from make_json import *

def main():
    node = 'news'  # 크롤링 할 대상
    srcText = input('검색어를 입력하세요: ')
    sort = 'sim'   # 관련도순
    cnt = 0
    jsonResult = []
    article_texts = []  # 기사 텍스트를 저장할 리스트 추가

    jsonResponse = getNaverSearch(node, srcText, 1, 10, sort)
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

    naver_news_count = 0  # 네이버 뉴스 가져온 개수를 세는 카운터 추가

    for item in jsonResult:
        url = item['link']
            
        # 네이버 뉴스를 가져올 경우에만 크롤링
        if url.startswith('https://n.news.naver.com/mnews/'):
            article_text = get_article_text(url)
            if article_text:
                article_texts.append(article_text)  # 텍스트를 리스트에 추가
                print(f"\n{article_text}")
                    
                # 네이버 뉴스를 3개 가져왔으면 루프 종료
                naver_news_count += 1
                if naver_news_count >= 3:
                    break
        
    # 기사 텍스트를 파일에 저장
    with open('%s_naver_%s_texts.txt' % (srcText, node), 'w', encoding='utf-8') as textfile:
        for text in article_texts:
            text=preprocess_text(text)
            textfile.write(text + '\n')
    
    #gpt요약결과 저장        
    file_path='%s_naver_%s_texts.txt' % (srcText, node)
    result=summarize_news(file_path)
    save_to_json(result,srcText, node)

    # naver_news_items = [item for item in jsonResult if item['link'].startswith('https://n.news.naver.com/mnews/')][:3]

    
    # jsonlist = {}
    # for news in naver_news_items:
    #     keyword = srcText
    #     titles, links = mkjs(news)
        
    #     if keyword in jsonlist:
    #         jsonlist[keyword]['title'].extend(titles)
    #         jsonlist[keyword]['link'].extend(links)
    #     else:
    #         # 해당 키워드가 없는 경우 새로운 아이템 추가
    #         jsonlist[keyword] = {'keyword': keyword, 'title': titles, 'link': links}
            
    # result_list = list(jsonlist.values())
    # result_list['news_summary'] = result
    
    # print(jsonlist)
    
    naver_news_items = [item for item in jsonResult if item['link'].startswith('https://n.news.naver.com/mnews/')][:3]

    jsonlist = {}
    for news in naver_news_items:
        keyword = srcText
        titles, links = mkjs(news)
    
        if keyword in jsonlist:
            jsonlist[keyword]['title'].extend(titles)
            jsonlist[keyword]['link'].extend(links)
        else:
            # 해당 키워드가 없는 경우 새로운 아이템 추가
            jsonlist[keyword] = {'keyword': keyword, 'title': titles, 'link': links}

    # 각 아이템에 news_summary 키를 추가
    for keyword, values in jsonlist.items():
        titles = values['title']
        links = values['link']
         
        values['news_summary'] = result
        
# jsonlist의 values만 가져와서 리스트로 만듦
    result_list = list(jsonlist.values())   
    with open('%s_naver_%s_merge.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        mergeFile = json.dumps(result_list, indent=4, ensure_ascii=False)
        outfile.write(mergeFile)
    

if __name__ == '__main__':
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    main()