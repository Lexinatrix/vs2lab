import zmq
import random
import time
import threading

class Splitter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def putText(self, text):
        self.text = text
        print("received text")

    def run(self):
        context = zmq.Context()

        #set up push socket to give work to mappers
        #socket-address is tcp://localhost:5557
        sender = context.socket(zmq.PUSH)
        sender.bind("tcp://*:5557")
        print(self, "bound PUSH to 5557")

        lines = str.splitlines(self.text)

        for line in lines:
            print(self, "sending a line")
            sender.send_string(f"{line}")
