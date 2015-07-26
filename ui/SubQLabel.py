from PyQt4 import QtGui, QtCore, Qt
import main


class SubQLabel(QtGui.QLabel):

    set_point = QtCore.pyqtSignal(int, int)

    def __init__(self):
        super(SubQLabel, self).__init__()
        self.imageWidth = 1
        self.imageHeight = 1
        self.calibration = ((), (), (), ())
        self.calibration_pos = 0

    def mousePressEvent(self, e):
        x = e.x()
        y = e.y()
        wdiff = self.width() - self.imageWidth
        hdiff = self.height() - self.imageHeight
        x_img = x - (wdiff / 2)
        y_img = y - (hdiff / 2)

        if e.button() == QtCore.Qt.LeftButton:
            print("Image clicked at pos: ({}, {}).".format(x_img, y_img))
        elif e.button() == QtCore.Qt.RightButton:
            self.set_point.emit(x_img, y_img)
            self.calibration_pos += 1


    def setPixmap(self, pixmap):
        super(SubQLabel, self).setPixmap(pixmap)
        self.imageWidth = pixmap.width()
        self.imageHeight = pixmap.height()
