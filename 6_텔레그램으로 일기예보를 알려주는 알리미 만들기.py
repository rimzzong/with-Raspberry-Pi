import urllib.request  # 외부 서버(날씨 API)와 통신하기 위한 라이브러리
import json            # 서버에서 받은 JSON 형식의 데이터를 파이썬에서 쓰기 좋게 변환
import datetime        # 현재 시간을 체크해서 정해진 시간에 알림을 보내기 위해 사용
import asyncio         # 비동기 프로그래밍(메시지 전송 대기 등)을 위한 라이브러리
from telegram import Bot # 텔레그램 봇 기능을 사용하기 위한 모듈

# 설정 정보 (보안 및 접속 주소)
telegram_id = '8197209442'  # 내 텔레그램 챗 ID (메시지 수신처)
my_token = '8686881281:AAFvh5mzWu9YZn89cmRrahigGdkvaggy1LQ' # BotFather에서 발급 받은 토큰
api_key = 'b442e1518dfd8f21a11fdd798e416a7f'  # OpenWeatherMap에서 발급받은 API 키

bot = Bot(token=my_token) # 텔레그램 봇 객체 생성

# 알림을 보낼 시간 설정 (3시간 단위 및 특정 시간대)
ALERT_HOURS = [7, 10, 13, 16, 19, 22]  # 3시간 간격 정각 알림 시간 목록
ALERT_TIMES = ["08:30", "19:47"]      # 추가 지정 시간 알림 목록

# 날씨 정보를 가져오는 함수 정의
def getWeather():  # 날씨 정보를 가져와 문자열로 반환하는 함수
    # 서울 지역의 3시간 단위 예보(최대 8개)를 요청하는 URL 생성
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"
    
    with urllib.request.urlopen(url) as r:  # API에 요청 보내기
        data = json.loads(r.read())  # 응답 받은 데이터를 JSON으로 변환
        
        text = "" # 결과 문자열 초기화
        for i in range(8):  # 8개의 예보 데이터를 반복문을 통해 하나씩 추출
            item = data['list'][i]  # i번째 날씨 데이터 가져오기
            hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)  # 영국 기준 시간을 한국 시간(+9시간)으로 변환하고 2자리 숫자로 유지
            temp = item['main']['temp']      # 온도 정보 추출
            humi = item['main']['humidity']  # 습도 정보 추출
            desc = item['weather'][0]['description']  # 날씨 상태 설명 추출
            text += f"({hour}h {temp}C {humi}% {desc})\n"  # 결과 문자열에 추가
            
        return text

# 메인 실행 로직 (비동기 처리)
async def main():  # 비동기 메인 함수
    try:
        while True:  # 무한 루프를 돌며 시간 감시
            now = datetime.datetime.now() # 현재 시스템 시간 가져오기
            hm = now.strftime('%H:%M')    # 현재 시:분 추출(예: "08:30") 
            
            # 조건 1: 정해진 시간(ALERT_HOURS)의 정각인지 확인
            is_alert_hour = now.hour in ALERT_HOURS and now.minute == 0 and now.second == 0
            # 조건 2: 지정된 특정 시간(ALERT_TIMES)의 0초인지 확인
            is_alert_time = hm in ALERT_TIMES and now.second == 0
            
            if is_alert_hour or is_alert_time:  # 두 조건 중 하나라도 만족하면 날씨 전송
                msg = getWeather() # API 호출하여 날씨 텍스트 생성
                print(msg)         # 터미널에 출력 (확인용)
                await bot.send_message(chat_id=telegram_id, text=msg)  # 텔레그램 서버를 통해 내 스마트폰 앱으로 메시지 전송
            
            await asyncio.sleep(1)  # CPU 부하를 줄이기 위해 1초마다 반복
            
    except KeyboardInterrupt:  # Ctrl+C 입력 시 정상 종료
        pass

asyncio.run(main())  # 비동기 메인 함수 실행