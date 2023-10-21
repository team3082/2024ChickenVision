from flask import Flask, render_template, Response, request
from camera import Camera
import camera
from detectors.apriltagDetection import ApriltagDetector3D, ApriltagDetector2D
from detectors.gamePieceDetection import ConeDetector, CubeDetector
from detectors.gamePieceDetectionML import GamePieceDetectionML
from apriltag import DetectorOptions
import json
import cv2
import numpy as np
import threading
import os
from queue import Queue

queue = Queue()

def start():
    app.run(host='0.0.0.0', debug=False, port=8000)
    
def runCameras():
    availableCams = camera.getAvailableCameraIndexes()
    print(availableCams)
    # availableCams = [0, 2]
    cams = []
    # print(availableCams)
    for cam in availableCams:
        cams.append([cam, Camera(cam)])
    
    print(cams)        

    apriltag2Detector = ApriltagDetector2D()
    apriltag3Detector = ApriltagDetector3D()
    cubeDetector = CubeDetector()
    coneDetector = ConeDetector()
    objDetector = GamePieceDetectionML()
    while True:
        # print("yo")
        pageDataJSON = open("pageData.json", "r")
        currentViewedCam = int(json.loads(pageDataJSON.read())["currentCamera"])
        pageDataJSON.close()
        
        cameraSettingsJSON = open("settings.json", "r")
        cameraSettings = json.loads(cameraSettingsJSON.read())
        cameraSettingsJSON.close()
                
        for cam in cams:
            try:
                # print(-1)
                # print(cam)
                cam[1].getCalibrationInfo()
                apriltag3Detector.setCamParams(cam[1].params)
                frame = cam[1].getLatestFrame()
                labeledFrame = frame
                cameraSettingsDict = cameraSettings["cam" + str(cam[0])]
                # print(0)
                if cameraSettingsDict["pipelineSettings"]["toggles"][0]:
                    optionsDict = cameraSettingsDict["pipelineSettings"]["apriltag2D"]
                    options = DetectorOptions(
                        families="tag16h5",
                        nthreads=int(optionsDict["nthreads"]),
                        quad_decimate=optionsDict["quadDecimate"],
                        quad_blur=optionsDict["quadBlur"],
                        refine_edges=optionsDict["refineEdges"],
                        refine_decode=optionsDict["refineDecode"],
                        refine_pose=optionsDict["refinePose"],
                        quad_contours=optionsDict["quadContours"]
                        )
                    apriltag2Detector.updateOptions(options)
                    apriltag2Detector.updateDecisionMargin(float(optionsDict["decisionMargin"]))
                    labeledFrame = apriltag2Detector.update(labeledFrame, frame)
                # print(1)
                if cameraSettingsDict["pipelineSettings"]["toggles"][1]:
                    optionsDict = cameraSettingsDict["pipelineSettings"]["apriltag3D"]
                    options = DetectorOptions(
                        families="tag16h5",
                        nthreads=int(optionsDict["nthreads"]),
                        quad_decimate=optionsDict["quadDecimate"],
                        quad_blur=optionsDict["quadBlur"],
                        refine_edges=optionsDict["refineEdges"],
                        refine_decode=optionsDict["refineDecode"],
                        refine_pose=optionsDict["refinePose"],
                        quad_contours=optionsDict["quadContours"]
                        )
                    apriltag3Detector.updateOptions(options)
                    apriltag3Detector.updateDecisionMargin(float(optionsDict["decisionMargin"]))
                    labeledFrame = apriltag3Detector.update(labeledFrame, frame)
                # print(2)
                if cameraSettingsDict["pipelineSettings"]["toggles"][2]:
                    optionsDict = cameraSettingsDict["pipelineSettings"]["gamePieceGeo"]
                    # print(0)
                    lowerYellow = np.array([int(optionsDict["lowerYellow"][0]), int(optionsDict["lowerYellow"][1]), int(optionsDict["lowerYellow"][2])])
                    upperYellow = np.array([int(optionsDict["upperYellow"][0]), int(optionsDict["upperYellow"][1]), int(optionsDict["upperYellow"][2])])
                    coneDetector.updateYellow(lowerYellow, upperYellow)
                    coneDetector.updateArbituaryValue(float(optionsDict["arbituaryValueCone"]) / 100)
                    # labeledFrame = cam["gamePieceGeoCube"].update(labeledFrame, frame)
                    # print(1)
                    lowerPurple = np.array([int(optionsDict["lowerPurple"][0]), int(optionsDict["lowerPurple"][1]), int(optionsDict["lowerPurple"][2])])
                    upperPurple = np.array([int(optionsDict["upperPurple"][0]), int(optionsDict["upperPurple"][1]), int(optionsDict["upperPurple"][2])])
                    cubeDetector.updatePurple(lowerPurple, upperPurple)
                    cubeDetector.updateArbituaryValue(float(optionsDict["arbituaryValueCube"]) / 100)
                    # labeledFrame = cam["gamePieceGeoCube"].update(labeledFrame, frame)
                    # print(cam["gamePieceGeoCube"])
                    labeledFrame = cubeDetector.update(labeledFrame, frame)
                    labeledFrame = coneDetector.update(labeledFrame, frame)
                    # print(2)
                # print(3)
                if cameraSettingsDict["pipelineSettings"]["toggles"][3]:
                    objDetector.detectInFrame(labeledFrame)
                # cam["cameraStream"].renderCameraStream(labeledFrame)
                # print(4)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # print(5)
                # print(cam)
                if cam[0] == currentViewedCam:
                    frameBytes = cam[1].convertFrameToBytes(labeledFrame)
                    cam[1].renderCameraStream(labeledFrame)
                    # print("bro")
                    queue.put(frameBytes)
                    # print(frameBytes)

            except:
                break

thread1 = threading.Thread(target=runCameras)

thread1.start()

app = Flask(__name__)
app.config['SERVER_NAME'] = 'chickenvision:8000'

# render main page template
@app.route('/')
def index():
    return render_template('index.html')
# render mjpeg camera stream

def getBytes():
    while True:
        try:
            frameBytes = queue.get()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frameBytes + b'\r\n\r\n')
        except KeyboardInterrupt:
            break
                
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
    data = json.dumps({"data": camera.getAvailableCameraIndexes()})
    print(data)
    return data
@app.route('/video_feed')
def video_feed():
    return Response(getBytes(),
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

start()

# if __name__ == '__main__':
#     threading.Thread(target=start, daemon=True).start()
#     threading.Thread(target=runCameras, daemon=True).start()
#     while(True):
#         pass