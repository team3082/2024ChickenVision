from flask import Flask, render_template, Response, request
from camera import Camera
from detectors.apriltagDetection import ApriltagDetector3D
apriltag3Detecting = True
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/button')
def button():
    return "baller"

def gen(index):
    cap = Camera(index)
    cap.getCalibrationInfo()
    
    apriltag3 = ApriltagDetector3D(camParams=cap.params)
    
    while True:
        frame = cap.getLatestFrame()
        labeledFrame = frame
        
        if apriltag3Detecting:
            labeledFrame = apriltag3.update(labeledFrame, frame)
        
        labeledFrame = cap.convertFrameToBytes(labeledFrame)
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + labeledFrame + b'\r\n\r\n')
        
    cap.cameraStream.release()
    
@app.route('/pageData.json', methods = ['GET', 'POST', 'DELETE'])
def getPageData():
    if request.method == 'GET':
        return open("pageData.json", "r")

@app.route('/video_feed_0')
def video_feed_0():
    return Response(gen(0),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed/<cam_id>')
def video_feed(cam_id):
    return Response(gen(cam_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/settings.html')
def settingsTemplate():
    return open('templates/settings.html', 'r')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)