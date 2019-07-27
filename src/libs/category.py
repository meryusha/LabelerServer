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

class Category(object):
    #when new class is created - has no color
    def __init__(self, name):
        if not isinstance(name, str):
            raise ValueError("Not a String")
        self._name = name.lower()
        self._color = None
    
    @property
    def name(self):
        return self._name 
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Not a String")
        self._name = value.lower()

    @property
    def color(self):
        return self._color 
    
    @color.setter
    def color(self, value):
        if not isinstance(value, list):
            raise ValueError("Not a RGB list")
        r, g, b = value
        self._color = QColor(r * 256, g * 256, b * 256, 100)

    def __eq__(self, other):
        if not isinstance(other, Category):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.name == other.name
    