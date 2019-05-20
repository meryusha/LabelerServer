# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(858, 603)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 858, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockLabel = QtWidgets.QDockWidget(MainWindow)
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
        self.quit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/quit")
        self.quit.setIcon(icon)
        self.quit.setObjectName("quit")
        self.open = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(":/open")
        self.open.setIcon(icon)
        self.open.setObjectName("open")
        self.opendir = QtWidgets.QAction(MainWindow)
        self.opendir.setObjectName("opendir")

        self.retranslateUi(MainWindow)
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
        self.quit.setText(_translate("MainWindow", "Quit"))
        self.quit.setToolTip(_translate("MainWindow", "Quit application"))
        self.quit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.open.setText(_translate("MainWindow", "Open"))
        self.open.setToolTip(_translate("MainWindow", "Open image or label file"))
        self.open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.opendir.setText(_translate("MainWindow", "Open Dir"))
        self.opendir.setToolTip(_translate("MainWindow", "Open Dir"))
        self.opendir.setShortcut(_translate("MainWindow", "Ctrl+U"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
