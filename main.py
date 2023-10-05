from apriltagDetection import ApriltagDetector2D
from gamePieceDetection import ConeDetector
from gamePieceDetection import CubeDetector
from calibrateCam import CameraCalibrator
from camera import Camera
from cv2 import waitKey

# apriltagDetector = ApriltagDetector2D()
# cubeDetector = CubeDetector()
# coneDetector = ConeDetector()
# cameraCalibrator = CameraCalibrator()
cam0 = Camera(0)

while True:
    frame = cam0.getLatestFrame()
    # labeledFrame = frame

    # labeledFrame = apriltagDetector.update(labeledFrame, frame)
    # labeledframe = cubeDetector.update(labeledFrame, frame)
    # labeledFrame = coneDetector.update(labeledFrame, frame)
    # labeledFrame = cameraCalibrator.renderCalibTarget(labeledFrame)
    # if waitKey(1) & 0xFF == ord('c'):
    #     cameraCalibrator.update(frame)
    #     print("calibrating for frame")

    cam0.renderCameraStream(frame)

    if waitKey(1) & 0xFF == ord('q'):
        break