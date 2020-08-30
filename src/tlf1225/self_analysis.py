# from datetime import datetime
from gzip import decompress
from http.client import InvalidURL
from json import loads
from re import compile
from urllib.error import HTTPError
from urllib.parse import parse_qs
from urllib.request import urlopen, Request

ORIGIN = "https://www.youtube-nocookie.com"

# noinspection SpellCheckingInspection
HD = {
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "curl"
}


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
            queries = parse_qs(j)
            ask = Request(queries["url"][0] + f'&{queries["sp"][0]}={queries["s"][0]}', headers=HD, origin_req_host=ORIGIN, method="HEAD")
            try:
                with urlopen(ask) as e:
                    if e.status == 200:
                        print("OK")
            except (HTTPError, InvalidURL) as e:
                print(e)


if __name__ == '__main__':
    # main(argv[1::])
    main(["WJ16v-hD1mw", "LRiuS9OxyP4"])
