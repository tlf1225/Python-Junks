#!/usr/bin/env python3
# coding=utf-8
from cgi import FieldStorage, parse
from io import StringIO
from json import dumps
from logging import getLogger, StreamHandler, Formatter, ERROR, INFO
from os import environ

from cgitb import enable
from traceback import format_exc
from youtube_dl import YoutubeDL

enable(display=False, logdir="../logs/")

buffer = StringIO()
header = environ
recieve = FieldStorage()
params = parse()

log = getLogger("cgi: youtube")
log.setLevel(ERROR)
handler = StreamHandler(buffer)
handler.setLevel(INFO)
formatting = Formatter("%(name)s %(message)s")
handler.setFormatter(formatting)
log.addHandler(handler)

result = {}
output = None

# noinspection PyBroadException
try:
    with YoutubeDL({"cachedir": False, "noplaylist": True, "ignoreerrors": False, "quiet": True,
                    "no_warnings": True, "verbose": False, "simulate": True, "logger": log, "logtostderr": True}) as ydl:
        result.update(ydl.extract_info(recieve.getvalue("id", ""), download=False) or {})
        if "formats" in result:
            for k, v in result.copy().items():
                if v is None:
                    del result[k]
            output = dumps(result, sort_keys=True)
        else:
            print("Status: 500 Internal Server Error")
except Exception as e:
    result.clear()
    result.update({
        "err": "Internal Server Error",
        "message": buffer.getvalue(),
        "exception": str(e)
    })
    if "verbose" in params:
        result.update({"stacktrace": format_exc()})
    output = dumps(result, sort_keys=True)
    print("Status: 500 Internal Server Error")
print("Content-Type: application/json")
print(f"Content-Length: {len(output)}")
print()
print(output, end="")
