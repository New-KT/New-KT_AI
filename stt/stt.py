from stt_save_file import * 

def stt():
    language_code = 'ko-KR'
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    # 파일을 열어서 쓰기 모드로 설정합니다.
    output_file_path = "output.txt"
    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        with MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (speech.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = client.streaming_recognize(streaming_config, requests)

            # 음성을 실시간으로 출력하고 파일에 추가합니다.
            listen_print_loop(responses, output_file)

if __name__ == '__main__':
    stt()
# [END speech_transcribe_streaming_mic]


