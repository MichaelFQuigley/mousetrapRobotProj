__author__ = 'zgrogan'
from PyQt4 import QtGui
from PyQt4.QtGui import QImage, qRgb
import numpy as np
import cv2
import sys
sys.path.insert(0, '../objectDetection')
import objectDetection
sys.path.insert(0, '../imageTransform')
import imageTransform



class ImageWidget(QtGui.QLabel):
    def __init__(self, parent):
        super(ImageWidget, self).__init__()
        self.gray_color_table = [qRgb(i, i, i) for i in range(256)]
        self.initWidget()

    def initWidget(self):
        self.setScaledContents(True)

    def showCVImage(self, cvimage):
        qimg = self.toQImage(cvimage).scaled(self.size())
        self.setPixmap(QtGui.QPixmap.fromImage(qimg))

    # toQImage implementation
    class NotImplementedException:
        pass

    def toQImage(self, im, copy=False):
        if im is None:
            return QImage()

        if im.dtype == np.uint8:
            if len(im.shape) == 2:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
                qim.setColorTable(self.gray_color_table)
                return qim.copy() if copy else qim

            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
                    return qim.copy() if copy else qim
                elif im.shape[2] == 4:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32)
                    return qim.copy() if copy else qim

        raise NotImplementedException

    # required: params['image']
    def transformedImage(self, img, pts):
        return


    # required: params['source'], the path to the image to be filtered
    def filterImage(self, params):
        img = params.get('image')
        filterMins = params.get('filterMins', (0, 0, 0))
        filterMaxs = params.get('filterMaxs', (255, 255, 255))
        dilation = params.get('dilation', (0, 0))
        erosion = params.get('erosion', (0, 0))

        filteredImg = objectDetection.filter(img, filterMins, filterMaxs)
        return objectDetection.postProcess(filteredImg, dilation, erosion)


