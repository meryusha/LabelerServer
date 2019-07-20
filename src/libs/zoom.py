import sys
from functools import partial
from libs.zoomWidget import ZoomWidget
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

from PyQt5 import QtCore, QtGui, QtWidgets
class Zoom(object):
    FIT_WINDOW, FIT_WIDTH, MANUAL_ZOOM = list(range(3))
    def __init__(self, win):
        self.parent = win
        self.zoomWidget = ZoomWidget()
        zoom = QWidgetAction(self.parent)
        zoom.setDefaultWidget(self.zoomWidget)
        self.zoomWidget.setWhatsThis(
            u"Zoom in or out of the image. Also accessible with"
            " %s and %s from the canvas." % (fmtShortcut("Ctrl+[-+]"),
                                                fmtShortcut("Ctrl+Wheel")))
        self.zoomWidget.setEnabled(False)

        self.parent.zoomIn.triggered.connect(partial(self.addZoom, 10))
        self.parent.zoomOut.triggered.connect(partial(self.addZoom, -10))
        self.parent.zoomOrg.triggered.connect(partial(self.setZoom, 100))

        # Callbacks:
        self.zoomWidget.valueChanged.connect(self.paintCanvas)


        self.parent.fitWindow.triggered.connect(self.setFitWindow)
        self.parent.fitWidth.triggered.connect(self.setFitWidth)


        self.zoomActions = (self.zoomWidget, self.parent.zoomIn, self.parent.zoomOut,
                       self.parent.zoomOrg, self.parent.fitWindow, self.parent.fitWidth)
        self.zoomMode = self.MANUAL_ZOOM
        self.scalers = {
            self.FIT_WINDOW: self.scaleFitWindow,
            self.FIT_WIDTH: self.scaleFitWidth,
            # Set to one to scale to 100% when loading files.
            self.MANUAL_ZOOM: lambda: 1,
        }



    def setZoom(self, value):
        self.parent.fitWidth.setChecked(False)
        self.parent.fitWindow.setChecked(False)
        self.zoomMode = self.MANUAL_ZOOM
        self.zoomWidget.setValue(value)

    def addZoom(self, increment = 10):
        self.setZoom(self.zoomWidget.value() + increment)

    def zoomRequest(self, delta):
        # get the current scrollbar positions
        # calculate the percentages ~ coordinates
        h_bar = self.parent.scrollBars[Qt.Horizontal]
        v_bar = self.parent.scrollBars[Qt.Vertical]

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

        w = self.parent.scroll.width()
        h = self.parent.scroll.height()

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
            self.parent.fitWidth.setChecked(False)
        self.zoomMode = self.FIT_WINDOW if value else self.MANUAL_ZOOM
        self.adjustScale()

    def setFitWidth(self, value=True):
        if value:
            self.parent.fitWindow.setChecked(False)
        self.zoomMode = self.FIT_WIDTH if value else self.MANUAL_ZOOM
        self.adjustScale()

    def paintCanvas(self):
        # assert not self.parent.image.isNull(), "cannot paint null image"
        self.parent.canvas.scale = 0.01 * self.zoomWidget.value()
        self.parent.canvas.adjustSize()
        self.parent.canvas.update()

    def adjustScale(self, initial=False):
        value = self.scalers[self.FIT_WINDOW if initial else self.zoomMode]()
        self.zoomWidget.setValue(int(100 * value))


    def resizeEvent(self, event):
        if self.parent.canvas and not self.parent.image.isNull()\
           and self.zoomMode != self.MANUAL_ZOOM:
            self.adjustScale()
        super(self.parent, self).resizeEvent(event)

  
    def scaleFitWindow(self):
        """Figure out the size of the pixmap in order to fit the main widget."""
        e = 2.0  # So that no scrollbars are generated.
        w1 = self.parent.centralWidget().width() - e
        h1 = self.parent.centralWidget().height() - e
        a1 = w1 / h1
        # Calculate a new scale value based on the pixmap's aspect ratio.
        w2 = self.parent.canvas.pixmap.width() - 0.0
        h2 = self.parent.canvas.pixmap.height() - 0.0
        a2 = w2 / h2
        return w1 / w2 if a2 >= a1 else h1 / h2

    def scaleFitWidth(self):
        # The epsilon does not seem to work too well here.
        w = self.parent.centralWidget().width() - 2.0
        return w / self.parent.canvas.pixmap.width()
