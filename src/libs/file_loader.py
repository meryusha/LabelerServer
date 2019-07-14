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
        '''scans all images in the project data file and project directories
            if images from directory are in the file, load them from the file
            otherwise, create new image object
            split images in verified, non-veriffied. Just created images are non-verified.
        '''
        # import  pdb;
        # pyqtRemoveInputHook(); pdb.set_trace()
        extensions = ['.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()]
        verified_images = {}
        non_verified_images = {}
        names = []

        for root, dirs, files in os.walk(self.project.path):
            for file in files:
                if file.lower().endswith(tuple(extensions)):
                    relativePath = os.path.join(root, file)
                    path = ustr(os.path.abspath(relativePath))
                    names.append(file)
                    if path not in self.project.all_image_names:
                        #we have a new image which is not in the project data file 
                        new_image = Image(path, file) 
                        non_verified_images[file] = new_image 
                        # non_verified_images.append(new_image)
                    else:
                        #do lookup
                        retrieved_image, is_ver = self.project.get_image_from_name(file)
                        if retrieved_image and is_ver:
                            # verified_images.append(retrieved_image)
                            verified_images[file] = retrieved_image
                        elif retrieved_image and not is_ver:
                            non_verified_images[file] = retrieved_image
                            # non_verified_images.append(retrieved_image)
                        else:
                            #there is an error/inconsistency:
                            new_image = Image(path, file) 
                            non_verified_images[file] = new_image 
                            # non_verified_images.append(new_image)

        self.project.non_verified_images = non_verified_images
        self.project.verified_images = verified_images
        self.project.all_image_names = names
        #TODO: sort them??
        # images.sort(key=lambda x: x.lower())

    def check_xml(self, filePath):
        pass

    # def load_xml(self, filePath):
    #     xmlPath = os.path.splitext(filePath)[0] + XML_EXT
    #     txtPath = os.path.splitext(filePath)[0] + TXT_EXT
    #     if os.path.isfile(xmlPath):
    #         self.loadPascalXMLByFilename(xmlPath)
    #     elif os.path.isfile(txtPath):
    #         self.loadYOLOTXTByFilename(txtPath)
