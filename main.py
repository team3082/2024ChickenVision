from apriltagDetection import CameraApriltag2D
from gamePieceDetection import CameraCone
from camera import Camera
from cv2 import waitKey
import cv2

apriltagCam1 = CameraApriltag2D(0)
coneCam1 = CameraCone(1)

while True:
    apriltagCam1.getLatestFrame()
    apriltagCam1.renderCameraStream()

    coneCam1.update()
    coneCam1.render()

    if waitKey(1) & 0xFF == ord('q'):
        break