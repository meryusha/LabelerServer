import random
import os
from libs.category import Category
from libs.file_loader import FileLoader
from libs.project_data import ProjectData
from libs.constants import *
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

class Project(object):
    #TODO : load file from the project file
    suffix = PROJECT_FILE_EXT
    def __init__(self, path, project_name ='project', project_file = None):
        #TODO: let user choose the name
        self.name = project_name
        self.path = path
        #dictionaries image name --> Image object
        self._verified_images = {}
        self._non_verified_images = {}

        self.all_image_names = []
        self._num_images = 0
        self._categories = []
        self._colors = []
        self.is_VOC_format = True #otherwise should be YOLO
        self.recent_files = []
        self.file_loader = FileLoader(self)   
        self._is_saved = False    
        #currently holds just a path to the Pickle file
        self._project_file = None
        if project_file is not None and Project.is_project_file(project_file):
            self._project_file = project_file
        self._project_data = None


    @property
    def verified_images(self):
        return self._verified_images

    @verified_images.setter
    def verified_images(self, value):
        #TODO: check that required format is satisfied.
        self._verified_images = value
    
    @property
    def non_verified_images(self):
        return self._non_verified_images

    @non_verified_images.setter
    def non_verified_images(self, value):
        #TODO: check that required format is satisfied.
        self._non_verified_images = value

    @property
    def num_images(self):
        return self.num_images

    @num_images.setter
    def num_images(self, value):
        #TODO: check that required format is satisfied.
        if not isinstance(value, int):
            raise ValueError("Not an int")    
        self._num_images = value

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        #TODO: check that required format is satisfied.
        self._categories = value


    # @property
    # def is_VOC_format(self):
    #     return self._is_VOC_format

    # @is_VOC_format.setter
    # def is_VOC_format(self, value):
    #     #TODO: check that required format is satisfied.
    #     if not isinstance(value, bool):
    #         raise ValueError("Not a boolean")
    #     self._is_VOC_format = value

    @property
    def is_saved(self):
        print('returning project save state', self._is_saved)
        return self._is_saved
    
    @is_saved.setter
    def is_saved(self, value):
        if not isinstance(value, bool):
            raise ValueError("Not a boolean")
        print('chaning project save state on', value)
        self._is_saved = value


    @staticmethod
    def is_project_file(filename):
        #TODO: check that Pickle file exists
        if not os.path.exists(filename):
            return False
        fileSuffix = os.path.splitext(filename)[1].lower()
        return fileSuffix == Project.suffix
   
    ##Project  loading, saving,
    # Loading images and files
     
    def save_project_file(self):
        '''saves the project in 'name.annt' format
        returns True if saved, False otherwise'''
        # import pdb;
        # pyqtRemoveInputHook(); pdb.set_trace()
        self.store_project_data()
        if self._project_data is not None:
            save_file = os.path.join(self.path, "{}{}".format(self.name, Project.suffix))
            try:
                with open(save_file, "w") as f:
                    f.write(self._project_data.rel_path)
                    print('written a file')
                    self._is_saved = True
                    return True
            except EnvironmentError as e: # parent of IOError, OSError *and* WindowsError where available
                    print(e)
                    self._is_saved = False
                    return False
        return False
                

    #Try to load project file and data file 
    #try to load (restore) files from the project data file
    def load_project_file(self):
        print('Trying to load the project file')
        if self._project_file is not None and os.path.exists(self._project_file):
            try:
                with open(self._project_file, "r") as f:
                    last_saved = f.read()
                    last_saved = last_saved.strip()
                    # last_saved = os.path.join(self.path, last_saved)
                    data = ProjectData(self, last_saved)
                    #if valid data file
                    if data.load():
                        self._project_data = data
                        self.restore_project_data() 
                        return True                   
            except IOError:
                # if file doesn't exist, maybe because it has just been
                # deleted by a separate process
                pass
            except ValueError as e:
                print (e)
        return False

    def restore_project_data(self):
        '''restore all project data (images with label files), categories from the binary
            check for consistency with the current data in the folder
        ''' 
        if self._project_data is None:
            return
        print("restoring project data")
        self._verified_images = self._project_data.get(PROJECT_VERIFIED_IMAGES, [])
        self._non_verified_images = self._project_data.get(PROJECT_NON_VERIFIED_IMAGES, [])
        self.all_image_names = self._project_data.get(PROJECT_ALL_IMAGES_NAMES, [])
        self._categories = self._project_data.get(PROJECT_CATEGORIES, [])
        self.check_for_consistency()

    def store_project_data(self):
        '''store all project data (images with label files), categories to the binary
            makes sure images are in the right dictionaries
        '''
        if self._project_data is None:
            self._project_data =  ProjectData(self, str(self.name) + '.pkl')
            
        self.check_for_consistency()
        self._project_data[PROJECT_VERIFIED_IMAGES]  = self._verified_images 
        self._project_data[PROJECT_NON_VERIFIED_IMAGES] = self._non_verified_images 
        self._project_data[PROJECT_ALL_IMAGES_NAMES] = self.all_image_names 
        self._project_data[PROJECT_CATEGORIES] = self._categories     
        self._project_data.save()
    
    def check_for_consistency(self):
        '''checks that images in verified and non-verified dict have the matching label'''
        for imageName in list(self._non_verified_images):
            if self._non_verified_images[imageName].is_verified:
                #there is an error, assume Image label is right
                self._verified_images[imageName] = self._non_verified_images.pop(imageName)
    

        for imageName in list(self.verified_images):
            if not self._verified_images[imageName].is_verified:
                #there is an error, assume Image label is right
                self._non_verified_images[imageName] = self._verified_images.pop(imageName)         
        
        
    def load_dir_images(self, window):
        def addParent(parent, column, title, data):
            item = QTreeWidgetItem(parent, [title])
            item.setData(column, Qt.UserRole, data)
            item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            item.setExpanded (True)
            return item

        def addChild( parent, column, title, data):
            item = QTreeWidgetItem(parent, [title])
            item.setData(column, Qt.UserRole, data)
            return item

        if not self.file_loader:
            return

        window.filePath = None
        window.fileTreeWidget.clear()
        window.fileTreeWidget.setColumnCount(FILE_TREE_COLUMNS_NUMBER) #2
        parent = window.fileTreeWidget.invisibleRootItem()
        window.fileTreeWidget.setColumnWidth(0, FILE_TREE_WIDTH_COL1)
        verified_item = addParent(parent, 0, 'verified', 'V')
        non_verified_item = addParent(parent, 0, 'non verified', "NV")

        self.file_loader.scanAllImages()
        # print(self.all_image_names)
        # window.openNextImg()
        
        for imageName in self._non_verified_images.keys():
            addChild(non_verified_item, 0, imageName, "")

        for imageName in self.verified_images.keys():
            addChild(verified_item,  0, imageName, "")

        # firstImage, _ = self.get_image_from_name(window.fileTreeWidget.topLevelItem(0).text(0))
        # window.loadImage(firstImage)
       


    def get_image_from_name(self, name):
        '''if image is in one of lists, returns the image and False if verified, otherwise, True
            if image is not in any of lists, return None and None
            assumes images were checked to be in the right dictionary
        '''
        if name in self._non_verified_images:
            return self._non_verified_images[name], False

        if name in self._verified_images:
            return self._verified_images[name], True
        
        return None, None    

    #appends a new class to the project's list if does not exist yet
    def append_class(self, new_class):
        if self._categories is not None:
            if not isinstance(new_class, Category):
                raise ValueError("Not a Class")
            if new_class in self._categories:
                #TODO notify user that class already exists
                return False
            self.assign_color(new_class)
            self._categories.append(new_class)
            return True

    #assigns unique color to a class, to be persited in the data file        
    def assign_color(self, new_class):
        color = self._colors.pop()
        new_class.color = color
        


