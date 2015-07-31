from PyQt4 import QtGui
import numpy as np
import cv2
import settings
RATIO_HEIGHT_WIDTH = 1.5


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


def raw_to_map(image, purpose, hue=187.0):
    # cv2.imwrite('calibratergb.jpg', image)
    warped_image = four_point_transform(image, np.array([settings.top_left, settings.top_right,
                                                         settings.bottom_right, settings.bottom_left], np.float32))
    warped_image = cv2.resize(warped_image, (settings.image_height, int(settings.image_height * RATIO_HEIGHT_WIDTH)))
    # cv2.imwrite('warped.jpg', warped_image)
    hsvImg = cv2.cvtColor(warped_image, cv2.COLOR_BGR2HSV)

    filtered_image = filter(hsvImg,
                            (purpose['hMin'], purpose['sMin'], purpose['vMin']),
                            (purpose['hMax'], purpose['sMax'], purpose['vMax']))
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


def resize_image(image):
    if settings.image_height is not None:
        h, w, c = image.shape
        ratio = settings.image_height / max(h, w)
        if ratio < 1:
            return cv2.resize(image, (int(w * ratio), int(h * ratio)), interpolation=cv2.INTER_AREA)

    return image


def get_bot_overlay():
    pass


def overlay(*args):
    oly = np.array(args[0])
    # oly = cv2.cvtColor(oly, cv2.COLOR_GRAY2HSV)
    for arg in args[1:]:
        oly += arg
    return oly


def draw_bot(position, front):
    img = settings.maze['image']
    if hasattr(img, 'shape'):
        image = np.zeros(settings.maze['image'].shape, np.float32)
    else:
        image = np.zeros((img.width(), img.height()), np.float32)
    try:
        arrow_tip = (int(front[0]), int(front[1]))
        position = (int(position[0]), int(position[1]))
        # image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.arrowedLine(image, position, arrow_tip, (180, 255, 255), 2)
        return image
    except TypeError:
        print "Bot missing!"
        return image


