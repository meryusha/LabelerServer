# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget
import sys
from os.path import dirname, join, exists
import pathlib
import torch
# sys.path.append("..")
# from .. import maskrcnn_benchmark
from maskrcnn_benchmark.structures.bounding_box import BoxList
from maskrcnn_benchmark.config import cfg
import torch
from maskrcnn_benchmark.data.datasets.evaluation.seed.seed_predict import SeedPredict
import time
from libs.constants import CONFIG_PATH
class FasterRCNN(QWidget):
 
    objectFound = pyqtSignal(list, str)  # (list, str) as [x,y,w,h]] and label
    objectsFound = pyqtSignal(tuple)  # tuple of (list, list) with BB and corresponding labels
    errorWithInference = pyqtSignal(str, str) #error message

    def __init__(self):
        super(FasterRCNN, self).__init__()
        self.pippo = 1

    def detectObjects(self, image_path):
        # start_time = time.time()
        if image_path is None:
            self.errorWithInference.emit(u'Could not detect boxes', 'Image path is None' )
            return
        print(dirname(dirname(__file__)))
        full_path = join(dirname(dirname(dirname(__file__))), CONFIG_PATH)
        print(f'trying to load model from {full_path}')
        if not exists(full_path):
            self.errorWithInference.emit(u'Could not detect boxes', 'Could not load config file for a model')
            return        

        print("FasterRCNN detectObjects")
        # print(os.getcwd())
        cfg.merge_from_file(full_path)
        cfg.freeze()

        seed_predict = SeedPredict(cfg,)
        print(image_path)
        predictions = seed_predict.run_on_opencv_image(image_path) 
        labels =  predictions.get_field("labels").numpy()
        labels_words = []
        for label in labels:
            labels_words.append(seed_predict.map_class_id_to_class_name(label))
        boxes = predictions.bbox.numpy()
        scores = predictions.get_field("scores").numpy()
        # shapes = list(predictions._split_into_xyxy())
       
        # print("Time: {:.2f} s / img".format(time.time() - start_time))
        self.objectsFound.emit((boxes, labels_words, scores))
        return
