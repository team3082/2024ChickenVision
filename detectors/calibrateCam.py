import cv2 as cv2
import numpy as np
import json
import os

class CameraCalibrator:
    def __init__(self):
        self.objpoints = []
        self.imgpoints = []
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
    
    def storeFrameData(self):
        self.objpoints.append(self.objp)
        self.imgpoints.append(self.cornersRefined)
    
    def showFrameCapture(self, frame):
        cv2.imshow("capture: " + str(len(self.objpoints)), frame)
        directory = "/home/kader/dev/2024ChickenVision/calibImgs"
        os.chdir(directory)
        cv2.imwrite("capture" + str(len(self.objpoints)) + ".png", frame)
        cv2.imwrite("captureGray" + str(len(self.objpoints)) + ".png", self.frameGray)

    def storeJson(self, camIndex):
        mtxs = []
        dists = []
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, self.frameGray.shape[::-1], None, None)
        
        fx = mtx[0,0]
        fy = mtx[1,1]
        cx = mtx[0,2]
        cy = mtx[1,2]

        params = (fx, fy, cx, cy)

        print()

        mtx = np.ndarray.tolist(mtx)
        dist = np.ndarray.tolist(dist)

        # storing values to json
        calibDataDict = {'mtx': mtx, 'dist': dist, 'params': list(params)}
        directory = "/home/kader/dev/2024ChickenVision/calibData"
        os.chdir(directory)
        calibDataJson = open("cam" + str(camIndex) + ".json", 'w')
        calibDataJson.write(json.dumps(calibDataDict))
        calibDataJson.close()

    def update(self, labeledFrame, frame):
        self.getLatestFrame(frame)
        labeledFrame = self.renderFrame(labeledFrame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            if self.ret:
                self.storeFrameData()
                self.showFrameCapture(labeledFrame)
        return labeledFrame
    
