import camera
import numpy as np
import cv2

class CameraCone(camera.Camera):
    def __init__(self, cameraIndex: int = 0, lowerYellow: np.array = np.array[0, 100, 100], upperYellow: np.array = np.array[40, 200, 200], arbituaryValue: int = 0.9):
        self.cameraIndex = cameraIndex
        self.cameraStream = cv2.VideoCapture(cameraIndex)
        self.frame = None
        self.lowerYellow = lowerYellow
        self.upperYellow = upperYellow
        # i dont rly know why it does what it does but it does what it does.
        self.arbituaryValue = arbituaryValue

    