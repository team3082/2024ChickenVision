import camera
import numpy as np
import cv2

class CameraCone(camera.Camera):
    def __init__(self, cameraIndex: int = 0, lowerYellow: np.ndarray = np.array([0, 100, 100]), upperYellow: np.ndarray = np.array([40, 200, 200]), arbituaryValue: float = 0.09):
        self.cameraIndex = cameraIndex
        self.cameraStream = cv2.VideoCapture(cameraIndex)
        self.frame = None
        self.frameHSV = None
        self.lowerYellow = lowerYellow
        self.upperYellow = upperYellow
        self.contours = None
        self.cones = ()
        # i dont rly know why it does what it does but it does what it does.
        self.arbituaryValue = arbituaryValue
        
    def printConeData(self):
        # printing out data to console for debugging
        for cone in self.cones:
            if cone != None:
                position = cone[0]
                area = cone[1]
                print(f"Position: ({position[0]}, {position[1]})")
                print(f"Area: {area}")

    def detectCones(self):
        # resetting data from previous frame
        if len(self.contours) > 0:
            self.cones = [None] * len(self.contours)

            index = 0
            # looping over each contour
            for cnt in self.contours:
                # getting perimeter of object
                perim = cv2.arcLength(cnt, True)

                # simplifying the vertices
                approx = cv2.approxPolyDP(cnt, self.arbituaryValue * perim, True)

                # checking if its a triangle or has 3 vertices
                if len(approx) == 3:
                    x, y, w, h = cv2.boundingRect(approx)
                    center = (x + (w / 2), y + (h / 2))
                    area = w * h
                    self.cones[index] = [center, area, cnt, [x, y, w, h]] 
                    index += 1

    def getContours(self):
        # detecting only specific colors
        imgThreshLow = cv2.inRange(self.frameHSV, self.lowerYellow, self.upperYellow)

        # simplifying the frames
        kernel = np.ones((5,5),np.uint8)
        threshed_img_smooth = cv2.erode(imgThreshLow, kernel, iterations = 3)
        threshed_img_smooth = cv2.dilate(threshed_img_smooth, kernel, iterations = 2)
        smoothed_img = cv2.dilate(threshed_img_smooth, kernel, iterations = 15)
        smoothed_img = cv2.erode(smoothed_img, kernel, iterations = 10)

        # getting edges
        edges_img = cv2.Canny(smoothed_img, 100, 200)

        # getting contours
        self.contours, heirarchy = cv2.findContours(edges_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def renderCones(self):
        # stuff for printing stuff to camera stream
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 2
        fontColor = (0, 0, 255)
        lineType = 2
    
        # rendering stuff for each cone detected
        for cone in self.cones:
            if cone != None:
                contour = cone[2]
                x, y, w, h = cone[3]
                bottomLeftCornerOfText = (x, y)
                cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(self.frame,'traffic_cone', 
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    lineType)
                cv2.drawContours(self.frame, [contour], -1, (0, 255, 0), 2)

    def render(self):
        self.renderCones()
        self.renderCameraStream(title="Cone: ")

    def getLatestFrame(self):
        ret, self.frame = self.cameraStream.read()
        self.frameHSV = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

    def update(self):
        self.getLatestFrame()
        self.getContours()
        self.detectCones()