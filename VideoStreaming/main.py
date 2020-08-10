# main.py
# import the necessary packages
from flask import Flask, render_template, Response
from camera import VideoCamera
import requests,json
app = Flask(__name__)

global captureStatus
global trackStatus

@app.route('/')
def index():
    response = json.loads(requests.get("7688網址:5000/api/status").text)
    initPos = str(6-int(response['pos']))
    # rendering webpage
    return render_template('index.html', barSty="width:"+str(20*int(initPos))+"%",pos=initPos)

def gen(camera):
    global captureStatus
    global trackStatus
    while(1):
        frame = camera.get_frame(trackStatus)
        if(frame != None and captureStatus): #wait the frame
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
            yield frame
            yield b'\r\n\r\n'

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

    
# @app.route('/video_feed')
# def video_feed():
#     return ""#Response(gen(VideoCamera()),
#                     #mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/conf_openCam')
def openCam():
    print("開啟鏡頭")
    global captureStatus
    captureStatus = True
    return "Done"

@app.route('/conf_closeCam')
def closeCam():
    print("關閉鏡頭")
    global captureStatus
    captureStatus = False
    return "Done"

@app.route('/conf_openTrack')
def openTrack():
    print("開啟追蹤")
    global trackStatus
    trackStatus = True
    return "Done"

@app.route('/conf_closeTrack')
def closeTrack():
    print("關閉追蹤")
    global trackStatus
    trackStatus = False
    return "Done"

if __name__ == '__main__':
    # defining server ip address and port
    global captureStatus
    global trackStatus
    trackStatus = False
    captureStatus = True
    app.debug = True
    app.run(
        host = "127.0.0.1",
        port = 5000,
        threaded=True
    )