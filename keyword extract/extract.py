import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Read content from a text file
file_path = '/content/drive/MyDrive/meeting.txt'  # Update with the actual path to your text file
with open(file_path, 'r', encoding='utf-8') as file:
    news_content = file.read()

# Set up OpenAI client
client = OpenAI(api_key="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")

# Define system and user messages
GPT_MODEL = "gpt-3.5-turbo"
messages = [
    {"role": "system", "content": "You are the best keyword extractor. You need to extract keywords from the meeting content. All responses should be in Korean."},
    {"role": "user", "content": f"회의 내용 텍스트파일이야. 너가 생각하기에 텍스트에서 주제라고 생각되는 키워드 3개만 추출해줘. 다른 사담없이 오직 키워드만. {meeting_content}"}
]

# Make API request using the content from the text file
response = client.chat.completions.create(
    model=GPT_MODEL,
    messages=messages,
    temperature=0
)

# Extract and print the generated response
response_message = response.choices[0].message.content
print(response_message)