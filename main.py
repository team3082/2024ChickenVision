from apriltagDetection import ApriltagDetector2D
from gamePieceDetection import ConeDetector
from gamePieceDetection import CubeDetector
from camera import Camera
from cv2 import waitKey
import cv2


apriltagDetector = ApriltagDetector2D()
cubeDetector = CubeDetector()
coneDetector = ConeDetector()
cam0 = Camera(0)

while True:
    frame = cam0.getLatestFrame()
    labeledFrame = frame

    labeledFrame = apriltagDetector.update(labeledFrame, frame)
    labeledframe = cubeDetector.update(labeledFrame, frame)
    labeledFrame = coneDetector.update(labeledFrame, frame)

    cam0.renderCameraStream(labeledframe)

    if waitKey(1) & 0xFF == ord('q'):
        break