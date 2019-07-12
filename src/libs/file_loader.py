import sys, os
from libs.ustr import ustr
from libs.image import Image
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
class FileLoader(object):

    def __init__(self, project):
        self.project = project

    def scanAllImages(self):
        extensions = ['.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()]
        # verified_images = []
        # non_verified_images = []
        images = []
        for root, dirs, files in os.walk(self.project.path):
            for file in files:
                if file.lower().endswith(tuple(extensions)):
                    relativePath = os.path.join(root, file)
                    path = ustr(os.path.abspath(relativePath))
                    if path is not in self.project.all_image_paths:
                        #we have a new image which is not in the project data file 
                        images.append(path)
        images.sort(key=lambda x: x.lower())
        return images

    def check_xml(self, filePath):
        pass

    def load_xml(self, filePath):
        xmlPath = os.path.splitext(filePath)[0] + XML_EXT
        txtPath = os.path.splitext(filePath)[0] + TXT_EXT
                if os.path.isfile(xmlPath):
                    self.loadPascalXMLByFilename(xmlPath)
                elif os.path.isfile(txtPath):
                    self.loadYOLOTXTByFilename(txtPath)
