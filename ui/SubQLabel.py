from PyQt4 import QtGui, QtCore, Qt


class SubQLabel(QtGui.QLabel):
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
        elif e.button() == QtCore.Qt.MiddleButton:
            # TODO: make it fire an event, passing in the position
            pass


    def setPixmap(self, pixmap):
        super(SubQLabel, self).setPixmap(pixmap)
        self.imageWidth = pixmap.width()
        self.imageHeight = pixmap.height()

