import numpy as np
import cv2

RATIO_HEIGHT_WIDTH = 1.571929824561403


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
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
    M = cv2.getPerspectiveTransform(rect, dst)
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
    medianImg = cv2.medianBlur(hsvImg, 5)
    filtered_img = cv2.inRange(medianImg, mins, maxes)
    return filtered_img


def all_the_things(image, params):
    cv2.imwrite('calibratergb.jpg', image)
    warped_image = four_point_transform(image, params['pts'])
    warped_image = cv2.resize(warped_image, (600, int(400*RATIO_HEIGHT_WIDTH)))
    cv2.imwrite('warped.jpg', warped_image)
    hsvImg = cv2.cvtColor(warped_image, cv2.COLOR_BGR2HSV)
    filtered_image = filter(hsvImg, params['mins'], params['maxes'])
    processed_image = postProcess(filtered_image, params['dilation'], params['erosion'])
    return processed_image


def bitmap_from_image(image):
    return cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]
