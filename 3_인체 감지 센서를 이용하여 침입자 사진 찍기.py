from gpiozero import MotionSensor        # gpiozero 라이브러리에서 MotionSensor 클래스를 가져옴
import time                              # 실행 간격(딜레이) 조절을 위해  time 라이브러리를 가져
from picamera2 import Picamera2          # picamera2 라이브러리에서 Picamera2 클래스를 가져옴
import datetime                          # 날짜/시간 처리를 위한 datetime 라이브러리를 가져옴(사진 파일명에 촬영 시간을 넣기 위해)

pirPin = MotionSensor(16)                # GPIO 16번 핀을 PIR 모션 센서 입력 핀으로 초기화

# 카메라를 쓰기 위한 기본 설정 과정
picam2 = Picamera2()                                   # Picamera2 객체생성
camera_config = picam2.create_preview_configuration()  # 카메라 미리보기 설정값 생성
picam2.configure(camera_config)                        # 생성된 설정을 카메라에 적용
picam2.start()                                         # 카메라 구동 시작

try:
    while True:                                        # 종료하기 전까지 계속 감시하기 위해 무한 루프 가동
        try:
            sensorValue = pirPin.value                 # 센서가 감지한 현재 상태(0 또는 1)를 변수에 저장
            
            if sensorValue == 1:                       # 센서값이 1이면 움직임이 감지된 것으로 판단
                now = datetime.datetime.now()          # 감지된 순간의 시각 정보 취득
                print(now)                             # 확인을 위해 터미널 창에 실시간 시각 출력
                
                # 시각을 '연-월-일 시:분:초' 모양의 파일명 형식 문자열로 변환
                fileName = now.strftime('%y-%m-%d %H:%M:%S')
                
                # 생성한 파일명에 .jpg를 붙여서 사진 촬영 후 저장
                picam2.capture_file(fileName + '.jpg')
                
                # 0.5초대기(연속촬영방지)
                time.sleep(0.5)
                
        except:                                        # 촬영 중 오류 발생 시 무시하고 계속 진행
            pass

except KeyboardInterrupt:                              # #Ctrl + C 입력 시 루프를 종료
    pass