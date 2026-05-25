import cv2  # OpenCV 라이브러리 불러오기
from gpiozero import Buzzer  #  GPIO 부저 제어 클래스 불러오기
import time  # 시간 관련 라이브러리 불러오기


buzzerPin = Buzzer(16) # GPIO 16번 핀에 부저 객체 생성


def main():
    # 0번 내장/외장 USB 웹캠 장치 활성화
    camera = cv2.VideoCapture(0)
    camera.set(3, 640)  # 카메라 영상의 가로 해상도를 640 픽셀로 설정
    camera.set(4, 480)  # 카메라 영상의 세로 해상도를 480 픽셀로 설정

    # OpenCV에서 제공하는 Haar Cascade 사전 학습된 XML 파일 경로 설정 (얼굴 및 안구 탐색용)
    face_xml = cv2.data.haarcascades + "haarcascade_frontalface_default.xml" # 얼굴 탐지 모델 경로
    eye_xml = cv2.data.haarcascades + "haarcascade_eye.xml" # 눈 탐지 모델 경로

    # 설정한 XML 파일 경로를 바탕으로 각각의 객체 탐지 분류기(Classifier) 생성
    face_cascade = cv2.CascadeClassifier(face_xml)  #얼굴 탐지 분류기 생성
    eye_cascade = cv2.CascadeClassifier(eye_xml)  #눈 탐지 분류기 생성

    # 웹캠 카메라가 정상적으로 열려 있는 동안 반복 실행 (무한 루프 제어)
    while camera.isOpened():
        # 웹캠으로부터 실시간 영상의 한 프레임을 읽어옴 (image에 프레임 저장)
        _, image = camera.read()

        # 연산 속도 향상 및 명암 차이 분석을 위해 컬러 프레임을 흑백(Grayscale) 이미지로 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 흑백 이미지 내에서 사전 설정한 조건에 맞춰 얼굴 영역을 1차로 탐색
        faces = face_cascade.detectMultiScale(gray, # 흑백 이미지에서 얼굴 탐지
                                              scaleFactor=1.1, # 탐지 윈도우 10%씩 확대
                                              minNeighbors=5, # 최소 5회 탐지 시 얼굴 확정
                                              minSize=(100, 100), # 탐지 최소 크기 100×100
                                              flags=cv2.CASCADE_SCALE_IMAGE) # 이미지 스케일링 방식 탐지

        # 터미널 창에 실시간으로 검출된 얼굴의 개수를 출력하여 디버깅 확인
        print("faces detected Number: " + str(len(faces)))

        # 화면 내에 검출된 얼굴이 최소 1개 이상 존재할 경우 진입
        if len(faces):
            # 탐지된 모든 얼굴 사각형 영역의 좌표(x, y)와 크기(w: 너비, h: 높이)를 순회
            for x, y, w, h in faces:
                # 원본 컬러 영상에 검출된 얼굴 영역을 파란색(255, 0, 0) 사각형으로 시각화 표시
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # 연산 효율성을 위해전체 화면이 아닌 '검출된 얼굴 영역 내부'만 관심영역(ROI)으로 지정
                face_gray = gray[y : y + h, x : x + w]  # 얼굴 영역 흑백 이미지 추출
                face_color = image[y : y + h, x : x + w]  # 얼굴 영역 컬러 이미지 추출

                # 추출한 얼굴 내부(흑백 관심영역)에서 안구(눈) 영역을 2차로 탐색
                eyes = eye_cascade.detectMultiScale(face_gray, # 얼굴 영역에서 눈 탐지
                                                    scaleFactor=1.1, # 탐지 윈도우 10%씩 확대
                                                    minNeighbors=5) # 최소 5회 탐지 시 눈 확정

                # 졸음 판단 조건문: 실시간으로 탐지된 눈의 개수가 1개 이하일 때 (졸음 상태)
                if len(eyes) <= 1: 
                    buzzerPin.on() # 눈 1개 이하 → 부저 켜기
                else:
                    buzzerPin.off()  # 눈 2개 이상 → 부저 끄기

                # 얼굴 관심영역 내에서 탐지된 눈 영역의 좌표와 크기를 순회
                for ex, ey, ew, eh in eyes:
                    # 얼굴 컬러 ROI 화면 내에 검출된 눈 영역을 초록색(0, 255, 0) 사각형으로 표시
                    cv2.rectangle(face_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        cv2.imshow("result", image) # 결과 이미지 GUI 창 출력

        # 프레임 간 1ms의 대기 시간을 가지며, 사용자가 키보드로 'q' 키를 누르면 루프 탈출
        if cv2.waitKey(1) == ord("q"):
            break

    # 프로그램 종료 프로세스: 웹캠 장치 해제 및 OpenCV 관련 모든 윈도우 창 닫기
    cv2.destroyAllWindows()
    buzzerPin.off()  # 프로그램 종료 시 부저가 켜진 상태로 멈추지 않도록 부저 강제 끄기


if __name__ == "__main__": main()  # 직접 실행 시 main() 호출