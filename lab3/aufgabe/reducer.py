import zmq
import random
import time
import threading

class Reducer(threading.Thread):
    def __init__(self,port):
        self.port = port
        threading.Thread.__init__(self)

    def run(self):
        context = zmq.Context()

        #set up pull socket to receive work from splitter
        #socket-address is tcp://localhost:[port]
        receiver = context.socket(zmq.PULL)
        receiver.bind("tcp://*:" + self.port)
        print(self, "bound PULL to", self.port)
