import cv2 as cv2
import numpy as np
import json

def getAvailableCameraIndexes():
    index = 0
    arr = []
    non = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            non += 1
            if non == 5:
                break
        else:
            arr.append(index)
            non = 0
        cap.release()
        index += 1
    return arr

class Camera:
    def __init__(self, cameraIndex: int = 0, resolution = [640, 480]):
        self.cameraIndex = cameraIndex
        self.cameraStream: cv2.VideoCapture = cv2.VideoCapture(cameraIndex)
        self.frame = None
        self.mtx = []
        self.dist = []
        self.params = ()
        self.cameraStream.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cameraStream.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
    
    def updateCameraIndex(self, cameraIndex: int = 0):
        self.cameraIndex = cameraIndex
        self.cameraStream = cv2.VideoCapture(cameraIndex)

    def getCalibrationInfo(self):
        with open("calibData/cam" + str(self.cameraIndex) + ".json", "r") as calibDataJson:
            calibDataDict = json.load(calibDataJson)

        try:
            mtx = calibDataDict['mtx']
            dist = calibDataDict['dist']

            self.mtx = cv2.Mat(np.array(mtx, dtype=np.float32))
            self.dist = cv2.Mat(np.array(dist, dtype=np.float32))
            self.params = tuple(calibDataDict['params'])

            # print("calibration data found")
        
        except:
            print("no calibration data found")

    def getLatestFrame(self):
        ret, self.frame = self.cameraStream.read()
        return self.frame
    
    def convertFrameToBytes(self, frame):
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    
    def getLatestFrameCalibrated(self):
        ret, frame = self.cameraStream.read()

        h, w = frame.shape[:2]

        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w,h), 1, (w,h))
        calibParams = cv2.undistort(frame, self.mtx, self.dist, None, newcameramtx)

        x, y, w, h = roi
        self.frame = calibParams[y:y+h, x:x+w]

        return self.frame

    def renderCameraStream(self, frame, title: str = "Camera: "):
        cv2.imshow(title + str(self.cameraIndex), frame)