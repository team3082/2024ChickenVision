import cv2

index = 0
arr = []
non = 0
while True:
    cap = cv2.VideoCapture(index)
    if not cap.read()[0]:
        non += 1
        if non == 5:
            break
    else:
        arr.append(index)
        non = 0
    cap.release()
    index += 1
print(arr)