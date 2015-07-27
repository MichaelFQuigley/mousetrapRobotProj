from PyQt4 import QtGui, QtCore


class SubQLabel(QtGui.QLabel):
    left_click = QtCore.pyqtSignal(int, int)
    right_click = QtCore.pyqtSignal(int, int)

    def __init__(self):
        super(SubQLabel, self).__init__()
        self.pixmap = QtGui.QPixmap()
        self.imageWidth = 1
        self.imageHeight = 1
        self.calibration = ((), (), (), ())
        self.setMinimumHeight(300)
        self.setMinimumWidth(300)
        self.setMaximumHeight(1080)
        self.setMaximumWidth(1920)
        self.scale_factor = 1.0

    def mousePressEvent(self, e):
        x = e.x()
        y = e.y()
        wdiff = self.width() - self.imageWidth
        hdiff = self.height() - self.imageHeight
        x_img = (x - (wdiff / 2)) / self.scale_factor
        y_img = (y - (hdiff / 2)) / self.scale_factor

        if e.button() == QtCore.Qt.LeftButton:
            self.left_click.emit(x_img, y_img)
        elif e.button() == QtCore.Qt.RightButton:
            self.right_click.emit(x_img, y_img)

    def setPixmap(self, pixmap):
        scaled_map = pixmap.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio)
        super(SubQLabel, self).setPixmap(scaled_map)
        self.scale_factor = float(scaled_map.width()) / pixmap.width()
        self.imageWidth = scaled_map.width()
        self.imageHeight = scaled_map.height()

