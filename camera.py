import cv2 as cv2
import numpy as np

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
    def __init__(self, cameraIndex: int = 0):
        self.cameraIndex = cameraIndex
        self.cameraStream: cv2.VideoCapture = cv2.VideoCapture(cameraIndex)
        self.frame = None
    
    def updateCameraIndex(self, cameraIndex: int = 0):
        self.cameraIndex = cameraIndex
        self.cameraStream = cv2.VideoCapture(cameraIndex)

    def getLatestFrame(self):
        ret, self.frame = self.cameraStream.read()
        return self.frame

    def renderCameraStream(self, frame, title: str = "Camera: "):
        cv2.imshow(title + str(self.cameraIndex), frame)