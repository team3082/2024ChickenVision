from detectors.apriltagDetection import ApriltagDetector2D, ApriltagDetector3D
from detectors.gamePieceDetection import ConeDetector, CubeDetector
from detectors.calibrateCam import CameraCalibrator
from camera import Camera
from cv2 import waitKey

# cubeDetector = CubeDetector()
# coneDetector = ConeDetector()
# cameraCalibrator = CameraCalibrator()
cam0 = Camera(0)
cam0.getCalibrationInfo()
cam4 = Camera(4)
cam4.getCalibrationInfo()

apriltagDetector31 = ApriltagDetector3D(camParams=cam0.params)
apriltagDetector32 = ApriltagDetector3D(camParams=cam4.params)
apriltagDetector21 = ApriltagDetector2D()
apriltagDetector22 = ApriltagDetector2D()

while True:
    frame0 = cam0.getLatestFrame()
    labeledFrame0 = frame0

    frame4 = cam4.getLatestFrame()
    labeledFrame4 = frame4

    labeledFrame0 = apriltagDetector21.update(labeledFrame0, labeledFrame0)
    labeledFrame4 = apriltagDetector22.update(labeledFrame4, frame4)

    decisionMargin0 = 0
    for tag in apriltagDetector21.tags:
        if tag.decision_margin > decisionMargin0:
            decisionMargin0 = tag.decision_margin

    decisionMargin4 = 0
    for tag in apriltagDetector22.tags:
        if tag.decision_margin > decisionMargin4:
            decisionMargin4 = tag.decision_margin

    if decisionMargin0 >= decisionMargin4:
        labeledFrame0 = apriltagDetector31.update(labeledFrame0, frame0)
    else:
        labeledFrame4 = apriltagDetector32.update(labeledFrame4, frame4)

    cam0.renderCameraStream(labeledFrame0, "stream: ")
    cam4.renderCameraStream(labeledFrame4, "stream: ")

    if waitKey(1) & 0xFF == ord('q'):
        # cameraCalibrator.storeJson(cam0.cameraIndex)
        break