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
        splitterSocket = context.socket(zmq.PULL)
        splitterSocket.connect("tcp://localhost:5557")
        #print(self, "connect PULL to 5557")

        reducer1Socket = context.socket(zmq.PUSH)
        reducer1Socket.connect("tcp://localhost:5558")
        #print(self, "connect PUSH to 5558")
        
        reducer2Socket = context.socket(zmq.PUSH)
        reducer2Socket.connect("tcp://localhost:5559")
        #print(self, "connect PUSH to 5559")

        while True:
            sentence = splitterSocket.recv().decode('UTF-8')
            #print(self, "received", sentence)
            sentence = str.lower(sentence)

            words = str.split(sentence, ' ')

            for word in words:
                if word[0] < 'm':
                    #print(self, "sending'" + word + "' to sender1")
                    reducer1Socket.send_string(word)
                
                else:
                    #print(self, "sending'" + word + "' to sender2")
                    reducer2Socket.send_string(word)
