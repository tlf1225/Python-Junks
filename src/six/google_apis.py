from json import loads
from sys import argv, stderr
from time import sleep
from urllib.parse import urlunsplit, urlencode
from urllib.request import urlopen

KEY = "AIzaSyDgqOE9EVLYILwq1bd7_7NzYSWlKLdrq1Q"
API_URL = "www.googleapis.com"
VIDEO = "/youtube/v3/videos"
LIVE_CHAT = "/youtube/v3/liveChat/messages"


def oauth2():
    code = ["https", "accounts.google.com", "/o/oauth2/v2/auth", "", None]
    code[3] = urlencode({
        "response_type": "code",
        "client_id": "962947645852-engitjeqegt7vo6q0jvvc29cf8433vml.apps.googleusercontent.com",
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "scope": "https://www.googleapis.com/auth/youtube",
        "access_type": "offline"
    })
    print(urlunsplit(code))
    with urlopen(urlunsplit(code)) as h:
        print(h.read())


def video_chat(vid):
    url = urlunsplit(("https", API_URL, VIDEO, urlencode({"part": "liveStreamingDetails", "key": KEY, "id": vid}), None))
    with urlopen(url) as f:
        return loads(f.read())


def chat_message(cid, token=None):
    code = ["https", API_URL, LIVE_CHAT, "", None]
    if token:
        code[3] = urlencode({
            "part": "authorDetails,snippet",
            "key": KEY,
            "liveChatId": cid,
            "pageToken": token
        })
    else:
        code[3] = urlencode({
            "part": "id",
            "key": KEY,
            "liveChatId": cid,
        })
    with urlopen(urlunsplit(code)) as g:
        return loads(g.read())


def main(vid):
    video = video_chat(vid)
    cid = video["items"][0]["liveStreamingDetails"]["activeLiveChatId"]
    chat = chat_message(cid)
    while True:
        # noinspection PyBroadException
        try:
            chat = chat_message(cid, chat["nextPageToken"])
            for s in chat["items"]:
                if hasattr(s['snippet'], "superChatDetails"):
                    print(f"[SuperChat {s['snippet']['superChatDetails']['amountDisplayString']}] Thanks!! => "
                          f"[{s['authorDetails']['displayName']}]: {s['snippet']['superChatDetails']['userComment']}")
                if hasattr(s['snippet'], "superStickerDetails"):
                    print(f"[SuperSticker {s['snippet']['superStickerDetails']['amountDisplayString']}] Thanks!! =>"
                          f" [{s['authorDetails']['displayName']}]: {s['snippet']['superStickerMetadata']['altText']}")
                print(f"[{s['authorDetails']['displayName']}]: {s['snippet']['displayMessage']}")
        except Exception as e:
            print(e, file=stderr)
        finally:
            sleep(2)


if __name__ == '__main__':
    if len(argv) < 2:
        main("nE5OSSmq4hI")
    else:
        main(argv[1])
