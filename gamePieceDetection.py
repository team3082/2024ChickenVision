import camera
import numpy as np
import cv2

class CameraConeDetection(camera.Camera):
    def __init__(self, cameraIndex: int = 0, lowerYellow: np.array = np.array[0, 100, 100], upperYellow: np.array = np.array[40, 200, 200]):
        self.cameraIndex = cameraIndex
        self.cameraStream = cv2.VideoCapture(cameraIndex)
        self.frame = None
        self.lowerYellow = lowerYellow
        self.upperYellow = upperYellow
        