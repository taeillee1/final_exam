from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False)  
GPIO.setmode(GPIO.BCM)

led_pin=4

GPIO.setup(led_pin, GPIO.OUT)

GPIO.setup(18, GPIO.OUT)

p=GPIO.PWM(18,50)

#센서에 연결한 Trig와 Echo 핀의 핀 번호 설정 
TRIG = 23
ECHO = 24
print("Distance measurement in progress")

p.start(0)

#Trig와 Echo 핀의 출력/입력 설정 
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

#Trig핀의 신호를 0으로 출력 
GPIO.output(TRIG, False)
print("Waiting for sensor to settle")
time.sleep(2)

lock=threading.Lock()     

stans = False
GPIO.setup(led_pin, GPIO.OUT)

def musicstart():
    global stans
    global Frq
    global p
    try:
        lock.acquire()
        lock.release()
                   
        return "ok"
    except :
        return "fail"

     


app = Flask(__name__)

@app.route("/")
def home():
    
    return render_template('index.html')

@app.route("/led/on")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def led_on():
    global distance
    try: 			     
            GPIO.output(TRIG, True)   # Triger 핀에  펄스신호를 만들기 위해 1 출력
            time.sleep(0.00001)       # 10µs 딜레이 
            GPIO.output(TRIG, False)
            
            while GPIO.input(ECHO)==0:
                start = time.time()	 # Echo 핀 상승 시간 
                
            while GPIO.input(ECHO)==1:
                stop = time.time()	 # Echo 핀 하강 시간 
                
            check_time = stop-start
            distance = check_time * 34300 / 2
            if distance<30 :
                GPIO.output(led_pin,1)
                return str(distance)
                
            else :
                GPIO.output(led_pin,0)
                p.stop()
                return str(distance)      

                    
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

@app.route("/led/holy")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def led_holy():
    try:
        GPIO.output(led_pin,0)         # 불을 켜고
        return "ok"                         # 함수가 'ok'문자열을 반환함
    except :
        return "fail"

        
    


if __name__ == "__main__":
    app.run(host="0.0.0.0")