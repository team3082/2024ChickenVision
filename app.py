from flask import Flask, render_template, Response, request
from camera import Camera
import camera
from detectors.apriltagDetection import ApriltagDetector3D, ApriltagDetector2D
from detectors.gamePieceDetection import ConeDetector, CubeDetector
import json
app = Flask(__name__)
app.config['SERVER_NAME'] = 'chickenvision:8000'

# render main page template
@app.route('/')
def index():
    return render_template('index.html')

# render mjpeg camera stream
def gen():
    with open("pageData.json", "r") as pageData:
        data = json.loads(pageData.read())
        camIndex = data["currentCamera"]
    print(camIndex)
    cap = Camera(camIndex)
    cap.getCalibrationInfo()
    
    apriltag2 = ApriltagDetector2D()
    apriltag3 = ApriltagDetector3D(camParams=cap.params)
    
    cone = ConeDetector()
    cube = CubeDetector()
    
    while True:
        frame = cap.getLatestFrame()
        labeledFrame = frame
        
        settings = open("settings.json", "r")
        settingsDict = json.loads(settings.read())
        settings.close()
        
        toggles = settingsDict["cam" + str(camIndex)]["pipelineSettings"]["toggles"]
        
        if toggles[0] == True:
            labeledFrame = apriltag2.update(labeledFrame, frame)
        if toggles[1] == True:
            labeledFrame = apriltag3.update(labeledFrame, frame)
        if toggles[2] == True:
            labeledFrame = cone.update(labeledFrame, frame)
            labeledFrame = cube.update(labeledFrame, frame)
        
        labeledFrame = cap.convertFrameToBytes(labeledFrame)
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + labeledFrame + b'\r\n\r\n')
        
    cap.cameraStream.release()
    
# GET/POST JSON STORAGE
@app.route('/pageData.json', methods = ['GET', 'POST'])
def getPageData():
    if request.method == 'GET':
        return open("pageData.json", "r")
    if request.method == "POST":
        data = json.dumps(request.json, indent=3)
        settings = open("pageData.json", "w")
        settings.write(data)
        settings.close()
        return "good"

@app.route('/settings.json', methods = ['GET', 'POST'])
def getSettings():
    if request.method == 'GET':
        return open("settings.json", "r")
    if request.method == "POST":
        data = json.dumps(request.json, indent=3)
        settings = open("settings.json", "w")
        settings.write(data)
        settings.close()
        return "good"

# GET VIDEO FEED STUFF
@app.route('/available_feeds')
def available_feeds():
    data = json.dumps({"data": [camera.getAvailableCameraIndexes()]})
    return data

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
# GET HTML TEMPLATES
@app.route('/cameraSettings.json')
def cameraSettingsTemplate():
    html = open('templates/settings/cameraSettings.html', 'r')
    return json.dumps({"data": html.read()})    

@app.route('/pipelineSettings.json')
def pipelineSettingsTemplate():
    html = open('templates/settings/pipelineSettings.html', 'r')
    return json.dumps({"data": html.read()})

@app.route('/apriltag2Settings.json')
def apriltag2SettingsTemplate():
    html = open('templates/settings/pipelineSettings/apriltag2.html', 'r')
    return json.dumps({"data": html.read()})

@app.route('/apriltag3Settings.json')
def apriltag3SettingsTemplate():
    html = open('templates/settings/pipelineSettings/apriltag3.html', 'r')
    return json.dumps({"data": html.read()})

@app.route('/gamePieceGeoSettings.json')
def gamePieceGeoSettingsTemplate():
    html = open('templates/settings/pipelineSettings/gamePieceGeo.html', 'r')
    return json.dumps({"data": html.read()})

@app.route('/gamePieceMLSettings.json')
def gamePieceMLSettingsTemplate():
    html = open('templates/settings/pipelineSettings/gamePieceML.html', 'r')
    return json.dumps({"data": html.read()})

@app.route('/retroReflectiveSettings.json')
def retroReflectiveSettingsTemplate():
    html = open('templates/settings/pipelineSettings/retroReflective.html', 'r')
    return json.dumps({"data": html.read()})
    
@app.route('/settings.json')
def settingsTemplate():
    html = open('templates/settings/settings.html', 'r')
    return json.dumps({"data": html.read()})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)