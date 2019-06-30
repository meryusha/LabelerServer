#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import os
import sys
from datetime import datetime
import argparse
import logging

from libs.config import CFG

try:
    from PyQt5.QtWidgets import QApplication
except ImportError:
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtCore import QApplication

from libs.lib import newIcon
from gui.LabelerWindow import LabelerWindow
from api.ObjectDetection import FasterRCNN


class ActiveImageLabelerWindow(LabelerWindow):

    def __init__(self,
                 defaultFilename=None,
                 defaultPrefdefClassFile=os.path.join(
                     os.path.dirname(sys.argv[0]), 'data',
                     'predefined_classes.txt'),
                 defaultSaveDir=None):
        super(ActiveImageLabelerWindow,
              self).__init__(defaultFilename, defaultPrefdefClassFile,
                             defaultSaveDir)
        self.pippo = 1


if __name__ == '__main__':
    '''construct main app and run it'''

    # Argument Parser
    parser = argparse.ArgumentParser(
        description="Image Labeler based on Active Learning")
    parser.add_argument("--defaultFilename",
                        default=None,
                        type=str,
                        help="defaultFilename")
    parser.add_argument("--defaultPrefdefClassFile",
                        default='predefined_classes.txt',
                        type=str,
                        help="defaultPrefdefClassFile")
    parser.add_argument("--defaultSaveDir",
                        default=None,
                        type=str,
                        help="defaultSaveDir")
    args = parser.parse_args()

    # define logging level (DEBUG/INFO/WARNING/ERROR)
    numeric_level = getattr(logging, CFG.logging.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % CFG.logging.loglevel)

    # set up logging configuration
    os.makedirs(CFG.logging.loggingPath, exist_ok=True)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        handlers=[
            # file handler
            logging.FileHandler(
                os.path.join(CFG.logging.loggingPath,
                             datetime.now().strftime('%Y-%m-%d %H-%M-%S.log'))),
            # stream handler
            logging.StreamHandler()
        ])
    # logging.info(f"Running with config:\n{CFG}")

    # create QtApplication
    app = QApplication(sys.argv)
    app.setApplicationName("ActiveImageLabeler")
    app.setWindowIcon(newIcon("app"))

    # Create GUI
    win = ActiveImageLabelerWindow(args.defaultFilename,
                                   args.defaultPrefdefClassFile,
                                   args.defaultSaveDir)
    # Create API
    api = FasterRCNN()

    # Connect API to GUI
    # GUI detection button connected to API Object Detection
    # (parameter is OpenCV Image)
    win.detect.triggered.connect(lambda: api.detectObjects(win.filePath))
    # win.detect.triggered.connect(lambda: api.detectObjects(win.image))
    # API Object Found connected to Window add Shape to current Image
    api.ObjectFound.connect(win.addShape)
    api.ObjectsFound.connect(win.addShapes)

    # Show window and run QtApplication
    win.showMaximized()
    sys.exit(app.exec_())
