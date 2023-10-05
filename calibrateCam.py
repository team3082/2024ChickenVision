import cv2 as cv2
import numpy as np

class CameraCalibrator:
    def __init__(self):
        self.data = {'objpoints': [], 'imgpoints': [], 'frames': []}
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.objp = np.zeros((7*9,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:9,0:7].T.reshape(-1,2)
        self.frameGray = None
        self.corners = None
        self.cornersRefined = None
        self.ret = None

    def getLatestFrame(self, frame):
        self.frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.ret, self.corners = cv2.findChessboardCorners(frame, (9, 7), None)
    
    def renderFrame(self, frame):
        if self.ret == True:
            self.cornersRefined = cv2.cornerSubPix(self.frameGray, self.corners, (11,11), (-1,-1), self.criteria)
            cv2.drawChessboardCorners(frame, (9, 7), self.cornersRefined, self.ret)
        return frame
    
    def storeFrameData(self, frame):
        self.data['objpoints'].append(self.objp)
        self.data['imgpoints'].append(self.cornersRefined)
        self.data['frames'].append(frame)
    
    def showFrameCapture(self, frame):
        cv2.imshow("capture: " + str(len(self.data['objpoints'])), frame)

    def update(self, labeledFrame, frame):
        self.getLatestFrame(frame)
        labeledFrame = self.renderFrame(labeledFrame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            if self.ret:
                self.storeFrameData(labeledFrame)
                self.showFrameCapture(labeledFrame)
        return labeledFrame
    
