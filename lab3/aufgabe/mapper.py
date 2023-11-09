import zmq
import random
import time
import threading

class Mapper(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        context = zmq.Context()

        #set up pull socket to receive work from splitter
        #socket-address is tcp://localhost:5557
        receiver = context.socket(zmq.PULL)
        receiver.connect("tcp://localhost:5557")
        print(self, "connect PULL to 5557")

        sender1 = context.socket(zmq.PUSH)
        sender1.connect("tcp://localhost:5558")
        print(self, "connect PUSH to 5558")
        
        sender2 = context.socket(zmq.PUSH)
        sender2.connect("tcp://localhost:5559")
        print(self, "connect PUSH to 5559")