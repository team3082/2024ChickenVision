import os
import sys
sys.path.append("detectors")
from detectors.apriltagDetection import ApriltagDetector3D
from detectors.gamePieceDetection import ConeDetector
from detectors.gamePieceDetection import CubeDetector
from detectors.calibrateCam import CameraCalibrator
from camera import Camera
from cv2 import waitKey
from detectors.gamePieceDetectionML import *
import os

cam0 = Camera(0)
<<<<<<< HEAD
# configPath = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
# modelPath = os.path.join("model_data", "frozen_inference_graph.pb")
# classesPath = os.path.join("model_data","coco.names")
# detector = GamePieceDetectionML()
apriltagDetector = ApriltagDetector3D()
=======
#detector = GamePieceDetectionML()
apriltagDetector = ApriltagDetector2D()
>>>>>>> origin/Minne-Mini
while True:
    
    frame = cam0.getLatestFrame()
    labeledFrame = frame
    
    labeledFrame = apriltagDetector.update(labeledFrame, frame)
    #detector.detectInFrame(labeledFrame)

    cam0.renderCameraStream(labeledFrame)

    if waitKey(1) & 0xFF == ord('q'):
        break

