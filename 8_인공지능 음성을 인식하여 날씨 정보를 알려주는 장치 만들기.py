import speech_recognition as sr  # 구글 음성 인식(STT) 사용을 위한 라이브러리 임포트
import requests                  # OpenWeatherMap 날씨 API와 웹 통신하기 위한 라이브러리 임포트
import os                        # 리눅스 시스템 명령어(espeak)를 파이어썬에서 실행하기 위해 임포트
import time                      # 시간 지연이나 제어에 필요할 수 있어 미리 임포트

# OpenWeatherMap 사이트에서 발급받은 고유 키
API_KEY = "b442e1518dfd8f21a11fdd798e416a7f"
# 날씨 데이터 요청할 주소 (서울 지역, 섭씨 온도 단위 설정)
url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"

# espeak TTS 엔진을 호출하여 라즈베리파이 스피커로 음성을 출력하는 사용자 정의 함수
def speak(option, msg):
    # os.system을 통해 리눅스 터미널에 espeak 옵션과 메시지를 문자열 포맷팅으로 전달하여 실행
    os.system("espeak {} '{}'".format(option, msg))

try:
    while True: # 사용자가 강제 종료할 때까지 상시 음성 인식을 위해 무한 루프 가동
        r = sr.Recognizer() # 음성 인식을 수행하는 고유 객체 생성
        
        # 라즈베리파이에 연결된 USB 마이크(장치 인덱스 1번)를 오디오 입력 소스로 지정
        with sr.Microphone(device_index=1) as source:
            print("Say something!") # 발화 타이밍을 알리기 위한 터미널 안내문 출력
            audio = r.listen(source) # 마이크로 소리가 들어올 때까지 대기(블로킹)했다가 오디오 데이터로 캡처
            
        try:
            # 구글 클라우드 STT 서버로 오디오를 전송하여 한국어(ko-KR) 텍스트 문자열로 변환
            text = r.recognize_google(audio, language='ko-KR')
            print("You said: " + text) # 전사된 문자열 결과를 터미널에 출력하여 확인
            
            # 구글 s.r에서 반환된 text 문자열 변수 안에 "날씨"라는 목적 키워드가 포함되어 있는지 검사
            if text in "날씨":
                print("날씨 음성을 인식하였습니다.") # 키워드 매칭 성공 로그 출력
                
                response = requests.get(url) # requests 라이브러리로 기상 서버에 HTTP GET 웹 요청 전송
                data = response.json()       # 수신된 HTTP 응답 본문을 파이썬 딕셔너리(JSON 포맷) 구조로 파싱
                
                temp = data["main"]["temp"]       # JSON 데이터의 main 계층에서 현재 기온 변수 추출
                humi = data["main"]["humidity"]   # JSON 데이터의 main 계층에서 현재 습도 변수 추출
                
                # 기온과 습도를 포함한 안내 문자 열생성
                msg = '    기온은 ' + str(int(temp)) + '도 습도는 ' + str(humi) + '퍼센트 입니다'
                
                # espeak 파라미터 세팅: 속도 180(-s), 음높이 50(-p), 볼륨 200(-a), 여성 한국어 5번 톤(-v ko+f5)
                option = '-s 180 -p 50 -a 200 -v ko+f5'
                speak(option, msg) # 설정한 음색 옵션과 가공된 안내 텍스트를 speak 함수에 넘겨 스피커 출력
            
        # 구글 API가 소리는 감지했으나 무슨 말인지 문자열로 전사하지 못했을 때의 예외 처리
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        # 네트워크 단절 등으로 인해 구글 클라우드 서비스 요청 자체가 실패했을 때의 예외 처리
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

# 터미널에서 Ctrl + C 키를 눌러 프로그램을 수동으로 안전하게 종료
except KeyboardInterrupt:
    pass # 별도의 에러 메시지 없이 루프를 빠져나와 프로그램 종료