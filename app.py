from flask import Flask, render_template, Response, request
from camera import Camera
import camera as cam
from detectors.apriltagDetection import ApriltagDetector3D, ApriltagDetector2D
from detectors.gamePieceDetection import ConeDetector, CubeDetector
from detectors.gamePieceDetectionML import GamePieceDetectionML
from apriltag import DetectorOptions
import json
import cv2
import numpy as np
import threading
from queue import Queue
# from networktables import NetworkTables

# setup getting general settings
generalSettings = open("generalSettings.json", "r")
generalSettingsDict = json.loads(generalSettings.read())
generalSettings.close()

# setting general settings
# teamNumber = generalSettingsDict["teamNumber"]
# webAddress = generalSettingsDict["webAddress"]
# port = generalSettingsDict["port"]

# starting data queues for inter-thread data management
queue = Queue()
settingsUpdated = Queue()
pageDataUpdate = Queue()

# network tables configuration
# NetworkTables.initialize(server='roborio-' + str(teamNumber) + '-frc.local')
# nt = NetworkTables.getTable('ChickenVision')

def startServer():
    app.run(host='0.0.0.0', debug=False, port=8000)
    
def startCameras():
    availableCams = cam.getAvailableCameraIndexes()
    threads = []
    for camIndex in availableCams:
        thread = threading.Thread(target=runCamera, args=(camIndex, ))
        threads.append(thread)
    
    for thread in threads:
        thread.start()

def runCamera(camIndex):
    camera = Camera(camIndex)
    apriltag2Detector = ApriltagDetector2D()
    apriltag3Detector = ApriltagDetector3D()
    cubeDetector = CubeDetector()
    coneDetector = ConeDetector()
    objDetector = GamePieceDetectionML()
    
    while True:
        pageDataJSON = open("pageData.json", "r")
        currentViewedCam = int(json.loads(pageDataJSON.read())["currentCamera"])
        pageDataJSON.close()
        
        settingsJSON = open("settings.json", "r")
        settings = json.loads(settingsJSON.read())
        settingsJSON.close()
        
        # checking if settings exist for the camera, if not creates a json entry
        try:
            cameraSettings = settings["cam" + str(camIndex)]
        except:
            settingsTemplate = open("settingsTemplate.json", "r")
            defaultSettings = json.loads(settingsTemplate.read())
            settingsTemplate.close()
            
            settingsJSON = open("settings.json", "w")
            settings = json.loads(settingsJSON.read())
            settings["cam" + str(camIndex)] = defaultSettings
            settingsJSON.write(json.dumps(settings))
            settingsJSON.close()
            
        cameraSettings = settings["cam" + str(camIndex)]
        try:
            try:
                camera.getCalibrationInfo()
                apriltag3Detector.setCamParams(camera.params)
            except:
                # will add some stuff to generate a templated calib file here
                pass
            frame = camera.getLatestFrame()
            labeledFrame = frame
            
            # checking if apriltag2D is enabled
            if cameraSettings["pipelineSettings"]["toggles"][0]:
                # gettings and updating the latest options
                # TODO only update settings when they are actually changed in order to increase performance
                optionsDict = cameraSettings["pipelineSettings"]["apriltag2D"]
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
                
                # running the detector
                labeledFrame = apriltag2Detector.update(labeledFrame, frame)
            
            # TODO get rid of this when it I add the automatically generating calib file
            try: 
                # checking if apriltag3D is enabled
                if cameraSettings["pipelineSettings"]["toggles"][1]:
                    # gettings and updating the latest options
                    # TODO only update settings when they are actually changed in order to increase performance
                    optionsDict = cameraSettings["pipelineSettings"]["apriltag3D"]
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
                    
                    # running the detector
                    labeledFrame = apriltag3Detector.update(labeledFrame, frame)
            except:
                pass
            
            # checking if Game Piece Detection Geometry is enabled
            if cameraSettings["pipelineSettings"]["toggles"][2]:
                # gettings and updating the latest options
                # TODO only update settings when they are actually changed in order to increase performance
                optionsDict = cameraSettings["pipelineSettings"]["gamePieceGeo"]
                lowerYellow = np.array([int(optionsDict["lowerYellow"][0]), int(optionsDict["lowerYellow"][1]), int(optionsDict["lowerYellow"][2])])
                upperYellow = np.array([int(optionsDict["upperYellow"][0]), int(optionsDict["upperYellow"][1]), int(optionsDict["upperYellow"][2])])
                coneDetector.updateYellow(lowerYellow, upperYellow)
                coneDetector.updateArbituaryValue(float(optionsDict["arbituaryValueCone"]) / 100)
                lowerPurple = np.array([int(optionsDict["lowerPurple"][0]), int(optionsDict["lowerPurple"][1]), int(optionsDict["lowerPurple"][2])])
                upperPurple = np.array([int(optionsDict["upperPurple"][0]), int(optionsDict["upperPurple"][1]), int(optionsDict["upperPurple"][2])])
                cubeDetector.updatePurple(lowerPurple, upperPurple)
                cubeDetector.updateArbituaryValue(float(optionsDict["arbituaryValueCube"]) / 100)
                
                # running the detectors
                labeledFrame = cubeDetector.update(labeledFrame, frame)
                labeledFrame = coneDetector.update(labeledFrame, frame)

    
            # checking if Game Piece Detection Machine Learning is enabled
            if cameraSettings["pipelineSettings"]["toggles"][3]:
                # TODO refactor this class
                objDetector.detectInFrame(labeledFrame)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            print(camIndex, currentViewedCam)
            if camIndex == currentViewedCam:
                print(camIndex)
                frameBytes = camera.convertFrameToBytes(labeledFrame)
                # camera.renderCameraStream(labeledFrame)
                queue.put(frameBytes)
                
            # NetworkTables
            

        except:
            break        

# starting cameras
startCameras()

# flask configuration
app = Flask(__name__)
# app.config['SERVER_NAME'] = + webAddress + ':' + str(port)

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
    
# SHOWS SELECTED VIDEO FEED
@app.route('/video_feed')
def video_feed():
    return Response(getBytes(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
# TODO make these not retarded
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

# start flask webserver
startServer()