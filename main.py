from apriltagDetection import CameraApriltag2D
from gamePieceDetection import CameraCone
from gamePieceDetection import CameraCube
from camera import Camera
from cv2 import waitKey
import cv2

apriltagCam1 = CameraApriltag2D(0)
# cubeCam1 = CameraCone(cameraIndex=0, arbituaryValue=0.08)

while True:
    apriltagCam1.update()
    apriltagCam1.render()

    # cubeCam1.update()
    # cubeCam1.printConeData()
    # cubeCam1.render()

    if waitKey(1) & 0xFF == ord('q'):
        break