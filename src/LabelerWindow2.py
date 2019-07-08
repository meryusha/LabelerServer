#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import distutils.spawn
import os.path
import platform
import re
import sys
import subprocess

from time import sleep
from functools import partial
from collections import defaultdict
import logging
try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    # if sys.version_info.major >= 3:
    #     import sip
    #     sip.setapi('QVariant', 2)
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *


import resources
# Add internal libs
from libs.constants import *
from libs.lib import struct, newAction, newIcon, addActions, fmtShortcut, generateColorByText
from libs.settings import Settings
from libs.shape import Shape, DEFAULT_LINE_COLOR, DEFAULT_FILL_COLOR
from libs.stringBundle import StringBundle
from libs.canvas import Canvas
from libs.zoomWidget import ZoomWidget
from libs.labelDialog import LabelDialog
from libs.colorDialog import ColorDialog
from libs.labelFile import LabelFile, LabelFileError
from libs.toolBar import ToolBar
from libs.pascal_voc_io import PascalVocReader
from libs.pascal_voc_io import XML_EXT
from libs.yolo_io import YoloReader
from libs.yolo_io import TXT_EXT
from libs.ustr import ustr
from libs.version import __version__
from libs.hashableQListWidgetItem import HashableQListWidgetItem

import collections
import numpy as np

__appname__ = 'labelImg'




from gui.ui_mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets


