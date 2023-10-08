from flask import Flask, render_template, Response, request
from camera import Camera
from detectors.apriltagDetection import ApriltagDetector3D
import json
apriltag3Detecting = True
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/button')
def button():
    return "baller"

def gen():
    with open("pageData.json", "r") as pageData:
        data = json.loads(pageData.read())
        camIndex = data["currentCamera"]
    print(camIndex)
    cap = Camera(camIndex)
    cap.getCalibrationInfo()
    
    apriltag3 = ApriltagDetector3D(camParams=cap.params)
    
    while True:
        frame = cap.getLatestFrame()
        labeledFrame = frame
        
        if apriltag3Detecting:
            labeledFrame = apriltag3.update(labeledFrame, frame)
        
        labeledFrame = cap.convertFrameToBytes(labeledFrame)
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + labeledFrame + b'\r\n\r\n')
        
    cap.cameraStream.release()
    
@app.route('/pageData.json', methods = ['GET', 'POST', 'DELETE'])
def getPageData():
    if request.method == 'GET':
        return open("pageData.json", "r")
    if request.method == "POST":
        data = request.json
        settings = open("pageData.json", "w")
        settings.write(data)
        settings.close()
        return "good"

@app.route('/settings.json', methods = ['GET', 'POST', 'DELETE'])
def getSettings():
    if request.method == 'GET':
        return open("settings.json", "r")
    if request.method == "POST":
        data = request.json
        settings = open("settings.json", "w")
        settings.write(data)
        settings.close()
        return "good"

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/pipelineSettings.json')
def pipelineSettingsTemplate():
    html = open('templates/settings/pipelineSettings.html', 'r')
    return json.dumps({"data": html.read()})
    
@app.route('/settings.html')
def settingsTemplate():
    return {"data": open('templates/settings/settings.html', 'r')}
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)