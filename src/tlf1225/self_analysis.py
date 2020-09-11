# from datetime import datetime
from gzip import decompress
from http.client import InvalidURL
from json import loads
from re import compile
from time import sleep
from urllib.error import HTTPError
from urllib.parse import unquote, quote, parse_qs
from urllib.request import urlopen, Request

ORIGIN = "https://www.youtube-nocookie.com"

# noinspection SpellCheckingInspection
HD = {
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "curl"
}


class Decrypt:

    def __init__(self, orig: list) -> None:
        self.key = orig

    def swap(self, a):
        c = a % len(self.key)
        self.key[0], self.key[c] = self.key[c], self.key[0]

    def rev(self):
        self.key.reverse()

    def sp(self, c):
        del self.key[0:c]

    def result(self):
        return "".join(self.key)


def work(key: str):
    d = Decrypt(list(unquote(key)))
    d.sp(3)
    d.rev()
    d.swap(1)
    d.swap(3)
    d.swap(51)
    d.rev()
    return quote(d.result())


# noinspection SpellCheckingInspection
def main(req: list) -> None:
    if isinstance(req, list):
        test = compile(r"(?:https://.+?(?:/|/watch\?v=))?([\w-]{11}).*$")
        for i, j in enumerate(req):
            oak = test.search(j)
            if oak:
                req[i] = oak.group(1)
    else:
        return

    for i in req:
        result = None
        try:
            ask = Request(f"{ORIGIN}/get_video_info?video_id={i}", headers=HD, origin_req_host=ORIGIN)
            with urlopen(ask) as res:
                if res.getcode() == 200:
                    if res.getheader("Content-Encoding") in ("gzip", "deflate"):
                        dump = parse_qs(decompress(res.read()).decode())
                    else:
                        dump = parse_qs(res.read().decode())
                    dump = loads(dump["player_response"][0])["streamingData"]
                    result = dump["formats"] + dump["adaptiveFormats"]
        except (HTTPError, KeyError) as e:
            print(e)

        li = list()
        for j in result:
            li.append(j["signatureCipher"])

        for j in li:
            queries = {k: "".join(v) for k, v in parse_qs(j).items()}
            ask = Request(f'{queries["url"]}&{queries["sp"]}={work(queries["s"])}&ratebypass=yes', headers=HD, origin_req_host=ORIGIN, method="HEAD")
            try:
                with urlopen(ask) as e:
                    if e.status == 200:
                        print(f"OK {e.url}")
            except (HTTPError, InvalidURL) as e:
                print(e)
            sleep(1)


if __name__ == '__main__':
    # main(argv[1::])
    # main(["WJ16v-hD1mw", "LRiuS9OxyP4"])
    main(["olFuCEWl_3M"])
