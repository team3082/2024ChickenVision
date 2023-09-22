import cv2
from pupil_apriltags import Detector

detector = Detector(families="tag16h5", 
                    nthreads=1,
                    quad_decimate=1.0,
                    quad_sigma=0.0,
                    refine_edges=1,
                    decode_sharpening=0.25
                    )

camera_index = 0
cap = cv2.VideoCapture(camera_index)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture a frame from the camera.")
        break

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

    cv2.imshow("AprilTag Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
