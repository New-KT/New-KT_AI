from extract import *
from crawling_main import *
keywords_list=['교육플랫폼','기부플랫폼', '지능적 에너지 관리', '친환경 교통', '사회적 기부 활동', '스마트 도시 개발']
def keyword(output_file_path,keywords_list): 
    load_dotenv()
    file_path = read_concatenate_news(output_file_path)
    result = extract_keywords_from_meeting(file_path,keywords_list)
    
    # 문자열 변수에 결과 추가
    result_string = f"{result}"
    
    # 파일에 추가하는 대신에 문자열 출력
    # print("키워드를 문자열에 추가했습니다.")
    # print("추가된 키워드:", result_string)

    
    lines = result_string.strip().split('\n')

    for line in lines:
        words = line.split('. ')
        if len(words) > 1:
            keyword = words[1]
            keywords_list.append(keyword)

    # 결과 출력
    print(result)
    print(keywords_list)
    
    
if __name__ == "__main__":
    # Load environment variables from a .env file
    keyword("meeting.txt",keywords_list)  
    # for word in keywords_list[-3:]:
    #     news=crawl(word)