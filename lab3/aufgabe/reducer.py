import zmq
import random
import time
import threading

class Reducer(threading.Thread):
    def __init__(self,port):
        self.port = port
        self.words = {}
        threading.Thread.__init__(self)

    def run(self):
        context = zmq.Context()

        #set up pull socket to receive work from splitter
        #socket-address is tcp://localhost:[port]
        mapperSocket = context.socket(zmq.PULL)
        mapperSocket.bind("tcp://*:" + self.port)
        #print(self, "bound PULL to", self.port)

        while True:
            word = mapperSocket.recv().decode('UTF-8')
            if word in self.words:
                self.words[word] += 1
            
            else:
                self.words[word] = 1

            print(self, "received" + "'" + word  + "'" +  "current count:" + str(self.words[word]))
            #print(self, "my dict:")
            #for word in self.words:
                #print(str(word) + ":" + str(self.words[word]))
