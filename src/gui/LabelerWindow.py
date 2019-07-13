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
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
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
from libs.projectDialog import ProjectDialog
# from libs.colorDialog import ColorDialog
from libs.labelFile import LabelFile, LabelFileError
from libs.toolBar import ToolBar
from libs.pascal_voc_io import PascalVocReader
from libs.pascal_voc_io import XML_EXT
from libs.yolo_io import YoloReader
from libs.yolo_io import TXT_EXT
from libs.ustr import ustr
from libs.version import __version__
from libs.hashableQListWidgetItem import HashableQListWidgetItem
from libs.project import Project
from zoom import Zoom
import collections
import numpy as np

__appname__ = 'labelImg'

# Utility functions and classes.

def have_qstring():
    '''p3/qt5 get rid of QString wrapper as py3 has native unicode str type'''
    return not (sys.version_info.major >= 3 or QT_VERSION_STR.startswith('5.'))

def util_qt_strlistclass():
    return QStringList if have_qstring() else list


from gui.ui_mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets


class LabelerWindow(QMainWindow, Ui_MainWindow):


    def __init__(self, defaultDir=None, defaultPrefdefClassFile=None, defaultPrefdefColorFile=None):
        super(LabelerWindow, self).__init__()
        # QtCore.QMetaObject.connectSlotsByName(self) #TODO connect SlotsByName!

        self.setupUi(self)

        #No project selected when open
        self.project  = None
        self.image_index = -1
        self.currentImage = None
        self.defaultDir = defaultDir
        if self.defaultDir is None:
            self.defaultDir = '.'
        self.load_views()
        self.zoom_navig = Zoom(self)
        self.setup_connections()       
        self.load_settings()

    #SETIING UP
    def setup_connections(self):

        ###MENU 
        self.hideAll.triggered.connect(partial(self.togglePolygons, False))
        self.showAll.triggered.connect(partial(self.togglePolygons, True))
        self.help.triggered.connect(self.showTutorialDialog)
        self.showInfo.triggered.connect(self.showInfoDialog)
        self.resetAllAction.triggered.connect(self.resetAll)

        ###MAIN TOOLBAR
        self.openProj.triggered.connect(self.openProjectDialog)
        self.quit.triggered.connect(self.close)
        self.createProject.triggered.connect(self.createProjectDialog)
        self.saveAnnot.triggered.connect(self.saveFile)
        self.saveProj.triggered.connect(self.saveProject)
        self.save_format.triggered.connect(self.change_format)
        # self.saveAs.triggered.connect(self.saveFileAs)
        self.closeAction.triggered.connect(self.closeFile)
        self.openNextImgAction.triggered.connect(self.openNextImg)
        self.openPrevImgAction.triggered.connect(self.openPrevImg)      
        self.verify.triggered.connect(self.verifyImg)


        ###RECTBOX
        #create Rect box pressed
        self.create.triggered.connect(self.createShape)
        #deleteShape is pressed
        self.deleteAction.triggered.connect(self.deleteSelectedShape)
        #copy shape is pressed
        self.copy.triggered.connect(self.copySelectedShape)
        self.edit.triggered.connect(self.editLabel)


        ###BOXLABELS & LABELLIST
        self.diffcButton.stateChanged.connect(self.btnstate)
        self.editButton.setDefaultAction(self.edit)
        self.labelList.itemActivated.connect(self.labelSelectionChanged)
        self.labelList.itemSelectionChanged.connect(self.labelSelectionChanged)
        self.labelList.itemDoubleClicked.connect(self.editLabel)
        self.labelList.itemChanged.connect(self.labelItemChanged)


        ###FILELIST    
        # self.fileTreeWidget.itemDoubleClicked.connect(self.fileitemDoubleClicked) 
        self.fileTreeWidget.itemDoubleClicked.connect(self.fileitemDoubleClicked)            
        self.menu_File.aboutToShow.connect(self.updateFileMenu)
         # self.scrollArea = self.scroll


         ###CANVAS
        self.canvas.scrollRequest.connect(self.scrollRequest)
        self.canvas.newShape.connect(self.newShape)
        self.canvas.newShapes.connect(self.newShapes)
        self.canvas.shapeMoved.connect(self.setUnsavedChanges)
        self.canvas.selectionChanged.connect(self.shapeSelectionChanged)
        self.canvas.drawingPolygon.connect(self.toggleDrawingSensitive)        
        self.canvas.zoomRequest.connect(self.zoom_navig.zoomRequest)

    def load_views(self):
        self.screencastViewer = self.getAvailableScreencastViewer()
        #TODO: put our tutorial there
        self.screencast = "https://youtu.be/p0nR2YsCY_U"

        # Load string bundle for i18n
        # self.stringBundle = StringBundle.getBundle()
        # getStr = lambda strId: self.stringBundle.getString(strId)
        self.canvas = Canvas(parent=self)
        # self.colorDialog = ColorDialog(parent=self)
        self.labelDialog = LabelDialog(parent=self, listItem=[])
        self.projectDialog = ProjectDialog(parent = self)
        self.itemsToShapes = {}
        self.shapesToItems = {}
        self.prevLabelText = ''
        self.lineColor = None
        self.fillColor = None
        self.difficult = False
            
        # For loading all image under a directory
        # self.project.all_image_names = []
    
        # Whether we need to save or not.
        self.unsavedChanges = False
         # what is it? 
        self._noSelectionSlot = False
        self.scroll.setWidget(self.canvas)
        # scroll.setWidgetResizable(True)
        self.scrollBars = {
            Qt.Vertical: self.scroll.verticalScrollBar(),
            Qt.Horizontal: self.scroll.horizontalScrollBar()
        }
       

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

        # STATUS BAR
        self.statusBar().showMessage('%s started.' % __appname__)
        self.statusBar().show()

        # Populate the File menu dynamically.
        self.updateFileMenu()

        # Display cursor coordinates at the right of status bar
        self.labelCoordinates = QLabel('')
        self.statusBar().addPermanentWidget(self.labelCoordinates)

    def load_settings(self):
        # Load setting in the main thread
        self.settings = Settings()
        self.settings.load()
        # Application state.
        # self.image = QImage()
        # self.filePath = ustr(self.defaultDir)
        #loading last project if possible
        # projDir = ustr(self.settings.get(SETTING_PROJECT_DIR, None))
        projFile = ustr(self.settings.get(SETTING_PROJECT_FILE, None))
        if self.project is None and self.openProject(projFile):
            if self.project is not None:
                self.statusBar().showMessage('%s started. Annotation will be saved to %s' %
                                            (__appname__, self.project.path))
                self.statusBar().show()
                # import pdb;
                # pyqtRemoveInputHook(); pdb.set_trace()

                self.autoSaving.setChecked(self.settings.get(SETTING_AUTO_SAVE, False))
                self.singleClassMode.setChecked(self.settings.get(SETTING_SINGLE_CLASS, False))
                self.displayLabelOption.setChecked(self.settings.get(SETTING_PAINT_LABEL, False))

                ## Fix the compatible issue for qt4 and qt5. Convert the QStringList to python list
                if self.settings.get(SETTING_RECENT_FILES):
                    if have_qstring():
                        recentFileQStringList = self.settings.get(SETTING_RECENT_FILES)
                        self.project.recent_files = [ustr(i) for i in recentFileQStringList]
                    else:
                        self.project.recent_files = recentFileQStringList = self.settings.get(SETTING_RECENT_FILES)

                size = self.settings.get(SETTING_WIN_SIZE, QSize(600, 500))
                position = QPoint(0, 0)
                saved_position = self.settings.get(SETTING_WIN_POSE, position)
                # Fix the multiple monitors issue
                for i in range(QApplication.desktop().screenCount()):
                    if QApplication.desktop().availableGeometry(i).contains(saved_position):
                        position = saved_position
                        break
                self.resize(size)
                self.move(position)

                # self.lastOpenDir = ustr(self.settings.get(SETTING_LAST_OPEN_DIR, None))

                self.restoreState(self.settings.get(SETTING_WIN_STATE, QByteArray()))
                Shape.line_color = self.lineColor = QColor(self.settings.get(SETTING_LINE_COLOR, DEFAULT_LINE_COLOR))
                Shape.fill_color = self.fillColor = QColor(self.settings.get(SETTING_FILL_COLOR, DEFAULT_FILL_COLOR))
                self.canvas.setDrawingColor(self.lineColor)
                # Add chris
                Shape.difficult = self.difficult  
    
    #Project creation, opening, saving, closing
    def createProjectDialog(self, _value=False, dirpath=None):
        if not self.mayContinue():
            return

        defaultOpenDirPath = dirpath if dirpath else '.'
        targetDirPath = ustr(QFileDialog.getExistingDirectory(self, '%s - Open Directory' % __appname__, defaultOpenDirPath,
                                                     QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks))
        self.project = Project(targetDirPath)
        self.project.load_dir_images(self)
        self.setUnsavedChanges()
      
    def openProjectDialog(self, _value=False):
        '''Triggered by button pressing
            Opens a dialog and passing selected folder to openProject() method
        '''
        if not self.mayContinue():
            return
        path = os.path.dirname(ustr(self.defaultDir)) if self.defaultDir else '.'
        # formats = ['*.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()]
        filters = "Project files (%s)" % ' '.join(['*%s' % Project.suffix])
        filename = QFileDialog.getOpenFileName(self, '%s - Choose Project file' % __appname__, path, filters)
        if filename:
            if isinstance(filename, (tuple, list)):
                filename = filename[0]
            self.openProject(filename)
            # self.loadFile(filename)

    def openProject(self, filePath=None):
        '''Trying to load project from the project .annt file
            shows error if file is not valid, then cleans the workspace and loads the images and project settings
        '''
        print("Selecting project file")

        if filePath is None:
            return
        self.resetState()
        self.canvas.setEnabled(False)
      
        # Make sure that filePath is a regular python string, rather than QString
        filePath = ustr(filePath)
        unicodeFilePath = ustr(filePath)

        if unicodeFilePath and os.path.exists(unicodeFilePath):
            if Project.is_project_file(unicodeFilePath):
                #TODO: change path to the current dir
                project = Project(os.path.dirname(filePath), project_file = unicodeFilePath)
                if project.load_project_file():
                    self.project = project 
                    self.status("Loaded %s" % os.path.basename(unicodeFilePath))
                    self.project.load_dir_images(self)
                    return True
                else:                  
                    self.errorMessage(u'Error opening project',
                                    (u"<p>Could open <i>%s</i>. But could not restore the files")
                                    % (unicodeFilePath))
                    self.status("Error reading %s" % unicodeFilePath)
                    return False
            else:
                self.errorMessage(u'Error opening project',
                                      (u"<p>Make sure <i>%s</i> is a valid project file.")
                                      % ( unicodeFilePath))         
        return False
    
    def saveProject(self):
        if  self.project.save_project_file():
            self.setProjectSaved()
        else: 
            self.errorMessage(u'Error saving project', 'Could not save the project file')
            self.status("Error saving the project")
                         
    #File creation, opening, saving, closing
  
    def saveFile(self, _value=False):
        if self.project.path is not None and len(ustr(self.project.path)):
            if self.currentImage and self.currentImage.label_file:
                # imgFileName = os.path.basename(self.filePath)
                savedFileName = os.path.splitext(self.currentImage.name)[0]
                savedPath = os.path.join(ustr(self.project.path), savedFileName)
                self._saveFile(savedPath)
        #TODO : throw and error if not saved

        # else:
        #     imgFileDir = os.path.dirname(self.filePath)
        #     imgFileName = os.path.basename(self.filePath)
        #     savedFileName = os.path.splitext(imgFileName)[0]
        #     savedPath = os.path.join(imgFileDir, savedFileName)
        #     self._saveFile(savedPath if self.labelFile
        #                    else self.saveFileDialog(removeExt=False))

    # def saveFileAs(self, _value=False):
    #     assert not self.image.isNull(), "cannot save empty image"
    #     self._saveFile(self.saveFileDialog())
  
    # def saveFileDialog(self, removeExt=True):
    #     caption = '%s - Choose File' % __appname__
    #     filters = 'File (*%s)' % LabelFile.suffix
    #     openDialogPath = self.currentPath()
    #     dlg = QFileDialog(self, caption, openDialogPath, filters)
    #     dlg.setDefaultSuffix(LabelFile.suffix[1:])
    #     dlg.setAcceptMode(QFileDialog.AcceptSave)
    #     filenameWithoutExtension = os.path.splitext(self.filePath)[0]
    #     dlg.selectFile(filenameWithoutExtension)
    #     dlg.setOption(QFileDialog.DontUseNativeDialog, False)
    #     if dlg.exec_():
    #         fullFilePath = ustr(dlg.selectedFiles()[0])
    #         if removeExt:
    #             return os.path.splitext(fullFilePath)[0] # Return file path without the extension.
    #         else:
    #             return fullFilePath
    #     return ''

    def _saveFile(self, annotationFilePath):
        if annotationFilePath and self.saveLabels(annotationFilePath):
            self.setFileSaved()
            self.statusBar().showMessage('Saved to  %s' % annotationFilePath)
            self.statusBar().show()

    def closeFile(self, _value=False):
        if not self.mayContinue():
            return
        self.resetState()
        self.setFileSaved()
        self.toggleActions(False)
        self.canvas.setEnabled(False)
        self.saveAs.setEnabled(False)

   
    ##STATE
    def resetState(self):
        self.itemsToShapes.clear()
        self.shapesToItems.clear()
        self.labelList.clear()
        self.currentImage = None
        self.imageData = None
        self.labelFile = None
        self.canvas.resetState()
        self.labelCoordinates.clear()

    def setUnsavedChanges(self):
        '''
            Being called by signal when canvas shapes are moved
            Meaning both file and project have to be saved
        '''
        if self.project is not None:
            self.project.is_saved = False
        self.unsavedChanges = True
        self.saveAnnot.setEnabled(True)
        self.saveProj.setEnabled(True)
    
   
    def setFileSaved(self):
        '''
            Called after a file is saved or closed
            Still might need to save a project
        '''
        self.unsavedChanges = False
        self.saveAnnot.setEnabled(False)
        # self.saveProj.setEnabled(False)
        self.create.setEnabled(True)
        self.detect.setEnabled(True)

    def setProjectSaved(self):
        '''Called when project was just saved
        '''

    def toggleActions(self, value=True):
        """Enable/Disable widgets which depend on an opened image."""
        for z in self.zoom_navig.zoomActions:
            z.setEnabled(value)
        for action in self.onLoadActive:
            action.setEnabled(value)

    def queueEvent(self, function):
        QTimer.singleShot(0, function)

    def status(self, message, delay=5000):
        self.statusBar().showMessage(message, delay)

   
    def currentItem(self):
        items = self.labelList.selectedItems()
        if items:
            return items[0]
        return None

    def addRecentFile(self, filePath):
        if self.project is not None:
            if filePath in self.project.recent_files:
                self.project.recent_files.remove(filePath)
            elif len(self.project.recent_files) >= MAX_RECENT:
                self.project.recent_files.pop()
            self.project.recent_files.insert(0, filePath)

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

    def showInfoDialog(self):
        msg = u'Name:{0} \nApp Version:{1} \n{2} '.format(__appname__, __version__, sys.version_info)
        QMessageBox.information(self, u'Information', msg)

    def createShape(self):
        # assert self.beginner()
        self.canvas.setEditing(False)
        self.create.setEnabled(False)
        self.detect.setEnabled(False)
        self.updateCount()


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

    def updateFileMenu(self):
        if self.project is not None:
            currFilePath = self.project.path
            print(currFilePath)

            def exists(filename):
                return os.path.exists(filename)
            menu = self.menu_RecentFiles
            menu.clear()
            files = [f for f in self.project.recent_files if f !=
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
            self.setUnsavedChanges()

    # Tzutalin 20160906 : Add file list and dock to move faster
    def fileitemDoubleClicked(self, item=None, col = 0):
        #Merey : In simple terms, index() method finds the given element in a list and returns its position.
        imageName = item.text(col)
        if imageName in self.project.all_image_names:
            self.index = self.project.all_image_names.index(imageName)
        # if self.index < len(self.project.all_image_names):
            image, isVerified = self.project.get_image_from_name(imageName)
            self.loadFile(image, index = self.index)

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
                self.setUnsavedChanges()
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
                    self.setUnsavedChanges()

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
                self.labelFile.savePascalVocFormat(annotationFilePath, shapes, self.imageData,
                                                   self.lineColor.getRgb(), self.fillColor.getRgb())
            elif self.usingYoloFormat is True:
                if annotationFilePath[-4:].lower() != ".txt":
                    annotationFilePath += TXT_EXT
                self.labelFile.saveYoloFormat(annotationFilePath, shapes, self.imageData, self.project.categories,
                                                   self.lineColor.getRgb(), self.fillColor.getRgb())
            else:
                self.labelFile.save(annotationFilePath, shapes, self.imageData,
                                    self.lineColor.getRgb(), self.fillColor.getRgb())
            # print('Image:{0} -> Annotation:{1}'.format(self.filePath, annotationFilePath))
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
            self.setUnsavedChanges()
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
                if len(self.project.categories) > 0:
                    self.labelDialog = LabelDialog(
                        parent=self, listItem=self.project.categories)

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

                if text not in self.project.categories:
                    self.project.categories.append(text)
            else:
                # self.canvas.undoLastLine()
                self.canvas.resetAllLines()

        # if self.beginner():  # Switch to edit mode.
        self.canvas.setEditing(True)
        self.create.setEnabled(True)
        self.detect.setEnabled(True)
        # else:
        #     self.actions.editMode.setEnabled(True)
        self.setUnsavedChanges()

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
            if len(self.project.categories) > 0:
                self.labelDialog = LabelDialog(
                    parent=self, listItem=self.project.categories)

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
            self.setUnsavedChanges()

            if text not in self.project.categories:
                self.project.categories.append(text)
        else:
            # self.canvas.undoLastLine()
            self.canvas.resetAllLines()

    def scrollRequest(self, delta, orientation):
        units = - delta / (8 * 15)
        bar = self.scrollBars[orientation]
        bar.setValue(bar.value() + bar.singleStep() * units)


    def togglePolygons(self, value):
        for item, shape in self.itemsToShapes.items():
            # print("label", shape.label)
            # print("item", item)
            # if (shape.label == "seed"):
            item.setCheckState(Qt.Checked if value else Qt.Unchecked)

    def loadFile(self, image=None, index = 0):
        # import pdb;
        # pyqtRemoveInputHook(); pdb.set_trace()
        """Load the specified file, or the last opened file if None."""
        self.resetState()
        self.canvas.setEnabled(False)
        if image is None:
            return False

        # Make sure that filePath is a regular python string, rather than QString
        unicodeFilePath = ustr(image.path)

        if unicodeFilePath and os.path.exists(unicodeFilePath):       
            #Merey: otherwise the file should be an image file
            # Load image:
            # read data first and store for saving into label file.
            self.imageData = read(unicodeFilePath, None)
            self.labelFile = None
            self.canvas.verified = False

            image = QImage.fromData(self.imageData)
            if image.isNull():
                self.errorMessage(u'Error opening file',
                                  u"<p>Make sure <i>%s</i> is a valid image file." % unicodeFilePath)
                self.status("Error reading %s" % unicodeFilePath)
                return False
            self.status("Loaded %s" % os.path.basename(unicodeFilePath))
            # self.image = image
            # self.filePath = unicodeFilePath
            self.canvas.loadPixmap(QPixmap.fromImage(image))
            if self.labelFile:
                self.loadLabels(self.labelFile.shapes)
            self.setFileSaved()
            self.canvas.setEnabled(True)
            self.zoom_navig.adjustScale(initial=True)
            self.zoom_navig.paintCanvas()
            self.addRecentFile(unicodeFilePath)
            self.toggleActions(True)

            # Label xml file and show bound box according to its filename
            # if self.usingPascalVocFormat is True:
            if self.project.path is not None:
                print("DEFAULT SAVE DIR OS NOT NULL")
                basename = os.path.basename(
                    os.path.splitext(unicodeFilePath)[0])
                xmlPath = os.path.join(self.project.path, basename + XML_EXT)
                txtPath = os.path.join(self.project.path, basename + TXT_EXT)

                """Annotation file priority:
                PascalXML > YOLO
                """
                if os.path.isfile(xmlPath):
                    self.loadPascalXMLByFilename(xmlPath)
                elif os.path.isfile(txtPath):
                    self.loadYOLOTXTByFilename(txtPath)
            else:
                #Merey: Load Xml if available
                xmlPath = os.path.splitext(unicodeFilePath)[0] + XML_EXT
                txtPath = os.path.splitext(unicodeFilePath)[0] + TXT_EXT
                if os.path.isfile(xmlPath):
                    self.loadPascalXMLByFilename(xmlPath)
                elif os.path.isfile(txtPath):
                    self.loadYOLOTXTByFilename(txtPath)

            self.setWindowTitle(__appname__ + ' ' + unicodeFilePath)

            # Default : select last item if there is at least one item
            if self.labelList.count():
                self.labelList.setCurrentItem(self.labelList.item(self.labelList.count()-1))
                self.labelList.item(self.labelList.count()-1).setSelected(True)

            self.canvas.setFocus(True)
            return True
        return False

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


    def closeEvent(self, event):
        if not self.mayContinue():
            event.ignore()
        # settings = self.settings
        # If it loads images from dir, don't load it at the begining
        if self.project is not None:
            if self.project.path is None:
            #     self.settings[SETTING_FILENAME] = self.filePath if self.filePath else ''
            # else:
            #     self.settings[SETTING_FILENAME] = ''

            self.settings[SETTING_WIN_SIZE] = self.size()
            self.settings[SETTING_WIN_POSE] = self.pos()
            self.settings[SETTING_WIN_STATE] = self.saveState()
            self.settings[SETTING_LINE_COLOR] = self.lineColor
            self.settings[SETTING_FILL_COLOR] = self.fillColor
            self.settings[SETTING_RECENT_FILES] = self.project.recent_files
            # self.settings[SETTING_ADVANCE_MODE] = not self._beginner
            if self.project.path and os.path.exists(self.project.path):
                self.settings[SETTING_PROJECT_DIR] = ustr(self.project.path)
            else:
                self.settings[SETTING_PROJECT_DIR] = ''

            # if self.lastOpenDir and os.path.exists(self.lastOpenDir):
            #     self.settings[SETTING_LAST_OPEN_DIR] = self.lastOpenDir
            # else:
            #     self.settings[SETTING_LAST_OPEN_DIR] = ''

            self.settings[SETTING_AUTO_SAVE] = self.autoSaving.isChecked()
            self.settings[SETTING_SINGLE_CLASS] = self.singleClassMode.isChecked()
            self.settings[SETTING_PAINT_LABEL] = self.displayLabelOption.isChecked()
            # self.settings[SETTING_DRAW_SQUARE] = self.drawSquaresOption.isChecked()
            self.settings.save()

    def loadRecent(self, filename):
        if self.mayContinue():
            self.loadFile(filename)    

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

    # def openPrevImg(self, _value=False):
    #     # Proceding prev image without dialog if having any label
    #     if self.autoSaving.isChecked():
    #         if self.project.path is not None:
    #             if self.unsavedChanges is True:
    #                 self.saveFile()
    #         else:
    #             # self.changeSavedirDialog()
    #             return

    #     if not self.mayContinue():
    #         return

    #     if len(self.project.all_image_names) <= 0:
    #         return

    #     if self.filePath is None:
    #         return

    #     if self.image_index - 1 < len(self.project.all_image_names) and self.image_index - 1 >= 0:
    #         self.image_index = self.image_index - 1
    #         image, isVerified = self.project.get_get_image_from_name(all_image_names[self.image_index])
    #         self.loadFile(image)


    # def openNextImg(self, _value=False):
    #     # Proceding prev image without dialog if having any label
    #     if self.autoSaving.isChecked():
    #         if self.project.path is not None:
    #             if self.unsavedChanges is True:
    #                 self.saveFile()
    #         else:
    #             # self.changeSavedirDialog()
    #             return

    #     if not self.mayContinue():
    #         return

    #     if len(self.project.all_image_names) <= 0:
    #         return

    #     if self.image_index + 1 < len(self.project.all_image_names) and self.image_index + 1 >= 0:
    #         self.image_index = self.image_index + 1
    #         image, isVerified = self.project.get_image_from_name(self.project.all_image_names[self.image_index])
    #         self.loadFile(image)

    def resetAll(self):
        self.settings.reset()
        self.close()
        proc = QProcess()
        proc.startDetached(os.path.abspath(__file__))

    def mayContinue(self):
        return not (self.unsavedChanges and not self.discardChangesDialog())

    def discardChangesDialog(self):
        yes, no = QMessageBox.Yes, QMessageBox.No
        msg = u'You have unsaved changes, proceed anyway?'
        return yes == QMessageBox.warning(self, u'Attention', msg, yes | no)

    def errorMessage(self, title, message):
        return QMessageBox.critical(self, title,
                                    '<p><b>%s</b></p>%s' % (title, message))

    # def currentPath(self):
    #     return os.path.dirname(self.filePath) if self.filePath else '.'


    def deleteSelectedShape(self):
        self.remLabel(self.canvas.deleteSelected())
        self.setUnsavedChanges()
        if self.noShapes():
            for action in self.onShapesPresent:
                action.setEnabled(False)

       #EVENTS HANDLING
   
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.canvas.setDrawingShapeToSquare(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            # Draw rectangle if Ctrl is pressed
            self.canvas.setDrawingShapeToSquare(True)

    def copyShape(self):
        self.canvas.endMove(copy=True)
        self.addLabel(self.canvas.selectedShape)
        self.setUnsavedChanges()

    def moveShape(self):
        self.canvas.endMove(copy=False)
        self.setUnsavedChanges()


    def loadPascalXMLByFilename(self, xmlPath):
        if self.currentImage is None:
            return
        if os.path.isfile(xmlPath) is False:
            return

        self.set_format(FORMAT_PASCALVOC)

        tVocParseReader = PascalVocReader(xmlPath)
        shapes = tVocParseReader.getShapes()
        self.loadLabels(shapes)
        self.canvas.verified = tVocParseReader.verified

    def loadYOLOTXTByFilename(self, txtPath):
        if self.currentImage is None:
            return
        if os.path.isfile(txtPath) is False:
            return

        self.set_format(FORMAT_YOLO)
        tYoloParseReader = YoloReader(txtPath, QImage.fromData(self.imageData))
        shapes = tYoloParseReader.getShapes()
        print (shapes)
        self.loadLabels(shapes)
        self.canvas.verified = tYoloParseReader.verified

    def togglePaintLabelsOption(self):
        for shape in self.canvas.shapes:
            shape.paintLabel = self.displayLabelOption.isChecked()

def inverted(color):
    return QColor(*[255 - v for v in color.getRgb()])


def read(filename, default=None):
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except:
        return default