from apriltagDetection import CameraApriltag2D
from gamePieceDetection import CameraCone
from gamePieceDetection import CameraCube
from camera import Camera
from cv2 import waitKey
import cv2

# apriltagCam1 = CameraApriltag2D(0)
cubeCam1 = CameraCube(0)

while True:
    # apriltagCam1.update()
    # apriltagCam1.render()

    cubeCam1.update()
    cubeCam1.printcubeData()
    cubeCam1.render()

    if waitKey(1) & 0xFF == ord('q'):
        break