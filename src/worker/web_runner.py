# import threading
# from subprocess import call
from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer, CGIHTTPRequestHandler
from logging import basicConfig, error, info, DEBUG
from mimetypes import add_type
from os import chdir
from ssl import create_default_context, Purpose
from sys import stderr

# noinspection SpellCheckingInspection
FORMAT = "%(levelname)s: %(asctime)s [%(funcName)s] {%(threadName)s:%(thread)d}: %(message)s"


class HTTPWorker(CGIHTTPRequestHandler):

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.address_string()} [{self.log_date_time_string()}] {fmt % args}", file=stderr)

    def do_GET(self) -> None:
        super().do_GET()


def http(root=None):
    chdir(root)
    basicConfig(level=DEBUG, format=FORMAT)
    with ThreadingHTTPServer(("", 80), HTTPWorker) as httpd:
        info("Running")
        httpd.serve_forever()
        error("Exit")


def https(root=None):
    ssl = create_default_context(Purpose.CLIENT_AUTH)
    ssl.load_cert_chain(certfile="../certificate.crt", keyfile="../private.key")
    # ssl.load_verify_locations(cafile="../ca_bundle.crt")
    ssl.set_alpn_protocols(["http/1.1", "h2"])
    chdir(root)
    basicConfig(level=DEBUG, format=FORMAT)
    with ThreadingHTTPServer(("", 443), HTTPWorker) as httpd:
        info("Running")
        httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True)
        httpd.serve_forever()
        error("Exit")


def main():
    chdir("root")
    add_type("text/javascript", ".js")
    with ThreadPoolExecutor(max_workers=5) as worker:
        root = "."
        a = [worker.submit(http, root=root),
             worker.submit(https, root=root)]
        for c in a:
            c.exception()


if __name__ == '__main__':
    main()
