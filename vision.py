import cv2
from pupil_apriltags import Detector
import numpy as np

detector = Detector(families="tag16h5", 
                    nthreads=1,
                    quad_decimate=1.0,
                    quad_sigma=0.0,
                    refine_edges=1,
                    decode_sharpening=0.25
                    )

camera_index = 0
cap = cv2.VideoCapture(camera_index)

def detect_cone():
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([20, 80, 100])
    upper_yellow = np.array([60, 255, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    middle_x = -1
    middle_y = -1

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 250:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                middle_x = cX
                middle_y = cY
                
                print(f"Cone: ({cX}, {cY})")

                cv2.circle(frame, (cX, cY), 7, (0, 0, 255), -1)
                cv2.putText(frame, "Cone Middle", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

def detect_apriltag():
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    tags = detector.detect(gray)

    for tag in tags:
        if tag.decision_margin >= 20:
            corners = tag.corners.astype(int)

            print(f"Tag ID: {tag.tag_id}")
            print(f"Tag Center: {tag.center}")
            print(f"Tag Rotation: {tag.pose_R}")
            print(f"Tag Translation: {tag.pose_t}\n")
            print(f"Tag Ambiguity; {tag.decision_margin}")

            cv2.polylines(frame, [corners], isClosed=True, color=(0, 255, 0), thickness=2)
            
while True:
    ret, frame = cap.read()
    detect_cone()
    detect_apriltag()

    cv2.imshow("Robot Vision", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()