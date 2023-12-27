from stt_keyword.keyword import keyword
from stt_save_file import * 

import time
def main():
    while True:
        # stt 함수를 호출하여 1분 동안 음성을 인식하고 파일에 저장
        stt()

        # 1분 간격으로 파일의 내용을 keyword 함수에 전달
        time.sleep(60)
        with open("output.txt", 'r', encoding='utf-8') as file:
            file_contents = file.read()
            keyword(file_contents)

if __name__ == '__main__':
    main()