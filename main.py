from apriltagDetection import CameraApriltag2D
from gamePieceDetection import CameraCone
from apriltag import DetectorOptions
from cv2 import waitKey

apriltagCam1 = CameraApriltag2D()
coneCam1 = CameraCone()

while True:
    # apriltagCam1.update()
    # apriltagCam1.render()
    # apriltagCam1.printTagData2D()
    # apriltagCam1.getLatestFrame()
    # apriltagCam1.renderCameraStream()

    coneCam1.getLatestFrame()
    coneCam1.renderCameraStream()
    # coneCam1.update()
    # coneCam1.render()
    # coneCam1.printConeData()

    if waitKey(1) & 0xFF == ord('q'):
        break