# Copyright (c) 2016 Tzutalin
# Create by TzuTaLin <tzu.ta.lin@gmail.com>

try:
    from PyQt5.QtGui import QImage
except ImportError:
    from PyQt4.QtGui import QImage

from base64 import b64encode, b64decode
from libs.pascal_voc_io import PascalVocWriter
from libs.yolo_io import YOLOWriter
from libs.pascal_voc_io import XML_EXT
import os.path
import sys


class LabelFileError(Exception):
    pass


class LabelFile(object):
    # It might be changed as window creates. By default, using XML ext
    # suffix = '.lif'
    suffix = XML_EXT

    def __init__(self, image = None, path = None):
        # self.shapes = ()
        self.image = image
        self.path = path
        self.is_verified = False

    def savePascalVocFormat(self, shapes,
                            lineColor=None, fillColor=None, databaseSrc=None):
        imgFolderPath = os.path.dirname(self.image.path)
        imgFolderName = os.path.split(imgFolderPath)[-1]
        imgFileName = os.path.basename(self.image.path)
        #imgFileNameWithoutExt = os.path.splitext(imgFileName)[0]
        image = QImage()
        image.load(self.image.path)
        imageShape = [image.height(), image.width(),
                      1 if image.isGrayscale() else 3]
        writer = PascalVocWriter(imgFolderName, imgFileName,
                                 imageShape, localImgPath=self.image.path)
        writer.verified = self.image.is_verified
        print('len of shapes is', len(shapes))
        for shape in shapes:
            points = shape['points']
            label = shape['label']
            # Add Chris
            difficult = int(shape['difficult'])
            bndbox = LabelFile.convertPoints2BndBox(points)
            writer.addBndBox(bndbox[0], bndbox[1], bndbox[2], bndbox[3], label, difficult)

        writer.save(targetFile = self.path)
        return

    def saveYoloFormat(self, shapes, classList,
                            lineColor=None, fillColor=None, databaseSrc=None):
        imgFolderPath = os.path.dirname(self.image.path)
        imgFolderName = os.path.split(imgFolderPath)[-1]
        imgFileName = os.path.basename(self.image.path)
        #imgFileNameWithoutExt = os.path.splitext(imgFileName)[0]
        image = QImage()
        image.load(self.image.path)
        imageShape = [image.height(), image.width(),
                      1 if image.isGrayscale() else 3]
        writer = YOLOWriter(imgFolderName, imgFileName,
                                 imageShape, localImgPath=self.image.path)
        writer.verified = self.image.is_verified()

        for shape in shapes:
            points = shape['points']
            label = shape['label']
            # Add Chris
            difficult = int(shape['difficult'])
            bndbox = LabelFile.convertPoints2BndBox(points)
            writer.addBndBox(bndbox[0], bndbox[1], bndbox[2], bndbox[3], label, difficult)

        writer.save(targetFile = self.path, classList=classList)
        return

    # def toggleVerify(self):
    #     self.verified = not self.verified


    @staticmethod
    def isLabelFile(filename):
        fileSuffix = os.path.splitext(filename)[1].lower()
        return fileSuffix == LabelFile.suffix

    @staticmethod
    def convertPoints2BndBox(points):
        xmin = float('inf')
        ymin = float('inf')
        xmax = float('-inf')
        ymax = float('-inf')
        for p in points:
            x = p[0]
            y = p[1]
            xmin = min(x, xmin)
            ymin = min(y, ymin)
            xmax = max(x, xmax)
            ymax = max(y, ymax)

        # Martin Kersner, 2015/11/12
        # 0-valued coordinates of BB caused an error while
        # training faster-rcnn object detector.
        if xmin < 1:
            xmin = 1

        if ymin < 1:
            ymin = 1

        return (int(xmin), int(ymin), int(xmax), int(ymax))
