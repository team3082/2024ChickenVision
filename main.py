from apriltagDetection import CameraApriltag2D
from apriltag import DetectorOptions
from cv2 import waitKey

camera1 = CameraApriltag2D()

while True:
    camera1.update()
    camera1.render()
    camera1.printTagData2D()

    if waitKey(1) & 0xFF == ord('q'):
        break