import cv2
import time
import numpy as np

'''
195,3,11
255,255,94
'''

windowName = 'testWin'
screen_res = 1920, 1080
initialImg = cv2.imread('mousetraps.jpg',cv2.IMREAD_COLOR)
img = initialImg #cv2.resize(initialImg, (0,0), fx=0.25, fy=0.25)

def scrollBarCallback(pos):
	print pos


def preProcess(img):
	#erosion
	kernel = np.ones((15,15),np.uint8)
	erodedImg = cv2.erode(img,kernel,iterations = 1)
	kernel2 = np.ones((10,10),np.uint8)
	dilatedImg = cv2.dilate(erodedImg,kernel,iterations = 1)
	return dilatedImg
	
cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
cv2.namedWindow(windowName + "2", cv2.WINDOW_NORMAL)

scale_width = screen_res[0] / img.shape[1]
scale_height = screen_res[1] / img.shape[0]
scale = min(scale_width, scale_height)
window_width = int(img.shape[1] * scale)
window_height = int(img.shape[0] * scale)

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


try:
	while True:
		img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		
		rMin = cv2.getTrackbarPos('Rmin', windowName)
		gMin = cv2.getTrackbarPos('Gmin', windowName)
		bMin = cv2.getTrackbarPos('Bmin', windowName)
		rMax = cv2.getTrackbarPos('Rmax', windowName)
		gMax = cv2.getTrackbarPos('Gmax', windowName)
		bMax = cv2.getTrackbarPos('Bmax', windowName)
		
		medianImg = cv2.medianBlur(img2,5)
		filtered_img = cv2.inRange(medianImg, (bMin, gMin, rMin), (bMax, gMax, rMax))
		filtered_img2 = cv2.inRange(img2, (bMin, gMin, rMin), (bMax, gMax, rMax))
		cv2.imshow(windowName, filtered_img)
		cv2.imshow(windowName + "2", preProcess(filtered_img2))
		cv2.waitKey(200)
finally:
	cv2.destroyAllWindows()