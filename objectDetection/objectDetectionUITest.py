import cv2
import objectDetection
import numpy as np

import sys
sys.path.insert(0, '../imageTransform')
import imageTransform

'''
195,3,11
255,255,94
'''

def scrollBarCallback(pos):
	pass

windowName = 'testWin'
img        = cv2.resize(cv2.imread('../img/mousetraps.jpg',cv2.IMREAD_COLOR), (0,0), fx=0.5, fy=0.5)
cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
#cv2.imwrite("picToCalibrate.png", img)
# create trackbars for color change
cv2.createTrackbar('Rmin',windowName, 0, 255, scrollBarCallback)
cv2.createTrackbar('Gmin',windowName, 0, 255, scrollBarCallback)
cv2.createTrackbar('Bmin',windowName, 0, 255, scrollBarCallback)
cv2.setTrackbarPos('Rmin',windowName, 143)
cv2.setTrackbarPos('Gmin',windowName, 3)
cv2.setTrackbarPos('Bmin',windowName, 3)

# create trackbars for color change
cv2.createTrackbar('Rmax',windowName, 0, 255, scrollBarCallback)
cv2.createTrackbar('Gmax',windowName, 0, 255, scrollBarCallback)
cv2.createTrackbar('Bmax',windowName, 0, 255, scrollBarCallback)
cv2.setTrackbarPos('Rmax',windowName, 255)
cv2.setTrackbarPos('Gmax',windowName, 255)
cv2.setTrackbarPos('Bmax',windowName, 94)

def display():
	rMin = cv2.getTrackbarPos('Rmin', windowName)
	gMin = cv2.getTrackbarPos('Gmin', windowName)
	bMin = cv2.getTrackbarPos('Bmin', windowName)
	rMax = cv2.getTrackbarPos('Rmax', windowName)
	gMax = cv2.getTrackbarPos('Gmax', windowName)
	bMax = cv2.getTrackbarPos('Bmax', windowName)

	img2 = objectDetection.filter(img, (bMin, gMin, rMin), (bMax, gMax, rMax))
	img3 = objectDetection.postProcess(img2)
	pts = np.array(eval("[(869, 229), (1842, 238), (2613, 1396), (67, 1407)]"), dtype="float32")
	img4 = imageTransform.four_point_transform(img3, pts)
	cv2.imshow(windowName, img4)

display()
try:
	while True:
		cv2.waitKey(200)
finally:
	cv2.destroyAllWindows()