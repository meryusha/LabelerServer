from PyQt5.QtCore import QObject, pyqtSlot
import platform
import codecs
# import distutils.spawn
import os.path

class Controller(QObject):
    def __init__(self, model, defaultSaveDir = None, defaultFilename = None,):
        super().__init__()

        self._model = model

        # Whether we need to save or not.
        #TODO: change the var name
        self.dirty = False
       
    def restore_app_state(self):
        self._model.restore_app_state()




