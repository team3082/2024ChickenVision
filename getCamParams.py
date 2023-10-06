import numpy as np
import cv2 as cv
import glob
import os
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
mtxs = []
dists = []
directory = "/home/kader/dev/2024ChickenVision/calibImgs"
os.chdir(directory)
images = glob.glob('*.png')
for fname in images:
 img = cv.imread(fname)
 gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
 # Find the chess board corners
 ret, corners = cv.findChessboardCorners(gray, (7,6), None)
 # If found, add object points, image points (after refining them)
 if ret == True:
  objpoints.append(objp)
  corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
  imgpoints.append(corners2)
  # Draw and display the corners
  cv.drawChessboardCorners(img, (7,6), corners2, ret)
  ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
  mtxs.append(mtx)
  dists.append(dist)
  cv.imshow('img', img)
#   cv.waitKey(100)

calibMtx = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

i1 = 0
i2 = 0
i3 = 0

for i1 in range(len(mtxs)):
   for i2 in range(3):
      for i3 in range(3):
         calibMtx[i2][i3] += mtxs[i1][i2][i3]

i3 = 0
i4 = 0

for i1 in calibMtx:
    for i2 in i1:
        i2 /= len(mtxs)
        calibMtx[i3][i4] = i2
        i4 += 1
    i3 += 1
    i4 = 0

# print(calibMtx)
calibMtx = cv.Mat(np.array(calibMtx, dtype=np.float32))

calibDist = [[0, 0, 0, 0, 0]]

i1 = 0
i2 = 0

for i1 in range(len(dists)):
   for i2 in range(5):
      calibDist[0][i2] += dists[i1][0][i2]

i2 = 0

for i1 in calibDist[0]:
   i1 /= len(dists)
   calibDist[0][i2] = i1
   i2 += 1

print("not calibrated: ")
print(dists)

print("calibrated: ")
print(calibDist)
calibDist = cv.Mat(np.array(calibDist, dtype=np.float32))

img = cv.imread('captureGray1.png')
h, w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(calibMtx, dist, (w,h), 1, (w,h))

calibParams = cv.undistort(img, mtx, calibDist, None, newcameramtx)

x, y, w, h = roi
dst = calibParams[y:y+h, x:x+w]
cv.imwrite('calibresult.png', dst)

cv.destroyAllWindows()

while True:
    cv.imshow('before calib', img)
    cv.imshow('after calib', dst)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# cv.destroyAllWindows()