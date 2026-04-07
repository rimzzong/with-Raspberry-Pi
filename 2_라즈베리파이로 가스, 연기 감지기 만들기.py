from gpiozero import DigitalInputDevice  # 가스 센서 불러오기
from gpiozero import OutputDevice        # 부저 불러오기
import time                              # 시간 조절용

bz  = OutputDevice(18)                   # 부저 18번 핀에 연결
gas = DigitalInputDevice(17)             # 가스 센서 17번 핀에 연결

try:                                     
    while True:                          # 계속 반복 실행
        if gas.value == 0:               # 센서에 가스가 잡히면 (0일 때가 감지임)
            print("가스 감지됨")          # 화면에 글자 띄우고
            bz.on()                      # 부저 울리기
        else:                            # 평소에는 (가스 없으면)
            print("정상")                # "정상"이라고 출력하고
            bz.off()                     # 부저 끄기

        time.sleep(0.2)                  # 0.2초마다 한 번씩 확인

except KeyboardInterrupt:                # Ctrl+C 눌러서 끌 때
    pass                                 # 그냥 종료

bz.off()                                 # 프로그램 꺼져도 부저 안 울리게 최종 정리