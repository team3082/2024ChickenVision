from camera import Camera
from cv2 import waitKey

cam0 = Camera(0)
cam2 = Camera(2)
cam4 = Camera(4)

while True:
    # cam0.renderCameraStream(cam0.getLatestFrame(), "0")
    cam2.renderCameraStream(cam2.getLatestFrame(), "2")
    cam4.renderCameraStream(cam4.getLatestFrame(), "4")

    if waitKey(1) & 0xFF == ord('q'):
        break