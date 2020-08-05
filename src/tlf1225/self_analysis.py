# from datetime import datetime
from http.client import InvalidURL
from json import loads
from re import compile
from sys import argv
from urllib.error import HTTPError
from urllib.parse import parse_qs
from urllib.request import urlopen, Request

from gzip import decompress

# from youtube_dl.extractor import youtube

ORIGIN = "https://www.youtube.com"
HD = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en",
    "Referer": ORIGIN,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36",
    "x-spf-referer": ORIGIN,
    "x-spf-previous": ORIGIN,
    "x-youtube-client-name": "1",
    "x-youtube-client-version": "2.20200221.03.00",
    # "x-youtube-client-version": "{}".format(datetime.today().strftime("2.%Y%m%d.%H.%M")),
    "x-youtube-device": "cbr=Chromium&cbrver=80.0.3987.116&cos=Windows&cosver=10.0",
    "x-youtube-time-zone": "Asia/Tokyo"
}


def main(req):
    if isinstance(req, list):
        test = compile(r"([\w-]{11}).*?$")
        for i, j in enumerate(req):
            oak = test.search(j)
            if oak:
                req[i] = oak.group(1)
    for i in req:
        result = []
        try:
            ask = Request(f"{ORIGIN}/watch?v={i}&pbj=1", headers=HD, origin_req_host=ORIGIN)
            with urlopen(ask) as res:
                if res.getcode() == 200:
                    if res.getheader("Content-Encoding") in ("gzip", "deflate"):
                        dump = loads(decompress(res.read()).decode())
                    else:
                        dump = loads(res.read().decode())
                    dump = loads(dump[2]["player"]["args"]["player_response"])["streamingData"]
                    result.append(dump["formats"] + dump["adaptiveFormats"])
        except (HTTPError, KeyError) as e:
            print(e)

        try:
            ask = Request(f"{ORIGIN}/get_video_info?video_id={i}&el=detailpage", headers=HD, origin_req_host=ORIGIN)
            with urlopen(ask) as res:
                if res.getcode() == 200:
                    if res.getheader("Content-Encoding") in ("gzip", "deflate"):
                        dump = parse_qs(decompress(res.read()).decode())
                    else:
                        dump = parse_qs(res.read().decode())
                    dump = loads(dump["player_response"][0])["streamingData"]
                    result.append(dump["formats"] + dump["adaptiveFormats"])
        except (HTTPError, KeyError) as e:
            print(e)

        li = list()
        for j in result:
            for k in j:
                li.append(k["cipher"])

        for j in li:
            l = parse_qs(j)
            ask = Request(l["url"][0] + f'&{l["sp"][0]}={l["s"][0]}', headers=HD, origin_req_host=ORIGIN, method="HEAD")
            try:
                with urlopen(ask) as e:
                    if e.status == 200:
                        print("OK")
            except (HTTPError, InvalidURL) as e:
                print(e)


if __name__ == '__main__':
    main(argv[1::])
