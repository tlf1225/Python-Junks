from base64 import b64encode
from hashlib import sha3_512
from json import dumps
from lzma import compress
# from textwrap import dedent
from random import random
from socket import gethostname, socket, AF_INET, SOCK_DGRAM, IPPROTO_UDP

if __name__ == '__main__':
    with socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) as s:
        s.connect((gethostname(), 65500))
        # noinspection SpellCheckingInspection
        for i in range(1, 100):
            a = {
                "A": random(),
                "B": "AXOL",
                "C": 12345
            }
            a["H"] = sha3_512(str(a).encode()).hexdigest()

            work = b64encode(dumps(a, sort_keys=True).encode())
            s.send(compress(work))
