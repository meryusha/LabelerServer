# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget
import sys
from os.path import dirname, join, exists
import pathlib
# from detection_server import *
from .detection_client import ThreadedClient

class FasterRCNN(QWidget):
 
    objectFound = pyqtSignal(list, str)  # (list, str) as [x,y,w,h]] and label
    objectsFound = pyqtSignal(tuple)  # tuple of (list, list) with BB and corresponding labels
    errorWithInference = pyqtSignal(str, str) #error message

    def __init__(self):
        super(FasterRCNN, self).__init__()

    def detectObjects(self, image_path):
        print('detectObjects is called')
        # start_time = time.time()
        if image_path is None:
            self.errorWithInference.emit(u'Could not detect boxes', 'Image path is None' )
            return
        client = ThreadedClient("", 8000)
        if client.connectToServer():
            tup = client.sendDetectionImage(image_path)
            if not tup:
                self.errorWithInference.emit(u'Could not detect boxes', 'Server stopped replying ' )
                return
            (boxes, labels_words, scores) =  tup
            self.objectsFound.emit((boxes, labels_words, scores))
        else:
            self.errorWithInference.emit(u'Could not detect boxes', 'Server is broken' )
        # print("Time: {:.2f} s / img".format(time.time() - start_time))

        return
