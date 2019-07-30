import socket
import threading
import json
import requests

class ThreadedClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
         
    def connectToServer(self):
                  
        # connect to the server on local computer 
        self.sock.connect(('127.0.0.1', self.port)) 

    def sendDetectionImage(self, image):
        self.
        # self.sock.send("Something sent from ".encode('utf-8'))
        # receive data from the server (buffer size)
        print(self.sock.recv(1024)) 
        # close the connection 
        self.sock.close()  

if __name__ == "__main__":
    while True:
        port_num = input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    ThreadedClient('',port_num).connectToServer()