from PyQt5.QtCore import QObject, pyqtSlot
import platform
import codecs
import sys
# import distutils.spawn
import os.path

# Utility functions and classes.

def have_qstring():
    '''p3/qt5 get rid of QString wrapper as py3 has native unicode str type'''
    return not (sys.version_info.major >= 3 or QT_VERSION_STR.startswith('5.'))

def util_qt_strlistclass():
    return QStringList if have_qstring() else list

class Model(QObject):
    settings_loaded = pyqtSignal(bool)
    update_status_bar = pyqtSignal(str)
    def __init__(self, defaultFilename = None, defaultPrefdefClassFile=None, defaultSaveDir=None):
        super().__init__()
     
        # Save as Pascal voc xml
        self.defaultSaveDir = defaultSaveDir
        self.usingPascalVocFormat = True
        self.usingYoloFormat = False

        # For loading all image under a directory
        self.mImgList = []
        self.dirname = None

        #Merey: Labels - loaded from the file
        self.labelHist = []
        # self.colorHist = []
        self.lastOpenDir = None
        # Load predefined classes to the list
        self.loadPredefinedClasses(defaultPrefdefClassFile)

        # Merey Load predefined colors to the list
        # self.loadPredefinedColors(defaultPrefdefColorFile)
 

    def restore_app_state(self):
        # Application state.
        self.image = QImage()
        self.filePath = ustr(defaultFilename)
        self.recentFiles = []
        self.maxRecent = 7
        self.lineColor = None
        self.fillColor = None
        self.zoom_level = 100
        self.fit_window = False
        # Add Chris
        self._difficult = False
        # import pdb;
        # pyqtRemoveInputHook(); pdb.set_trace()

        # Load setting in the main thread
        self._settings = Settings()
        self.settings_loaded.emit(self._settings.load())
            


        ## Fix the compatible issue for qt4 and qt5. Convert the QStringList to python list
        if self._settings.get(SETTING_RECENT_FILES):
            if have_qstring():
                recentFileQStringList = self._settings.get(SETTING_RECENT_FILES)
                self.recentFiles = [ustr(i) for i in recentFileQStringList]
            else:
                self.recentFiles = recentFileQStringList = self._settings.get(SETTING_RECENT_FILES)

       
        saveDir = ustr(self._settings.get(SETTING_SAVE_DIR, None))
        self.lastOpenDir = ustr(self._settings.get(SETTING_LAST_OPEN_DIR, None))
        if self.defaultSaveDir is None and saveDir is not None and os.path.exists(saveDir):
            self.defaultSaveDir = saveDir
            self.update_status_bar.emit(self.defaultSaveDir)

 
        Shape.line_color = self.lineColor = QColor(self._settings.get(SETTING_LINE_COLOR, DEFAULT_LINE_COLOR))
        Shape.fill_color = self.fillColor = QColor(self._settings.get(SETTING_FILL_COLOR, DEFAULT_FILL_COLOR))

        ##CHANGE
        self.canvas.setDrawingColor(self.lineColor)

        
        # Add chris
        Shape.difficult = self.difficult

    

    def loadPredefinedClasses(self, predefClassesFile):
        if os.path.exists(predefClassesFile) is True:
            with codecs.open(predefClassesFile, 'r', 'utf8') as f:
                for line in f:
                    line = line.strip()
                    if self._labelHist is None:
                        self._labelHist = [line]
                    else:
                        self._labelHist.append(line)
    @property 
    def settings(self):
        return self._settings

    # @settings.setter 
    # def settings(self, settings):
    #     self._settings = settings
    
    # def loadPredefinedColors(self, predefColorsFile):
    #     if os.path.exists(predefColorsFile) is True:
    #         with codecs.open(predefColorsFile, 'r', 'utf8') as f:
    #             for line in f:
    #                 line = line.strip()
    #                 if self.colorHist is None:
    #                     self.colorHist = [line]
    #                 else:
    #                     self.colorHist.append(line)
