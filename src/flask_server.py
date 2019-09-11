from flask import Flask, request, jsonify

import numpy as np
import cv2


import json
import torch
import sys
from os.path import dirname, join, exists
from maskrcnn_benchmark.structures.bounding_box import BoxList
from maskrcnn_benchmark.config import cfg
import torch
from maskrcnn_benchmark.data.datasets.evaluation.seed.seed_predict import SeedPredict
import time
import pickle
# from ../libs.constants import CONFIG_PATH
import pathlib


CONFIG_PATH = "./seeds_faster/configs/seed/e2e_faster_rcnn_R_50_C4_1x_seed_strat2.yaml"
class FlaskServer(object):
    def __init__(self):
        self.model = None 

    def setup(self, args):
        # print(dirname(dirname(__file__)))
        full_path = join('.', CONFIG_PATH)
        print(f'trying to load model from {full_path}')
        if not exists(full_path):
            print("Dir does not exists")
            # self.errorWithInference.emit(u'Could not detect boxes', 'Could not load config file for a model')
            return   
        cfg.merge_from_file(full_path)
        cfg.freeze()           
        self.model = SeedPredict(cfg,) 
        print("worked fine")
        app.run(host="localhost", port=5000, debug=True)


app = Flask(__name__)
server = None

@app.route("/") # main webpage
def home():
    return "Hello world!"
    
# class NumpyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, np.ndarray):
#             return obj.tolist()
#         return json.JSONEncoder.default(self, obj)

@app.route("/api/predict", methods=['POST'])
def predict():
    headers = request.headers
    print(headers)
    print("got something")
    if (headers["content-type"] == "image/jpeg") and server.model is not None:
        # print("got something")
        image_bytes = request.data
        # nparr = np.frombuffer(data,np.uint8)
        # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        predictions = server.model.run_on_opencv_image(image_bytes)
            # print(predictions) 
        labels =  predictions.get_field("labels").numpy().tolist()
        labels_words = []
        print(labels)
        for label in labels:
            # print("SENDING TUPLE")
            # print(labels)
            labels_words.append(server.model.map_class_id_to_class_name(label))

        boxes = predictions.bbox.numpy().tolist()
        # print(boxes)
        scores = predictions.get_field("scores").numpy().tolist()
        print(scores)
        
        result = jsonify({'boxes': boxes,
                        'labels_words' : labels_words,
                        'scores':scores
                        })
        print(result)
        return result
        # return response



if __name__ == "__main__":
    server = FlaskServer()
    server.setup(sys.argv[1:])   

    