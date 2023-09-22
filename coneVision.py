import cv2
import numpy as np

def detect_yellow_cone(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([10, 80, 100])
    upper_yellow = np.array([60, 255, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    middle_x = -1
    middle_y = -1

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 150:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                middle_x = cX
                middle_y = cY

                cv2.circle(frame, (cX, cY), 7, (0, 0, 255), -1)
                cv2.putText(frame, "Cone Middle", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

    return frame, middle_x, middle_y

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    frame_with_tip, middle_x, middle_y = detect_yellow_cone(frame)

    cv2.imshow("Yellow Cone Detection", frame_with_tip)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
