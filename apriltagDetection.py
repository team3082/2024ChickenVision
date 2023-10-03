import apriltag as apriltag
import cv2 as cv2
import numpy as np

class camApriltag:
    def __init__(self, cameraIndex: int = 0, options: apriltag.DetectorOptions = apriltag.DetectorOptions(), decisionMargin: int = 40):
        self.cameraIndex = cameraIndex
        self.cameraStream = cv2.VideoCapture(cameraIndex)
        self.options = options
        self.detector = apriltag.Detector(options)
        self.decisionMargin = decisionMargin
        self.frame
        self.frameGrey
        self.tags
    
    def updateCameraIndex(self, cameraIndex: int):
        self.cameraIndex = cameraIndex
        self.cameraStream = cv2.VideoCapture(cameraIndex)

    def updateOptions(self, options: apriltag.DetectorOptions = apriltag.DetectorOptions()):
        self.options = options
        self.detector = apriltag.Detector(options)

    def updateDecisionMargin(self, decisionMargin: int):
        self.decisionMargin = decisionMargin
        
    def getLatestFrame(self):
        self.frame = self.cameraStream.read()
        self.frameGrey = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

class camApriltag2D(camApriltag):
    def detectTags2D(self):
        self.tags = self.detector.detect(self.frameGrey)
        
    def update(self):
        self.getLatestFrame()
        self.detectTags2D()

# class camApriltag3D(camApriltag):
    