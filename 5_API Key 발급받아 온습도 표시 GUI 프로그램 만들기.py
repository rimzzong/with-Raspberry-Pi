import urllib.request  # 웹에 데이터를 요청하기 위해 사용하는 라이브러리
import json            # 서버에서 받은 텍스트(JSON)를 파이썬에서 쓰기 좋게 변환하는 라이브러리
import tkinter         # 파이썬으로 윈도우 창(GUI)을 만들기 위한 기본 라이브러리
import tkinter.font    # 글자 크기나 폰트 설정을 세밀하게 하기 위해 가져옴

# OpenWeatherMap 사이트에서 발급받은 고유 키
API_KEY = "b442e1518dfd8f21a11fdd798e416a7f"

def tick1Min():
    # 날씨 데이터 요청할 주소 (서울 지역, 섭씨 온도 단위 설정)
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"
    
    # 웹 브라우저처럼 해당 URL에 접속해서 응답을 받아옴
    with urllib.request.urlopen(url) as r:
        # 받아온 복잡한 텍스트 데이터를 파이썬 '딕셔너리' 형태로 변환 (파싱)
        data = json.loads(r.read())
    
    # 데이터 중에서 'main' 안에 들어있는 'temp'(온도) 값을 가져옴
    temp = data["main"]["temp"]
    # 데이터 중에서 'main' 안에 들어있는 'humidity'(습도) 값을 가져옴
    humi = data["main"]["humidity"]
    
    # 가져온 온도와 습도를 화면에 보일 라벨에 업데이트 (온도는 소수점 첫째자리까지 표시)
    label.config(text=f"{temp:.1f}C   {humi}%")
    
    # 10초 후에 다시 이 함수(tick1Min)를 실행하도록 예약 (실시간 업데이트)
    window.after(10000, tick1Min)

# 메인 창 생성 및 설정
window = tkinter.Tk()
window.title("TEMP HUMI DISPLAY")  # 창 제목 설정
window.geometry("400x100")         # 창 크기 설정 (가로 400, 세로 100)
window.resizable(False, False)     # 사용자가 창 크기를 조절하지 못하게 고정

# 화면에 보여줄 글자 모양과 크기 설정
font = tkinter.font.Font(size=30)
# 데이터를 표시할 빈 라벨 생성
label = tkinter.Label(window, text="", font=font)
label.pack()  # 생성한 라벨을 창에 배치

# 프로그램 시작 시 날씨 함수를 처음으로 호출
tick1Min()

# 창이 닫히지 않고 계속 유지되도록 실행 (이벤트 루프)
window.mainloop()