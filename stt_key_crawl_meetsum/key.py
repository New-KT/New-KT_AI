from extract import *
from crawling_main import *
keywords_list=[]
def keyword(output_file_path): 
    load_dotenv()
    file_path = read_concatenate_news(output_file_path)
    result = extract_keywords_from_meeting(file_path)
    
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
    print(keywords_list)
    
    
if __name__ == "__main__":
    # Load environment variables from a .env file
    keyword("output.txt")  
    
# for word in keywords_list[-3:]:
#     crawl(word)