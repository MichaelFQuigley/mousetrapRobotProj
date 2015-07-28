import cv2


def find_the_object(img):
    ret, thresh = cv2.threshold(img, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)

    cnt = contours[0]
    largest_area = 0
    for contour in contours:
        a = cv2.contourArea(contour, False)
        if a > largest_area:
            cnt = contour

    pnt, radius = cv2.minEnclosingCircle(cnt)
    return pnt
