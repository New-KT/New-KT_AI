import os
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd


def extract_keywords_from_meeting(file_path,keywords_list):
    # Set up OpenAI client
    load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Define system and user messages
    GPT_MODEL = "gpt-3.5-turbo"
    messages = [
        {"role": "system", "content": "You are the best keyword extractor. You need to extract keywords from the meeting content. All responses should be in Korean."},
        {"role": "user", "content": f"아래는 회의 내용 텍스트파일이야. {file_path} 위 텍스트에서 list= {keywords_list} list 내의 단어는 제외한 텍스트를 이용하여, 키워드 2개 추출해. 다른 사담없이 오직 키워드 두개만! 번호 매겨줘 "}
    ]

    # Make API request using the content from the text file
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0.3
    )

    # Extract and return the generated response
    response_message = response.choices[0].message.content
    return response_message

def read_concatenate_news(file_path):
    news = pd.read_csv(file_path, delimiter='\t', header=None, names=['text'])
    concatenated_text = news['text'].str.cat(sep=' ')
    return concatenated_text
