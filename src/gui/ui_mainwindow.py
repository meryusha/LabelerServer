# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(624, 562)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.scroll = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("scroll")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 283, 439))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scroll.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_4.addWidget(self.scroll, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockLabel = QtWidgets.QDockWidget(MainWindow)
        self.dockLabel.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockLabel.setObjectName("dockLabel")
        self.labelListContainer = QtWidgets.QWidget()
        self.labelListContainer.setObjectName("labelListContainer")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.labelListContainer)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.listLayout = QtWidgets.QVBoxLayout()
        self.listLayout.setObjectName("listLayout")
        self.diffcButton = QtWidgets.QCheckBox(self.labelListContainer)
        self.diffcButton.setObjectName("diffcButton")
        self.listLayout.addWidget(self.diffcButton)
        self.editButton = QtWidgets.QToolButton(self.labelListContainer)
        self.editButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.editButton.setObjectName("editButton")
        self.listLayout.addWidget(self.editButton)
        self.useDefaultLabelQHBoxLayout = QtWidgets.QHBoxLayout()
        self.useDefaultLabelQHBoxLayout.setObjectName("useDefaultLabelQHBoxLayout")
        self.useDefaultLabelCheckbox = QtWidgets.QCheckBox(self.labelListContainer)
        self.useDefaultLabelCheckbox.setObjectName("useDefaultLabelCheckbox")
        self.useDefaultLabelQHBoxLayout.addWidget(self.useDefaultLabelCheckbox)
        self.defaultLabelTextLine = QtWidgets.QLineEdit(self.labelListContainer)
        self.defaultLabelTextLine.setObjectName("defaultLabelTextLine")
        self.useDefaultLabelQHBoxLayout.addWidget(self.defaultLabelTextLine)
        self.listLayout.addLayout(self.useDefaultLabelQHBoxLayout)
        self.labelList = QtWidgets.QListWidget(self.labelListContainer)
        self.labelList.setObjectName("labelList")
        self.listLayout.addWidget(self.labelList)
        self.countLabel = QtWidgets.QLabel(self.labelListContainer)
        self.countLabel.setObjectName("countLabel")
        self.listLayout.addWidget(self.countLabel)
        self.gridLayout_2.addLayout(self.listLayout, 0, 0, 1, 1)
        self.dockLabel.setWidget(self.labelListContainer)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockLabel)
        self.filedock = QtWidgets.QDockWidget(MainWindow)
        self.filedock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.filedock.setObjectName("filedock")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.fileListWidget = QtWidgets.QListWidget(self.dockWidgetContents_3)
        self.fileListWidget.setObjectName("fileListWidget")
        self.verticalLayout.addWidget(self.fileListWidget)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.filedock.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.filedock)
        self.toolBar_Open = QtWidgets.QToolBar(MainWindow)
        self.toolBar_Open.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar_Open.setObjectName("toolBar_Open")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_Open)
        self.toolBar_Zoom = QtWidgets.QToolBar(MainWindow)
        self.toolBar_Zoom.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar_Zoom.setObjectName("toolBar_Zoom")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar_Zoom)
        self.toolBar_Edit = QtWidgets.QToolBar(MainWindow)
        self.toolBar_Edit.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar_Edit.setObjectName("toolBar_Edit")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar_Edit)
        self.dockWidget_View = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_View.setEnabled(True)
        self.dockWidget_View.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockWidget_View.setObjectName("dockWidget_View")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.toolButton_ZoomOut = QtWidgets.QToolButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme(":/zoom-out")
        self.toolButton_ZoomOut.setIcon(icon)
        self.toolButton_ZoomOut.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_ZoomOut.setObjectName("toolButton_ZoomOut")
        self.gridLayout.addWidget(self.toolButton_ZoomOut, 0, 1, 1, 1)
        self.pushButton_ZoomOut = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton_ZoomOut.setObjectName("pushButton_ZoomOut")
        self.gridLayout.addWidget(self.pushButton_ZoomOut, 1, 1, 1, 1)
        self.toolButton_ZoomIn = QtWidgets.QToolButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme(":/zoom-in")
        self.toolButton_ZoomIn.setIcon(icon)
        self.toolButton_ZoomIn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_ZoomIn.setObjectName("toolButton_ZoomIn")
        self.gridLayout.addWidget(self.toolButton_ZoomIn, 0, 0, 1, 1)
        self.pushButton_ZoomIn = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton_ZoomIn.setObjectName("pushButton_ZoomIn")
        self.gridLayout.addWidget(self.pushButton_ZoomIn, 1, 0, 1, 1)
        self.dockWidget_View.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_View)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 624, 22))
        self.menuBar.setObjectName("menuBar")
        self.menu_File = QtWidgets.QMenu(self.menuBar)
        self.menu_File.setObjectName("menu_File")
        self.menu_RecentFiles = QtWidgets.QMenu(self.menu_File)
        self.menu_RecentFiles.setObjectName("menu_RecentFiles")
        self.menu_Edit = QtWidgets.QMenu(self.menuBar)
        self.menu_Edit.setObjectName("menu_Edit")
        self.menu_View = QtWidgets.QMenu(self.menuBar)
        self.menu_View.setObjectName("menu_View")
        self.menu_Help = QtWidgets.QMenu(self.menuBar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menuBar)
        self.quit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/quit")
        self.quit.setIcon(icon)
        self.quit.setObjectName("quit")
        self.open = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/open")
        self.open.setIcon(icon)
        self.open.setObjectName("open")
        self.opendir = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/open")
        self.opendir.setIcon(icon)
        self.opendir.setObjectName("opendir")
        self.changeSavedir = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/open")
        self.changeSavedir.setIcon(icon)
        self.changeSavedir.setObjectName("changeSavedir")
        self.openAnnotation = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/open")
        self.openAnnotation.setIcon(icon)
        self.openAnnotation.setObjectName("openAnnotation")
        self.openNextImgAction = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/next")
        self.openNextImgAction.setIcon(icon)
        self.openNextImgAction.setObjectName("openNextImgAction")
        self.openPrevImgAction = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/prev")
        self.openPrevImgAction.setIcon(icon)
        self.openPrevImgAction.setObjectName("openPrevImgAction")
        self.verify = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/verify")
        self.verify.setIcon(icon)
        self.verify.setObjectName("verify")
        self.save = QtWidgets.QAction(MainWindow)
        self.save.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/save")
        self.save.setIcon(icon)
        self.save.setObjectName("save")
        self.save_format = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/format_voc")
        self.save_format.setIcon(icon)
        self.save_format.setObjectName("save_format")
        self.saveAs = QtWidgets.QAction(MainWindow)
        self.saveAs.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/save-as")
        self.saveAs.setIcon(icon)
        self.saveAs.setObjectName("saveAs")
        self.closeAction = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/close")
        self.closeAction.setIcon(icon)
        self.closeAction.setObjectName("closeAction")
        self.resetAllAction = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/resetall")
        self.resetAllAction.setIcon(icon)
        self.resetAllAction.setObjectName("resetAllAction")
        self.color1 = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/color")
        self.color1.setIcon(icon)
        self.color1.setObjectName("color1")
        self.createMode = QtWidgets.QAction(MainWindow)
        self.createMode.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/new")
        self.createMode.setIcon(icon)
        self.createMode.setObjectName("createMode")
        self.editMode = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/icons/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editMode.setIcon(icon)
        self.editMode.setObjectName("editMode")
        self.create = QtWidgets.QAction(MainWindow)
        self.create.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/new")
        self.create.setIcon(icon)
        self.create.setObjectName("create")
        self.deleteAction = QtWidgets.QAction(MainWindow)
        self.deleteAction.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/delete")
        self.deleteAction.setIcon(icon)
        self.deleteAction.setObjectName("deleteAction")
        self.copy = QtWidgets.QAction(MainWindow)
        self.copy.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/copy")
        self.copy.setIcon(icon)
        self.copy.setObjectName("copy")
        self.detect = QtWidgets.QAction(MainWindow)
        self.detect.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/new")
        self.detect.setIcon(icon)
        self.detect.setObjectName("detect")
        self.advancedMode = QtWidgets.QAction(MainWindow)
        self.advancedMode.setCheckable(True)
        icon = QtGui.QIcon.fromTheme(":/expert")
        self.advancedMode.setIcon(icon)
        self.advancedMode.setObjectName("advancedMode")
        self.hideAll = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/hide")
        self.hideAll.setIcon(icon)
        self.hideAll.setObjectName("hideAll")
        self.showAll = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/hide")
        self.showAll.setIcon(icon)
        self.showAll.setObjectName("showAll")
        self.help = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/help")
        self.help.setIcon(icon)
        self.help.setObjectName("help")
        self.showInfo = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/help")
        self.showInfo.setIcon(icon)
        self.showInfo.setObjectName("showInfo")
        self.zoomIn = QtWidgets.QAction(MainWindow)
        self.zoomIn.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/zoom-in")
        self.zoomIn.setIcon(icon)
        self.zoomIn.setObjectName("zoomIn")
        self.zoomOut = QtWidgets.QAction(MainWindow)
        self.zoomOut.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/zoom-out")
        self.zoomOut.setIcon(icon)
        self.zoomOut.setObjectName("zoomOut")
        self.zoomOrg = QtWidgets.QAction(MainWindow)
        self.zoomOrg.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/zoom")
        self.zoomOrg.setIcon(icon)
        self.zoomOrg.setIconVisibleInMenu(True)
        self.zoomOrg.setShortcutVisibleInContextMenu(True)
        self.zoomOrg.setObjectName("zoomOrg")
        self.fitWindow = QtWidgets.QAction(MainWindow)
        self.fitWindow.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/fit-window")
        self.fitWindow.setIcon(icon)
        self.fitWindow.setShortcut("")
        self.fitWindow.setObjectName("fitWindow")
        self.fitWidth = QtWidgets.QAction(MainWindow)
        self.fitWidth.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/fit-width")
        self.fitWidth.setIcon(icon)
        self.fitWidth.setObjectName("fitWidth")
        self.edit = QtWidgets.QAction(MainWindow)
        self.edit.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(":/edit")
        self.edit.setIcon(icon)
        self.edit.setObjectName("edit")
        self.shapeLineColor = QtWidgets.QAction(MainWindow)
        self.shapeLineColor.setEnabled(False)
        self.shapeLineColor.setObjectName("shapeLineColor")
        self.shapeFillColor = QtWidgets.QAction(MainWindow)
        self.shapeFillColor.setEnabled(False)
        self.shapeFillColor.setObjectName("shapeFillColor")
        self.actiontest = QtWidgets.QAction(MainWindow)
        self.actiontest.setObjectName("actiontest")
        self.autoSaving = QtWidgets.QAction(MainWindow)
        self.autoSaving.setCheckable(True)
        self.autoSaving.setObjectName("autoSaving")
        self.singleClassMode = QtWidgets.QAction(MainWindow)
        self.singleClassMode.setCheckable(True)
        self.singleClassMode.setObjectName("singleClassMode")
        self.displayLabelOption = QtWidgets.QAction(MainWindow)
        self.displayLabelOption.setCheckable(True)
        self.displayLabelOption.setObjectName("displayLabelOption")
        self.toolBar_Open.addAction(self.open)
        self.toolBar_Open.addAction(self.opendir)
        self.toolBar_Open.addAction(self.changeSavedir)
        self.toolBar_Open.addAction(self.openPrevImgAction)
        self.toolBar_Open.addAction(self.openNextImgAction)
        self.toolBar_Open.addAction(self.verify)
        self.toolBar_Open.addAction(self.save)
        self.toolBar_Open.addAction(self.save_format)
        self.toolBar_Zoom.addAction(self.zoomOut)
        self.toolBar_Zoom.addAction(self.zoomIn)
        self.toolBar_Zoom.addAction(self.zoomOrg)
        self.toolBar_Zoom.addAction(self.fitWindow)
        self.toolBar_Zoom.addAction(self.fitWidth)
        self.toolBar_Edit.addAction(self.create)
        self.toolBar_Edit.addAction(self.detect)
        self.toolBar_Edit.addAction(self.edit)
        self.toolBar_Edit.addAction(self.copy)
        self.toolBar_Edit.addAction(self.deleteAction)
        self.menu_RecentFiles.addAction(self.actiontest)
        self.menu_File.addAction(self.open)
        self.menu_File.addAction(self.opendir)
        self.menu_File.addAction(self.changeSavedir)
        self.menu_File.addAction(self.openAnnotation)
        self.menu_File.addAction(self.menu_RecentFiles.menuAction())
        self.menu_File.addAction(self.save)
        self.menu_File.addAction(self.saveAs)
        self.menu_File.addAction(self.save_format)
        self.menu_File.addAction(self.closeAction)
        self.menu_File.addAction(self.resetAllAction)
        self.menu_Edit.addAction(self.create)
        self.menu_Edit.addAction(self.deleteAction)
        self.menu_Edit.addAction(self.edit)
        self.menu_Edit.addAction(self.copy)
        self.menu_Edit.addAction(self.detect)
        self.menu_View.addAction(self.autoSaving)
        self.menu_View.addAction(self.singleClassMode)
        self.menu_View.addAction(self.displayLabelOption)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.hideAll)
        self.menu_View.addAction(self.showAll)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.zoomIn)
        self.menu_View.addAction(self.zoomOut)
        self.menu_View.addAction(self.zoomOrg)
        self.menu_View.addAction(self.fitWindow)
        self.menu_View.addAction(self.fitWidth)
        self.menu_View.addSeparator()
        self.menu_Help.addAction(self.help)
        self.menu_Help.addAction(self.showInfo)
        self.menuBar.addAction(self.menu_File.menuAction())
        self.menuBar.addAction(self.menu_Edit.menuAction())
        self.menuBar.addAction(self.menu_View.menuAction())
        self.menuBar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.toolButton_ZoomOut.clicked.connect(self.zoomOut.trigger)
        self.toolButton_ZoomIn.clicked.connect(self.zoomIn.trigger)
        self.pushButton_ZoomOut.clicked.connect(self.zoomOut.trigger)
        self.pushButton_ZoomIn.clicked.connect(self.zoomIn.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Active Image Labeler"))
        self.dockLabel.setWindowTitle(_translate("MainWindow", "Box Labels"))
        self.diffcButton.setText(_translate("MainWindow", "difficult"))
        self.editButton.setText(_translate("MainWindow", "..."))
        self.useDefaultLabelCheckbox.setText(_translate("MainWindow", "Use default label"))
        self.countLabel.setText(_translate("MainWindow", "TextLabel"))
        self.filedock.setWindowTitle(_translate("MainWindow", "File List"))
        self.toolBar_Open.setWindowTitle(_translate("MainWindow", "Handle Image"))
        self.toolBar_Zoom.setWindowTitle(_translate("MainWindow", "Zoom"))
        self.toolBar_Edit.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.dockWidget_View.setWindowTitle(_translate("MainWindow", "Viewer"))
        self.toolButton_ZoomOut.setText(_translate("MainWindow", "Zoom Out"))
        self.pushButton_ZoomOut.setText(_translate("MainWindow", "Zoom Out"))
        self.toolButton_ZoomIn.setText(_translate("MainWindow", "Zoom In"))
        self.pushButton_ZoomIn.setText(_translate("MainWindow", "Zoom In"))
        self.menu_File.setTitle(_translate("MainWindow", "File"))
        self.menu_RecentFiles.setTitle(_translate("MainWindow", "RecentFiles"))
        self.menu_Edit.setTitle(_translate("MainWindow", "Edit"))
        self.menu_View.setTitle(_translate("MainWindow", "View"))
        self.menu_Help.setTitle(_translate("MainWindow", "Help"))
        self.quit.setText(_translate("MainWindow", "Quit"))
        self.quit.setToolTip(_translate("MainWindow", "Quit application"))
        self.quit.setStatusTip(_translate("MainWindow", "Quit application"))
        self.quit.setWhatsThis(_translate("MainWindow", "Quit application"))
        self.quit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.open.setText(_translate("MainWindow", "Open"))
        self.open.setToolTip(_translate("MainWindow", "Open image or label file"))
        self.open.setStatusTip(_translate("MainWindow", "Open image or label file"))
        self.open.setWhatsThis(_translate("MainWindow", "Open image or label file"))
        self.open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.opendir.setText(_translate("MainWindow", "Open Dir"))
        self.opendir.setToolTip(_translate("MainWindow", "Open Directory"))
        self.opendir.setStatusTip(_translate("MainWindow", "Open Directory"))
        self.opendir.setWhatsThis(_translate("MainWindow", "Open Directory"))
        self.opendir.setShortcut(_translate("MainWindow", "Ctrl+U"))
        self.changeSavedir.setText(_translate("MainWindow", "Change Save Dir"))
        self.changeSavedir.setIconText(_translate("MainWindow", "Change\n"
"Save Dir"))
        self.changeSavedir.setToolTip(_translate("MainWindow", "Change default saved Annotation dir"))
        self.changeSavedir.setStatusTip(_translate("MainWindow", "Change default saved Annotation dir"))
        self.changeSavedir.setWhatsThis(_translate("MainWindow", "Change default saved Annotation dir"))
        self.changeSavedir.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.openAnnotation.setText(_translate("MainWindow", "Open Annotation"))
        self.openAnnotation.setToolTip(_translate("MainWindow", "Open an annotation file"))
        self.openAnnotation.setStatusTip(_translate("MainWindow", "Open an annotation file"))
        self.openAnnotation.setWhatsThis(_translate("MainWindow", "Open an annotation file"))
        self.openAnnotation.setShortcut(_translate("MainWindow", "Ctrl+Shift+O"))
        self.openNextImgAction.setText(_translate("MainWindow", "Next Image"))
        self.openNextImgAction.setToolTip(_translate("MainWindow", "Open the next Image"))
        self.openNextImgAction.setStatusTip(_translate("MainWindow", "Open the next Image"))
        self.openNextImgAction.setWhatsThis(_translate("MainWindow", "Open the next Image"))
        self.openNextImgAction.setShortcut(_translate("MainWindow", "D"))
        self.openPrevImgAction.setText(_translate("MainWindow", "Previous Image"))
        self.openPrevImgAction.setToolTip(_translate("MainWindow", "Open the previous Image"))
        self.openPrevImgAction.setStatusTip(_translate("MainWindow", "Open the previous Image"))
        self.openPrevImgAction.setWhatsThis(_translate("MainWindow", "Open the previous Image"))
        self.openPrevImgAction.setShortcut(_translate("MainWindow", "A"))
        self.verify.setText(_translate("MainWindow", "Verify Image"))
        self.verify.setStatusTip(_translate("MainWindow", "Verify Image"))
        self.verify.setWhatsThis(_translate("MainWindow", "Verify Image"))
        self.verify.setShortcut(_translate("MainWindow", "Space"))
        self.save.setText(_translate("MainWindow", "Save"))
        self.save.setStatusTip(_translate("MainWindow", "Save the labels to a file"))
        self.save.setWhatsThis(_translate("MainWindow", "Save the labels to a file"))
        self.save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.save_format.setText(_translate("MainWindow", "Change save format"))
        self.save_format.setIconText(_translate("MainWindow", "PascalVOC"))
        self.save_format.setStatusTip(_translate("MainWindow", "Change save format"))
        self.save_format.setWhatsThis(_translate("MainWindow", "Change save format"))
        self.saveAs.setText(_translate("MainWindow", "Save As"))
        self.saveAs.setToolTip(_translate("MainWindow", "Save the labels to a different file"))
        self.saveAs.setStatusTip(_translate("MainWindow", "Save the labels to a different file"))
        self.saveAs.setWhatsThis(_translate("MainWindow", "Save the labels to a different file"))
        self.saveAs.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.closeAction.setText(_translate("MainWindow", "Close"))
        self.closeAction.setToolTip(_translate("MainWindow", "Close the current file"))
        self.closeAction.setStatusTip(_translate("MainWindow", "Close the current file"))
        self.closeAction.setWhatsThis(_translate("MainWindow", "Close the current file"))
        self.closeAction.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.resetAllAction.setText(_translate("MainWindow", "Reset All"))
        self.resetAllAction.setStatusTip(_translate("MainWindow", "Reset All"))
        self.resetAllAction.setWhatsThis(_translate("MainWindow", "Reset All"))
        self.color1.setText(_translate("MainWindow", "Box Line Color"))
        self.color1.setToolTip(_translate("MainWindow", "Choose Box line color"))
        self.color1.setStatusTip(_translate("MainWindow", "Choose Box line color"))
        self.color1.setWhatsThis(_translate("MainWindow", "Choose Box line color"))
        self.createMode.setText(_translate("MainWindow", "Create\\nRectBox"))
        self.createMode.setIconText(_translate("MainWindow", "Create\n"
"RectBox"))
        self.createMode.setToolTip(_translate("MainWindow", "Draw a new box"))
        self.createMode.setStatusTip(_translate("MainWindow", "Draw a new box"))
        self.createMode.setWhatsThis(_translate("MainWindow", "Draw a new box"))
        self.createMode.setShortcut(_translate("MainWindow", "W"))
        self.editMode.setText(_translate("MainWindow", "Edit Label"))
        self.editMode.setToolTip(_translate("MainWindow", "Modify the label of the selected Box"))
        self.editMode.setStatusTip(_translate("MainWindow", "Modify the label of the selected Box"))
        self.editMode.setWhatsThis(_translate("MainWindow", "Modify the label of the selected Box"))
        self.editMode.setShortcut(_translate("MainWindow", "Ctrl+J"))
        self.create.setText(_translate("MainWindow", "Create RectBox"))
        self.create.setToolTip(_translate("MainWindow", "Draw a new box"))
        self.create.setStatusTip(_translate("MainWindow", "Draw a new box"))
        self.create.setWhatsThis(_translate("MainWindow", "Draw a new box"))
        self.create.setShortcut(_translate("MainWindow", "W"))
        self.deleteAction.setText(_translate("MainWindow", "Delete RectBox"))
        self.deleteAction.setToolTip(_translate("MainWindow", "Remove the box"))
        self.deleteAction.setStatusTip(_translate("MainWindow", "Remove the box"))
        self.deleteAction.setWhatsThis(_translate("MainWindow", "Remove the box"))
        self.deleteAction.setShortcut(_translate("MainWindow", "Backspace"))
        self.copy.setText(_translate("MainWindow", "Copy RectBox"))
        self.copy.setToolTip(_translate("MainWindow", "Copy the current box"))
        self.copy.setStatusTip(_translate("MainWindow", "Copy the current box"))
        self.copy.setWhatsThis(_translate("MainWindow", "Copy the current box"))
        self.copy.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.detect.setText(_translate("MainWindow", "Detect RectBox"))
        self.detect.setToolTip(_translate("MainWindow", "Detect all boxes"))
        self.detect.setStatusTip(_translate("MainWindow", "Detect all boxes"))
        self.detect.setWhatsThis(_translate("MainWindow", "Detect all boxes"))
        self.detect.setShortcut(_translate("MainWindow", "Ctrl+Shift+D"))
        self.advancedMode.setText(_translate("MainWindow", "Advanced Mode"))
        self.advancedMode.setIconText(_translate("MainWindow", "Advanced Mode"))
        self.advancedMode.setToolTip(_translate("MainWindow", "Swtich to advanced mode"))
        self.advancedMode.setStatusTip(_translate("MainWindow", "Swtich to advanced mode"))
        self.advancedMode.setWhatsThis(_translate("MainWindow", "Swtich to advanced mode"))
        self.advancedMode.setShortcut(_translate("MainWindow", "Ctrl+Shift+A"))
        self.hideAll.setText(_translate("MainWindow", "Hide all bounding boxes"))
        self.hideAll.setIconText(_translate("MainWindow", "Hide all\n"
"bounding boxes"))
        self.hideAll.setToolTip(_translate("MainWindow", "Hide all bounding boxes"))
        self.hideAll.setStatusTip(_translate("MainWindow", "Hide all bounding boxes"))
        self.hideAll.setWhatsThis(_translate("MainWindow", "Hide all bounding boxes"))
        self.hideAll.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.showAll.setText(_translate("MainWindow", "Show all bounding boxes"))
        self.showAll.setIconText(_translate("MainWindow", "Show all\n"
"bounding boxes"))
        self.showAll.setToolTip(_translate("MainWindow", "Show all bounding boxes"))
        self.showAll.setStatusTip(_translate("MainWindow", "Show all bounding boxes"))
        self.showAll.setWhatsThis(_translate("MainWindow", "Show all bounding boxes"))
        self.showAll.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.help.setText(_translate("MainWindow", "Tutorial"))
        self.help.setToolTip(_translate("MainWindow", "Show demo"))
        self.help.setStatusTip(_translate("MainWindow", "Show demo"))
        self.help.setWhatsThis(_translate("MainWindow", "Show demo"))
        self.showInfo.setText(_translate("MainWindow", "Information"))
        self.showInfo.setStatusTip(_translate("MainWindow", "Information"))
        self.showInfo.setWhatsThis(_translate("MainWindow", "Information"))
        self.zoomIn.setText(_translate("MainWindow", "Zoom In"))
        self.zoomIn.setToolTip(_translate("MainWindow", "Increase zoom level"))
        self.zoomIn.setStatusTip(_translate("MainWindow", "Increase zoom level"))
        self.zoomIn.setWhatsThis(_translate("MainWindow", "Increase zoom level"))
        self.zoomIn.setShortcut(_translate("MainWindow", "Ctrl+Shift+="))
        self.zoomOut.setText(_translate("MainWindow", "Zoom Out"))
        self.zoomOut.setToolTip(_translate("MainWindow", "Decrease zoom level"))
        self.zoomOut.setStatusTip(_translate("MainWindow", "Decrease zoom level"))
        self.zoomOut.setWhatsThis(_translate("MainWindow", "Decrease zoom level"))
        self.zoomOut.setShortcut(_translate("MainWindow", "Ctrl+-"))
        self.zoomOrg.setText(_translate("MainWindow", "Original size"))
        self.zoomOrg.setToolTip(_translate("MainWindow", "Zoom to original size"))
        self.zoomOrg.setStatusTip(_translate("MainWindow", "Zoom to original size"))
        self.zoomOrg.setWhatsThis(_translate("MainWindow", "Zoom to original size"))
        self.zoomOrg.setShortcut(_translate("MainWindow", "Ctrl+="))
        self.fitWindow.setText(_translate("MainWindow", "Fit Window"))
        self.fitWindow.setToolTip(_translate("MainWindow", "Zoom follows window size"))
        self.fitWindow.setStatusTip(_translate("MainWindow", "Zoom follows window size"))
        self.fitWindow.setWhatsThis(_translate("MainWindow", "Zoom follows window size"))
        self.fitWidth.setText(_translate("MainWindow", "Fit Width"))
        self.fitWidth.setToolTip(_translate("MainWindow", "Zoom follows window width"))
        self.fitWidth.setStatusTip(_translate("MainWindow", "Zoom follows window width"))
        self.fitWidth.setWhatsThis(_translate("MainWindow", "Zoom follows window width"))
        self.fitWidth.setShortcut(_translate("MainWindow", "Ctrl+Shift+F"))
        self.edit.setText(_translate("MainWindow", "Edit RectBox"))
        self.edit.setToolTip(_translate("MainWindow", "Modify the label of the selected Box"))
        self.edit.setStatusTip(_translate("MainWindow", "Modify the label of the selected Box"))
        self.edit.setWhatsThis(_translate("MainWindow", "Modify the label of the selected Box"))
        self.edit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.shapeLineColor.setText(_translate("MainWindow", "Shape Line Color"))
        self.shapeLineColor.setToolTip(_translate("MainWindow", "Change the line color for this specific shape"))
        self.shapeLineColor.setStatusTip(_translate("MainWindow", "Change the line color for this specific shape"))
        self.shapeLineColor.setWhatsThis(_translate("MainWindow", "Change the line color for this specific shape"))
        self.shapeFillColor.setText(_translate("MainWindow", "Shape Fill Color"))
        self.shapeFillColor.setToolTip(_translate("MainWindow", "Change the fill color for this specific shape"))
        self.shapeFillColor.setStatusTip(_translate("MainWindow", "Change the fill color for this specific shape"))
        self.shapeFillColor.setWhatsThis(_translate("MainWindow", "Change the fill color for this specific shape"))
        self.actiontest.setText(_translate("MainWindow", "test"))
        self.autoSaving.setText(_translate("MainWindow", "Auto Save mode"))
        self.singleClassMode.setText(_translate("MainWindow", "Single Class Mode"))
        self.singleClassMode.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.displayLabelOption.setText(_translate("MainWindow", "Display Labels"))
        self.displayLabelOption.setShortcut(_translate("MainWindow", "Ctrl+Shift+P"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

