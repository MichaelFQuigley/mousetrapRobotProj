import cv2 
import numpy as np

def postProcess(img):
	#erosion
	kernel     = np.ones((15,15),np.uint8)
	erodedImg  = cv2.erode(img,kernel,iterations = 1)
	kernel2    = np.ones((10,10),np.uint8)
	dilatedImg = cv2.dilate(erodedImg,kernel,iterations = 1)
	return dilatedImg
	
#mins = (bMin, gMin, rMin)
#maxes = (bMax, gMax, rMax)
def filter(img, mins, maxes):
	hsvImg       = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	medianImg    = cv2.medianBlur(hsvImg,5)
	filtered_img = cv2.inRange(medianImg, mins, maxes)
	return filtered_img
	
