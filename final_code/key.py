from extract import *
from crawling_main import *
import os

from konlpy.tag import Okt
import re
from krwordrank.word import KRWordRank

def remove_keywords(keywords_to_remove, dictionary):
    for keyword in keywords_to_remove:
        dictionary.pop(keyword, None)

def split_noun_sentences(text):
    okt = Okt()
    sentences = re.sub(r'([^\n\s다요죠]+[^\n다요죠]*[다요죠])', r'\1\n', text).strip().split("\n")

    result = []
    for sentence in sentences:
        if len(sentence) == 0:
            continue
        sentence_pos = okt.pos(sentence, stem=True)
        nouns = [word for word, pos in sentence_pos if pos == 'Noun']
        if len(nouns) == 1:
            continue
        result.append(' '.join(nouns) + '.')

    return result

#kr-wordrank    
def krwr(word_list,output_file_path):
    text=read_concatenate_news(output_file_path)
    min_count = 1   # 단어의 최소 출현 빈도수 (그래프 생성 시)
    max_length = 10 # 단어의 최대 길이
    wordrank_extractor = KRWordRank(min_count=min_count, max_length=max_length)
    beta = 0.85    # PageRank의 decaying factor beta
    max_iter = 20
    texts = split_noun_sentences(text)
    keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter)
    keyword_dict = {}

    # 결과를 딕셔너리에 저장
    for word, r in sorted(keywords.items(), key=lambda x: x[1], reverse=True):
        keyword_dict[word] = r

        # 딕셔너리 출력
    print(keyword_dict)
        
    result_dict = {}

    for words in word_list:
        split_words = words.split()

         # 각 단어의 가중치를 더함
        total_weight = sum(keyword_dict.get(word, 0) for word in split_words)

        result_dict[words] = total_weight

    print(result_dict)

    stopwords = ["아이디어", "프로젝트","기획 회의","진행","아이디어",' 교육 플랫폼', ' 기부 플랫폼','아이디어 기획회의']

        # 함수를 사용하여 딕셔너리에서 여러 키워드 제거
    remove_keywords(stopwords, result_dict)

    sorted_keywords = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)

        # 상위 두 개의 키 출력
    top_two_keywords = [key for key, _ in sorted_keywords[:2]]

        # 결과 출력
    print("상위 두 개의 키:", top_two_keywords)
    return top_two_keywords, stopwords
    
def keyword(output_file_path,keywords_list): 
    load_dotenv()
    file_path = read_concatenate_news(output_file_path)
    result = extract_keywords_from_meeting(file_path,keywords_list)
    
    # 문자열 변수에 결과 추가
    result_string = f"{result}"
    
    lines = result_string.split(', ')
    for line in lines:
        keywords_list.append(line)
    print(keywords_list) 
    final_keyword, stopwords =krwr(keywords_list,output_file_path)
    stopwords.extend(final_keyword)
    print(final_keyword)   
    return final_keyword
        
if __name__ == "__main__":
    # Load environment variables from a .env file
    os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-21\bin\server'
    final_keyword = []
    keyword("output.txt",final_keyword)  