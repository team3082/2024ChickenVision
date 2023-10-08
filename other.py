from camera import Camera
from cv2 import waitKey

cam0 = Camera(0)

def gen():
    while True:
        print('amogus')
        frame = cam0.getLatestFrame()
        frame = cam0.convertFrameToBytes(frame)
        
        if waitKey(1) & 0xFF == ord('q'):
            break
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')