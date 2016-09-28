import os
import time
import signal
import subprocess
from threading import Thread, Event

from tornado.tcpserver import TCPServer

import config
from logutils import setup_logger

logger = setup_logger("boilerplate.server")


class Connection(object):
    """Client connection handler (one per TCP client)"""
    address = None

    def __init__(self, stream, address, server):
        """Initialize base params and call stream reader for next line"""
        logger.info("connection - address: %s", address)
        self.stream = stream
        self.address = address
        self.server = server
        self.stream.set_close_callback(self._on_disconnect)
        self.wait()

    def _on_read(self, line):
        """Called when new line received from connection"""
        # Some game logic (or magic)
        line = line.strip()
        logger.info("RCV> %s", line)
        if not line:
            self.stream.close()
            return

        self.stream.write("echo: %s\n" % line)

        # Wait for further input on this connection
        self.wait()

    def wait(self):
        """Read from stream until the next signed end of line"""
        self.stream.read_until("\n", self._on_read)

    def _on_disconnect(self, *args, **kwargs):
        """Called on client disconnected"""
        logger.info('Client disconnected %r', self.address)
        self.server.client_disconnected(self)
        # self.unregister()

    def __str__(self):
        """Build string representation, will be used for working with
        server identity (not only name) in future"""
        return str(self.address)


class Server(TCPServer):
    """TCP server for handling incoming connections from clients"""
    clients = {}

    def handle_stream(self, stream, address):
        """Called when new IOStream object is ready for usage"""
        logger.info('Incoming connection from %r', address)
        client = Connection(stream, address, server=self)
        self.clients[address] = (client)

    def client_disconnected(self, client):
        del self.clients[client.address]
        logger.info("clients after disconnect: %s", self.clients)

    def send_to_clients(self, message):
        message = message + "\n"
        for addr in self.clients:
            self.clients[addr].stream.write(message)
