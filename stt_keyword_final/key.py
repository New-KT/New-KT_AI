from extract import *

def keyword(output_file_path): 
    load_dotenv()
    file_path= read_concatenate_news(output_file_path)
    result = extract_keywords_from_meeting(file_path)
    with open("keyword_log.txt", 'a', encoding='utf-8') as keyword_log_file:
        keyword_log_file.write(result + '\n')
        print("키워드를 파일에 추가했습니다.")
        print("추가된 키워드:", result)
    
    
if __name__ == "__main__":
    # Load environment variables from a .env file
    keyword()

 