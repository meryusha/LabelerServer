import random
import os
from libs.category import Category
from libs.shape import Shape
from libs.constants import IMAGE_DEFAULT_SCORE, IMAGE_HUMAN_VERIFIED_SCORE
from libs.pascal_voc_io import PascalVocReader
from libs.pascal_voc_io import XML_EXT
from libs.yolo_io import YoloReader
from libs.yolo_io import TXT_EXT
from libs.lib import struct, newAction, newIcon, addActions, fmtShortcut, generateColorByText
try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

class Image(object):
    
    def __init__(self,  path, name = None, label_file = None, score = IMAGE_DEFAULT_SCORE):
        self.name = name
        #TODO get name from the path?, raise error if project is None
        self.path = path
        self._is_verified = False
        self.label_file = label_file
        # self.annotations = []
        # self.category = category
        self.score = score

    
    @property
    def is_verified(self):
        return self._is_verified
    
    def load_labels(self, window, image_data):
        if self.label_file:
            print('TRYING TO LOAD LABELS from object')
            self.load_shapes(window, self.label_file.shapes)
        else:                        
            print('TRYING TO LOAD LABELS from file')     
            if self.path is not None:
                basename = os.path.splitext(self.path)[0]
                xmlPath = os.path.join(basename + XML_EXT)
                txtPath = os.path.join( basename + TXT_EXT)
                if os.path.isfile(xmlPath):
                    self.load_labels_from_file(window, xmlPath, True)
                elif os.path.isfile(txtPath):
                    self.load_labels_from_file(window, txtPath, False, image_data)

    def load_labels_from_file(self, window, annotationFilePath, is_VOC = True, image_data = None):
        if not os.path.isfile(annotationFilePath) :
            return
        if is_VOC:
            parseReader = PascalVocReader(annotationFilePath)
        else: 
            if image_data:
                parseReader = YoloReader(annotationFilePath, QImage.fromData(image_data))
        if parseReader:
            shapes = parseReader.getShapes()
            self.load_shapes(window, shapes)
        # self.canvas.verified = parseReader.verified

    def load_shapes(self, window,  shapes):
        s = []
        # print(shapes)
        for label, points, line_color, fill_color, difficult in shapes:
            shape = Shape(label=label)
            for x, y in points:
                # Ensure the labels are within the bounds of the image. If not, fix them.
                x, y, snapped = window.canvas.snapPointToCanvas(x, y)
                if snapped:
                    window.setUnsavedChanges()
                shape.addPoint(QPointF(x, y))
                shape.difficult = difficult
                shape.close()
                s.append(shape)

            if line_color:
                shape.line_color = QColor(*line_color)
            else:
                shape.line_color = generateColorByText(label)

            if fill_color:
                shape.fill_color = QColor(*fill_color)
            else:
                shape.fill_color = generateColorByText(label)

            window.addLabel(shape)

        window.canvas.loadShapes(s)

    def save_labels_to_path(self, canvas, annotationFilePath, is_VOC):
        annotationFilePath = ustr(annotationFilePath)
        if self.label_file is None:
            self.label_file = LabelFile()
            self.label_file.is_verified = self._is_verified

        def format_shape(s):
            return dict(label=s.label,
                        line_color=s.line_color.getRgb(),
                        fill_color=s.fill_color.getRgb(),
                        points=[(p.x(), p.y()) for p in s.points],
                       # add chris
                        difficult = s.difficult)
        if canvas is None:
            return False
        shapes = [format_shape(shape) for shape in canvas.shapes]
        # Can add differrent annotation formats here
        try:
            if is_VOC :
                if annotationFilePath[-4:].lower() != ".xml":
                    annotationFilePath += XML_EXT
                self.label_file.savePascalVocFormat(annotationFilePath, shapes, 
                                                   Shape.lineColor.getRgb(), Shape.fillColor.getRgb())
                return True
            elif self.usingYoloFormat is True:
                if annotationFilePath[-4:].lower() != ".txt":
                    annotationFilePath += TXT_EXT
                self.label_file.savesYoloFormat(annotationFilePath, shapes, [],   # self.project.categories,
                                                  Shape.lineColor.getRgb(), Shape.fillColor.getRgb())
         
                return True
        except LabelFileError as e:
            self.errorMessage(u'Error saving label data', u'<b>%s</b>' % e)
        return False

    def save_labels(self, canvas, is_VOC = True):
        if self.label_file:
            savedFileName = os.path.splitext(self.name)[0]
            annotationFilePath = os.path.join(ustr(self.project.path), savedFileName)
            if self.save_labels_to_path(canvas, annotationFilePath, is_VOC):
                self.setFileSaved()
                self.statusBar().showMessage('Saved to  %s' % annotationFilePath)
                self.statusBar().show()

     


    def verify(self):
        if self.label_file is not None:
            self._is_verified = True
        

