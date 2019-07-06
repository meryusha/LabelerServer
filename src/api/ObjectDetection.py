# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget
from maskrcnn_benchmark.structures.bounding_box import BoxList
# import sys
from maskrcnn_benchmark.config import cfg
import torch
from maskrcnn_benchmark.data.datasets.evaluation.seed.seed_predict import SeedPredict
import time
class FasterRCNN(QWidget):
 
    ObjectFound = pyqtSignal(list, str)  # (list, str) as [x,y,w,h]] and label
    ObjectsFound = pyqtSignal(tuple)  # tuple of (list, list) with BB and corresponding labels

    def __init__(self):
        super(FasterRCNN, self).__init__()
        self.pippo = 1

    def detectObjects(self, image_path):
        # start_time = time.time()
        print("FasterRCNN detectObjects")

        # self.ObjectFound.emit([100, 100, 30, 200], "myLabelClass")
        # shapes = [[[i, i, 50 + i, 50 + i], "obj" + str(i)] for i in range(200)]
        # TODO: change config file 
        cfg_file ="/home/ramazam/Documents/maskrcnn-benchmark/configs/seed/e2e_faster_rcnn_R_50_C4_1x_seed_strat2.yaml"
        cfg.merge_from_file(cfg_file)
        cfg.freeze()

        seed_predict = SeedPredict(cfg,)
        print(image_path)
        predictions = seed_predict.run_on_opencv_image(image_path) 
        labels =  predictions.get_field("labels").numpy()
        labels_words = []
        for label in labels:
            labels_words.append(seed_predict.map_class_id_to_class_name(label))
        boxes = predictions.bbox.numpy()

        # shapes = list(predictions._split_into_xyxy())
       
        # print("Time: {:.2f} s / img".format(time.time() - start_time))
        self.ObjectsFound.emit((boxes, labels_words))
        # self.ObjectsFound.emit([[[100, 100, 30, 200], "myLabelClass"],
        #                         [[200, 200, 60, 400], "myLabelClass2"]])
        return