class LabelerWindow2(QMainWindow, Ui_MainWindow):
    FIT_WINDOW, FIT_WIDTH, MANUAL_ZOOM = list(range(3))

    def __init__(self, model, controller):
        super(LabelerWindow, self).__init__()
        # QtCore.QMetaObject.connectSlotsByName(self) #TODO connect SlotsByName!

        self.setupUi(self)

        self._model = model 
        self._controller = controller
        self._controller.restore_app_state()
        self.build_model_signals()
        self.build_controller_signals()

        # # Load string bundle for i18n
        # self.stringBundle = StringBundle.getBundle()
        # getStr = lambda strId: self.stringBundle.getString(strId)
        self.screencastViewer = self.getAvailableScreencastViewer()
        #TODO: put our tutorial there
        self.screencast = "https://youtu.be/p0nR2YsCY_U"


         # what is it? 
        self._noSelectionSlot = False

        # Main widgets and related state.
        self.labelDialog = LabelDialog(parent=self, listItem=self._controller.labelHist)

        self.itemsToShapes = {}
        self.shapesToItems = {}
        self.prevLabelText = ''

        self.diffcButton.stateChanged.connect(self.btnstate)
       
        self.labelList.itemActivated.connect(self.labelSelectionChanged)
        self.labelList.itemSelectionChanged.connect(self.labelSelectionChanged)
        self.labelList.itemDoubleClicked.connect(self.editLabel)

        self.labelList.itemChanged.connect(self.labelItemChanged)
      
        self.fileListWidget.itemDoubleClicked.connect(self.fileitemDoubleClicked)
   

        self.zoomWidget = ZoomWidget()
        self.colorDialog = ColorDialog(parent=self)

        self.canvas = Canvas(parent=self)
        self.canvas.zoomRequest.connect(self.zoomRequest)
      
        self.scroll.setWidget(self.canvas)
        # scroll.setWidgetResizable(True)
        self.scrollBars = {
            Qt.Vertical: self.scroll.verticalScrollBar(),
            Qt.Horizontal: self.scroll.horizontalScrollBar()
        }
        # self.scrollArea = self.scroll
        self.canvas.scrollRequest.connect(self.scrollRequest)

        self.canvas.newShape.connect(self.newShape)
        self.canvas.newShapes.connect(self.newShapes)
        self.canvas.shapeMoved.connect(self.setDirty)
        self.canvas.selectionChanged.connect(self.shapeSelectionChanged)
        self.canvas.drawingPolygon.connect(self.toggleDrawingSensitive)

      
        action = partial(newAction, self)

        self.quit.triggered.connect(self.close)
       
        self.open.triggered.connect(self.openFile)
      

        self.opendir.triggered.connect(self.openDirDialog)
      
        self.changeSavedir.triggered.connect(self.changeSavedirDialog)


        self.openAnnotation.triggered.connect(self.openAnnotationDialog)

        self.openNextImgAction.triggered.connect(self.openNextImg)

      
        self.openPrevImgAction.triggered.connect(self.openPrevImg)

       
        self.verify.triggered.connect(self.verifyImg)

   
        self.save.triggered.connect(self.saveFile)

        self.save_format.triggered.connect(self.change_format)

        self.saveAs.triggered.connect(self.saveFileAs)

        self.closeAction.triggered.connect(self.closeFile)

        self.resetAllAction.triggered.connect(self.resetAll)
        self.color1.triggered.connect(self.chooseColor1)


        self.createMode.triggered.connect(self.setCreateMode)

        self.editMode.triggered.connect(self.setEditMode)



        self.create.triggered.connect(self.createShape)

        self.deleteAction.triggered.connect(self.deleteSelectedShape)

        self.copy.triggered.connect(self.copySelectedShape)
       

        self.hideAll.triggered.connect(partial(self.togglePolygons, False))
        self.showAll.triggered.connect(partial(self.togglePolygons, True))



        self.help.triggered.connect(self.showTutorialDialog)
        self.showInfo.triggered.connect(self.showInfoDialog)

      
        zoom = QWidgetAction(self)
        zoom.setDefaultWidget(self.zoomWidget)
        self.zoomWidget.setWhatsThis(
            u"Zoom in or out of the image. Also accessible with"
            " %s and %s from the canvas." % (fmtShortcut("Ctrl+[-+]"),
                                             fmtShortcut("Ctrl+Wheel")))
        self.zoomWidget.setEnabled(False)


        self.zoomIn.triggered.connect(partial(self.addZoom, 10))
        self.zoomOut.triggered.connect(partial(self.addZoom, -10))
        self.zoomOrg.triggered.connect(partial(self.setZoom, 100))


        self.fitWindow.triggered.connect(self.setFitWindow)
        self.fitWidth.triggered.connect(self.setFitWidth)


        self.zoomActions = (self.zoomWidget, self.zoomIn, self.zoomOut,
                       self.zoomOrg, self.fitWindow, self.fitWidth)
        self.zoomMode = self.MANUAL_ZOOM
        self.scalers = {
            self.FIT_WINDOW: self.scaleFitWindow,
            self.FIT_WIDTH: self.scaleFitWidth,
            # Set to one to scale to 100% when loading files.
            self.MANUAL_ZOOM: lambda: 1,
        }

        self.edit.triggered.connect(self.editLabel)

        self.editButton.setDefaultAction(self.edit)


        self.shapeLineColor.triggered.connect(self.chshapeLineColor)
        self.shapeFillColor.triggered.connect(self.chshapeFillColor)


        self.labelMenu = QMenu()
        addActions(self.labelMenu, (self.edit, self.deleteAction))
        self.labelList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.labelList.customContextMenuRequested.connect(
            self.popLabelListMenu)

        self.onLoadActive = (self.closeAction, self.create, self.detect,
                          self.createMode, self.editMode)

        # Active actions when Shape are present
        self.onShapesPresent = (self.saveAs, self.hideAll, self.showAll)

      
        self.lastLabel = None
       
        self.displayLabelOption.triggered.connect(self.togglePaintLabelsOption)



        self.menu_File.aboutToShow.connect(self.updateFileMenu)

        # STATUS BAR
        self.statusBar().showMessage('%s started.' % __appname__)
        self.statusBar().show()


        # Since loading the file may take some time, make sure it runs in the background.
        if self.filePath and os.path.isdir(self.filePath):
            self.queueEvent(partial(self.importDirImages, self.filePath or ""))
        elif self.filePath:
            self.queueEvent(partial(self.loadFile, self.filePath or ""))

        # Callbacks:
        self.zoomWidget.valueChanged.connect(self.paintCanvas)

        # self.populateModeActions()

        # Display cursor coordinates at the right of status bar
        self.labelCoordinates = QLabel('')
        self.statusBar().addPermanentWidget(self.labelCoordinates)

        # Open Dir if deafult file
        if self.filePath and os.path.isdir(self.filePath):
            self.openDirDialog(dirpath=self.filePath)

    def build_model_signals(self):
        self._model.settings_loaded.connect(self.restore_app_state)
        self._model.update_status_bar.connect(self.update_status_bar)

    def build_controller_signals(self):
        


    #listening to amodel signals
    def restore_app_state(self):
        self.autoSaving.setChecked(self._model.settings.get(SETTING_AUTO_SAVE, False))
        self.singleClassMode.setChecked(self._model.settings.get(SETTING_SINGLE_CLASS, False))
        self.displayLabelOption.setChecked(self._model.settings.get(SETTING_PAINT_LABEL, False))
        size = self._model.settings.get(SETTING_WIN_SIZE, QSize(600, 500))
        position = QPoint(0, 0)
        saved_position = self._model.settings.get(SETTING_WIN_POSE, position)
        # Fix the multiple monitors issue
        for i in range(QApplication.desktop().screenCount()):
            if QApplication.desktop().availableGeometry(i).contains(saved_position):
                position = saved_position
                break
        self.resize(size)
        self.move(position)
        self.restoreState(self._model.settings.get(SETTING_WIN_STATE, QByteArray()))
        # Populate the File menu dynamically.
        self.updateFileMenu()

    #listening to model signals
    def update_status_bar(self, dir):
        self.statusBar().showMessage('%s started. Annotation will be saved to %s' %(__appname__, dir))
        self.statusBar().show() 

    def getAvailableScreencastViewer(self):
        osName = platform.system()

        if osName == 'Windows':
            return ['C:\\Program Files\\Internet Explorer\\iexplore.exe']
        elif osName == 'Linux':
            return ['xdg-open']
        elif osName == 'Darwin':
            return ['open', '-a', 'Safari']

    ## Callbacks ##
    def showTutorialDialog(self):
        subprocess.Popen(self.screencastViewer + [self.screencast])

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.canvas.setDrawingShapeToSquare(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            # Draw rectangle if Ctrl is pressed
            self.canvas.setDrawingShapeToSquare(True)

    ## Support Functions ##
    def set_format(self, save_format):
        if save_format == FORMAT_PASCALVOC:
            self.save_format.setText(FORMAT_PASCALVOC)
            self.save_format.setIcon(newIcon("format_voc"))
            self.usingPascalVocFormat = True
            self.usingYoloFormat = False
            LabelFile.suffix = XML_EXT

        elif save_format == FORMAT_YOLO:
            self.save_format.setText(FORMAT_YOLO)
            self.save_format.setIcon(newIcon("format_yolo"))
            self.usingPascalVocFormat = False
            self.usingYoloFormat = True
            LabelFile.suffix = TXT_EXT

    def change_format(self):
        if self.usingPascalVocFormat: self.set_format(FORMAT_YOLO)
        elif self.usingYoloFormat: self.set_format(FORMAT_PASCALVOC)

    def noShapes(self):
        return not self.itemsToShapes

    def setDirty(self):
        self.dirty = True
        self.save.setEnabled(True)

    def setClean(self):
        self.dirty = False
        self.save.setEnabled(False)
        self.create.setEnabled(True)
        self.detect.setEnabled(True)

    def toggleActions(self, value=True):
        """Enable/Disable widgets which depend on an opened image."""
        for z in self.zoomActions:
            z.setEnabled(value)
        for action in self.onLoadActive:
            action.setEnabled(value)

    def queueEvent(self, function):
        QTimer.singleShot(0, function)

    def status(self, message, delay=5000):
        self.statusBar().showMessage(message, delay)

    def resetState(self):
        self.itemsToShapes.clear()
        self.shapesToItems.clear()
        self.labelList.clear()
        self.filePath = None
        self.imageData = None
        self.labelFile = None
        self.canvas.resetState()
        self.labelCoordinates.clear()

    def currentItem(self):
        items = self.labelList.selectedItems()
        if items:
            return items[0]
        return None

    def addRecentFile(self, filePath):
        if filePath in self._model.recentFiles:
            self.recentFiles.remove(filePath)
        elif len(self.recentFiles) >= self.maxRecent:
            self.recentFiles.pop()
        self.recentFiles.insert(0, filePath)

   

    def showInfoDialog(self):
        msg = u'Name:{0} \nApp Version:{1} \n{2} '.format(__appname__, __version__, sys.version_info)
        QMessageBox.information(self, u'Information', msg)

    def createShape(self):
        # assert self.beginner()
        self.canvas.setEditing(False)
        self.create.setEnabled(False)
        self.detect.setEnabled(False)
        self.updateCount()


    # def detectShape(self):
    #     # assert self.beginner()
    #     # self.canvas.setEditing(False)
    #     # self.actions.create.setEnabled(False)
    #     # self.actions.detect.setEnabled(False)
    #     self.canvas.detectShapes(self.image)
    #     self.updateCount()

    @property
    def imageCV(self):
        return self.canvas.fromQTtoCV(self.image)


    def toggleDrawingSensitive(self, drawing=True):
        """In the middle of drawing, toggling between modes should be disabled."""
        self.editMode.setEnabled(not drawing)
        if not drawing:
            # Cancel creation.
            print('Cancel creation.')
            self.canvas.setEditing(True)
            self.canvas.restoreCursor()
            self.create.setEnabled(True)
            self.detect.setEnabled(True)

    def toggleDrawMode(self, edit=True):
        self.canvas.setEditing(edit)
        self.createMode.setEnabled(edit)
        self.editMode.setEnabled(not edit)

    def setCreateMode(self):
        # assert self.advanced()
        self.toggleDrawMode(False)

    def setEditMode(self):
        # assert self.advanced()
        self.toggleDrawMode(True)
        self.labelSelectionChanged()

    def updateFileMenu(self):
        currFilePath = self._model.filePath

        def exists(filename):
            return os.path.exists(filename)
        menu = self.menu_RecentFiles
        menu.clear()
        files = [f for f in self.recentFiles if f !=
                 currFilePath and exists(f)]
        for i, f in enumerate(files):
            icon = newIcon('labels')
            action = QAction(
                icon, '&%d %s' % (i + 1, QFileInfo(f).fileName()), self)
            action.triggered.connect(partial(self.loadRecent, f))
            menu.addAction(action)

    def popLabelListMenu(self, point):
        print(point)
        # self.menu_Edit.exec_(self.labelList.mapToGlobal(point))
        self.labelMenu.exec_(self.labelList.mapToGlobal(point))

    def editLabel(self):
        if not self.canvas.editing():
            return
        item = self.currentItem()
        text = self.labelDialog.popUp(item.text())
        if text is not None:
            item.setText(text)
            item.setBackground(generateColorByText(text))
            self.setDirty()

    # Tzutalin 20160906 : Add file list and dock to move faster
    def fileitemDoubleClicked(self, item=None):
        currIndex = self.mImgList.index(ustr(item.text()))
        if currIndex < len(self.mImgList):
            filename = self.mImgList[currIndex]
            if filename:
                self.loadFile(filename)

    # Add chris
    def btnstate(self, item= None):
        """ Function to handle difficult examples
        Update on each object """
        if not self.canvas.editing():
            return

        item = self.currentItem()
        if not item: # If not selected Item, take the first one
            item = self.labelList.item(self.labelList.count()-1)

        difficult = self.diffcButton.isChecked()

        try:
            shape = self.itemsToShapes[item]
        except:
            pass
        # Checked and Update
        try:
            if difficult != shape.difficult:
                shape.difficult = difficult
                self.setDirty()
            else:  # User probably changed item visibility
                self.canvas.setShapeVisible(shape, item.checkState() == Qt.Checked)
        except:
            pass

    # React to canvas signals.
    def shapeSelectionChanged(self, selected=False):
        if self._noSelectionSlot:
            self._noSelectionSlot = False
        else:
            shape = self.canvas.selectedShape
            if shape:
                self.shapesToItems[shape].setSelected(True)
            else:
                self.labelList.clearSelection()
        self.deleteAction.setEnabled(selected)
        self.copy.setEnabled(selected)
        self.edit.setEnabled(selected)
        self.shapeLineColor.setEnabled(selected)
        self.shapeFillColor.setEnabled(selected)
        self.updateCount()

    def addLabel(self, shape):
        shape.paintLabel = self.displayLabelOption.isChecked()
        item = HashableQListWidgetItem(shape.label)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked)
        item.setBackground(generateColorByText(shape.label))
        self.itemsToShapes[item] = shape
        self.shapesToItems[shape] = item
        self.labelList.addItem(item)
        for action in self.onShapesPresent:
            action.setEnabled(True)
        self.updateCount()

    def updateCount(self):
        cnt = collections.Counter(
            np.array([shape.label for shape in self.canvas.shapes]))
        # self.countLabel.setText([ c for c in cnt.most_common()])
        countString = [f"{cl} : {count} \n" for (cl, count) in cnt.most_common()]
        # self.countLabel.setText("".join(str(c) for c in cnt.most_common()))
        self.countLabel.setText("".join(c for c in countString ))

    def remLabel(self, shape):
        if shape is None:
            # print('rm empty label')
            return
        item = self.shapesToItems[shape]
        self.labelList.takeItem(self.labelList.row(item))
        del self.shapesToItems[shape]
        del self.itemsToShapes[item]
        self.updateCount()

    def loadLabels(self, shapes):
        s = []
        for label, points, line_color, fill_color, difficult in shapes:
            shape = Shape(label=label)
            for x, y in points:

                # Ensure the labels are within the bounds of the image. If not, fix them.
                x, y, snapped = self.canvas.snapPointToCanvas(x, y)
                if snapped:
                    self.setDirty()

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

            self.addLabel(shape)

        self.canvas.loadShapes(s)

    def saveLabels(self, annotationFilePath):
        annotationFilePath = ustr(annotationFilePath)
        if self.labelFile is None:
            self.labelFile = LabelFile()
            self.labelFile.verified = self.canvas.verified

        def format_shape(s):
            return dict(label=s.label,
                        line_color=s.line_color.getRgb(),
                        fill_color=s.fill_color.getRgb(),
                        points=[(p.x(), p.y()) for p in s.points],
                       # add chris
                        difficult = s.difficult)

        shapes = [format_shape(shape) for shape in self.canvas.shapes]
        # Can add differrent annotation formats here
        try:
            if self.usingPascalVocFormat is True:
                if annotationFilePath[-4:].lower() != ".xml":
                    annotationFilePath += XML_EXT
                self.labelFile.savePascalVocFormat(annotationFilePath, shapes, self.filePath, self.imageData,
                                                   self.lineColor.getRgb(), self.fillColor.getRgb())
            elif self.usingYoloFormat is True:
                if annotationFilePath[-4:].lower() != ".txt":
                    annotationFilePath += TXT_EXT
                self.labelFile.saveYoloFormat(annotationFilePath, shapes, self.filePath, self.imageData, self.labelHist,
                                                   self.lineColor.getRgb(), self.fillColor.getRgb())
            else:
                self.labelFile.save(annotationFilePath, shapes, self.filePath, self.imageData,
                                    self.lineColor.getRgb(), self.fillColor.getRgb())
            print('Image:{0} -> Annotation:{1}'.format(self.filePath, annotationFilePath))
            return True
        except LabelFileError as e:
            self.errorMessage(u'Error saving label data', u'<b>%s</b>' % e)
            return False

    def copySelectedShape(self):
        try:
            self.addLabel(self.canvas.copySelectedShape())
            # fix copy and delete
            self.shapeSelectionChanged(True)
        except:
            print("Error while duplicating shape")

    def labelSelectionChanged(self):
        item = self.currentItem()
        if item and self.canvas.editing():
            self._noSelectionSlot = True
            self.canvas.selectShape(self.itemsToShapes[item])
            shape = self.itemsToShapes[item]
            # Add Chris
            self.diffcButton.setChecked(shape.difficult)

    def labelItemChanged(self, item):
        shape = self.itemsToShapes[item]
        label = item.text()
        if label != shape.label:
            shape.label = item.text()
            shape.line_color = generateColorByText(shape.label)
            self.setDirty()
        else:  # User probably changed item visibility
            self.canvas.setShapeVisible(shape, item.checkState() == Qt.Checked)

    #params: tuple of (boxes, labels) 
    def addShapes(self, box_label_tup):
        boxes, labels = box_label_tup
        # add all shapes
        for box, label in zip(boxes, labels):
            # self.addShape(box, label)
            # TODO add all shape at once
            # print(label)
            minX, minY, maxX, maxY  = box
            self.canvas.current = Shape()
            self.canvas.current.addPoint(QPointF(minX, minY))
            self.canvas.current.addPoint(QPointF(maxX, minY))
            self.canvas.current.addPoint(QPointF(maxX, maxY))
            self.canvas.current.addPoint(QPointF(minX, maxY))
            self.canvas.current.label = str(label)
            self.canvas.current.close()
            self.canvas.shapes.append(self.canvas.current)

        # repaint only once
        self.canvas.current = None
        self.canvas.newShapes.emit(len(boxes))
        self.canvas.update()
        self.canvas.repaint()

    def addShape(self, box, label):
        # import pdb;
        # pyqtRemoveInputHook(); pdb.set_trace()
        # print("GUI addShape", box)
        # minX = box[0]
        # minY = box[1]
        # maxX = box[0] + box[2]
        # maxY = box[1] + box[3]
        minX = box[0]
        minY = box[1]
        maxX = box[2]
        maxY = box[3]
        self.canvas.current = Shape()
        self.canvas.current.addPoint(QPointF(minX, minY))
        self.canvas.current.addPoint(QPointF(maxX, minY))
        self.canvas.current.addPoint(QPointF(maxX, maxY))
        self.canvas.current.addPoint(QPointF(minX, maxY))
        self.canvas.current.label = label
        self.canvas.current.close()

        self.canvas.shapes.append(self.canvas.current)
        self.canvas.current = None
        self.canvas.newShape.emit()
        self.canvas.update()
        self.canvas.repaint()
        return



    # Callback functions:
    def newShapes(self, n):
        """Pop-up and give focus to the label editor.

        position MUST be in global coordinates.
        """
        for i in range(n):
            shape = self.canvas.shapes[-1 - i]
            # print(i, shape.label)
            if shape.label is not None:
                text = shape.label
            elif not self.useDefaultLabelCheckbox.isChecked() or not self.defaultLabelTextLine.text():
                if len(self.labelHist) > 0:
                    self.labelDialog = LabelDialog(
                        parent=self, listItem=self.labelHist)

                # Sync single class mode from PR#106
                if self.singleClassMode.isChecked() and self.lastLabel:
                    text = self.lastLabel
                else:
                    text = self.labelDialog.popUp(text=self.prevLabelText)
                    self.lastLabel = text
            else:
                text = self.defaultLabelTextLine.text()

            # Add Chris
            self.diffcButton.setChecked(False)
            if text is not None:
                self.prevLabelText = text
                generate_color = generateColorByText(text)
                # shape = self.canvas.setLastLabel(text, generate_color, generate_color)

                assert text
                shape.label = text
                if generate_color:
                    shape.line_color = generate_color

                if generate_color:
                    shape.fill_color = generate_color

                self.addLabel(shape)

                if text not in self.labelHist:
                    self.labelHist.append(text)
            else:
                # self.canvas.undoLastLine()
                self.canvas.resetAllLines()

        # if self.beginner():  # Switch to edit mode.
        self.canvas.setEditing(True)
        self.create.setEnabled(True)
        self.detect.setEnabled(True)
        # else:
        #     self.actions.editMode.setEnabled(True)
        self.setDirty()

    # Callback functions:
    def newShape(self):
        # import pdb
        # InputHook(); pdb.set_trace()
        """Pop-up and give focus to the label editor.

        position MUST be in global coordinates.
        """
        # print(self.canvas.shapes[-1].label)
        if self.canvas.shapes[-1].label is not None:
            text = self.canvas.shapes[-1].label
        elif not self.useDefaultLabelCheckbox.isChecked() or not self.defaultLabelTextLine.text():
            if len(self.labelHist) > 0:
                self.labelDialog = LabelDialog(
                    parent=self, listItem=self.labelHist)

            # Sync single class mode from PR#106
            if self.singleClassMode.isChecked() and self.lastLabel:
                text = self.lastLabel
            else:
                text = self.labelDialog.popUp(text=self.prevLabelText)
                self.lastLabel = text
        else:
            text = self.defaultLabelTextLine.text()

        # Add Chris
        self.diffcButton.setChecked(False)
        if text is not None:
            self.prevLabelText = text
            generate_color = generateColorByText(text)
            shape = self.canvas.setLastLabel(text, generate_color, generate_color)
            self.addLabel(shape)
            # if self.beginner():  # Switch to edit mode.
            self.canvas.setEditing(True)
            self.create.setEnabled(True)
            self.detect.setEnabled(True)
            # else:
            #     self.actions.editMode.setEnabled(True)
            self.setDirty()

            if text not in self.labelHist:
                self.labelHist.append(text)
        else:
            # self.canvas.undoLastLine()
            self.canvas.resetAllLines()

    def scrollRequest(self, delta, orientation):
        units = - delta / (8 * 15)
        bar = self.scrollBars[orientation]
        bar.setValue(bar.value() + bar.singleStep() * units)

    def setZoom(self, value):
        self.fitWidth.setChecked(False)
        self.fitWindow.setChecked(False)
        self.zoomMode = self.MANUAL_ZOOM
        self.zoomWidget.setValue(value)

    def addZoom(self, increment=10):
        self.setZoom(self.zoomWidget.value() + increment)

    def zoomRequest(self, delta):
        # get the current scrollbar positions
        # calculate the percentages ~ coordinates
        h_bar = self.scrollBars[Qt.Horizontal]
        v_bar = self.scrollBars[Qt.Vertical]

        # get the current maximum, to know the difference after zooming
        h_bar_max = h_bar.maximum()
        v_bar_max = v_bar.maximum()

        # get the cursor position and canvas size
        # calculate the desired movement from 0 to 1
        # where 0 = move left
        #       1 = move right
        # up and down analogous
        cursor = QCursor()
        pos = cursor.pos()
        relative_pos = QWidget.mapFromGlobal(self, pos)

        cursor_x = relative_pos.x()
        cursor_y = relative_pos.y()

        w = self.scroll.width()
        h = self.scroll.height()

        # the scaling from 0 to 1 has some padding
        # you don't have to hit the very leftmost pixel for a maximum-left movement
        margin = 0.1
        move_x = (cursor_x - margin * w) / (w - 2 * margin * w)
        move_y = (cursor_y - margin * h) / (h - 2 * margin * h)

        # clamp the values from 0 to 1
        move_x = min(max(move_x, 0), 1)
        move_y = min(max(move_y, 0), 1)

        # zoom in
        units = delta / (8 * 15)
        scale = 10
        self.addZoom(scale * units)

        # get the difference in scrollbar values
        # this is how far we can move
        d_h_bar_max = h_bar.maximum() - h_bar_max
        d_v_bar_max = v_bar.maximum() - v_bar_max

        # get the new scrollbar values
        new_h_bar_value = h_bar.value() + move_x * d_h_bar_max
        new_v_bar_value = v_bar.value() + move_y * d_v_bar_max

        h_bar.setValue(new_h_bar_value)
        v_bar.setValue(new_v_bar_value)

    def setFitWindow(self, value=True):
        if value:
            self.fitWidth.setChecked(False)
        self.zoomMode = self.FIT_WINDOW if value else self.MANUAL_ZOOM
        self.adjustScale()

    def setFitWidth(self, value=True):
        if value:
            self.fitWindow.setChecked(False)
        self.zoomMode = self.FIT_WIDTH if value else self.MANUAL_ZOOM
        self.adjustScale()

    # def hidePolygons(self):
    #     self.togglePolygons(False)

    # def showPolygons(self):
    #     self.togglePolygons(True)

    # def on_toolButton_ShowSeed_triggered(self):
    #     print("on_toolButton_ShowSeed_triggered")

    def togglePolygons(self, value):
        for item, shape in self.itemsToShapes.items():
            # print("label", shape.label)
            # print("item", item)
            # if (shape.label == "seed"):
            item.setCheckState(Qt.Checked if value else Qt.Unchecked)

    def loadFile(self, filePath=None):
        # import pdb;
        # pyqtRemoveInputHook(); pdb.set_trace()
        """Load the specified file, or the last opened file if None."""
        self.resetState()
        self.canvas.setEnabled(False)
        self._controller.loadFile(filePath)
      
       

    def resizeEvent(self, event):
        if self.canvas and not self.image.isNull()\
           and self.zoomMode != self.MANUAL_ZOOM:
            self.adjustScale()
        super(LabelerWindow, self).resizeEvent(event)

    def paintCanvas(self):
        assert not self.image.isNull(), "cannot paint null image"
        self.canvas.scale = 0.01 * self.zoomWidget.value()
        self.canvas.adjustSize()
        self.canvas.update()

    def adjustScale(self, initial=False):
        value = self.scalers[self.FIT_WINDOW if initial else self.zoomMode]()
        self.zoomWidget.setValue(int(100 * value))

    def scaleFitWindow(self):
        """Figure out the size of the pixmap in order to fit the main widget."""
        e = 2.0  # So that no scrollbars are generated.
        w1 = self.centralWidget().width() - e
        h1 = self.centralWidget().height() - e
        a1 = w1 / h1
        # Calculate a new scale value based on the pixmap's aspect ratio.
        w2 = self.canvas.pixmap.width() - 0.0
        h2 = self.canvas.pixmap.height() - 0.0
        a2 = w2 / h2
        return w1 / w2 if a2 >= a1 else h1 / h2

    def scaleFitWidth(self):
        # The epsilon does not seem to work too well here.
        w = self.centralWidget().width() - 2.0
        return w / self.canvas.pixmap.width()

    def closeEvent(self, event):
        if not self.mayContinue():
            event.ignore()
        # settings = self.settings
        # If it loads images from dir, don't load it at the begining
        if self.dirname is None:
            self.settings[SETTING_FILENAME] = self.filePath if self.filePath else ''
        else:
            self.settings[SETTING_FILENAME] = ''

        self.settings[SETTING_WIN_SIZE] = self.size()
        self.settings[SETTING_WIN_POSE] = self.pos()
        self.settings[SETTING_WIN_STATE] = self.saveState()
        self.settings[SETTING_LINE_COLOR] = self.lineColor
        self.settings[SETTING_FILL_COLOR] = self.fillColor
        self.settings[SETTING_RECENT_FILES] = self.recentFiles
        # self.settings[SETTING_ADVANCE_MODE] = not self._beginner
        if self.defaultSaveDir and os.path.exists(self.defaultSaveDir):
            self.settings[SETTING_SAVE_DIR] = ustr(self.defaultSaveDir)
        else:
            self.settings[SETTING_SAVE_DIR] = ''

        if self.lastOpenDir and os.path.exists(self.lastOpenDir):
            self.settings[SETTING_LAST_OPEN_DIR] = self.lastOpenDir
        else:
            self.settings[SETTING_LAST_OPEN_DIR] = ''

        self.settings[SETTING_AUTO_SAVE] = self.autoSaving.isChecked()
        self.settings[SETTING_SINGLE_CLASS] = self.singleClassMode.isChecked()
        self.settings[SETTING_PAINT_LABEL] = self.displayLabelOption.isChecked()
        # self.settings[SETTING_DRAW_SQUARE] = self.drawSquaresOption.isChecked()
        self.settings.save()

    def loadRecent(self, filename):
        if self.mayContinue():
            self.loadFile(filename)

    def scanAllImages(self, folderPath):
        extensions = ['.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()]
        images = []

        for root, dirs, files in os.walk(folderPath):
            for file in files:
                if file.lower().endswith(tuple(extensions)):
                    relativePath = os.path.join(root, file)
                    path = ustr(os.path.abspath(relativePath))
                    images.append(path)
        images.sort(key=lambda x: x.lower())
        return images

    def changeSavedirDialog(self, _value=False):
        if self.defaultSaveDir is not None:
            path = ustr(self.defaultSaveDir)
        else:
            path = '.'

        dirpath = ustr(QFileDialog.getExistingDirectory(self,
                                                       '%s - Save annotations to the directory' % __appname__, path,  QFileDialog.ShowDirsOnly
                                                       | QFileDialog.DontResolveSymlinks))

        if dirpath is not None and len(dirpath) > 1:
            self.defaultSaveDir = dirpath

        self.statusBar().showMessage('%s . Annotation will be saved to %s' %
                                     ('Change saved folder', self.defaultSaveDir))
        self.statusBar().show()

    def openAnnotationDialog(self, _value=False):
        if self.filePath is None:
            self.statusBar().showMessage('Please select image first')
            self.statusBar().show()
            return

        path = os.path.dirname(ustr(self.filePath))\
            if self.filePath else '.'
        if self.usingPascalVocFormat:
            filters = "Open Annotation XML file (%s)" % ' '.join(['*.xml'])
            filename = ustr(QFileDialog.getOpenFileName(self,'%s - Choose a xml file' % __appname__, path, filters))
            if filename:
                if isinstance(filename, (tuple, list)):
                    filename = filename[0]
            self.loadPascalXMLByFilename(filename)

    def openDirDialog(self, _value=False, dirpath=None):
        if not self.mayContinue():
            return

        defaultOpenDirPath = dirpath if dirpath else '.'
        if self.lastOpenDir and os.path.exists(self.lastOpenDir):
            defaultOpenDirPath = self.lastOpenDir
        else:
            defaultOpenDirPath = os.path.dirname(self.filePath) if self.filePath else '.'

        targetDirPath = ustr(QFileDialog.getExistingDirectory(self,
                                                     '%s - Open Directory' % __appname__, defaultOpenDirPath,
                                                     QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks))
        self.importDirImages(targetDirPath)

    def importDirImages(self, dirpath):
        if not self.mayContinue() or not dirpath:
            return

        self.lastOpenDir = dirpath
        self.dirname = dirpath
        self.filePath = None
        self.fileListWidget.clear()
        self.mImgList = self.scanAllImages(dirpath)
        self.openNextImg()
        for imgPath in self.mImgList:
            item = QListWidgetItem(imgPath)
            self.fileListWidget.addItem(item)

    def verifyImg(self, _value=False):
        # Proceding next image without dialog if having any label
        if self.filePath is not None:
            try:
                self.labelFile.toggleVerify()
            except AttributeError:
                # If the labelling file does not exist yet, create if and
                # re-save it with the verified attribute.
                self.saveFile()
                if self.labelFile != None:
                    self.labelFile.toggleVerify()
                else:
                    return

            self.canvas.verified = self.labelFile.verified
            self.paintCanvas()
            self.saveFile()

    def openPrevImg(self, _value=False):
        # Proceding prev image without dialog if having any label
        if self.autoSaving.isChecked():
            if self.defaultSaveDir is not None:
                if self.dirty is True:
                    self.saveFile()
            else:
                self.changeSavedirDialog()
                return

        if not self.mayContinue():
            return

        if len(self.mImgList) <= 0:
            return

        if self.filePath is None:
            return

        currIndex = self.mImgList.index(self.filePath)
        if currIndex - 1 >= 0:
            filename = self.mImgList[currIndex - 1]
            if filename:
                self.loadFile(filename)

    def openNextImg(self, _value=False):
        # Proceding prev image without dialog if having any label
        if self.autoSaving.isChecked():
            if self.defaultSaveDir is not None:
                if self.dirty is True:
                    self.saveFile()
            else:
                self.changeSavedirDialog()
                return

        if not self.mayContinue():
            return

        if len(self.mImgList) <= 0:
            return

        filename = None
        if self.filePath is None:
            filename = self.mImgList[0]
        else:
            currIndex = self.mImgList.index(self.filePath)
            if currIndex + 1 < len(self.mImgList):
                filename = self.mImgList[currIndex + 1]

        if filename:
            self.loadFile(filename)

    def openFile(self, _value=False):
        if not self.mayContinue():
            return
        path = os.path.dirname(ustr(self.filePath)) if self.filePath else '.'
        formats = ['*.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()]
        filters = "Image & Label files (%s)" % ' '.join(formats + ['*%s' % LabelFile.suffix])
        filename = QFileDialog.getOpenFileName(self, '%s - Choose Image or Label file' % __appname__, path, filters)
        if filename:
            if isinstance(filename, (tuple, list)):
                filename = filename[0]
            self.loadFile(filename)

    def saveFile(self, _value=False):
        if self.defaultSaveDir is not None and len(ustr(self.defaultSaveDir)):
            if self.filePath:
                imgFileName = os.path.basename(self.filePath)
                savedFileName = os.path.splitext(imgFileName)[0]
                savedPath = os.path.join(ustr(self.defaultSaveDir), savedFileName)
                self._saveFile(savedPath)
        else:
            imgFileDir = os.path.dirname(self.filePath)
            imgFileName = os.path.basename(self.filePath)
            savedFileName = os.path.splitext(imgFileName)[0]
            savedPath = os.path.join(imgFileDir, savedFileName)
            self._saveFile(savedPath if self.labelFile
                           else self.saveFileDialog(removeExt=False))

    def saveFileAs(self, _value=False):
        assert not self.image.isNull(), "cannot save empty image"
        self._saveFile(self.saveFileDialog())

    def saveFileDialog(self, removeExt=True):
        caption = '%s - Choose File' % __appname__
        filters = 'File (*%s)' % LabelFile.suffix
        openDialogPath = self.currentPath()
        dlg = QFileDialog(self, caption, openDialogPath, filters)
        dlg.setDefaultSuffix(LabelFile.suffix[1:])
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        filenameWithoutExtension = os.path.splitext(self.filePath)[0]
        dlg.selectFile(filenameWithoutExtension)
        dlg.setOption(QFileDialog.DontUseNativeDialog, False)
        if dlg.exec_():
            fullFilePath = ustr(dlg.selectedFiles()[0])
            if removeExt:
                return os.path.splitext(fullFilePath)[0] # Return file path without the extension.
            else:
                return fullFilePath
        return ''

    def _saveFile(self, annotationFilePath):
        if annotationFilePath and self.saveLabels(annotationFilePath):
            self.setClean()
            self.statusBar().showMessage('Saved to  %s' % annotationFilePath)
            self.statusBar().show()

    def closeFile(self, _value=False):
        if not self.mayContinue():
            return
        self.resetState()
        self.setClean()
        self.toggleActions(False)
        self.canvas.setEnabled(False)
        self.saveAs.setEnabled(False)

    def resetAll(self):
        self.settings.reset()
        self.close()
        proc = QProcess()
        proc.startDetached(os.path.abspath(__file__))

    def mayContinue(self):
        return not (self.dirty and not self.discardChangesDialog())

    def discardChangesDialog(self):
        yes, no = QMessageBox.Yes, QMessageBox.No
        msg = u'You have unsaved changes, proceed anyway?'
        return yes == QMessageBox.warning(self, u'Attention', msg, yes | no)

    def errorMessage(self, title, message):
        return QMessageBox.critical(self, title,
                                    '<p><b>%s</b></p>%s' % (title, message))

    def currentPath(self):
        return os.path.dirname(self.filePath) if self.filePath else '.'

    def chooseColor1(self):
        color = self.colorDialog.getColor(self.lineColor, u'Choose line color',
                                          default=DEFAULT_LINE_COLOR)
        if color:
            self.lineColor = color
            Shape.line_color = color
            self.canvas.setDrawingColor(color)
            self.canvas.update()
            self.setDirty()

    def deleteSelectedShape(self):
        self.remLabel(self.canvas.deleteSelected())
        self.setDirty()
        if self.noShapes():
            for action in self.onShapesPresent:
                action.setEnabled(False)

    def chshapeLineColor(self):
        color = self.colorDialog.getColor(self.lineColor, u'Choose line color',
                                          default=DEFAULT_LINE_COLOR)
        if color:
            self.canvas.selectedShape.line_color = color
            self.canvas.update()
            self.setDirty()

    def chshapeFillColor(self):
        color = self.colorDialog.getColor(self.fillColor, u'Choose fill color',
                                          default=DEFAULT_FILL_COLOR)
        if color:
            self.canvas.selectedShape.fill_color = color
            self.canvas.update()
            self.setDirty()

    def copyShape(self):
        self.canvas.endMove(copy=True)
        self.addLabel(self.canvas.selectedShape)
        self.setDirty()

    def moveShape(self):
        self.canvas.endMove(copy=False)
        self.setDirty()


    def loadPascalXMLByFilename(self, xmlPath):
        if self.filePath is None:
            return
        if os.path.isfile(xmlPath) is False:
            return

        self.set_format(FORMAT_PASCALVOC)

        tVocParseReader = PascalVocReader(xmlPath)
        shapes = tVocParseReader.getShapes()
        self.loadLabels(shapes)
        self.canvas.verified = tVocParseReader.verified

    def loadYOLOTXTByFilename(self, txtPath):
        if self.filePath is None:
            return
        if os.path.isfile(txtPath) is False:
            return

        self.set_format(FORMAT_YOLO)
        tYoloParseReader = YoloReader(txtPath, self.image)
        shapes = tYoloParseReader.getShapes()
        print (shapes)
        self.loadLabels(shapes)
        self.canvas.verified = tYoloParseReader.verified

    def togglePaintLabelsOption(self):
        for shape in self.canvas.shapes:
            shape.paintLabel = self.displayLabelOption.isChecked()

    # def toogleDrawSquare(self):
    #     self.canvas.setDrawingShapeToSquare(self.drawSquaresOption.isChecked())



def inverted(color):
    return QColor(*[255 - v for v in color.getRgb()])


def read(filename, default=None):
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except:
        return default