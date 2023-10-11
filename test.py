import os
import sys
sys.path.append("detectors")
from detectors.apriltagDetection import ApriltagDetector2D
from detectors.gamePieceDetection import ConeDetector
from detectors.gamePieceDetection import CubeDetector
from detectors.calibrateCam import CameraCalibrator
from camera import Camera
from cv2 import waitKey
from detectors.gamePieceDetectionML import *
import os

cam0 = Camera(0)
#detector = GamePieceDetectionML()
apriltagDetector = ApriltagDetector2D()
while True:
    
    frame = cam0.getLatestFrame()
    labeledFrame = frame
    
    labeledFrame = apriltagDetector.update(labeledFrame, frame)
    #detector.detectInFrame(labeledFrame)

    cam0.renderCameraStream(labeledFrame)

    if waitKey(1) & 0xFF == ord('q'):
        break

