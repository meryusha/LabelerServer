import random
import os
from libs.category import Category
from libs.constants import IMAGE_DEFAULT_SCORE, IMAGE_HUMAN_VERIFIED_SCORE
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
    
    def __init__(self, path, name = None, category = None, annotFile = None, score = IMAGE_DEFAULT_SCORE):
        self.name = name
        #TODO get name from the path?
        self.path = path
        self._is_verified = False
        self.annotFile = annotFile
        self.annotations = []
        self.category = category
        self.score = score

    
    @property
    def is_verified(self):
        return self._is_verified
  
    def load_annotations(self):
        pass
    
    def save_annotations(self):
        pass
    
    def verify(self):
        pass

