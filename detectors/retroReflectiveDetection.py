import cv2
import numpy as np

class CubeDetector:
    def __init__(self, lowerGreen: np.ndarray = np.array([110, 150, 150]), upperGreen: np.ndarray = np.array([160, 270, 270]), minimumArea: float = 100):
        self.frame = None
        self.lowerGreen = lowerGreen
        self.upperGreen = upperGreen
        self.contours = None
        self.detections = []
        # i dont rly know why it does what it does but it does what it does.
        self.minimumArea = minimumArea
        
    def updatePurple(self, lowerPurple: np.ndarray, upperPurple: np.ndarray):
        self.lowerPurple = lowerPurple
        self.upperPurple = upperPurple
    
    def updateArbituaryValue(self, arbituaryValue: float):
        self.arbituaryValue = arbituaryValue
        
    def printcubeData(self):
        # printing out data to console for debugging
        for detection in self.detections:
            if detection != None:
                position = detection["pose"]
                area = detection["area"]
                print(f"Position: ({position[0]}, {position[1]})")
                print(f"Area: {area}")

    def getContours(self):
        # detecting only specific colors
        imgThreshLow = cv2.inRange(self.frame, self.lowerPurple, self.upperPurple)

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


    def detectTape(self):
        self.detections = []
        # looping over each contour
        for cnt in self.contours:
            # getting perimeter of object
            perim = cv2.arcLength(cnt, True)
            
            # simplifying the vertices
            approx = cv2.approxPolyDP(cnt, 0.09 * perim, True)
            
            x, y, w, h = cv2.boundingRect(approx)
            center = [x + (w / 2), y + (h / 2)]
            area = w * h
            dimensions = [w, h]
            if area >= self.minimumArea:
                self.detections.append({"pose": center, "area": area, "dimensions": dimensions})

    def renderTape(self, frame):
        # stuff for printing stuff to camera stream
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 2
        fontColor = (0, 0, 255)
        lineType = 2
    
        # rendering stuff for each cube detected
        for detection in self.detections:
            if detection != None:
                contour = detection[2]
                x, y, w, h = detection[3]
                bottomLeftCornerOfText = (x, y)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(frame,'cube', 
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    lineType)
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
        return frame

    def getLatestFrame(self, frame):
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    def update(self, labeledFrame, frame):
        self.getLatestFrame(frame)
        self.getContours()
        self.detectTape()
        renderedFrame = self.renderTape(labeledFrame)
        return renderedFrame