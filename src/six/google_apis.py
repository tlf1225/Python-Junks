from json import loads
from urllib.parse import urlunsplit, urlencode
from urllib.request import urlopen

KEY = "AIzaSyDgqOE9EVLYILwq1bd7_7NzYSWlKLdrq1Q"
API_URL = "www.googleapis.com"
VIDEO = "/youtube/v3/videos"
LIVE_CHAT = "/youtube/v3/liveChat/messages"


def main(id):
    with urlopen(urlunsplit(("https", API_URL, VIDEO, urlencode({
        "part": "liveStreamingDetails",
        "key": KEY,
        "id": id
    }), None))) as f:
        info = loads(f.read())
        with urlopen(urlunsplit(("https", API_URL, LIVE_CHAT, urlencode({
            "pass": "authorDetails,snippet",
            "key": KEY,
            "liveChatId": info["items"][0]["liveStreamingDetails"]["activeLiveChatId"]
        }), None))) as g:
            chat = loads(g.read())
            print(chat)


if __name__ == '__main__':
    main("nE5OSSmq4hI")
