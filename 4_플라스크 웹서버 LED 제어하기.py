from flask import Flask        # 웹 서버 구축을 위한 플라스크 모듈 가져오기
from gpiozero import LED       # 라즈베리파이 GPIO 핀을 쉽게 제어하기 위한 라이브러리

app = Flask(__name__)          # Flask 앱 인스턴스 생성 (현재 파일을 메인으로 설정)

red_led = LED(21)              # GPIO 21번 핀에 연결된 LED 객체 생성

@app.route('/')                # 사용자가 기본 주소(/) 접속했을 때 실행                  
def home():
    return render_template("index.html") # templates 폴더에 있는 index.html 파일을 읽어서 사용자 화면에 띄워줌        

@app.route('/data', methods = ['POST']) # 사용자가 버튼을 눌러서 /data 주소로 데이터를 보냈을 때(POST 방식) 실행         
def data():
    data = request.form['led'] # HTML의 폼(Form)에서 'led' 값(on 또는 off)을 가져옴                  
    
    if(data == 'on'):         # 받아온 값이 'on'이면
        red_led.on()          # 21번 핀에 연결된 LED를 켬
        
    elif(data == 'off'):      # 받아온 값이 'off'이면
        red_led.off()         # LED를 끔
        
    return home()  # 처리가 끝난 후 다시 메인 페이지(홈)를 보여줘서 화면 유지                             

# 이 파일이 직접 실행될 때만 서버를 가동함
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = "80") # 모든 접속(0.0.0.0)을 허용하고, HTTP 기본 포트인 80번으로 서버 시작