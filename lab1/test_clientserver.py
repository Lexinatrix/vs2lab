"""
Simple client server unit test
"""

import logging
import threading
import unittest

import clientserver
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestEchoService(unittest.TestCase):
    """The test"""
    _server = clientserver.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = clientserver.Client()  # create new client for each test

    def test_simple_get(self):
        msg = self.client.get("Charlotte")
        self.assertEqual(msg,"+49 5555 01723")

    def test_simple_get_all(self):
        msg = self.client.get_all()
        self.assertEqual(msg, "{'Lennart': '+49 1234 987654', 'Charlotte': '+49 5555 01723', 'Tim': '+49 9182 736455', 'Telemarketing AG': '0 800 800 3'}")

    def test_error_get(self):
        msg = self.client.get("fgaiu")
        self.assertEqual(msg, "Entry with given name not found.") # ausgegebener error

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate


if __name__ == '__main__':
    unittest.main()
