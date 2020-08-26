# import threading
# from subprocess import call
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from http.server import ThreadingHTTPServer, CGIHTTPRequestHandler
from logging import basicConfig, error, info, DEBUG
from mimetypes import add_type
from os import chdir
from ssl import create_default_context, Purpose

# noinspection PyUnresolvedReferences
from typing import Tuple, Optional, Union

FORMAT = "%(levelname)s: %(asctime)s [%(funcName)s] {%(threadName)s:%(thread)d}: %(message)s"


class HTTPWorker(CGIHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def handle_one_request(self):
        try:
            super(HTTPWorker, self).handle_one_request()
        except OSError as e:
            print(e)


def http(root=None):
    chdir(root)
    basicConfig(level=DEBUG, format=FORMAT)
    with ThreadingHTTPServer(("localhost", 80), HTTPWorker) as httpd:
        info("Running")
        httpd.serve_forever()
        error("Exit")


def https(root=None):
    ssl = create_default_context(Purpose.CLIENT_AUTH)
    ssl.load_cert_chain(certfile="../certificate.crt", keyfile="../private.key")
    ssl.load_verify_locations(cafile="../ca_bundle.crt")
    ssl.set_alpn_protocols(["http/1.1"])
    chdir(root)
    basicConfig(level=DEBUG, format=FORMAT)
    with ThreadingHTTPServer(("localhost", 443), HTTPWorker) as httpd:
        info("Running")
        httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True)
        httpd.serve_forever()
        error("Exit")


def main():
    chdir("root")
    add_type("text/javascript", ".js")
    with ProcessPoolExecutor(max_workers=5) as worker:
        root = "."
        a = [worker.submit(http, root=root),
             worker.submit(https, root=root)]
        for c in a:
            try:
                c.exception()
            except (FileNotFoundError, KeyboardInterrupt, BrokenProcessPool):
                print("Cancelling")
                c.cancel()


if __name__ == '__main__':
    main()
