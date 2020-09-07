from base64 import b64decode
from json import loads, dumps
from lzma import decompress
from socket import gethostname
from socketserver import ThreadingUDPServer, DatagramRequestHandler


class SVC(DatagramRequestHandler):
    def handle(self) -> None:
        data = loads(b64decode(decompress(self.rfile.read())))
        print(dumps(data, indent=4, sort_keys=True))


if __name__ == '__main__':
    with ThreadingUDPServer((gethostname(), 65500), SVC) as f:
        f.serve_forever(10)
