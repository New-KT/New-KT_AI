from extract import *

def keyword(): 
    load_dotenv()
    file_path = r"keyword_extract\meeting.txt"
    file_path= read_concatenate_news(file_path)
    # Call the function and print the result
    result = extract_keywords_from_meeting(file_path)
    print(result)
    
    
if __name__ == "__main__":
    # Load environment variables from a .env file
    keyword()

