from gpiozero import LED
from time import sleep #시간 지연 기능을 위한 라이브러리

carLedRed = 2 #차량용 빨강
carLedBlue = 3 #차량용 파랑(노랑)
carLedGreen = 4 #차량용 초록
humanLedRed = 20 #보행자용 빨강
humanLedGreen = 21 #보행자용 초록

carLedRed = LED(2)
carLedBlue = LED(3)
carLedGreen = LED(4)
humanLedRed = LED(20)
humanLedGreen = LED(21)

try:
    while 1:
        #차량 초록(ON), 보행자 빨강(ON)
        carLedRed.value = 0
        carLedBlue.value = 0
        carLedGreen.value = 1
        humanLedRed.value = 1
        humanLedGreen.value = 0
        sleep(3.0) #3초 대기
        #차량 파랑(노랑)(ON), 보행자 빨강 유지(ON)
        carLedRed.value = 0
        carLedBlue.value = 1
        carLedGreen.value = 0
        humanLedRed.value = 1
        humanLedGreen.value = 0
        sleep(1.0) #1초 대기
        #차량 빨강(ON), 보행자 초록(ON)
        carLedRed.value = 1
        carLedBlue.value = 0
        carLedGreen.value = 0
        humanLedRed.value = 0
        humanLedGreen.value = 1
        sleep(3.0) #3초 대기
   
except KeyboardInterrupt:
    pass #Ctrl + C 입력 시 루프를 종료하고 아래 코드로 이동

#프로그램 종료 시 모든 LED OFF
carLedRed.value = 0
carLedBlue.value = 0
carLedGreen.value = 0
humanLedRed.value = 0
humanLedGreen.value = 0