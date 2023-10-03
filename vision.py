import cv2
import numpy as np
import apriltag

options = apriltag.DetectorOptions(families="tag16h5", 
                    nthreads=2,
                    quad_decimate=1.0
                    )

detector = apriltag.Detector(options)

camera_index = 0
cap = cv2.VideoCapture(camera_index)

def detect_cone():
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow1 = np.array([0, 100, 100])
    lower_yellow2 = np.array([40, 200, 200])
    
    imgThreshLow = cv2.inRange(hsv, lower_yellow1, lower_yellow2)
    # cv2.imshow("thresh low", imgThreshLow)
    
    kernel = np.ones((5,5),np.uint8)
    
    threshed_img_smooth = cv2.erode(imgThreshLow, kernel, iterations = 3)
    threshed_img_smooth = cv2.dilate(threshed_img_smooth, kernel, iterations = 2)
    
    smoothed_img = cv2.dilate(threshed_img_smooth, kernel, iterations = 15)
    smoothed_img = cv2.erode(smoothed_img, kernel, iterations = 10)
    # cv2.imshow("mask", smoothed_img)
    
    edges_img = cv2.Canny(smoothed_img, 100, 200)
    contours = cv2.findContours(edges_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow("edge", edges_img)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 2
    fontColor = (0, 0, 255)
    lineType = 2

    if contours[0] != ():
        for cnt in contours:
            print(cnt)
            # perim = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.09, True)
            
            if len(approx) == 3:
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                bottomLeftCornerOfText = (x, y)
                cv2.putText(frame,'traffic_cone', 
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    lineType)
                cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
            
while True:
    ret, frame = cap.read()
    detect_cone()

    cv2.imshow("Robot Vision", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()