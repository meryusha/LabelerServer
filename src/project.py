import random
from category import Category
from libs.file_loader import FileLoader
class Project(object):

    def __init__(self, path):
        self.path = path
        self._verified_images = []
        self._non_verified_images = []
        self._num_images = 0
        self._categories = []
        self._colors = []
        self._is_VOC_format = True
        self.recent_files = []
        self.file_loader = FileLoader(self.path)

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



    #appends a new class to the project's list if does not exist yet
    def append_class(self, new_class):
        if self._categories is not None:
            if not isinstance(new_class, Category):
                raise ValueError("Not a Class")
            if new_class in self._categories:
                #TODO notify user that class already exists
                return False
            assign_color(new_class)
            self._categories.append(new_class)
            return True

    #assigns unique color to a class, to be persited in the settings        
    def assign_color(self, new_class):
        color = self._colors.pop()
        new_class.color = color
        


