from PyQt4 import QtGui
import numpy as np
import cv2
import settings

RATIO_HEIGHT_WIDTH = 1.571929824561403

def four_point_transform(image, pts):

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((pts[2][0] - pts[3][0]) ** 2) + ((pts[2][1] - pts[3][1]) ** 2))
    widthB = np.sqrt(((pts[1][0] - pts[0][0]) ** 2) + ((pts[1][1] - pts[0][1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((pts[1][0] - pts[2][0]) ** 2) + ((pts[1][1] - pts[2][1]) ** 2))
    heightB = np.sqrt(((pts[0][0] - pts[3][0]) ** 2) + ((pts[0][1] - pts[3][1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped


def postProcess(img, dilation, erosion):
    # erosion
    kernel = np.ones(erosion, np.uint8)
    erodedImg = cv2.erode(img, kernel, iterations=1)
    kernel2 = np.ones(dilation, np.uint8)
    dilatedImg = cv2.dilate(erodedImg, kernel2, iterations=1)
    return dilatedImg


# mins = (bMin, gMin, rMin)
# maxes = (bMax, gMax, rMax)
def filter(hsvImg, mins, maxes):
    # medianImg = cv2.medianBlur(hsvImg, 0)
    filtered_img = cv2.inRange(hsvImg, mins, maxes)
    return filtered_img


def raw_to_map(image, purpose):
    # cv2.imwrite('calibratergb.jpg', image)
    warped_image = four_point_transform(image, np.array([purpose['top_left'], purpose['top_right'],
                                                         purpose['bottom_right'],
                                                         purpose['bottom_left']], np.float32))
    warped_image = cv2.resize(warped_image, (settings.image_height, int(settings.image_height*RATIO_HEIGHT_WIDTH)))
    # cv2.imwrite('warped.jpg', warped_image)
    hsvImg = cv2.cvtColor(warped_image, cv2.COLOR_BGR2HSV)
    filtered_image = filter(hsvImg,
                            (purpose['rMin'], purpose['gMin'], purpose['bMin']),
                            (purpose['rMax'], purpose['gMax'], purpose['bMax']))
    processed_image = postProcess(filtered_image,
                                  (purpose['dy'], purpose['dx']),
                                  (purpose['ey'], purpose['ex']))
    return processed_image

def bitmap_from_image(image):
    return cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]

def as_pixmap(frame):
    gray = False
    if len(frame.shape) == 2:
        gray = True
    if gray:
        img = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    else:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    qt_image = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
    return QtGui.QPixmap.fromImage(qt_image)
