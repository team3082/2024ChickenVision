import cv2 as cv2
import numpy as np

class Camera:
    def __init__(self, cameraIndex: int = 0):
        self.cameraIndex = cameraIndex
        self.cameraStream = cv2.VideoCapture(cameraIndex)
        self.frame = None
    
    def updateCameraIndex(self, cameraIndex: int = 0):
        self.cameraIndex = cameraIndex
        self.cameraStream = cv2.VideoCapture(cameraIndex)

    def getLatestFrame(self):
        ret, self.frame = self.cameraStream.read()

    def renderCameraStream(self):
        cv2.imshow("Camera: " + str(self.cameraIndex), self.frame)