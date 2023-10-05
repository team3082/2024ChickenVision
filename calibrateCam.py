import cv2
import numpy as np
import glob

class CameraCalibrator:
    def __init__(self):
        self.frames = []
        self.objPoints = [] # 3d point in real world space
        self.imgPoints = [] # 2d points in image plane.
    
    def getFrame(self, frame):
        self.frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

    def calibFrame(self):
        frame = self.frames[-1]

        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6*7,3), np.float32)
        objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        
        ret, corners = cv2.findChessboardCorners(frame, (7,6), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            self.objPoints.append(objp)
            corners2 = cv2.cornerSubPix(frame, corners, (11,11), (-1,-1), criteria)
            self.imgPoints.append(corners2)
        else:
            del self.frames[-1]

    def renderCalibTarget(self, frame):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        ret, corners = cv2.findChessboardCorners(frame, (7,6), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            corners2 = cv2.cornerSubPix(frame, corners, (11,11), (-1,-1), criteria)
            # Draw and display the corners
            cv2.drawChessboardCorners(frame, (7,6), corners2, ret)
        return frame
    
    def update(self, frame):
        self.getFrame(frame)
        self.calibFrame(frame)
