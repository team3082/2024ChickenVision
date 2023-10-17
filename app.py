from flask import Flask, render_template, Response, request
from camera import Camera
import camera as cameraClass
from detectors.apriltagDetection import ApriltagDetector3D, ApriltagDetector2D
from detectors.gamePieceDetection import ConeDetector, CubeDetector
from apriltag import DetectorOptions
import json
import cv2
import numpy as np
app = Flask(__name__)
app.config['SERVER_NAME'] = 'chickenvision.local:8000'

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

def runCameras():
    # availableCams = cameraClass.getAvailableCameraIndexes()
    availableCams = [0]
    cams = []
    # print(availableCams)
    for cam in availableCams:
        # print(cam)
        cams.append({
            "camIndex": cam,
            "cameraStream": Camera(cam),
            "apriltag2D": ApriltagDetector2D(),
            "apriltag3D": ApriltagDetector3D(),
            "gamePieceGeoCube": CubeDetector(),
            "gamePieceGeoCone": ConeDetector()
        })
        cubeDetector = CubeDetector()
        coneDetector = ConeDetector()
        objDetector = GamePieceDetectionML()
    while True:
        currentViewedCamJSON = open("pageData.json", "r")
        currentViewedCam = json.loads(currentViewedCamJSON.read())["currentCamera"]
        currentViewedCamJSON.close()
        for cam in cams:
            try:
                cam["cameraStream"].getCalibrationInfo()
                cam["apriltag3D"].setCamParams(cam["cameraStream"].params)

                frame = cam["cameraStream"].getLatestFrame()
                labeledFrame = frame

                cameraSettingsJSON = open("settings.json", "r")
                cameraSettings = json.loads(cameraSettingsJSON.read())
                # print(cameraSettings)
                cameraSettingsDict = cameraSettings["cam" + str(cam["camIndex"])]
                cameraSettingsJSON.close()
                
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
                    cam["apriltag2D"].updateOptions(options)
                    cam["apriltag2D"].updateDecisionMargin(float(optionsDict["decisionMargin"]))
                    labeledFrame = cam["apriltag2D"].update(labeledFrame, frame)
                    
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
                    cam["apriltag3D"].updateOptions(options)
                    cam["apriltag3D"].updateDecisionMargin(float(optionsDict["decisionMargin"]))
                    cam["apriltag3D"].updateFov(optionsDict["fov"])
                    labeledFrame = cam["apriltag3D"].update(labeledFrame, frame)
                    
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
                if cameraSettingsDict["pipelineSettings"]["toggles"][3]:
                    objDetector.detectInFrame(labeledFrame)
                # cam["cameraStream"].renderCameraStream(labeledFrame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                if cam["camIndex"] == currentViewedCam:
                    frameBytes = cam["cameraStream"].convertFrameToBytes(labeledFrame)
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frameBytes + b'\r\n\r\n')
            except:
                None
                
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
    return Response(runCameras(),
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