import random
import os
from category import Category
from libs.file_loader import FileLoader
from libs.project_settings import ProjectSettings
from libs.constants import PROJECT_FILE_EXT

class Project(object):
    #TODO : load file from the project file
    suffix = PROJECT_FILE_EXT
    def __init__(self, path, project_file = None):
        #TODO: let user choose the name
        self.name = 'project'
        self.path = path
        self._verified_images = []
        self._non_verified_images = []
        self._num_images = 0
        self._categories = []
        self._colors = []
        self._is_VOC_format = True
        self.recent_files = []
        self.file_loader = FileLoader(self.path)   
        self._is_saved = False    
        #currently holds just a path to the Pickle file
        self._project_file = None
        if project_file is not None and Project.is_project_file(project_file):
            self._project_file = project_file
        # self._project_settings = ProjectSettings(self.path)
        self._project_settings = None

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


    @property
    def is_VOC_format(self):
        return self._is_VOC_format

    @is_VOC_format.setter
    def is_VOC_format(self, value):
        #TODO: check that required format is satisfied.
        if not isinstance(value, bool):
            raise ValueError("Not a boolean")
        self._is_VOC_format = value

    @property
    def is_saved(self):
        return self._is_saved
    
    @is_saved.setter
    def is_saved(self, value):
        if not isinstance(value, bool):
            raise ValueError("Not a boolean")
        self._is_saved = value


    @staticmethod
    def is_project_file(filename):
        #TODO: check that Pickle file exists
        if not os.path.exists(filename):
            return False
        fileSuffix = os.path.splitext(filename)[1].lower()
        return fileSuffix == Project.suffix

    
    def save_project_file(self):
    '''saves the project in 'name.annt' format
        returns True if saved, False otherwise
    '''
        if self._project_settings is not None:
            save_file = os.path.join(self.path, "{}.{}".format(self.name, Project.suffix))
            try:
                with open(self.path, "w") as f:
                    f.write(save_file)
                    self._is_saved = True
                    return True
            except EnvironmentError as e: # parent of IOError, OSError *and* WindowsError where available
                    print(e)
                    self._is_saved = False
                    return False
        return False
                

    #Try to load project file and setings file 
    def load_project_file(self):
        print('Trying to load the project file')
        if self._project_file is not None and os.path.exists(self._project_file):
            try:
                with open(self._project_file, "r") as f:
                    last_saved = f.read()
                    last_saved = last_saved.strip()
                    # last_saved = os.path.join(self.path, last_saved)
                    settings = ProjectSettings(self, last_saved)
                    #if valid settings file
                    if settings.load():
                        self._project_settings = settings 
                        return True                   
            except IOError:
                # if file doesn't exist, maybe because it has just been
                # deleted by a separate process
                pass
            except ValueError as e:
                print (e)
        return False
                

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

    #assigns unique color to a class, to be persited in the settings        
    def assign_color(self, new_class):
        color = self._colors.pop()
        new_class.color = color
        


