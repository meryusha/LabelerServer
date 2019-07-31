import socket
import threading
import json
import requests
import pickle
import time
import threading 
import select
class ThreadedClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(30)
        self.buffer_size = 16384
        # self.sock.setblocking(0)   
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
         
    def connectToServer(self):
                  
        # connect to the server on local computer
        try: 
            self.sock.connect(('127.0.0.1', self.port))
            return True
        except: 
            return False

    def processImageLabels(self, data):
        # print(image_path)
        return pickle.loads(data)
 
    def sendDetectionImage(self, image_path):
        try:
            print('Trying to send Image to server')
            if image_path is None:
                return
            im = open(image_path, 'rb')
            image_bytes = im.read()
            size = len(image_bytes)
            print(size)
            request = f"DETECT SIZE={size}"
            self.sock.send(request.encode('utf-8'))
            # receive data from the server (buffer size)
            response = self.sock.recv(self.buffer_size)
            if not response:
                #connection lost
                self.sock.close() 
                print('Connection lost? ') 
                return None
            if str(response.decode()).startswith("OK"):
                print('sending image bytes')
                self.sock.sendall(image_bytes)
                # t = Timer(10, return None )
                # t.start()
                while True:
                    ready = select.select([self.sock], [], [], 7)
                    if ready[0]:
                        response = self.sock.recv(self.buffer_size)
                        # if response.startswith(b'BOXES'):
                        print('got boxes')
                        # data = response.split(b':')[1]
                        tup = self.processImageLabels(response)
                        # close the connection 
                        self.sock.close()  
                        return tup
                    else:
                        return None
        except Exception as e:
                print("Closed a thread for server", str(e))
        self.sock.close()
        return None

if __name__ == "__main__":
    ThreadedClient('', 8000).connectToServer()