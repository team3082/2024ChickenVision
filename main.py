from detectors.apriltagDetection import ApriltagDetector2D
from detectors.gamePieceDetection import ConeDetector
from detectors.gamePieceDetection import CubeDetector
from detectors.calibrateCam import CameraCalibrator
from camera import Camera
from cv2 import waitKey

# apriltagDetector = ApriltagDetector2D()
# cubeDetector = CubeDetector()
# coneDetector = ConeDetector()
cameraCalibrator = CameraCalibrator()
cam0 = Camera(4)

while True:
    frame = cam0.getLatestFrame()
    labeledFrame = frame

    labeledFrame = cameraCalibrator.update(labeledFrame, frame)

    cam0.renderCameraStream(labeledFrame)

    if waitKey(1) & 0xFF == ord('q'):
        cameraCalibrator.storeJson(cam0.cameraIndex)
        break