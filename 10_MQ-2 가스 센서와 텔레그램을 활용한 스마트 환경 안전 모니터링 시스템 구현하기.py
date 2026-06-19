import time                             # 시간 지연(sleep) 기능을 사용하기 위한 모듈
from gpiozero import DigitalInputDevice, OutputDevice  # 라즈베리파이 GPIO 핀 제어(센서 입력, 부저 출력)를 위한 모듈
import urllib.request                   # 텔레그램 API 서버로 HTTP 요청을 보내기 위한 모듈
import json                             # 텔레그램으로 보낼 데이터를 JSON 형식으로 변환하기 위한 모듈

# 텔레그램 봇 API, 사용자 ID 설정
TELEGRAM_ID = '8197209442' 
MY_TOKEN = '8686881281:AAFvh5mzWu9YZn89cmRrahigGdkvaggy1LQ'

# 부저(Output)와 가스 센서(Input)의 GPIO 핀 번호 지정
bz = OutputDevice(18)       # 부저는 18번 핀에 연결
gas = DigitalInputDevice(17) # 가스 센서는 17번 핀에 연결

# 가스 감지 시 텔레그램으로 경고 메시지를 보내는 함수
def send_telegram_message():
    # 텔레그램 봇 API 호출을 위한 URL 생성
    url = f"https://api.telegram.org/bot{MY_TOKEN}/sendMessage"
    
    # 텔레그램으로 보낼 메시지 내용 (JSON 형식으로 전송 예정)
    payload = {
        "chat_id": TELEGRAM_ID,
        "text": "[비상 경보] 가스 및 유독 연기 누출 감지. 즉시 확인 바랍니다."
    }
    
    try:
        # 딕셔너리 데이터를 JSON 문자열로 변환하고 바이트로 인코딩
        data = json.dumps(payload).encode('utf-8')
        
        # HTTP POST 요청 생성 및 헤더 설정
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        # 네트워크 지연을 고려해 타임아웃(1.5초)을 두고 메시지 전송
        with urllib.request.urlopen(req, timeout=1.5) as response:
            pass
        print("-> 텔레그램 경보 메시지 전송 완료")
        
    except Exception as e:
        # 네트워크 오류나 토큰 에러 등으로 전송 실패 시 예외 처리
        print(f"-> 텔레그램 전송 실패: {e}")

# [메인 루프] 센서 상태를 실시간으로 모니터링하는 반복문
try:
    while True:
        # 기본적으로 현재 센서의 상태값(0 또는 1)을 터미널에 계속 출력
        print(f"상태: 안전(현재 센서 감지 상태값: {gas.value})")
        
        # 가스 센서의 값이 0일 때 (보통 DO(Digital Output) 핀은 감지 시 LOW(0)가 됨)
        if gas.value == 0:
            print("[위험] 가스 및 유독 연기 감지됨")
            bz.on()                  # 1. 경보용 부저 켜기
            send_telegram_message()  # 2. 사용자에게 텔레그램 알림 전송
        else:
            # 가스가 감지되지 않는 정상 상태라면 부저를 끔
            bz.off()
        
        # 센서 과부하 방지 및 안정적인 측정을 위해 2초 간격으로 반복 실행
        time.sleep(2.0)

except KeyboardInterrupt:
    # 사용자가 Ctrl+C를 눌러 프로그램을 강제 종료했을 때 처리
    pass

finally:
    # 프로그램이 종료될 때 부저가 켜진 상태로 멈추지 않도록 안전하게 끄기
    bz.off()