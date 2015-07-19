import cameras
from PyQt4 import QtCore, QtGui
from PIL import ImageQt
import numpy as np
import Image

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Mousetrap Navigator')
        self.setWindowIcon(QtGui.QIcon('img/mousetrap.png'))

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)

        self.raw = QtGui.QLabel()
        self.raw.resize(640, 640)
        hbox.addWidget(self.raw)

        self.processed = QtGui.QLabel()
        self.processed.resize(640, 640)
        hbox.addWidget(self.processed)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def on_image_ready(self, orig, new):
        self.raw.setPixmap(as_pixmap(orig))
        self.processed.setPixmap(as_pixmap(new))

def as_pixmap(frame):
    pil_image = Image.fromarray(np.uint8(frame))
    qt_image = ImageQt.ImageQt(pil_image)
    return QtGui.QPixmap.fromImage(qt_image)
