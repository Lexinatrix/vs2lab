"""
Client and server using classes
"""

import logging
import socket

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))
        self.book = {
            "Lennart" : "+49 1234 987654",
            "Charlotte" : "+49 5555 01723",
            "Tim" : "+49 9182 736455",
            "Telemarketing AG" : "0 800 800 3"
            }

    def serve(self):
        """ Serve echo """
        self.sock.listen(1)
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                
                while True:  # forever
                    data = connection.recv(1024)  # receive data from client
                    if not data:
                        break  # stop if client stopped

                    ##business logic here
                    msg_in = data.decode('ascii') #decode bytes to string
                    self._logger.info("Received message: " + msg_in)

                    if msg_in.startswith("GET:"):
                        book_entry = self.book.get(msg_in.removeprefix("GET:"))
                        if book_entry is None:
                            return_msg = "Entry with given name not found."
                        else:
                            return_msg = book_entry

                    elif msg_in.startswith("GETALL"):
                        return_msg = str(self.book)

                    else:
                        return_msg = str("Data received='" + msg_in + "' did not contain valid keywords.")

                    self._logger.info("Sending message: " + return_msg)

                    connection.send(return_msg.encode('ascii'))

                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")


class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.open()
        self.logger.info("Client connected to socket " + str(self.sock))

    def get(self, name):
        return self._call(str("GET:" + name))
    
    def get_all(self):
        return self._call(str("GETALL"))

    def _call(self, msg_in):
        """ Call server """
        self.logger.info("Sending message: " + msg_in)
        self.sock.send(msg_in.encode('ascii'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('ascii')
        self.logger.info("Received message: " + msg_out)
        return msg_out

    def open(self):
        self.sock.connect((const_cs.HOST, const_cs.PORT))

    def close(self):
        """ Close socket """
        self.sock.close()
        self.logger.info("Client down.")
