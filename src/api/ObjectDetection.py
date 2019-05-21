from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class FasterRCNN(QWidget):
    ObjectFound = pyqtSignal(list, str)

    def __init__(self):
        super(FasterRCNN, self).__init__()
        self.pippo = 1

    def detectObjects(self, image):
        print("FasterRCNN detectObjects")
        self.ObjectFound.emit([100, 100, 30, 200], "myLabelClass")
        return
        # self.detect.triggered.connect()
