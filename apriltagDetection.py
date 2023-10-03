import apriltag as apriltag
import cv2 as cv2
import numpy as np
import camera

class CameraApriltag(camera.Camera):
    def __init__(self, cameraIndex: int = 0, options: apriltag.DetectorOptions = apriltag.DetectorOptions(families="tag16h5"), decisionMargin: int = 30):
        self.cameraIndex = cameraIndex
        self.cameraStream = cv2.VideoCapture(cameraIndex)
        self.frame = None
        self.options = options
        self.detector = apriltag.Detector(options)
        self.decisionMargin = decisionMargin
        self.frameGrey = None
        self.tags = None
    
    def updateOptions(self, options: apriltag.DetectorOptions = apriltag.DetectorOptions()):
        self.options = options
        self.detector = apriltag.Detector(options)

    def updateDecisionMargin(self, decisionMargin: int):
        self.decisionMargin = decisionMargin
        
    def getLatestFrame(self):
        ret, self.frame = self.cameraStream.read()
        self.frameGrey = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

class CameraApriltag2D(CameraApriltag):
    def detectTags2D(self):
        self.tags = self.detector.detect(self.frameGrey)
        
    def printTagData2D(self):
        print("tags: ")
        for tag in self.tags:
            if tag.decision_margin >= self.decisionMargin:
                print(f"Tag ID: {tag.tag_id}")
                print(f"Tag Center: {tag.center}")
                print(f"Decision Margin: {tag.decision_margin}")
                print("")

    def renderTag(self):
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        fontColor = (0, 0, 255)
        lineType = 2
        for tag in self.tags:
            if tag.decision_margin >= self.decisionMargin:
                tagCorners = tag.corners.astype(int)
                cv2.polylines(self.frame, [tagCorners], isClosed=True, color=(0, 255, 0), thickness=2)
                cv2.putText(self.frame, str(tag.tag_id), (int(tag.center[0]), int(tag.center[1])), font, fontScale, fontColor, lineType)

    def render(self):
        self.renderTag()
        self.renderCameraStream()

    def update(self):
        self.getLatestFrame()
        self.detectTags2D()

# class CameraApriltag3D(CameraApriltag):