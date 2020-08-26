# import threading
# from subprocess import call
from concurrent.futures import ProcessPoolExecutor
from email.utils import formatdate
from http import HTTPStatus
from http.server import ThreadingHTTPServer, CGIHTTPRequestHandler
from io import open
from logging import basicConfig, error, info, DEBUG, getLogger
from mimetypes import guess_type, add_type
from os import linesep, chdir, scandir
from os.path import exists, isfile
from socketserver import ThreadingTCPServer, StreamRequestHandler, ThreadingMixIn
from ssl import create_default_context, Purpose
from time import time

# noinspection PyUnresolvedReferences
from string import Template

FORMAT = "%(levelname)s: %(asctime)s [%(funcName)s] {%(threadName)s:%(thread)d}: %(message)s"


class HTTPWorker(CGIHTTPRequestHandler):

    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)
        self.cgi_info = None

    def handle_one_request(self):
        try:
            super(HTTPWorker, self).handle_one_request()
        except OSError as e:
            print(e)

    def is_cgi(self):
        if not super(HTTPWorker, self).is_cgi():
            if self.path.find("cgi-bin"):
                temp = self.path.split("/")
                self.cgi_info = '/'.join(temp[1:3]), '/'.join(temp[3:])
                return True
            return False
        else:
            return True


class ThreadingStreamRequestHandler(ThreadingMixIn, StreamRequestHandler):
    daemon_threads = True
    logger = getLogger(__name__)
    template = Template("""\
    <html>
        <head>
            <title>Directory</title>
        </head>
        <body>
            ${info}
        </body>
    </html>\
    """)

    def setup(self):
        super().setup()
        self.logger.setLevel(DEBUG)

    def handle(self):
        super().handle()
        try:
            proto = self.rfile.readline().decode().split()
            if len(proto) == 3:
                method, path, (protocol, version) = proto[0], proto[1], proto[2].split("/")
            header = {}
            while True:
                line = self.rfile.readline().decode()
                if line in (linesep, ''):
                    break
                temp = line.rstrip(linesep).split(": ")
                if len(temp) == 2:
                    header[temp[0]] = temp[1]
            local = locals()
            if all(x in local for x in ("method", "path", "protocol", "version")):
                self.logger.info("%s:%s %s %s %s/%s", self.client_address[0], self.client_address[1], method, path, protocol, version)
                path = '/'.join(path.split("/")[1::])
                path, query, *_ = path.split("?") + [""]
                # "OPTIONS", "PUT", "DELETE", "CONNECT", "PATCH", "TRACE"
                if version in "1.1" and method in ("HEAD", "GET", "POST", "SHUTDOWN"):
                    if method == "SHUTDOWN":
                        self.server.shutdown()
                        return
                    response = [f"Date: {formatdate(time(), usegmt=True)}", "Server: Python"]
                    if not path:
                        response.insert(0, f"{protocol}/{version} {HTTPStatus.OK} OK")
                        response.append("Content-Type: text/html")
                        dire = list()
                        with scandir() as it:
                            for its in it:
                                if its.is_file():
                                    dire.append(its.path)
                        size = len(linesep.join(dire))
                        response.extend([f"Content-Length: {size}", ""])
                        self.template.safe_substitute({"info": dire})
                        response.extend(dire)
                        self.wfile.write(linesep.join(response).encode())
                    elif exists(path) and isfile(path):
                        try:
                            posted = {}
                            if all(x in header for x in ("Content-Length", "Content-Type")):
                                if header["Content-Type"] == "application/x-www-form-urlencoded":
                                    for x in self.rfile.read(int(header["Content-Length"])).decode().split("&"):
                                        y = x.split("=")
                                        if len(y) == 2:
                                            posted[y[0]] = y[1]
                            buffer = None
                            if "cgi-bin" in path:
                                if path.endswith(".py"):
                                    with open(path, "r", encoding="utf-8") as rs:
                                        exec(rs.read())
                                    if 'output' in locals():
                                        buffer = eval("output.encode()")
                                        exec("del output")
                                        if eval("hasattr(result, 'err')"):
                                            response.insert(0, f"{protocol}/{version} {HTTPStatus.INTERNAL_SERVER_ERROR} INTERNAL SERVER ERROR")
                                        else:
                                            response.insert(0, f"{protocol}/{version} {HTTPStatus.OK} OK")
                                    else:
                                        buffer = ""
                                        response.insert(0, f"{protocol}/{version} {HTTPStatus.INTERNAL_SERVER_ERROR} INTERNAL SERVER ERROR")
                                    response.append("Content-Type: application/json")
                            else:
                                with open(path, "rb") as e:
                                    buffer = e.read()
                                response.append("Content-Type: {}".format(guess_type(path)[0]))
                                response.insert(0, f"{protocol}/{version} {HTTPStatus.OK} OK")
                            response.extend([f"Content-Length: {len(buffer)}", "", ""])
                            self.wfile.write(linesep.join(response).encode())
                            self.wfile.write(buffer)
                        except IOError as e:
                            response.insert(0, f"{protocol}/{version} {HTTPStatus.INTERNAL_SERVER_ERROR} INTERNAL_SERVER_ERROR")
                            self.wfile.write(linesep.join(response).encode())
                            self.logger.error(f"{e.errno} {e.strerror}")
                    else:
                        response.insert(0, f"{protocol}/{version} {HTTPStatus.NOT_FOUND} NOT FOUND")
                        response.extend(["", ""])
                        self.wfile.write(linesep.join(response).encode())
        except Exception as e:
            self.logger.error(e)
            super(ThreadingStreamRequestHandler, self).handle()


def default_http(root=None):
    chdir(root)
    basicConfig(level=DEBUG, format=FORMAT)
    with ThreadingHTTPServer(("localhost", 80), HTTPWorker) as httpd:
        info("Running")
        httpd.serve_forever()
        error("Exit")


def default_https(root=None):
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


def http(root=None):
    chdir(root)
    basicConfig(level=DEBUG, format=FORMAT)
    with ThreadingTCPServer(("localhost", 8080), ThreadingStreamRequestHandler) as httpd:
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
    with ThreadingTCPServer(("localhost", 8443), ThreadingStreamRequestHandler) as httpd:
        info("Running")
        httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True)
        httpd.serve_forever()
        error("Exit")


def main():
    chdir("root")
    add_type("text/javascript", ".js")
    with ProcessPoolExecutor(max_workers=5) as worker:
        root = "."
        a = [worker.submit(default_http, root=root),
             worker.submit(default_https, root=root),
             worker.submit(http, root=root),
             worker.submit(https, root=root)]
        for c in a:
            print(c.result())


if __name__ == '__main__':
    main()
