import os
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd

def summary_meeting(file_path):
    # Set up OpenAI client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Define system and user messages
    GPT_MODEL = "gpt-3.5-turbo"
    messages = [
        {"role": "system", "content": "You are the best summarizer for meetings. Summarize the entire content of the meeting efficiently."},
        {"role": "user", "content": f"회의 전체 내용 텍스트파일이야. 회의 내용을 요약해줘. 회의 제목, 주요 이슈 및 진행상황, 새로운 상황 및 공지사항, 추가 안건 등 회의록 작성해줘 . {file_path}"}
    ]

    # Make API request using the content from the text file
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0
    )

    # Extract and return the generated response
    response_message = response.choices[0].message.content
    return response_message

def read_concatenate_news(file_path):
    news = pd.read_csv(file_path, delimiter='\t', header=None, names=['text'])
    concatenated_text = news['text'].str.cat(sep=' ')
    return concatenated_text

def mts(output_file_path): 
    load_dotenv()
    file_path= read_concatenate_news(output_file_path)
    # Call the function and print the result
    result = summary_meeting(file_path)
    
    with open('result.txt', 'w', encoding='utf-8') as result_file:
        result_file.write(result)
    

    
if __name__ == "__main__":
    # Load environment variables from a .env file
    mts()

