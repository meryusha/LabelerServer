import socket
import threading
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
CONFIG_PATH = "seeds_faster/configs/seed/e2e_faster_rcnn_R_50_C4_1x_seed_strat2.yaml"

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.model = None
        self.buffer_size = 16384

    def listen(self):
        self.sock.listen(5)
        print(socket.gethostbyname(socket.getfqdn()))
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        print("Createed a thread for client")
        size = self.buffer_size
        while True:
            try:
                # print(size)
                response = client.recv(self.buffer_size)
                # print('request', request)
                if response:
                    # Set the response to echo back the recieved data 
                    if response.startswith(b'DETECT SIZE'):
                        response = response.decode()
                        print("Client requested to decode", response)
                        size = int(response.split('=')[1]) 
                        print(size)
                        request = 'OK'
                        client.send(request.encode('utf-8'))
                        # print(bytes_sent)
                    else:
                        #response is image bytes
                        if self.model is not None:
                            image_bytes = response
                            i = 0
                            while response and len(image_bytes) < size:
                                print(len(image_bytes))
                                # print("---", response)
                                # print('len of req', len(response))
                                response = client.recv(self.buffer_size)
                                image_bytes += response
                                # i += 1
                                # print("Part #", str(i))
                            predictions = self.model.run_on_opencv_image(image_bytes)
                            print(predictions) 
                            labels =  predictions.get_field("labels").numpy()
                            labels_words = []
                            print(labels)
                            for label in labels:
                                # print("SENDING TUPLE")
                                # print(labels)
                                labels_words.append(self.model.map_class_id_to_class_name(label))

                            boxes = predictions.bbox.numpy()
                            # print(boxes)
                            scores = predictions.get_field("scores").numpy()
                            print(scores)
                            # response = b'BOXES:' + pickle.dumps((boxes, labels_words, scores))
                            #TODO make sure fits in one buffer
                            response = pickle.dumps((boxes, labels_words, scores))
                            print(len(response))
                            client.sendall(response)
                            size = self.buffer_size
                    # raise error('Client disconnected')
            except Exception as e:
                print("Closed a thread for client", str(e))
                client.close()
                return False

def setup(args):
    # print(dirname(dirname(__file__)))
    full_path = join(dirname(dirname(dirname(__file__))), CONFIG_PATH)
    print(f'trying to load model from {full_path}')
    if not exists(full_path):
        # self.errorWithInference.emit(u'Could not detect boxes', 'Could not load config file for a model')
        return   
    cfg.merge_from_file(full_path)
    cfg.freeze()        
    server = ThreadedServer('', 8000)
    server.model = SeedPredict(cfg,) 
    server.listen()

if __name__ == "__main__":
    setup(sys.argv[1:])
 