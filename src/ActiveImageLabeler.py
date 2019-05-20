#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import codecs
# import distutils.spawn
import os.path
import os
# import platform
# import re
import sys
# import subprocess

# try:
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
# except ImportError:
#     # needed for py3+qt4
#     # Ref:
#     # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
#     # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
#     if sys.version_info.major >= 3:
#         import sip
#         sip.setapi('QVariant', 2)
#     from PyQt4.QtGui import *
#     from PyQt4.QtCore import *

from libs.lib import newIcon
# import numpy as np

__appname__ = 'labelImg'


from gui import MainWindow

class ActiveImageLabelerWindow(MainWindow):

    def __init__(self, 
    defaultFilename=None, 
    defaultPrefdefClassFile=os.path.join(
                         os.path.dirname(sys.argv[0]),
                         'data', 'predefined_classes.txt'), 
    defaultSaveDir=None):
        super(ActiveImageLabelerWindow, self).__init__(defaultFilename, defaultPrefdefClassFile, defaultSaveDir)
        self.pippo = 1
        # self.detect.triggered.connect()
    


    
from api import FasterRCNN

def main():
    '''construct main app and run it'''
    """
    Standard boilerplate Qt application code.
    Do everything but app.exec_() -- so that we can test the application in one thread
    """
    app = QApplication(sys.argv)
    app.setApplicationName(__appname__)
    app.setWindowIcon(newIcon("app"))
    # Tzutalin 201705+: Accept extra agruments to change predefined class file
    # Usage : labelImg.py image predefClassFile saveDir
    #TODO argparse
    win = ActiveImageLabelerWindow(sys.argv[1] if len(sys.argv) >= 2 else None,
                     sys.argv[2] if len(sys.argv) >= 3 else os.path.join(
                         os.path.dirname(sys.argv[0]),
                         'data', 'predefined_classes.txt'),
                     sys.argv[3] if len(sys.argv) >= 4 else None)

    api = FasterRCNN()
    # GUI detection button connected to API Object Detection (parameter is OpenCV Image)
    # win.detect.triggered.connect(api.detectObjects)
    # API Object Found connected to Window add Shape to current Image
    api.ObjectFound.connect(win.addShape)

    win.show()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
