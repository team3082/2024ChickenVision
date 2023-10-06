import cv2 as cv2
import numpy as np
import json
import os

class CameraCalibrator:
    def __init__(self):
        self.data = {'objpoints': [], 'imgpoints': [], 'frames': []}
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.objp = np.zeros((6*7,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        self.frameGray = None
        self.corners = None
        self.cornersRefined = None
        self.ret = None

    def getLatestFrame(self, frame):
        self.frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.ret, self.corners = cv2.findChessboardCorners(frame, (7, 6), None)
    
    def renderFrame(self, frame):
        if self.ret == True:
            self.cornersRefined = cv2.cornerSubPix(self.frameGray, self.corners, (11,11), (-1,-1), self.criteria)
            cv2.drawChessboardCorners(frame, (7, 6), self.cornersRefined, self.ret)
        return frame
    
    def storeFrameData(self, frame):
        self.data['objpoints'].append(self.objp)
        self.data['imgpoints'].append(self.cornersRefined)
        self.data['frames'].append(frame)
    
    def showFrameCapture(self, frame):
        cv2.imshow("capture: " + str(len(self.data['objpoints'])), frame)
        directory = "/home/kader/dev/2024ChickenVision/calibImgs"
        os.chdir(directory)
        cv2.imwrite("capture" + str(len(self.data['objpoints'])) + ".png", frame)
        cv2.imwrite("captureGray" + str(len(self.data['objpoints'])) + ".png", self.frameGray)


    # fix this its no worky
    def storeJson(self, camIndex):
        save_file = open("cameraParams" + str(camIndex) + ".json", "w") 
        calibData = []
        for i in range(len(self.data['objpoints'])):
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.data['objpoints'][i], self.data['imgpoints'][i], (640, 480), None, None)
            calibData.append([ret, mtx, dist, rvecs, tvecs])

        avgmtx = 0
        avgdist = 0
        for data in calibData:
            avgmtx += data[1]
            avgdist += data[2]

        avgmtx /= len(calibData)
        avgdist /= len(calibData)

        dataJson = {'avgmtx': avgmtx, 'avgdist': avgdist, 'data': calibData}
        save_file.write(dataJson)
        save_file.close()  

    def update(self, labeledFrame, frame):
        self.getLatestFrame(frame)
        labeledFrame = self.renderFrame(labeledFrame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            if self.ret:
                self.storeFrameData(labeledFrame)
                self.showFrameCapture(labeledFrame)
        return labeledFrame
    
